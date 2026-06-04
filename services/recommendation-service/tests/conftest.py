"""Shared fixtures for recommendation-service tests."""
import pytest
import os
from unittest.mock import AsyncMock, MagicMock
from typing import List

# Set env before any imports
os.environ.setdefault("CHROMA_EPHEMERAL", "true")
os.environ.setdefault("KAFKA_URL", "kafka:9092")


# ── Stub implementations of ports ──────────────────────────────────────────

class FakeEmbedder:
    """Returns a fixed 384-dim vector for deterministic tests."""
    def encode(self, text: str) -> List[float]:
        # Use a hash-seeded deterministic vector
        seed = hash(text) % 1000
        import math
        vec = [math.sin(seed + i) for i in range(384)]
        norm = sum(v ** 2 for v in vec) ** 0.5
        return [v / norm for v in vec]


class FakeMoodDetector:
    """Returns a fixed happy mood for tests."""
    async def detect(self, image_b64: str) -> dict:
        return {"mood": "happy", "confidence": 0.92}


@pytest.fixture
def fake_embedder():
    return FakeEmbedder()


@pytest.fixture
def fake_detector():
    return FakeMoodDetector()


@pytest.fixture
def fake_publisher():
    pub = AsyncMock()
    return pub


@pytest.fixture
def ephemeral_vector_store():
    from infrastructure.chroma_client import ChromaVectorStore
    return ChromaVectorStore(ephemeral=True)


@pytest.fixture
def dna_repo():
    from infrastructure.dna_repository import InMemoryDNARepository
    return InMemoryDNARepository()
