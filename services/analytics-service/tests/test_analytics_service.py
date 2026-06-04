import pytest
from unittest.mock import AsyncMock
from datetime import date
from application.analytics_service import AnalyticsService
from domain.models import DailyUserStats


@pytest.mark.asyncio
async def test_get_listening_stats(mock_repo):
    mock_repo.get_daily_stats_range = AsyncMock(return_value=[
        DailyUserStats(user_id="u1", stat_date=date(2023,1,1), total_plays=10, total_skips=2),
        DailyUserStats(user_id="u1", stat_date=date(2023,1,2), total_plays=10, total_skips=3)
    ])
    
    svc = AnalyticsService(mock_repo)
    stats = await svc.get_listening_stats("u1", 30)
    
    assert stats.total_plays == 20
    assert stats.total_skips == 5
    assert stats.completion_rate == 15 / 20


@pytest.mark.asyncio
async def test_get_mood_trend(mock_repo):
    mock_repo.get_daily_stats_range = AsyncMock(return_value=[
        DailyUserStats(user_id="u1", stat_date=date(2023,1,1), dominant_mood="happy"),
        DailyUserStats(user_id="u1", stat_date=date(2023,1,2), dominant_mood="happy"),
        DailyUserStats(user_id="u1", stat_date=date(2023,1,3), dominant_mood="chill")
    ])
    
    svc = AnalyticsService(mock_repo)
    trend = await svc.get_mood_trend("u1", 30)
    
    assert trend.mood_counts["happy"] == 2
    assert trend.mood_counts["chill"] == 1
    assert trend.dominant_mood == "happy"


@pytest.mark.asyncio
async def test_get_music_personality(mock_repo):
    mock_repo.get_daily_stats_range = AsyncMock(return_value=[
        DailyUserStats(user_id="u1", stat_date=date.today(), total_plays=1100, total_skips=50)
    ])
    
    svc = AnalyticsService(mock_repo)
    personality = await svc.get_music_personality("u1")
    
    assert "Avid Listener" in personality.traits
    assert "Patient Explorer" in personality.traits


@pytest.mark.asyncio
async def test_get_year_in_review(mock_repo):
    mock_repo.get_daily_stats_range = AsyncMock(return_value=[
        DailyUserStats(user_id="u1", stat_date=date(2023,1,1), total_plays=100, dominant_mood="energetic")
    ])
    
    svc = AnalyticsService(mock_repo)
    review = await svc.get_year_in_review("u1", 2023)
    
    assert review.total_minutes == 300
    assert review.year == 2023
    assert review.dominant_mood == "energetic"
