from api.client import APIClient
from utils.config import settings

class AIAPI(APIClient):
    def __init__(self):
        super().__init__(settings.AI_SERVICE_URL)

    def chat_with_dj(self, session_id: str, message: str, context: dict = None):
        payload = {
            "session_id": session_id,
            "message": message,
            "context": context or {}
        }
        return self.post("/api/v1/ai/dj", json=payload)

    def get_recommendations(self, mood: str, preferences: dict = None):
        return self.post("/api/v1/ai/playlist", json={
            "theme": mood,
            "mood": mood,
            "context": {"preferences": preferences or {}}
        })
