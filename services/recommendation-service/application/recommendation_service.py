"""
Recommendation Service — core ranking engine.

Ranking pipeline per user request:
  1. Fetch user's Music DNA embedding
  2. Vector search for similar tracks in ChromaDB
  3. Find similar users via DNA similarity
  4. Apply mood energy signal to re-weight scores
  5. Apply time-of-day decay (morning → calmer, evening → energetic)
  6. Blend signals into a final normalized score
  7. Attach human-readable explanations
  8. Cold start fallback: return genre seeded tracks if DNA is immature

Signal weights (configurable via env):
  DNA_WEIGHT     = 0.40
  MOOD_WEIGHT    = 0.25
  SOCIAL_WEIGHT  = 0.20
  TOD_WEIGHT     = 0.15
"""
import os
from datetime import datetime, timezone
from typing import List, Optional

from domain.models import (
    Mood, MusicDNA, Recommendation, RecommendationFeed, SimilarUser
)
from domain.ports import VectorStorePort, EmbeddingPort, EventPublisherPort, DNARepositoryPort
from application.mood_service import MoodService, MOOD_ENERGY
import uuid

DNA_W = float(os.getenv("SIGNAL_DNA_WEIGHT", "0.40"))
MOOD_W = float(os.getenv("SIGNAL_MOOD_WEIGHT", "0.25"))
SOCIAL_W = float(os.getenv("SIGNAL_SOCIAL_WEIGHT", "0.20"))
TOD_W = float(os.getenv("SIGNAL_TOD_WEIGHT", "0.15"))

# Cold-start curated genre seed (used when DNA is immature)
COLD_START_GENRES = ["pop", "indie", "electronic", "hip-hop", "rock"]


def _time_of_day_energy() -> float:
    """Returns a 0–1 energy level based on the current hour (UTC)."""
    hour = datetime.now(timezone.utc).hour
    if 6 <= hour < 12:
        return 0.4   # morning — calmer
    elif 12 <= hour < 17:
        return 0.65  # afternoon — moderate
    elif 17 <= hour < 22:
        return 0.85  # evening — energetic
    else:
        return 0.3   # late night — chill


def _build_explanation(track: dict, signals: dict, mood: Optional[Mood], is_social: bool) -> str:
    parts = []
    if mood and signals.get("mood", 0) > 0.5:
        parts.append(f"Matches your {mood.value} mood")
    if signals.get("dna", 0) > 0.6:
        parts.append("fits your Music DNA")
    if is_social:
        parts.append("popular with listeners like you")
    genre = track.get("genres", "").split(",")[0] if track.get("genres") else ""
    if genre:
        parts.append(f"in {genre}")
    return " · ".join(parts) if parts else "Recommended for you"


class RecommendationService:
    def __init__(
        self,
        vector_store: VectorStorePort,
        embedder: EmbeddingPort,
        dna_repo: DNARepositoryPort,
        publisher: Optional[EventPublisherPort] = None,
    ):
        self._vector_store = vector_store
        self._embedder = embedder
        self._dna_repo = dna_repo
        self._publisher = publisher

    async def generate_feed(
        self,
        user_id: str,
        mood: Optional[Mood] = None,
        limit: int = 20,
    ) -> RecommendationFeed:
        dna = await self._dna_repo.get(user_id)
        is_cold = dna is None or dna.is_cold_start

        if is_cold:
            return self._cold_start_feed(user_id, mood, limit)

        # Step 1: Vector search using user DNA
        similar_tracks = await self._vector_store.query_similar_tracks(
            dna.embedding, top_k=limit * 2
        )

        # Step 2: Find social signal from similar users
        similar_users = await self._vector_store.query_similar_users(
            dna.embedding, top_k=5
        )
        social_track_ids = {u.user_id for u in similar_users}  # simplified social signal

        # Step 3: Mood energy
        mood_energy = MOOD_ENERGY.get(mood, 0.5) if mood else 0.5
        tod_energy = _time_of_day_energy()

        # Step 4: Score and rank
        ranked: List[Recommendation] = []
        for track in similar_tracks:
            dna_score = float(track.get("similarity", 0))
            mood_score = 1.0 - abs(mood_energy - dna_score)
            social_score = 0.8 if track["track_id"] in social_track_ids else 0.2
            tod_score = 1.0 - abs(tod_energy - dna_score)

            final_score = (
                DNA_W * dna_score
                + MOOD_W * mood_score
                + SOCIAL_W * social_score
                + TOD_W * tod_score
            )

            signals = {
                "dna": round(dna_score, 3),
                "mood": round(mood_score, 3),
                "social": round(social_score, 3),
                "time_of_day": round(tod_score, 3),
            }

            explanation = _build_explanation(
                track, signals, mood, track["track_id"] in social_track_ids
            )

            ranked.append(Recommendation(
                track_id=track["track_id"],
                title=track.get("title", ""),
                artist=track.get("artist", ""),
                score=round(final_score, 4),
                explanation=explanation,
                signals=signals,
            ))

        ranked.sort(key=lambda r: r.score, reverse=True)

        feed = RecommendationFeed(
            user_id=user_id,
            recommendations=ranked[:limit],
            mood=mood,
            is_cold_start=False,
        )

        if self._publisher:
            await self._publisher.publish({
                "headers": {
                    "event_id": str(uuid.uuid4()),
                    "version": "v1",
                    "timestamp": datetime.utcnow().isoformat(),
                },
                "payload": {
                    "user_id": user_id,
                    "feed_size": len(feed.recommendations),
                    "mood": mood.value if mood else None,
                }
            })

        return feed

    def _cold_start_feed(
        self, user_id: str, mood: Optional[Mood], limit: int
    ) -> RecommendationFeed:
        """Returns placeholder recommendations for new users with empty DNA."""
        recs = [
            Recommendation(
                track_id=f"cold_start_{g}",
                title=f"Top {g.capitalize()} Tracks",
                artist="Various Artists",
                score=0.5,
                explanation=f"Popular in {g} to get you started",
                signals={"cold_start": 1.0},
            )
            for g in COLD_START_GENRES[:limit]
        ]
        return RecommendationFeed(
            user_id=user_id,
            recommendations=recs,
            mood=mood,
            is_cold_start=True,
        )

    async def find_similar_users(self, user_id: str) -> List[SimilarUser]:
        dna = await self._dna_repo.get(user_id)
        if dna is None:
            return []
        return await self._vector_store.query_similar_users(dna.embedding, top_k=10)
