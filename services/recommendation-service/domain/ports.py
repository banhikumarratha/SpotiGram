"""
Domain ports (abstract interfaces) for the recommendation-service.
Application logic depends only on these interfaces — never on concrete infrastructure.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from domain.models import MusicDNA, TrackEmbedding, SimilarUser, Recommendation


class VectorStorePort(ABC):
    """Port for storing and querying embeddings."""

    @abstractmethod
    async def upsert_user_dna(self, user_id: str, embedding: List[float], metadata: dict) -> None:
        """Store or update a user's Music DNA embedding."""
        ...

    @abstractmethod
    async def query_similar_users(self, embedding: List[float], top_k: int = 10) -> List[SimilarUser]:
        """Find users with similar Music DNA."""
        ...

    @abstractmethod
    async def upsert_track(self, track: TrackEmbedding) -> None:
        """Store or update a track embedding."""
        ...

    @abstractmethod
    async def query_similar_tracks(self, embedding: List[float], top_k: int = 20) -> List[dict]:
        """Find tracks similar to a given embedding."""
        ...


class EmbeddingPort(ABC):
    """Port for generating text embeddings from track metadata."""

    @abstractmethod
    def encode(self, text: str) -> List[float]:
        """Return a fixed-dimension float vector for the given text."""
        ...


class MoodDetectorPort(ABC):
    """Port for detecting mood from a raw image."""

    @abstractmethod
    async def detect(self, image_b64: str) -> dict:
        """Return a dict with 'mood' (Mood enum value) and 'confidence' (float)."""
        ...


class DNARepositoryPort(ABC):
    """Port for persisting and loading Music DNA state."""

    @abstractmethod
    async def get(self, user_id: str) -> Optional[MusicDNA]:
        ...

    @abstractmethod
    async def save(self, dna: MusicDNA) -> None:
        ...


class EventPublisherPort(ABC):
    """Port for publishing outbound domain events."""

    @abstractmethod
    async def publish(self, event: dict) -> None:
        ...
