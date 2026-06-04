from libs.shared.schemas.domain import TrackInfo
from libs.shared.enums import Mood
from typing import List
from infrastructure.vector.chroma_client import ChromaClientMock

class AiService:
    def __init__(self, vector_client: ChromaClientMock):
        self.vector_client = vector_client

    def get_recommendations(self, mood: Mood) -> List[TrackInfo]:
        # Mocking AI logic and vector search
        results = self.vector_client.search(mood.value)
        return [
            TrackInfo(
                spotify_id=r["id"],
                title=f"AI Recommendation for {mood.value}",
                artist="AI Generated Artist",
                duration_ms=150000
            ) for r in results
        ]
