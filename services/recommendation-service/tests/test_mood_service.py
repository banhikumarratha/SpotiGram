"""Unit tests for the MoodService application layer."""
import pytest
from domain.models import Mood, MoodProfile
from application.mood_service import MoodService, MOOD_ENERGY


@pytest.mark.asyncio
async def test_scan_returns_mood_profile(fake_detector):
    service = MoodService(fake_detector)
    profile = await service.scan("u1", "fake_image_b64")
    assert isinstance(profile, MoodProfile)
    assert profile.mood == Mood.HAPPY
    assert profile.confidence == 0.92
    assert profile.user_id == "u1"


@pytest.mark.asyncio
async def test_scan_with_detector_fallback():
    """If detector raises, it should return NEUTRAL."""
    class BrokenDetector:
        async def detect(self, _):
            raise RuntimeError("camera error")

    # DeepFaceMoodDetector wraps errors internally; test via the real adapter
    from infrastructure.mood_detector import DeepFaceMoodDetector
    detector = DeepFaceMoodDetector()
    # Bogus image — DeepFace will fail gracefully
    result = await detector.detect("not_real_image_data")
    assert result["mood"] == Mood.NEUTRAL.value
    assert result["confidence"] == 0.0


def test_mood_energy_levels():
    assert MoodService.energy_level(Mood.ENERGETIC) == 1.0
    assert MoodService.energy_level(Mood.SAD) == 0.2
    assert MoodService.energy_level(Mood.CALM) == 0.3
    assert MoodService.energy_level(Mood.HAPPY) == 0.8


def test_mood_energy_unknown_defaults_to_neutral():
    # Passing a string that's not in the map should not crash
    result = MoodService.energy_level("non_existent_mood")  # type: ignore
    assert result == 0.5
