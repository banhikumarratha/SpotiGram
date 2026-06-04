from api.client import APIClient
from utils.config import settings

class MoodAPI(APIClient):
    def __init__(self):
        super().__init__(settings.MOOD_SERVICE_URL)

    def analyze_audio(self, audio_bytes: bytes, filename: str):
        files = {"audio_file": (filename, audio_bytes, "audio/mpeg")}
        return self.post("/api/v1/mood/analyze/audio", files=files)

    def analyze_text(self, text: str):
        return self.post("/api/v1/mood/analyze/text", json={"text": text})
