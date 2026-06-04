from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from libs.shared.schemas.domain import TrackInfo
from application.recommendation_logic import RecommendationLogic

router = APIRouter(prefix="/api/v1/recommend", tags=["Recommendation"])
logic = RecommendationLogic()

class RecommendRequest(BaseModel):
    vector: List[float]

@router.post("", response_model=List[TrackInfo])
async def get_recommendations(req: RecommendRequest):
    tracks = logic.get_similar_tracks(req.vector)
    return tracks
