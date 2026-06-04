from fastapi import APIRouter, Header, HTTPException, Query
from application.analytics_service import AnalyticsService

router = APIRouter(prefix="/api/v1/analytics", tags=["Analytics"])

_analytics_service = None

def get_analytics_service() -> AnalyticsService:
    if not _analytics_service:
        raise RuntimeError("Analytics Service not initialized")
    return _analytics_service


@router.get("/listening-stats")
async def get_listening_stats(
    days: int = Query(30, description="Number of days to look back"),
    x_user_id: str = Header(..., alias="X-User-ID")
):
    try:
        svc = get_analytics_service()
        stats = await svc.get_listening_stats(user_id=x_user_id, days=days)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/mood-trends")
async def get_mood_trends(
    days: int = Query(30, description="Number of days to look back"),
    x_user_id: str = Header(..., alias="X-User-ID")
):
    try:
        svc = get_analytics_service()
        trends = await svc.get_mood_trend(user_id=x_user_id, days=days)
        return trends
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/personality")
async def get_music_personality(x_user_id: str = Header(..., alias="X-User-ID")):
    try:
        svc = get_analytics_service()
        personality = await svc.get_music_personality(user_id=x_user_id)
        return personality
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/year-in-review")
async def get_year_in_review(
    year: int = Query(..., description="The year for the review"),
    x_user_id: str = Header(..., alias="X-User-ID")
):
    try:
        svc = get_analytics_service()
        review = await svc.get_year_in_review(user_id=x_user_id, year=year)
        return review
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
