from typing import List
from libs.shared.schemas.domain import TrackInfo

class RecommendationLogic:
    def get_similar_tracks(self, vector: List[float]) -> List[TrackInfo]:
        """
        In a real scenario, this would query ChromaDB using the vector.
        """
        # Mock logic
        return [
            TrackInfo(
                spotify_id="mock_recc_123",
                title="Similar Vibe Track",
                artist="Algo Artist",
                duration_ms=180000
            )
        ]
