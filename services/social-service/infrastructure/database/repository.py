from sqlalchemy.orm import Session
from infrastructure.database.models import PostRecord
from typing import List

class PostRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_recent_posts(self, limit: int = 20, offset: int = 0) -> List[PostRecord]:
        return self.db.query(PostRecord).order_by(PostRecord.created_at.desc()).offset(offset).limit(limit).all()

    def create(self, user_id: str, track: dict, caption: str = None, mood: str = None) -> PostRecord:
        post = PostRecord(user_id=user_id, track=track, caption=caption, mood=mood)
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)
        return post
