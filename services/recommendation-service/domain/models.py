"""
Domain models for the recommendation-service.
Pure dataclasses — no framework dependencies.
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime


class Mood(str, Enum):
    HAPPY = "happy"
    SAD = "sad"
    ENERGETIC = "energetic"
    CALM = "calm"
    ANGRY = "angry"
    NEUTRAL = "neutral"


class InteractionType(str, Enum):
    PLAY = "play"
    SKIP = "skip"
    LIKE = "like"
    SAVE = "save"
    SHARE = "share"


@dataclass
class MoodProfile:
    """Detected mood from webcam image or inferred from listening history."""
    user_id: str
    mood: Mood
    confidence: float
    detected_at: datetime = field(default_factory=datetime.utcnow)
    source: str = "webcam"  # webcam | inferred


@dataclass
class TrackEmbedding:
    """A music track represented as a vector embedding."""
    track_id: str
    title: str
    artist: str
    genres: List[str]
    embedding: Optional[List[float]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MusicDNA:
    """
    A user's musical fingerprint — a weighted embedding of their listening
    history, genre affinities, and interaction signals.
    """
    user_id: str
    embedding: List[float]
    top_genres: List[str]
    top_artists: List[str]
    mood_distribution: Dict[str, float]  # mood -> fraction
    total_interactions: int
    last_updated: datetime = field(default_factory=datetime.utcnow)
    is_cold_start: bool = True  # True until >= COLD_START_THRESHOLD interactions

    COLD_START_THRESHOLD: int = field(default=10, init=False, repr=False)


@dataclass
class Recommendation:
    """A single recommended track with ranking metadata."""
    track_id: str
    title: str
    artist: str
    score: float                  # 0.0 – 1.0 normalized final rank score
    explanation: str              # Human-readable reason
    signals: Dict[str, float]     # Individual signal breakdown: mood, dna, social, etc.


@dataclass
class RecommendationFeed:
    """Paginated feed of recommendations for a user."""
    user_id: str
    recommendations: List[Recommendation]
    mood: Optional[Mood]
    generated_at: datetime = field(default_factory=datetime.utcnow)
    is_cold_start: bool = False


@dataclass
class SimilarUser:
    """A user discovered as similar via Music DNA vector search."""
    user_id: str
    similarity_score: float
    shared_genres: List[str]


@dataclass
class MusicInteractionEvent:
    """Inbound Kafka event from music-service."""
    user_id: str
    track_id: str
    action: InteractionType
    timestamp: datetime
    track_title: str = ""
    track_artist: str = ""
    track_genres: List[str] = field(default_factory=list)
