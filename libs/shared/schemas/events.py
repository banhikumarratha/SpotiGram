from pydantic import BaseModel, Field
from datetime import datetime
from typing import Any, Dict
import uuid

class BaseEventEnvelope(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    correlation_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    event_type: str
    version: str = "1.0"
    payload: Dict[str, Any]

class UserCreatedPayload(BaseModel):
    user_id: str
    username: str

class TrackPlayedPayload(BaseModel):
    user_id: str
    spotify_track_id: str
    context_uri: str | None = None
