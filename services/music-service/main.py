from fastapi import FastAPI, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from api.v1.router import router
from infrastructure.cache import close_cache
from infrastructure.kafka_publisher import close_kafka_producer
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await close_cache()
    await close_kafka_producer()

app = FastAPI(title="music-service", lifespan=lifespan)
app.include_router(router)

@app.get("/health")
def health_check(): return {"status": "healthy"}
@app.get("/ready")
def readiness_check(): return {"status": "ready"}
@app.get("/metrics")
def metrics(): return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
