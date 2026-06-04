from dataclasses import dataclass, field
from datetime import date, datetime
from typing import List, Dict, Optional


@dataclass
class DailyUserStats:
    """Materialized daily aggregate per user."""
    user_id: str
    stat_date: date
    total_plays: int = 0
    total_skips: int = 0
    total_likes: int = 0
    total_shares: int = 0
    dominant_mood: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class ListeningStats:
    """Response model for listening statistics."""
    user_id: str
    timeframe: str
    total_plays: int
    total_skips: int
    completion_rate: float


@dataclass
class MoodTrend:
    """Response model for mood trends."""
    user_id: str
    timeframe: str
    mood_counts: Dict[str, int]
    dominant_mood: str


@dataclass
class MusicPersonality:
    """Response model for derived music personality traits."""
    user_id: str
    traits: List[str]
    description: str


@dataclass
class YearInReview:
    """Response model for Year in Review (Spotigram Wrapped)."""
    user_id: str
    year: int
    total_minutes: int
    top_genres: List[str]
    top_artists: List[str]
    dominant_mood: str
