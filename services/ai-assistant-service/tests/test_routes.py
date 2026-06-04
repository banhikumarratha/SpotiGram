"""Contract and integration tests for the API router."""
import pytest
from fastapi.testclient import TestClient

from main import app
from memory.conversation_store import InMemoryConversationStore
from application.assistant_service import AssistantService
from application.dj_service import DJService, _sessions
from application.playlist_service import PlaylistService
import api.v1.router as router_module


client = TestClient(app)


@pytest.fixture(autouse=True)
def override_services(fake_provider, fake_playlist_provider):
    """Override the singletons in the router with our mocked services."""
    store = InMemoryConversationStore()
    
    router_module._memory_store = store
    router_module._assistant_service = AssistantService(fake_provider, store)
    router_module._dj_service = DJService(fake_provider)
    router_module._playlist_service = PlaylistService(fake_playlist_provider)
    
    _sessions.clear()
    
    yield
    
    # Cleanup
    router_module._assistant_service = None
    router_module._dj_service = None
    router_module._playlist_service = None


def test_health_check():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "healthy"}


def test_ready_check():
    res = client.get("/ready")
    assert res.status_code == 200
    assert res.json() == {"status": "ready"}


def test_chat_endpoint():
    res = client.post(
        "/api/v1/ai/chat",
        headers={"X-User-ID": "u1"},
        json={
            "message": "Hello",
            "context": {"top_genres": ["pop"]}
        }
    )
    assert res.status_code == 200
    data = res.json()
    assert data["content"] == "Fake LLM response"
    assert data["provider"] == "ollama"


def test_chat_missing_header_returns_422():
    res = client.post("/api/v1/ai/chat", json={"message": "Hello"})
    assert res.status_code == 422


def test_dj_interact_endpoint():
    res = client.post(
        "/api/v1/ai/dj",
        headers={"X-User-ID": "u1"},
        json={
            "message": "Play next",
            "current_track": "Song A"
        }
    )
    assert res.status_code == 200
    data = res.json()
    assert data["response"] == "Fake LLM response"
    assert "session_id" in data


def test_playlist_endpoint():
    res = client.post(
        "/api/v1/ai/playlist",
        headers={"X-User-ID": "u1"},
        json={"theme": "Workout"}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["name"] == "Test Playlist"
    assert len(data["track_queries"]) == 2


def test_explain_endpoint():
    res = client.post(
        "/api/v1/ai/explain",
        headers={"X-User-ID": "u1"},
        json={
            "track_title": "Song A",
            "track_artist": "Artist B"
        }
    )
    assert res.status_code == 200
    data = res.json()
    assert "Testing" in data["explanation"]
