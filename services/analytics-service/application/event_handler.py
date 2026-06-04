from datetime import datetime
from domain.events import MusicInteractionEvent, MoodDetectedEvent
from domain.ports import AnalyticsRepositoryPort
from pydantic import ValidationError


class EventHandler:
    def __init__(self, repo: AnalyticsRepositoryPort):
        self.repo = repo

    async def handle_event(self, topic: str, data: dict):
        if topic == "music.interactions.v1":
            try:
                event = MusicInteractionEvent(**data)
                stat_date = event.timestamp.date()
                await self.repo.increment_interaction(event.user_id, stat_date, event.action)
            except ValidationError as e:
                print(f"Validation error on interaction event: {e}")
                
        elif topic == "mood.detected.v1":
            try:
                event = MoodDetectedEvent(**data)
                stat_date = event.timestamp.date()
                # A naive approach: the latest mood of the day becomes dominant
                await self.repo.update_dominant_mood(event.user_id, stat_date, event.mood)
            except ValidationError as e:
                print(f"Validation error on mood event: {e}")
