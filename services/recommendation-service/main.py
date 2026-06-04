import asyncio
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from api.v1.router import router, _dna_svc
from infrastructure.kafka_consumer import start_consumer
from infrastructure.kafka_publisher import close_kafka_producer


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start Kafka consumer as background task (gracefully degraded if Kafka is down)
    consumer_task = asyncio.create_task(start_consumer(_dna_svc))
    yield
    consumer_task.cancel()
    await close_kafka_producer()


app = FastAPI(
    title="recommendation-service",
    description="Mood-aware, Music DNA-driven recommendation engine for Spotigram",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router)


@app.get("/health", tags=["Observability"])
def health_check():
    return {"status": "healthy"}


@app.get("/ready", tags=["Observability"])
def readiness_check():
    return {"status": "ready"}


@app.get("/metrics", tags=["Observability"])
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
