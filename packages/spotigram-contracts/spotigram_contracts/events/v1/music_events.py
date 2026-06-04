from pydantic import BaseModel
from typing import Optional
from .base import BaseEvent
from ...enums import MoodType

class TrackPlayedPayload(BaseModel):
    user_id: str
    track_id: str
    context_type: str  # e.g., "feed", "playlist", "ai_dj"

class TrackPlayedEvent(BaseEvent):
    payload: TrackPlayedPayload

class MoodScannedPayload(BaseModel):
    user_id: str
    detected_mood: MoodType
    confidence: float

class MoodScannedEvent(BaseEvent):
    payload: MoodScannedPayload
