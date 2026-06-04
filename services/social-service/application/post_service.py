from infrastructure.database.repository import PostRepository
from libs.shared.schemas.domain import Post, TrackInfo
from libs.shared.enums import Mood
from typing import List

class PostService:
    def __init__(self, repo: PostRepository):
        self.repo = repo

    def get_feed(self, limit: int = 20, offset: int = 0) -> List[Post]:
        records = self.repo.get_recent_posts(limit, offset)
        return [
            Post(
                id=r.id,
                user_id=r.user_id,
                track=TrackInfo(**r.track),
                caption=r.caption,
                mood=Mood(r.mood) if r.mood else None,
                created_at=r.created_at
            ) for r in records
        ]

    def create_post(self, user_id: str, track: TrackInfo, caption: str = None, mood: Mood = None) -> Post:
        record = self.repo.create(
            user_id=user_id, 
            track=track.model_dump(), 
            caption=caption, 
            mood=mood.value if mood else None
        )
        return Post(
            id=record.id,
            user_id=record.user_id,
            track=TrackInfo(**record.track),
            caption=record.caption,
            mood=Mood(record.mood) if record.mood else None,
            created_at=record.created_at
        )
