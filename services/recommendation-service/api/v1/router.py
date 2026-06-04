"""
API v1 router for the recommendation-service.

Endpoints:
  POST /api/v1/recommendations/mood-scan          → run emotion detection
  GET  /api/v1/recommendations/feed               → personalized track feed
  GET  /api/v1/recommendations/similar-users      → users with similar Music DNA
  GET  /api/v1/recommendations/music-dna          → user's DNA insights
  POST /api/v1/recommendations/feedback           → submit interaction feedback
"""
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Optional, List
import os

from domain.models import Mood
from infrastructure.chroma_client import ChromaVectorStore
from infrastructure.embedder import SentenceTransformerEmbedder
from infrastructure.dna_repository import InMemoryDNARepository
from infrastructure.kafka_publisher import KafkaRecommendationPublisher
from infrastructure.mood_detector import DeepFaceMoodDetector
from application.mood_service import MoodService
from application.dna_service import DNAService
from application.recommendation_service import RecommendationService

router = APIRouter(prefix="/api/v1/recommendations", tags=["Recommendations"])

# ── Shared singletons (created once at router import time) ──────────────────
_vector_store = ChromaVectorStore(ephemeral=os.getenv("CHROMA_EPHEMERAL", "false").lower() == "true")
_embedder = SentenceTransformerEmbedder()
_dna_repo = InMemoryDNARepository()
_publisher = KafkaRecommendationPublisher()
_detector = DeepFaceMoodDetector()

_mood_svc = MoodService(_detector)
_dna_svc = DNAService(_vector_store, _embedder, _dna_repo)
_rec_svc = RecommendationService(_vector_store, _embedder, _dna_repo, _publisher)


# ── Request / Response schemas ───────────────────────────────────────────────

class MoodScanRequest(BaseModel):
    image_b64: str  # Base64-encoded webcam frame (JPEG/PNG)

class FeedbackRequest(BaseModel):
    track_id: str
    action: str   # play | like | save | skip | share
    track_title: Optional[str] = ""
    track_artist: Optional[str] = ""
    track_genres: Optional[List[str]] = []


# ── Endpoints ────────────────────────────────────────────────────────────────

@router.post("/mood-scan")
async def mood_scan(
    req: MoodScanRequest,
    x_user_id: str = Header(..., alias="X-User-ID"),
):
    """Analyze a webcam image and return detected mood."""
    try:
        profile = await _mood_svc.scan(x_user_id, req.image_b64)
        return {
            "user_id": profile.user_id,
            "mood": profile.mood.value,
            "confidence": profile.confidence,
            "detected_at": profile.detected_at.isoformat(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/feed")
async def get_feed(
    mood: Optional[str] = None,
    limit: int = 20,
    x_user_id: str = Header(..., alias="X-User-ID"),
):
    """Return a personalized recommendation feed, optionally filtered by mood."""
    try:
        mood_enum = Mood(mood) if mood else None
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid mood: {mood}")

    try:
        feed = await _rec_svc.generate_feed(x_user_id, mood_enum, limit)
        return {
            "user_id": feed.user_id,
            "mood": feed.mood.value if feed.mood else None,
            "is_cold_start": feed.is_cold_start,
            "generated_at": feed.generated_at.isoformat(),
            "recommendations": [
                {
                    "track_id": r.track_id,
                    "title": r.title,
                    "artist": r.artist,
                    "score": r.score,
                    "explanation": r.explanation,
                    "signals": r.signals,
                }
                for r in feed.recommendations
            ],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/similar-users")
async def get_similar_users(
    x_user_id: str = Header(..., alias="X-User-ID"),
):
    """Find users with similar Music DNA."""
    try:
        users = await _rec_svc.find_similar_users(x_user_id)
        return {
            "user_id": x_user_id,
            "similar_users": [
                {
                    "user_id": u.user_id,
                    "similarity_score": u.similarity_score,
                    "shared_genres": u.shared_genres,
                }
                for u in users
            ],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/music-dna")
async def get_music_dna(
    x_user_id: str = Header(..., alias="X-User-ID"),
):
    """Return a user's Music DNA insights."""
    try:
        insights = await _dna_svc.get_dna_insights(x_user_id)
        return insights
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/feedback")
async def submit_feedback(
    req: FeedbackRequest,
    x_user_id: str = Header(..., alias="X-User-ID"),
):
    """Submit user interaction feedback to update Music DNA."""
    from domain.models import MusicInteractionEvent, InteractionType
    from datetime import datetime

    try:
        action = InteractionType(req.action)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid action: {req.action}")

    event = MusicInteractionEvent(
        user_id=x_user_id,
        track_id=req.track_id,
        action=action,
        timestamp=datetime.utcnow(),
        track_title=req.track_title or "",
        track_artist=req.track_artist or "",
        track_genres=req.track_genres or [],
    )

    try:
        dna = await _dna_svc.process_interaction(event)
        return {
            "user_id": x_user_id,
            "total_interactions": dna.total_interactions,
            "is_cold_start": dna.is_cold_start,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
