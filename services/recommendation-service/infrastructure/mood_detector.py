"""
Mood detector adapter — implements MoodDetectorPort.
Uses DeepFace for local emotion inference (no cloud).
Falls back to NEUTRAL with low confidence if DeepFace is unavailable
or the image cannot be analyzed (graceful degradation).
"""
import base64
import os
import tempfile
from typing import Dict

from domain.models import Mood
from domain.ports import MoodDetectorPort

# Map DeepFace raw emotions to our Mood domain buckets
_EMOTION_MAP: Dict[str, Mood] = {
    "happy": Mood.HAPPY,
    "surprise": Mood.HAPPY,
    "sad": Mood.SAD,
    "disgust": Mood.SAD,
    "fear": Mood.SAD,
    "angry": Mood.ANGRY,
    "neutral": Mood.NEUTRAL,
}


class DeepFaceMoodDetector(MoodDetectorPort):
    """
    Accepts a base64-encoded JPEG/PNG and returns dominant mood + confidence.
    DeepFace is imported lazily so the service can boot without a GPU.
    """

    async def detect(self, image_b64: str) -> dict:
        try:
            return await self._analyze(image_b64)
        except Exception:
            return {"mood": Mood.NEUTRAL.value, "confidence": 0.0}

    async def _analyze(self, image_b64: str) -> dict:
        from deepface import DeepFace  # lazy import — heavy dep

        img_bytes = base64.b64decode(image_b64)
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            tmp.write(img_bytes)
            tmp_path = tmp.name

        try:
            result = DeepFace.analyze(
                img_path=tmp_path,
                actions=["emotion"],
                enforce_detection=False,
                silent=True,
            )
            if isinstance(result, list):
                result = result[0]

            emotions: dict = result.get("emotion", {})
            dominant = result.get("dominant_emotion", "neutral").lower()
            confidence = emotions.get(dominant, 0.0) / 100.0
            mood = _EMOTION_MAP.get(dominant, Mood.NEUTRAL)

            return {"mood": mood.value, "confidence": round(confidence, 3)}
        finally:
            os.unlink(tmp_path)
