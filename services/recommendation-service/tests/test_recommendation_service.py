"""
Unit tests for the RecommendationService — ranking, cold start, similar users.
Uses ephemeral ChromaDB and fake embedder — no external dependencies.
"""
import pytest
import math
from domain.models import Mood, MusicDNA, MusicInteractionEvent, InteractionType
from application.recommendation_service import RecommendationService
from application.dna_service import COLD_START_THRESHOLD
from infrastructure.chroma_client import ChromaVectorStore
from infrastructure.dna_repository import InMemoryDNARepository
from datetime import datetime


def _make_vec(seed: int, dim: int = 384) -> list:
    vec = [math.sin(seed + i) for i in range(dim)]
    norm = sum(v ** 2 for v in vec) ** 0.5
    return [v / norm for v in vec]


@pytest.mark.asyncio
async def test_cold_start_feed_for_new_user(fake_embedder, fake_publisher):
    store = ChromaVectorStore(ephemeral=True)
    repo = InMemoryDNARepository()
    service = RecommendationService(store, fake_embedder, repo, fake_publisher)

    feed = await service.generate_feed("new_user", mood=None, limit=5)
    assert feed.is_cold_start is True
    assert len(feed.recommendations) > 0
    assert all("cold_start" in r.signals for r in feed.recommendations)


@pytest.mark.asyncio
async def test_feed_returns_recs_after_dna_populated(fake_embedder, fake_publisher):
    store = ChromaVectorStore(ephemeral=True)
    repo = InMemoryDNARepository()

    # Seed a track into ChromaDB
    vec = _make_vec(42)
    from domain.models import TrackEmbedding
    await store.upsert_track(TrackEmbedding(
        track_id="t_seeded", title="Pop Hit", artist="PopStar",
        genres=["pop"], embedding=vec,
    ))

    # Create a mature DNA (not cold start)
    dna = MusicDNA(
        user_id="mature_user",
        embedding=vec,
        top_genres=["pop"],
        top_artists=["PopStar"],
        mood_distribution={"happy": 1.0},
        total_interactions=COLD_START_THRESHOLD + 1,
        is_cold_start=False,
    )
    await repo.save(dna)

    service = RecommendationService(store, fake_embedder, repo, fake_publisher)
    feed = await service.generate_feed("mature_user", mood=Mood.HAPPY, limit=5)

    assert feed.is_cold_start is False
    assert len(feed.recommendations) >= 1
    first = feed.recommendations[0]
    assert first.score >= 0.0
    assert first.explanation != ""
    assert "dna" in first.signals


@pytest.mark.asyncio
async def test_feed_publishes_kafka_event(fake_embedder):
    from unittest.mock import AsyncMock
    store = ChromaVectorStore(ephemeral=True)
    repo = InMemoryDNARepository()
    publisher = AsyncMock()

    vec = _make_vec(7)
    from domain.models import TrackEmbedding
    await store.upsert_track(TrackEmbedding(
        track_id="t7", title="Track 7", artist="Artist 7",
        genres=["rock"], embedding=vec,
    ))

    dna = MusicDNA(
        user_id="u_pub",
        embedding=vec,
        top_genres=["rock"],
        top_artists=["Artist 7"],
        mood_distribution={},
        total_interactions=COLD_START_THRESHOLD + 1,
        is_cold_start=False,
    )
    await repo.save(dna)

    service = RecommendationService(store, fake_embedder, repo, publisher)
    await service.generate_feed("u_pub", limit=5)

    assert publisher.publish.called


@pytest.mark.asyncio
async def test_similar_users_returns_empty_for_unknown_user(fake_embedder, fake_publisher):
    store = ChromaVectorStore(ephemeral=True)
    repo = InMemoryDNARepository()
    service = RecommendationService(store, fake_embedder, repo, fake_publisher)

    users = await service.find_similar_users("ghost_user")
    assert users == []


@pytest.mark.asyncio
async def test_feed_mood_parameter_accepted(fake_embedder, fake_publisher):
    store = ChromaVectorStore(ephemeral=True)
    repo = InMemoryDNARepository()
    service = RecommendationService(store, fake_embedder, repo, fake_publisher)

    # Cold start path — mood should still be stored in feed
    feed = await service.generate_feed("u1", mood=Mood.SAD, limit=3)
    assert feed.mood == Mood.SAD
