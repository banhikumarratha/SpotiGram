from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from libs.shared.schemas.domain import Post, TrackInfo
from libs.shared.enums import Mood
from infrastructure.database.session import get_db
from infrastructure.database.repository import PostRepository
from application.post_service import PostService
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/api/v1/posts", tags=["Posts"])

class CreatePostRequest(BaseModel):
    user_id: str
    track: TrackInfo
    caption: str | None = None
    mood: Mood | None = None

def get_post_service(db: Session = Depends(get_db)) -> PostService:
    repo = PostRepository(db)
    return PostService(repo)

@router.get("", response_model=List[Post])
async def get_feed(limit: int = 20, offset: int = 0, svc: PostService = Depends(get_post_service)):
    return svc.get_feed(limit, offset)

@router.post("", response_model=Post, status_code=status.HTTP_201_CREATED)
async def create_post(req: CreatePostRequest, svc: PostService = Depends(get_post_service)):
    return svc.create_post(req.user_id, req.track, req.caption, req.mood)
