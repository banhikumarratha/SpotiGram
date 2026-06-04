from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class HealthResponse(BaseModel):
    status: str

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Basic health check endpoint."""
    return HealthResponse(status="ok")

@router.get("/ready", response_model=HealthResponse)
async def readiness_check():
    """
    Readiness check endpoint.
    In a real service, this would verify connections to DBs, Redis, etc.
    """
    return HealthResponse(status="ok")
