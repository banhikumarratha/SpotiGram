"""
Shared fixtures — all tests use a FakeProvider that never hits a real LLM.
This makes the entire test suite infrastructure-free.
"""
import pytest
import os
from typing import Optional, AsyncIterator
from domain.models import AIResponse, AIProvider
from domain.ports import AIProviderPort

os.environ.setdefault("AI_PROVIDER", "ollama")
os.environ.setdefault("OLLAMA_BASE_URL", "http://localhost:11434")


class FakeProvider(AIProviderPort):
    """Deterministic fake LLM — returns predictable canned responses."""

    def __init__(self, response: str = "Fake LLM response"):
        self._response = response
        self._available = True

    async def complete(self, prompt, system="", model=None, temperature=0.7, max_tokens=1024) -> AIResponse:
        return AIResponse(
            content=self._response,
            provider=AIProvider.OLLAMA,
            model="fake-model",
            prompt_version="v1",
            latency_ms=0.1,
        )

    async def stream(self, prompt, system="", model=None, temperature=0.7) -> AsyncIterator[str]:
        for word in self._response.split():
            yield word + " "

    async def is_available(self) -> bool:
        return self._available


class FakePlaylistProvider(FakeProvider):
    """Returns a valid JSON playlist response."""

    def __init__(self):
        super().__init__(
            response='{"name": "Test Playlist", "description": "A test playlist", '
                     '"reasoning": "Testing", "track_queries": ["Artist A - Track 1", "Artist B - Track 2"]}'
        )


@pytest.fixture
def fake_provider():
    return FakeProvider()


@pytest.fixture
def fake_playlist_provider():
    return FakePlaylistProvider()


@pytest.fixture
def memory_store():
    from memory.conversation_store import InMemoryConversationStore
    return InMemoryConversationStore()
