"""
Sentence-Transformers embedding adapter — implements EmbeddingPort.
Uses all-MiniLM-L6-v2 (384-dim, ~80MB model) for fast local inference.
Loaded lazily to avoid startup overhead in test environments.
"""
from typing import List
from domain.ports import EmbeddingPort

_model = None


def _get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


class SentenceTransformerEmbedder(EmbeddingPort):
    """Generates 384-dimensional embeddings from track metadata text."""

    def encode(self, text: str) -> List[float]:
        model = _get_model()
        return model.encode(text, normalize_embeddings=True).tolist()

    @staticmethod
    def build_track_text(title: str, artist: str, genres: List[str]) -> str:
        """Canonical text representation of a track for embedding."""
        genre_str = " ".join(genres) if genres else "unknown"
        return f"{artist} - {title} [{genre_str}]"
