from contextlib import asynccontextmanager
from fastapi import FastAPI, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from infrastructure.postgres_repo import PostgresAnalyticsRepository, Base
from infrastructure.kafka_consumer import KafkaEventConsumer
from application.event_handler import EventHandler
from application.analytics_service import AnalyticsService
import api.v1.router as router_module


_repo = PostgresAnalyticsRepository()
_handler = EventHandler(_repo)
_consumer = KafkaEventConsumer(_handler)

# Initialize singletons for router
router_module._analytics_service = AnalyticsService(_repo)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure tables exist
    async with _repo.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    # Start background consumer
    await _consumer.start()
    
    yield
    
    # Graceful shutdown
    await _consumer.stop()
    await _repo.engine.dispose()


app = FastAPI(
    title="analytics-service",
    description="Event-driven read models for Spotigram analytics",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(router_module.router)


@app.get("/health", tags=["Observability"])
def health_check():
    return {"status": "healthy"}


@app.get("/ready", tags=["Observability"])
def readiness_check():
    return {"status": "ready"}


@app.get("/metrics", tags=["Observability"])
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
