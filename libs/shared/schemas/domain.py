from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from libs.shared.enums import Mood

class UserProfile(BaseModel):
    id: str
    username: str
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None
    created_at: datetime

class TrackInfo(BaseModel):
    spotify_id: str
    title: str
    artist: str
    album_art_url: Optional[str] = None
    duration_ms: int

class Post(BaseModel):
    id: str
    user_id: str
    track: TrackInfo
    caption: Optional[str] = None
    mood: Optional[Mood] = None
    created_at: datetime
