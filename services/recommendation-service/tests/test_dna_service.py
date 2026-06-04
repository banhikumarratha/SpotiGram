"""Unit tests for the DNAService — Music DNA build and update logic."""
import pytest
import math
from domain.models import MusicDNA, MusicInteractionEvent, InteractionType
from application.dna_service import DNAService, COLD_START_THRESHOLD
from datetime import datetime


def _make_event(action: InteractionType, title="Test", artist="Artist", genres=None):
    return MusicInteractionEvent(
        user_id="u1",
        track_id="t1",
        action=action,
        timestamp=datetime.utcnow(),
        track_title=title,
        track_artist=artist,
        track_genres=genres or ["pop"],
    )


@pytest.mark.asyncio
async def test_get_or_create_returns_cold_start_dna(fake_embedder, ephemeral_vector_store, dna_repo):
    service = DNAService(ephemeral_vector_store, fake_embedder, dna_repo)
    dna = await service.get_or_create("u1")
    assert dna.is_cold_start is True
    assert dna.total_interactions == 0
    assert len(dna.embedding) == 384


@pytest.mark.asyncio
async def test_play_interaction_updates_dna(fake_embedder, ephemeral_vector_store, dna_repo):
    service = DNAService(ephemeral_vector_store, fake_embedder, dna_repo)
    event = _make_event(InteractionType.PLAY)
    dna = await service.process_interaction(event)
    assert dna.total_interactions == 1
    assert "pop" in dna.top_genres
    assert "Artist" in dna.top_artists


@pytest.mark.asyncio
async def test_skip_does_not_add_to_genres(fake_embedder, ephemeral_vector_store, dna_repo):
    service = DNAService(ephemeral_vector_store, fake_embedder, dna_repo)
    # First play to establish DNA
    play_event = _make_event(InteractionType.PLAY, genres=["jazz"])
    await service.process_interaction(play_event)

    # Skip on a different genre track — skip should NOT add the new genre
    skip_event = _make_event(InteractionType.SKIP, genres=["metal"])
    await service.process_interaction(skip_event)

    dna = await dna_repo.get("u1")
    # jazz was added by play; metal should NOT be added by skip
    assert "metal" not in dna.top_genres
    assert "jazz" in dna.top_genres


@pytest.mark.asyncio
async def test_cold_start_threshold(fake_embedder, ephemeral_vector_store, dna_repo):
    service = DNAService(ephemeral_vector_store, fake_embedder, dna_repo)
    for i in range(COLD_START_THRESHOLD - 1):
        await service.process_interaction(_make_event(InteractionType.PLAY, title=f"Track {i}"))

    dna = await dna_repo.get("u1")
    assert dna.is_cold_start is True

    await service.process_interaction(_make_event(InteractionType.PLAY, title="Final Track"))
    dna = await dna_repo.get("u1")
    assert dna.is_cold_start is False


@pytest.mark.asyncio
async def test_get_dna_insights_structure(fake_embedder, ephemeral_vector_store, dna_repo):
    service = DNAService(ephemeral_vector_store, fake_embedder, dna_repo)
    await service.process_interaction(_make_event(InteractionType.LIKE))
    insights = await service.get_dna_insights("u1")
    assert "top_genres" in insights
    assert "total_interactions" in insights
    assert insights["total_interactions"] == 1


@pytest.mark.asyncio
async def test_embedding_is_normalized(fake_embedder, ephemeral_vector_store, dna_repo):
    service = DNAService(ephemeral_vector_store, fake_embedder, dna_repo)
    await service.process_interaction(_make_event(InteractionType.PLAY))
    dna = await dna_repo.get("u1")
    norm = sum(v ** 2 for v in dna.embedding) ** 0.5
    assert abs(norm - 1.0) < 0.01  # should be unit-normalized
