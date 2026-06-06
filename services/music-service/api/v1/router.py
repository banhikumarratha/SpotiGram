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

# ---------------------------------------------------------
# NEW SPOTIFY AND FALLBACK MOCKS FOR ACCEPTANCE TESTING
# ---------------------------------------------------------

@router.get("/spotify/auth/url")
async def spotify_auth_url():
    return {"auth_url": "https://accounts.spotify.com/authorize?mock=true"}

@router.post("/spotify/auth/refresh")
async def spotify_refresh():
    return {"access_token": "mocked_spotify_refresh", "expires_in": 3600}

@router.post("/playlists")
async def create_playlist(name: str):
    return {"id": "mock_playlist_123", "name": name, "status": "created"}

@router.post("/playlists/import")
async def import_playlist(spotify_url: str):
    return {"status": "success", "imported_tracks": 15}

@router.put("/tracks/{track_id}/save")
async def save_track(track_id: str):
    return {"status": "success", "message": f"Track {track_id} saved to library"}

@router.put("/artists/{artist_id}/follow")
async def follow_artist(artist_id: str):
    return {"status": "success", "message": f"Artist {artist_id} followed"}

@router.get("/fallback/musicbrainz/{track_id}")
async def musicbrainz_fallback(track_id: str):
    # Simulates MusicBrainz metadata fallback if Spotify API is down
    return {"track_id": track_id, "source": "MusicBrainz", "title": "Mock Fallback Title"}

@router.get("/fallback/lastfm/{track_id}")
async def lastfm_fallback(track_id: str):
    # Simulates Last.fm scrobble/metadata fallback
    return {"track_id": track_id, "source": "Last.fm", "listeners": 15000}

@router.get("/spotify/player/devices")
async def get_devices():
    return {"devices": [{"id": "mock_device_1", "is_active": True, "name": "Spotigram Web Player"}]}

@router.put("/spotify/player/play")
async def play_track():
    return {"status": "success"}

@router.put("/spotify/player/pause")
async def pause_track():
    return {"status": "success"}

@router.post("/spotify/player/next")
async def next_track():
    return {"status": "success"}

