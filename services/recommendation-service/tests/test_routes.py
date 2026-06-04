"""
Health check and API contract tests.
Validates endpoint schemas, status codes, and header requirements.
"""
import pytest
import os
from fastapi.testclient import TestClient

os.environ["CHROMA_EPHEMERAL"] = "true"

from main import app

client = TestClient(app)


# ── Observability ─────────────────────────────────────────────────────────────

def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "healthy"}


def test_ready():
    res = client.get("/ready")
    assert res.status_code == 200
    assert res.json() == {"status": "ready"}


def test_metrics():
    res = client.get("/metrics")
    assert res.status_code == 200


# ── Mood Scan ─────────────────────────────────────────────────────────────────

def test_mood_scan_returns_expected_schema(mocker):
    from unittest.mock import AsyncMock
    from domain.models import MoodProfile, Mood
    from datetime import datetime

    mock_profile = MoodProfile(
        user_id="u1",
        mood=Mood.HAPPY,
        confidence=0.9,
        detected_at=datetime(2024, 1, 1),
        source="webcam",
    )
    mocker.patch("api.v1.router._mood_svc.scan", new=AsyncMock(return_value=mock_profile))

    res = client.post(
        "/api/v1/recommendations/mood-scan",
        json={"image_b64": "fake_b64"},
        headers={"X-User-ID": "u1"},
    )
    assert res.status_code == 200
    body = res.json()
    assert body["mood"] == "happy"
    assert "confidence" in body



def test_mood_scan_missing_header():
    res = client.post("/api/v1/recommendations/mood-scan", json={"image_b64": "x"})
    assert res.status_code == 422  # missing required header


# ── Feed ──────────────────────────────────────────────────────────────────────

def test_feed_cold_start():
    res = client.get(
        "/api/v1/recommendations/feed",
        headers={"X-User-ID": "brand_new_user"},
    )
    assert res.status_code == 200
    body = res.json()
    assert body["is_cold_start"] is True
    assert isinstance(body["recommendations"], list)


def test_feed_invalid_mood():
    res = client.get(
        "/api/v1/recommendations/feed?mood=InvalidMood",
        headers={"X-User-ID": "u1"},
    )
    assert res.status_code == 400


def test_feed_valid_mood():
    res = client.get(
        "/api/v1/recommendations/feed?mood=happy",
        headers={"X-User-ID": "u_happy"},
    )
    assert res.status_code == 200


# ── Music DNA ─────────────────────────────────────────────────────────────────

def test_music_dna_schema():
    res = client.get(
        "/api/v1/recommendations/music-dna",
        headers={"X-User-ID": "u_dna"},
    )
    assert res.status_code == 200
    body = res.json()
    assert "top_genres" in body
    assert "total_interactions" in body
    assert "is_cold_start" in body


# ── Similar Users ─────────────────────────────────────────────────────────────

def test_similar_users_schema():
    res = client.get(
        "/api/v1/recommendations/similar-users",
        headers={"X-User-ID": "u_sim"},
    )
    assert res.status_code == 200
    body = res.json()
    assert "similar_users" in body
    assert isinstance(body["similar_users"], list)


# ── Feedback ──────────────────────────────────────────────────────────────────

def test_feedback_updates_dna(mocker):
    from unittest.mock import AsyncMock
    from domain.models import MusicDNA
    from datetime import datetime

    mock_dna = MusicDNA(
        user_id="u_feedback",
        embedding=[0.0] * 384,
        top_genres=["pop"],
        top_artists=["Test Artist"],
        mood_distribution={},
        total_interactions=1,
        is_cold_start=True,
    )
    mocker.patch("api.v1.router._dna_svc.process_interaction", new=AsyncMock(return_value=mock_dna))

    res = client.post(
        "/api/v1/recommendations/feedback",
        json={
            "track_id": "t_test",
            "action": "play",
            "track_title": "Test Song",
            "track_artist": "Test Artist",
            "track_genres": ["pop"],
        },
        headers={"X-User-ID": "u_feedback"},
    )
    assert res.status_code == 200
    body = res.json()
    assert body["total_interactions"] == 1



def test_feedback_invalid_action():
    res = client.post(
        "/api/v1/recommendations/feedback",
        json={"track_id": "t1", "action": "invalid_action"},
        headers={"X-User-ID": "u1"},
    )
    assert res.status_code == 400
