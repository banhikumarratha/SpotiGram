"""
API v1 router for ai-assistant-service.

Endpoints:
  POST /api/v1/ai/chat       → single-turn chat with memory
  POST /api/v1/ai/stream     → streaming SSE chat
  POST /api/v1/ai/dj         → AI DJ session interaction
  POST /api/v1/ai/playlist   → generate themed playlist
  POST /api/v1/ai/explain    → explain a recommendation
"""
from fastapi import APIRouter, Header, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from domain.models import UserContext
from memory.conversation_store import InMemoryConversationStore
from providers.registry import ProviderRegistry
from application.assistant_service import AssistantService
from application.dj_service import DJService
from application.playlist_service import PlaylistService

router = APIRouter(prefix="/api/v1/ai", tags=["AI Assistant"])

# ── Singletons ────────────────────────────────────────────────────────────────
_memory_store = InMemoryConversationStore()
_registry = ProviderRegistry()
_dj_service = None
_assistant_service = None
_playlist_service = None


async def _get_provider():
    return await _registry.get_provider()


async def _get_assistant():
    global _assistant_service
    if _assistant_service is None:
        provider = await _get_provider()
        _assistant_service = AssistantService(provider, _memory_store)
    return _assistant_service


async def _get_dj():
    global _dj_service
    if _dj_service is None:
        provider = await _get_provider()
        _dj_service = DJService(provider)
    return _dj_service


async def _get_playlist():
    global _playlist_service
    if _playlist_service is None:
        provider = await _get_provider()
        _playlist_service = PlaylistService(provider)
    return _playlist_service


# ── Request schemas ───────────────────────────────────────────────────────────

class UserContextSchema(BaseModel):
    top_genres: List[str] = []
    top_artists: List[str] = []
    current_mood: Optional[str] = None
    recent_tracks: List[str] = []
    preferences: Dict[str, Any] = {}

    def to_domain(self, user_id: str) -> UserContext:
        return UserContext(
            user_id=user_id,
            top_genres=self.top_genres,
            top_artists=self.top_artists,
            current_mood=self.current_mood,
            recent_tracks=self.recent_tracks,
            preferences=self.preferences,
        )


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    context: Optional[UserContextSchema] = None
    prompt_version: str = "v1"


class DJRequest(BaseModel):
    session_id: Optional[str] = None
    message: str
    current_track: Optional[str] = None
    mood: Optional[str] = None
    context: Optional[UserContextSchema] = None


class PlaylistRequest(BaseModel):
    theme: str
    mood: str = "any"
    context: Optional[UserContextSchema] = None
    prompt_version: str = "v1"


class ExplainRequest(BaseModel):
    track_title: str
    track_artist: str
    signals: Dict[str, float] = {}
    context: Optional[UserContextSchema] = None
    prompt_version: str = "v1"


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.post("/chat")
async def chat(req: ChatRequest, x_user_id: str = Header(..., alias="X-User-ID")):
    """Single-turn chat with conversation memory."""
    try:
        svc = await _get_assistant()
        ctx = req.context.to_domain(x_user_id) if req.context else None
        response = await svc.chat(
            user_id=x_user_id,
            message=req.message,
            context=ctx,
            conversation_id=req.conversation_id,
            prompt_version=req.prompt_version,
        )
        return {
            "content": response.content,
            "provider": response.provider.value,
            "model": response.model,
            "prompt_version": response.prompt_version,
            "latency_ms": response.latency_ms,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/stream")
async def stream_chat(req: ChatRequest, x_user_id: str = Header(..., alias="X-User-ID")):
    """Streaming SSE chat response."""
    try:
        svc = await _get_assistant()
        ctx = req.context.to_domain(x_user_id) if req.context else None

        async def generate():
            async for token in svc.stream(
                user_id=x_user_id,
                message=req.message,
                context=ctx,
                conversation_id=req.conversation_id,
            ):
                yield f"data: {token}\n\n"
            yield "data: [DONE]\n\n"

        return StreamingResponse(generate(), media_type="text/event-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/dj")
async def dj_interact(req: DJRequest, x_user_id: str = Header(..., alias="X-User-ID")):
    """Interact with the AI DJ — get the next track suggestion."""
    try:
        svc = await _get_dj()
        ctx = req.context.to_domain(x_user_id) if req.context else None

        # Auto-start session if no session_id
        if not req.session_id:
            session = await svc.start_session(x_user_id, req.mood)
            session_id = session.session_id
        else:
            session_id = req.session_id

        response = await svc.interact(
            session_id=session_id,
            user_message=req.message,
            context=ctx,
            current_track=req.current_track,
        )
        return {"session_id": session_id, "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/playlist")
async def create_playlist(req: PlaylistRequest, x_user_id: str = Header(..., alias="X-User-ID")):
    """Generate a themed playlist from natural language."""
    try:
        svc = await _get_playlist()
        ctx = req.context.to_domain(x_user_id) if req.context else None
        playlist = await svc.create(
            theme=req.theme,
            context=ctx,
            mood=req.mood,
            prompt_version=req.prompt_version,
        )
        return {
            "name": playlist.name,
            "description": playlist.description,
            "reasoning": playlist.reasoning,
            "track_queries": playlist.track_queries,
            "mood": playlist.mood,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/explain")
async def explain_recommendation(
    req: ExplainRequest, x_user_id: str = Header(..., alias="X-User-ID")
):
    """Generate a human-readable explanation for a recommendation."""
    try:
        svc = await _get_playlist()
        ctx = req.context.to_domain(x_user_id) if req.context else None
        explanation = await svc.explain(
            track_title=req.track_title,
            track_artist=req.track_artist,
            signals=req.signals,
            context=ctx,
            prompt_version=req.prompt_version,
        )
        return {"explanation": explanation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
