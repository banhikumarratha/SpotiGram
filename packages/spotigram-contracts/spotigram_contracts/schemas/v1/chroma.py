from pydantic import BaseModel
from typing import List
from ...enums import MoodType

class ChromaTrackMetadata(BaseModel):
    track_id: str
    artist_ids: List[str]
    genres: List[str]
    associated_moods: List[MoodType]
    tempo: float
