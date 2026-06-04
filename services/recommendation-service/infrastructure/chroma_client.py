"""
ChromaDB adapter — implements VectorStorePort.
Uses an embedded ChromaDB instance (no separate server required).
"""
import os
from typing import List
import chromadb
from chromadb.config import Settings

from domain.models import TrackEmbedding, SimilarUser
from domain.ports import VectorStorePort

CHROMA_PATH = os.getenv("CHROMA_PERSIST_DIR", "./chroma_data")

# Collections
USER_DNA_COLLECTION = "user_dna"
TRACK_COLLECTION = "tracks"


def _get_client(ephemeral: bool = False) -> chromadb.Client:
    if ephemeral:
        return chromadb.EphemeralClient()
    return chromadb.PersistentClient(path=CHROMA_PATH)


class ChromaVectorStore(VectorStorePort):
    """
    Persistent ChromaDB adapter for user Music DNA and track embeddings.
    Pass ephemeral=True in tests to avoid touching the filesystem.
    """

    def __init__(self, ephemeral: bool = False):
        self._client = _get_client(ephemeral)
        self._users = self._client.get_or_create_collection(
            name=USER_DNA_COLLECTION,
            metadata={"hnsw:space": "cosine"},
        )
        self._tracks = self._client.get_or_create_collection(
            name=TRACK_COLLECTION,
            metadata={"hnsw:space": "cosine"},
        )

    async def upsert_user_dna(self, user_id: str, embedding: List[float], metadata: dict) -> None:
        self._users.upsert(
            ids=[user_id],
            embeddings=[embedding],
            metadatas=[metadata],
        )

    async def query_similar_users(self, embedding: List[float], top_k: int = 10) -> List[SimilarUser]:
        if self._users.count() == 0:
            return []
        results = self._users.query(
            query_embeddings=[embedding],
            n_results=min(top_k, self._users.count()),
            include=["metadatas", "distances"],
        )
        similar = []
        for uid, distance, meta in zip(
            results["ids"][0], results["distances"][0], results["metadatas"][0]
        ):
            similarity = 1.0 - distance  # cosine distance → similarity
            genres = meta.get("top_genres", "").split(",") if meta.get("top_genres") else []
            similar.append(SimilarUser(user_id=uid, similarity_score=similarity, shared_genres=genres))
        return similar

    async def upsert_track(self, track: TrackEmbedding) -> None:
        if track.embedding is None:
            return
        meta = {
            "title": track.title,
            "artist": track.artist,
            "genres": ",".join(track.genres),
        }
        meta.update({k: str(v) for k, v in track.metadata.items()})
        self._tracks.upsert(
            ids=[track.track_id],
            embeddings=[track.embedding],
            metadatas=[meta],
        )

    async def query_similar_tracks(self, embedding: List[float], top_k: int = 20) -> List[dict]:
        if self._tracks.count() == 0:
            return []
        results = self._tracks.query(
            query_embeddings=[embedding],
            n_results=min(top_k, self._tracks.count()),
            include=["metadatas", "distances"],
        )
        tracks = []
        for tid, distance, meta in zip(
            results["ids"][0], results["distances"][0], results["metadatas"][0]
        ):
            tracks.append({
                "track_id": tid,
                "similarity": 1.0 - distance,
                **meta,
            })
        return tracks
