import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Base API URLs for the backend microservices
    AUTH_SERVICE_URL: str = os.getenv("AUTH_SERVICE_URL", "http://localhost:8001")
    SPOTIFY_SERVICE_URL: str = os.getenv("SPOTIFY_SERVICE_URL", "http://localhost:8002")
    MOOD_SERVICE_URL: str = os.getenv("MOOD_SERVICE_URL", "http://localhost:8003")
    AI_SERVICE_URL: str = os.getenv("AI_SERVICE_URL", "http://localhost:8004")
    ANALYTICS_SERVICE_URL: str = os.getenv("ANALYTICS_SERVICE_URL", "http://localhost:8005")

    # API Timeouts
    DEFAULT_TIMEOUT: int = int(os.getenv("API_TIMEOUT", "15"))

settings = Settings()
