from datetime import datetime
from domain.events import MusicInteractionEvent, MoodDetectedEvent
from domain.ports import AnalyticsRepositoryPort
from pydantic import ValidationError


class EventHandler:
    def __init__(self, repo: AnalyticsRepositoryPort):
        self.repo = repo

    async def handle_event(self, topic: str, data: dict):
        if topic in ("music.events.v1", "music.interactions.v1"):
            try:
                payload = data.get("payload", {}) if "payload" in data else data
                headers = data.get("headers", {}) if "headers" in data else data
                user_id = payload.get("user_id")
                action = payload.get("action")
                track_id = payload.get("track_id")
                
                timestamp_str = headers.get("timestamp")
                if timestamp_str:
                    try:
                        timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
                    except Exception:
                        timestamp = datetime.utcnow()
                else:
                    timestamp = datetime.utcnow()

                if user_id and action and track_id:
                    stat_date = timestamp.date()
                    await self.repo.increment_interaction(user_id, stat_date, action)
            except Exception as e:
                print(f"Error handling music interaction event: {e}")
                
        elif topic in ("moods.events.v1", "mood.detected.v1", "recommendation.events.v1"):
            try:
                payload = data.get("payload", {}) if "payload" in data else data
                headers = data.get("headers", {}) if "headers" in data else data
                user_id = payload.get("user_id")
                mood = payload.get("mood") or payload.get("detected_mood")
                
                timestamp_str = headers.get("timestamp")
                if timestamp_str:
                    try:
                        timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
                    except Exception:
                        timestamp = datetime.utcnow()
                else:
                    timestamp = datetime.utcnow()

                if user_id and mood:
                    stat_date = timestamp.date()
                    await self.repo.update_dominant_mood(user_id, stat_date, str(mood).lower())
            except Exception as e:
                print(f"Error handling mood event: {e}")
