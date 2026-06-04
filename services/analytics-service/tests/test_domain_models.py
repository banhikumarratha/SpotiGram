import pytest
from datetime import date
from domain.models import DailyUserStats, ListeningStats, MoodTrend, MusicPersonality, YearInReview
from domain.events import MusicInteractionEvent, MoodDetectedEvent
from pydantic import ValidationError


def test_daily_user_stats():
    stats = DailyUserStats(user_id="u1", stat_date=date.today(), total_plays=5)
    assert stats.total_plays == 5
    assert stats.total_skips == 0


def test_listening_stats():
    ls = ListeningStats(user_id="u1", timeframe="Last 30 days", total_plays=10, total_skips=2, completion_rate=0.8)
    assert ls.completion_rate == 0.8


def test_music_interaction_event_valid():
    event = MusicInteractionEvent(event_id="e1", user_id="u1", track_id="t1", action="play")
    assert event.action == "play"


def test_music_interaction_event_invalid():
    with pytest.raises(ValidationError):
        # Missing user_id
        MusicInteractionEvent(event_id="e1", track_id="t1", action="play")


def test_mood_detected_event_valid():
    event = MoodDetectedEvent(event_id="e2", user_id="u1", mood="happy", confidence=0.9)
    assert event.mood == "happy"
