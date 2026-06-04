from fastapi import APIRouter, Depends, HTTPException, status
from libs.shared.schemas.domain import TrackInfo
from libs.shared.schemas.common import ErrorResponse, ErrorDetail
from application.music_service import MusicService

router = APIRouter(prefix="/api/v1/music", tags=["Music"])

def get_music_service() -> MusicService:
    return MusicService()

@router.get("/tracks/{track_id}", response_model=TrackInfo, responses={404: {"model": ErrorResponse}})
async def get_track(track_id: str, svc: MusicService = Depends(get_music_service)):
    track = svc.get_track_info(track_id)
    if not track:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=ErrorResponse(success=False, error=ErrorDetail(code="TRACK_NOT_FOUND", message="Track not found")).model_dump()
        )
    return track
