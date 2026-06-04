"""Unit tests for domain models."""
import pytest
from dataclasses import asdict
from datetime import datetime

from domain.models import (
    Mood, MoodProfile, MusicDNA, TrackEmbedding,
    Recommendation, RecommendationFeed, SimilarUser,
    MusicInteractionEvent, InteractionType,
)


def test_mood_enum_values():
    assert Mood.HAPPY.value == "happy"
    assert Mood.ENERGETIC.value == "energetic"
    assert Mood.SAD.value == "sad"


def test_mood_profile_defaults():
    profile = MoodProfile(user_id="u1", mood=Mood.CALM, confidence=0.85)
    assert profile.source == "webcam"
    assert isinstance(profile.detected_at, datetime)


def test_music_dna_cold_start_default():
    dna = MusicDNA(
        user_id="u1",
        embedding=[0.0] * 384,
        top_genres=["pop"],
        top_artists=["Artist A"],
        mood_distribution={"happy": 0.6},
        total_interactions=0,
    )
    assert dna.is_cold_start is True


def test_interaction_type_negative_signal():
    assert InteractionType.SKIP.value == "skip"
    assert InteractionType.LIKE.value == "like"


def test_recommendation_score_range():
    rec = Recommendation(
        track_id="t1",
        title="Song",
        artist="Artist",
        score=0.75,
        explanation="Because you like pop",
        signals={"dna": 0.8, "mood": 0.7},
    )
    assert 0.0 <= rec.score <= 1.0


def test_recommendation_feed_structure():
    feed = RecommendationFeed(
        user_id="u1",
        recommendations=[],
        mood=Mood.HAPPY,
        is_cold_start=True,
    )
    assert feed.user_id == "u1"
    assert feed.mood == Mood.HAPPY


def test_track_embedding_no_embedding_by_default():
    track = TrackEmbedding(track_id="t1", title="Song", artist="A", genres=["pop"])
    assert track.embedding is None
