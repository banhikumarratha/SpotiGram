from pydantic import BaseModel
from typing import List
from ...enums import MoodType
from .music import Track

class MoodScanResult(BaseModel):
    mood: MoodType
    confidence: float
    recommended_tracks: List[Track]

class ChatPrompt(BaseModel):
    text: str

class ChatResponse(BaseModel):
    response_text: str
    playlist: List[Track] = []
