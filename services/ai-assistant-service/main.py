from fastapi import FastAPI, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from api.v1.router import router

app = FastAPI(
    title="ai-assistant-service",
    description="Multi-provider AI assistant with LangChain/LangGraph orchestration for Spotigram",
    version="1.0.0",
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
