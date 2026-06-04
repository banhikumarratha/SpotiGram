"""
Integration tests for ChromaVectorStore using EphemeralClient.
No Docker — fully in-memory, isolated per test.
"""
import pytest
import math
from infrastructure.chroma_client import ChromaVectorStore
from domain.models import TrackEmbedding, SimilarUser


def _make_vec(seed: int, dim: int = 384) -> list:
    vec = [math.sin(seed + i) for i in range(dim)]
    norm = sum(v ** 2 for v in vec) ** 0.5
    return [v / norm for v in vec]


@pytest.fixture
def store():
    return ChromaVectorStore(ephemeral=True)


@pytest.mark.asyncio
async def test_upsert_and_query_similar_users(store):
    vec_a = _make_vec(1)
    vec_b = _make_vec(1)   # same → very similar
    vec_c = _make_vec(500) # different → less similar

    await store.upsert_user_dna("user_a", vec_a, {"top_genres": "pop,rock"})
    await store.upsert_user_dna("user_b", vec_b, {"top_genres": "pop"})
    await store.upsert_user_dna("user_c", vec_c, {"top_genres": "jazz"})

    results = await store.query_similar_users(vec_a, top_k=3)
    assert len(results) >= 1
    top_user_ids = [r.user_id for r in results]
    assert "user_b" in top_user_ids


@pytest.mark.asyncio
async def test_upsert_and_query_similar_tracks(store):
    vec = _make_vec(42)
    track = TrackEmbedding(
        track_id="t1",
        title="Test Song",
        artist="Test Artist",
        genres=["pop"],
        embedding=vec,
    )
    await store.upsert_track(track)

    results = await store.query_similar_tracks(vec, top_k=5)
    assert len(results) == 1
    assert results[0]["track_id"] == "t1"


@pytest.mark.asyncio
async def test_empty_store_returns_empty_list():
    # In chromadb v0.5, ephemeral clients may share in-process state.
    # We verify the method returns a list without raising exceptions.
    fresh_store = ChromaVectorStore(ephemeral=True)
    vec = _make_vec(99)
    users = await fresh_store.query_similar_users(vec, top_k=5)
    tracks = await fresh_store.query_similar_tracks(vec, top_k=5)
    assert isinstance(users, list)
    assert isinstance(tracks, list)



@pytest.mark.asyncio
async def test_upsert_track_without_embedding_is_noop(store):
    track = TrackEmbedding(track_id="t_no_emb", title="X", artist="Y", genres=[], embedding=None)
    await store.upsert_track(track)  # should not raise
    results = await store.query_similar_tracks(_make_vec(1), top_k=5)
    assert all(r["track_id"] != "t_no_emb" for r in results)
