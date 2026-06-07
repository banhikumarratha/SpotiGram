from api.client import APIClient
from utils.config import settings

class MoodAPI(APIClient):
    def __init__(self):
        super().__init__(settings.MOOD_SERVICE_URL)

    def analyze_audio(self, audio_bytes: bytes, filename: str):
        files = {"audio_file": (filename, audio_bytes, "audio/mpeg")}
        return self.post("/api/v1/recommendations/mood-scan/audio", files=files)

    def analyze_text(self, text: str):
        return self.post("/api/v1/recommendations/mood-scan/text", json={"text": text})

    def analyze_image(self, image_bytes: bytes, filename: str):
        headers = self._get_headers()
        headers.pop("Content-Type", None)
        headers["Content-Type"] = "application/octet-stream"
        import httpx
        with httpx.Client(base_url=self.base_url, headers=headers, timeout=120.0) as client:
            return client.post("/api/v1/recommendations/mood-scan/image", content=image_bytes)

    def get_feed(self, mood: str = None, limit: int = 20):
        params = {"limit": limit}
        if mood:
            params["mood"] = mood.lower()
        return self.get("/api/v1/recommendations/feed", params=params)
