from fastapi import FastAPI, Response, Request, Depends
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from contextlib import asynccontextmanager
import redis.asyncio as redis
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from core.middleware import CorrelationIdMiddleware, AuthMiddleware
from core.proxy import forward_request
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    redis_client = redis.from_url(redis_url, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis_client)
    yield
    await redis_client.close()

app = FastAPI(title="api-gateway", lifespan=lifespan)

app.add_middleware(AuthMiddleware)
app.add_middleware(CorrelationIdMiddleware)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/ready")
def readiness_check():
    return {"status": "ready"}

@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.api_route("/api/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"], dependencies=[Depends(RateLimiter(times=100, seconds=60))])
async def proxy(request: Request, path: str):
    return await forward_request(request)
