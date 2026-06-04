"""Unit tests for domain models."""
import pytest
from datetime import datetime
from domain.models import (
    Message, Conversation, Role, AIProvider,
    UserContext, AIResponse, GeneratedPlaylist, DJSession
)


def test_message_defaults():
    msg = Message(role=Role.USER, content="Hello")
    assert isinstance(msg.timestamp, datetime)
    assert msg.metadata == {}


def test_conversation_add_message():
    conv = Conversation(conversation_id="c1", user_id="u1")
    conv.add_message(Role.USER, "Hi")
    conv.add_message(Role.ASSISTANT, "Hello!")
    assert len(conv.messages) == 2


def test_conversation_history_text():
    conv = Conversation(conversation_id="c1", user_id="u1")
    conv.add_message(Role.USER, "What's good?")
    conv.add_message(Role.ASSISTANT, "Lots!")
    text = conv.history_text()
    assert "user: What's good?" in text
    assert "assistant: Lots!" in text


def test_user_context_as_context_string():
    ctx = UserContext(
        user_id="u1",
        top_genres=["pop", "rock"],
        top_artists=["Artist A"],
        current_mood="happy",
        recent_tracks=["Song X"],
    )
    s = ctx.as_context_string()
    assert "pop" in s
    assert "Artist A" in s
    assert "happy" in s


def test_user_context_empty():
    ctx = UserContext(user_id="u1")
    s = ctx.as_context_string()
    assert "u1" in s


def test_ai_response_defaults():
    r = AIResponse(content="test", provider=AIProvider.OLLAMA, model="llama3.2", prompt_version="v1")
    assert r.structured is None
    assert r.latency_ms == 0.0


def test_generated_playlist():
    pl = GeneratedPlaylist(
        name="Morning Chill",
        description="Relaxing tracks",
        track_queries=["Artist - Track 1", "Artist - Track 2"],
        reasoning="Calm morning vibes",
        mood="calm",
    )
    assert len(pl.track_queries) == 2


def test_dj_session_initial_state():
    session = DJSession(session_id="s1", user_id="u1")
    assert session.state == "idle"
    assert session.current_track is None
