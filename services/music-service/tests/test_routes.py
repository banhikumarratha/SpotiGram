import pytest
from fastapi.testclient import TestClient
from main import app
from unittest.mock import AsyncMock

client = TestClient(app)

def test_health():
    res = client.get("/health")
    assert res.status_code == 200

def test_ready():
    res = client.get("/ready")
    assert res.status_code == 200

def test_metrics():
    res = client.get("/metrics")
    assert res.status_code == 200

def test_search_music(mocker):
    mocker.patch("api.v1.router.CatalogService.search", return_value={"tracks": []})
    res = client.get("/api/v1/music/search?q=test")
    assert res.status_code == 200
    assert "tracks" in res.json()

def test_get_track(mocker):
    mocker.patch("api.v1.router.CatalogService.get_track", return_value={"id": "t1"})
    res = client.get("/api/v1/music/tracks/t1")
    assert res.status_code == 200
    assert res.json()["id"] == "t1"

def test_playback(mocker):
    mocker.patch("api.v1.router.PlaybackService.emit_playback_event", return_value={"status": "event_emitted", "action": "play"})
    res = client.post("/api/v1/music/playback", json={"track_id": "t1", "action": "play"})
    assert res.status_code == 200
    assert res.json()["status"] == "event_emitted"
