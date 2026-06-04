"""Unit tests for PlaylistService."""
import pytest
from domain.models import UserContext
from application.playlist_service import PlaylistService


@pytest.mark.asyncio
async def test_playlist_create(fake_playlist_provider):
    svc = PlaylistService(fake_playlist_provider)
    ctx = UserContext(user_id="u1", top_genres=["indie"])
    
    playlist = await svc.create(theme="Late night drive", context=ctx, mood="chill")
    
    assert playlist.name == "Test Playlist"
    assert len(playlist.track_queries) == 2
    assert playlist.mood == "chill"


@pytest.mark.asyncio
async def test_playlist_create_fallback_on_json_error(fake_provider):
    # fake_provider returns "Fake LLM response" which is invalid JSON
    svc = PlaylistService(fake_provider)
    
    playlist = await svc.create(theme="Workout")
    
    assert playlist.name == "Playlist for: Workout"
    assert len(playlist.track_queries) == 1
    assert playlist.track_queries[0] == "Fake LLM response"


@pytest.mark.asyncio
async def test_playlist_explain(fake_provider):
    svc = PlaylistService(fake_provider)
    
    explanation = await svc.explain(
        track_title="Song A",
        track_artist="Artist B",
        signals={"dna": 0.8},
    )
    
    assert explanation == "Fake LLM response"
