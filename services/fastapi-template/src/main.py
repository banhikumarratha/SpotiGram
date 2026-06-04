from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from .api.v1 import health

app = FastAPI(
    title="SpotiGram FastAPI Template",
    description="A template service for SpotiGram microservices.",
    version="1.0.0"
)

# Instrument the app for Prometheus metrics
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

# Include routers
app.include_router(health.router, tags=["Health"])

@app.get("/")
async def root():
    return {"message": "Welcome to SpotiGram API Template"}
