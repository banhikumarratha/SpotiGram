from abc import ABC, abstractmethod
from datetime import date
from typing import List, Dict, Optional
from domain.models import DailyUserStats


class AnalyticsRepositoryPort(ABC):
    @abstractmethod
    async def increment_interaction(self, user_id: str, stat_date: date, action: str) -> None:
        """Increment the daily count for a specific interaction action."""
        pass

    @abstractmethod
    async def update_dominant_mood(self, user_id: str, stat_date: date, mood: str) -> None:
        """Update the daily dominant mood."""
        pass

    @abstractmethod
    async def get_daily_stats_range(self, user_id: str, start_date: date, end_date: date) -> List[DailyUserStats]:
        """Fetch daily stats for a specific user and date range."""
        pass


class EventConsumerPort(ABC):
    @abstractmethod
    async def start(self):
        pass

    @abstractmethod
    async def stop(self):
        pass
