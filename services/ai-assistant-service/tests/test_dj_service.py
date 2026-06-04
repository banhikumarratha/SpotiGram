"""Unit tests for the DJService and LangGraph workflow."""
import pytest
from domain.models import UserContext
from application.dj_service import DJService, _sessions


@pytest.fixture(autouse=True)
def clear_dj_sessions():
    """Clear the module-level session dict before each test."""
    _sessions.clear()
    yield


@pytest.mark.asyncio
async def test_dj_start_session(fake_provider):
    svc = DJService(fake_provider)
    session = await svc.start_session(user_id="u1", mood="energetic")
    
    assert session.session_id is not None
    assert session.user_id == "u1"
    assert session.mood == "energetic"
    assert session.state == "idle"
    assert session.session_id in _sessions


@pytest.mark.asyncio
async def test_dj_interact(fake_provider):
    svc = DJService(fake_provider)
    session = await svc.start_session(user_id="u1", mood="calm")
    
    ctx = UserContext(user_id="u1", top_genres=["jazz"])
    response = await svc.interact(
        session_id=session.session_id,
        user_message="Play something smooth",
        context=ctx,
        current_track="Miles Davis - Blue in Green"
    )
    
    assert response == "Fake LLM response"
    assert session.state == "playing"
    assert session.current_track == "Miles Davis - Blue in Green"


@pytest.mark.asyncio
async def test_dj_interact_auto_creates_session(fake_provider):
    svc = DJService(fake_provider)
    
    response = await svc.interact(
        session_id="unknown_session",
        user_message="Next track"
    )
    
    assert response == "Fake LLM response"
    assert "unknown_session" in _sessions
    assert _sessions["unknown_session"].state == "playing"
