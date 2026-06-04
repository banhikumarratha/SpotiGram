from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserProfile(BaseModel):
    user_id: str
    display_name: str
    avatar_url: Optional[str] = None
    follower_count: int = 0
    following_count: int = 0
    created_at: datetime
