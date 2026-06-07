from api.client import APIClient
from utils.config import settings

class MusicAPI(APIClient):
    def __init__(self):
        super().__init__(settings.SPOTIFY_SERVICE_URL)

    def search(self, query: str):
        return self.get("/api/v1/music/search", params={"q": query})

    def register_playback(self, track_id: str, action: str = "play"):
        return self.post("/api/v1/music/playback", json={"track_id": track_id, "action": action})
