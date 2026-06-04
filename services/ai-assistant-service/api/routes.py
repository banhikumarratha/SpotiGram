from fastapi import APIRouter, Depends
from libs.shared.schemas.domain import TrackInfo
from libs.shared.enums import Mood
from application.workflows import build_ai_dj_workflow
from typing import List

router = APIRouter(prefix="/api/v1/ai", tags=["AI"])
dj_app = build_ai_dj_workflow()

@router.get("/recommendations", response_model=List[TrackInfo])
async def get_recommendations(mood: Mood, user_id: str = "default_user"):
    # Run the LangGraph workflow
    inputs = {"user_id": user_id, "mood": mood.value, "history": "", "recommendation": ""}
    output = dj_app.invoke(inputs)
    
    return [
        TrackInfo(
            spotify_id="ai_track_1",
            title=output["recommendation"][:50], # Truncated for schema fit
            artist="AI DJ",
            duration_ms=180000
        )
    ]
