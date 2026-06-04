import pytest
from unittest.mock import AsyncMock
from application.event_handler import EventHandler
@pytest.mark.asyncio
async def test_handle_music_interaction_event(mock_repo):
    handler = EventHandler(mock_repo)
    
    event_data = {
        "event_id": "123",
        "user_id": "u1",
        "track_id": "t1",
        "action": "play",
        "timestamp": "2023-01-01T12:00:00Z"
    }
    
    await handler.handle_event("music.interactions.v1", event_data)
    
    assert len(mock_repo.interactions) == 1
    assert mock_repo.interactions[0][0] == "u1"
    assert mock_repo.interactions[0][2] == "play"


@pytest.mark.asyncio
async def test_handle_mood_detected_event(mock_repo):
    handler = EventHandler(mock_repo)
    
    event_data = {
        "event_id": "123",
        "user_id": "u1",
        "mood": "chill",
        "confidence": 0.8,
        "timestamp": "2023-01-01T12:00:00Z"
    }
    
    await handler.handle_event("mood.detected.v1", event_data)
    
    assert len(mock_repo.moods) == 1
    assert mock_repo.moods[0][0] == "u1"
    assert mock_repo.moods[0][2] == "chill"


@pytest.mark.asyncio
async def test_handle_invalid_event_does_not_throw(mock_repo):
    handler = EventHandler(mock_repo)
    
    event_data = {"missing": "fields"}
    
    # Should catch ValidationError and print
    await handler.handle_event("music.interactions.v1", event_data)
    await handler.handle_event("mood.detected.v1", event_data)
    
    assert len(mock_repo.interactions) == 0
    assert len(mock_repo.moods) == 0
