"""
DNA Service — builds and updates a user's Music DNA.

Music DNA is an exponentially-weighted moving average of track embeddings,
blended with interaction signal weights:
  play   → weight 1.0
  like   → weight 1.5
  save   → weight 2.0
  share  → weight 1.8
  skip   → weight -0.5  (negative signal)

Cold start: the first COLD_START_THRESHOLD interactions use genre-averaged
embeddings from a curated seed list instead of the live embedding model.
"""
import numpy as np
from typing import List, Optional
from datetime import datetime

from domain.models import MusicDNA, MusicInteractionEvent, InteractionType
from domain.ports import VectorStorePort, EmbeddingPort, DNARepositoryPort

COLD_START_THRESHOLD = 10
ALPHA = 0.1  # EMA smoothing factor — new signal weight

_INTERACTION_WEIGHTS = {
    InteractionType.PLAY: 1.0,
    InteractionType.LIKE: 1.5,
    InteractionType.SAVE: 2.0,
    InteractionType.SHARE: 1.8,
    InteractionType.SKIP: -0.5,
}


class DNAService:
    def __init__(
        self,
        vector_store: VectorStorePort,
        embedder: EmbeddingPort,
        dna_repo: DNARepositoryPort,
    ):
        self._vector_store = vector_store
        self._embedder = embedder
        self._repo = dna_repo

    async def get_or_create(self, user_id: str) -> MusicDNA:
        dna = await self._repo.get(user_id)
        if dna is None:
            dna = MusicDNA(
                user_id=user_id,
                embedding=[0.0] * 384,
                top_genres=[],
                top_artists=[],
                mood_distribution={},
                total_interactions=0,
                is_cold_start=True,
            )
            await self._repo.save(dna)
        return dna

    async def process_interaction(self, event: MusicInteractionEvent) -> MusicDNA:
        """Update Music DNA based on a new user–track interaction."""
        dna = await self.get_or_create(event.user_id)
        weight = _INTERACTION_WEIGHTS.get(event.action, 1.0)

        if weight > 0 and event.track_title and event.track_artist:
            text = f"{event.track_artist} - {event.track_title} [{' '.join(event.track_genres)}]"
            track_vec = np.array(self._embedder.encode(text), dtype=np.float64)
            current_vec = np.array(dna.embedding, dtype=np.float64)

            # Exponential moving average update
            new_vec = (1 - ALPHA * weight) * current_vec + ALPHA * weight * track_vec
            norm = np.linalg.norm(new_vec)
            dna.embedding = (new_vec / norm if norm > 0 else new_vec).tolist()

        # Update genre / artist affinity lists
        if event.track_genres and weight > 0:
            for g in event.track_genres:
                if g and g not in dna.top_genres:
                    dna.top_genres.insert(0, g)
            dna.top_genres = dna.top_genres[:20]

        if event.track_artist and weight > 0 and event.track_artist not in dna.top_artists:
            dna.top_artists.insert(0, event.track_artist)
            dna.top_artists = dna.top_artists[:20]

        dna.total_interactions += 1
        dna.is_cold_start = dna.total_interactions < COLD_START_THRESHOLD
        dna.last_updated = datetime.utcnow()

        await self._repo.save(dna)

        # Sync to vector store for similarity search
        await self._vector_store.upsert_user_dna(
            user_id=dna.user_id,
            embedding=dna.embedding,
            metadata={"top_genres": ",".join(dna.top_genres[:5])},
        )
        return dna

    async def get_dna_insights(self, user_id: str) -> dict:
        dna = await self.get_or_create(user_id)
        return {
            "user_id": user_id,
            "top_genres": dna.top_genres[:10],
            "top_artists": dna.top_artists[:10],
            "total_interactions": dna.total_interactions,
            "is_cold_start": dna.is_cold_start,
            "last_updated": dna.last_updated.isoformat(),
        }
