from fastapi import APIRouter, Request, HTTPException
from application.catalog_service import CatalogService
from application.playback_service import PlaybackService
from infrastructure.kafka_publisher import KafkaPublisher
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/music", tags=["Music"])
publisher = KafkaPublisher(topic="music.events.v1")

class PlaybackRequest(BaseModel):
    track_id: str
    action: str

@router.get("/search")
async def search_music(q: str, type: str = "track"):
    service = CatalogService()
    try:
        res = await service.search(q, type)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tracks/{track_id}")
async def get_track(track_id: str):
    service = CatalogService()
    try:
        res = await service.get_track(track_id)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/playback")
async def register_playback(req: PlaybackRequest, request: Request):
    user_id = request.headers.get("X-User-ID", "anonymous")
    service = PlaybackService(publisher)
    try:
        res = await service.emit_playback_event(user_id, req.track_id, req.action)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


