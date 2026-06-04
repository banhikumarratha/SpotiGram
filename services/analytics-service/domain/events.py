from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class MusicInteractionEvent(BaseModel):
    """Event schema for music.interactions.v1"""
    event_id: str
    user_id: str
    track_id: str
    action: str  # play, skip, like, share, complete
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class MoodDetectedEvent(BaseModel):
    """Event schema for mood.detected.v1"""
    event_id: str
    user_id: str
    mood: str
    confidence: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)
