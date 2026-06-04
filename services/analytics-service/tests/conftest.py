import pytest
from domain.ports import AnalyticsRepositoryPort

class MockRepo(AnalyticsRepositoryPort):
    def __init__(self):
        self.interactions = []
        self.moods = []

    async def increment_interaction(self, user_id, stat_date, action):
        self.interactions.append((user_id, stat_date, action))

    async def update_dominant_mood(self, user_id, stat_date, mood):
        self.moods.append((user_id, stat_date, mood))

    async def get_daily_stats_range(self, user_id, start, end):
        return []

@pytest.fixture
def mock_repo():
    return MockRepo()
