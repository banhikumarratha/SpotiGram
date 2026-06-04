from pydantic import BaseModel
from typing import List, Optional

class Artist(BaseModel):
    id: str
    name: str
    genres: List[str]

class Track(BaseModel):
    id: str
    name: str
    artists: List[Artist]
    album_image_url: Optional[str] = None
    preview_url: Optional[str] = None
    duration_ms: int
