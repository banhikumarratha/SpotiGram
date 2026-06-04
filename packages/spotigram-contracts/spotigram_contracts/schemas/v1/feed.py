from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from ...enums import FeedItemType
from .user import UserProfile
from .music import Track

class Comment(BaseModel):
    comment_id: str
    user: UserProfile
    text: str
    timestamp: datetime

class FeedPost(BaseModel):
    post_id: str
    user: UserProfile
    item_type: FeedItemType
    track: Optional[Track] = None
    caption: str
    like_count: int = 0
    comments: List[Comment] = []
    created_at: datetime
