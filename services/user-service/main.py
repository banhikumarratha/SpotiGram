from fastapi import FastAPI, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from api.v1.router import router, auth_router
from infrastructure.database import engine, Base
from infrastructure.kafka_publisher import close_kafka_producer
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup DB schema for testing/local dev if no alembic
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await close_kafka_producer()

app = FastAPI(title="user-service", lifespan=lifespan)
app.include_router(router)
app.include_router(auth_router)

@app.get("/health")
def health_check(): return {"status": "healthy"}
@app.get("/ready")
def readiness_check(): return {"status": "ready"}
@app.get("/metrics")
def metrics(): return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
