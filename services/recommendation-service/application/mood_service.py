"""
Mood Service — orchestrates mood detection.
Maps detected emotion to a domain Mood bucket and exposes
a clean API for the recommendation pipeline.
"""
from domain.models import Mood, MoodProfile
from domain.ports import MoodDetectorPort
from datetime import datetime


# Mood → energy level mapping used for recommendation ranking
MOOD_ENERGY: dict = {
    Mood.HAPPY: 0.8,
    Mood.ENERGETIC: 1.0,
    Mood.CALM: 0.3,
    Mood.NEUTRAL: 0.5,
    Mood.SAD: 0.2,
    Mood.ANGRY: 0.9,
}


class MoodService:
    def __init__(self, detector: MoodDetectorPort):
        self._detector = detector

    async def scan(self, user_id: str, image_b64: str) -> MoodProfile:
        """Analyze a webcam frame and return a MoodProfile for the user."""
        result = await self._detector.detect(image_b64)
        mood = Mood(result.get("mood", Mood.NEUTRAL.value))
        confidence = float(result.get("confidence", 0.0))
        return MoodProfile(
            user_id=user_id,
            mood=mood,
            confidence=confidence,
            detected_at=datetime.utcnow(),
            source="webcam",
        )

    @staticmethod
    def energy_level(mood: Mood) -> float:
        """Return a 0–1 energy level for ranking mood-matched tracks."""
        return MOOD_ENERGY.get(mood, 0.5)
