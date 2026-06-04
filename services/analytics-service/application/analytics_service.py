from datetime import date, timedelta
from typing import List

from domain.models import ListeningStats, MoodTrend, MusicPersonality, YearInReview
from domain.ports import AnalyticsRepositoryPort


class AnalyticsService:
    def __init__(self, repo: AnalyticsRepositoryPort):
        self.repo = repo

    async def get_listening_stats(self, user_id: str, days: int = 30) -> ListeningStats:
        end_date = date.today()
        start_date = end_date - timedelta(days=days)
        
        stats = await self.repo.get_daily_stats_range(user_id, start_date, end_date)
        
        total_plays = sum(s.total_plays for s in stats)
        total_skips = sum(s.total_skips for s in stats)
        
        completion_rate = 0.0
        if total_plays > 0:
            completion_rate = (total_plays - total_skips) / total_plays
            
        return ListeningStats(
            user_id=user_id,
            timeframe=f"Last {days} days",
            total_plays=total_plays,
            total_skips=total_skips,
            completion_rate=completion_rate
        )

    async def get_mood_trend(self, user_id: str, days: int = 30) -> MoodTrend:
        end_date = date.today()
        start_date = end_date - timedelta(days=days)
        
        stats = await self.repo.get_daily_stats_range(user_id, start_date, end_date)
        
        mood_counts = {}
        for s in stats:
            if s.dominant_mood:
                mood_counts[s.dominant_mood] = mood_counts.get(s.dominant_mood, 0) + 1
                
        dominant = max(mood_counts.items(), key=lambda x: x[1])[0] if mood_counts else "Unknown"
        
        return MoodTrend(
            user_id=user_id,
            timeframe=f"Last {days} days",
            mood_counts=mood_counts,
            dominant_mood=dominant
        )

    async def get_music_personality(self, user_id: str) -> MusicPersonality:
        # Simplistic derivation based on listening stats
        stats = await self.get_listening_stats(user_id, days=90)
        
        traits = []
        if stats.total_plays > 1000:
            traits.append("Avid Listener")
        
        if stats.completion_rate > 0.8:
            traits.append("Patient Explorer")
        elif stats.total_skips > stats.total_plays * 0.5:
            traits.append("Vibe Checker")
            
        return MusicPersonality(
            user_id=user_id,
            traits=traits,
            description="Based on 90 days of listening habits."
        )

    async def get_year_in_review(self, user_id: str, year: int) -> YearInReview:
        start_date = date(year, 1, 1)
        end_date = date(year, 12, 31)
        
        stats = await self.repo.get_daily_stats_range(user_id, start_date, end_date)
        
        total_plays = sum(s.total_plays for s in stats)
        # assuming ~3 mins per play
        total_minutes = total_plays * 3 
        
        mood_counts = {}
        for s in stats:
            if s.dominant_mood:
                mood_counts[s.dominant_mood] = mood_counts.get(s.dominant_mood, 0) + 1
        dominant_mood = max(mood_counts.items(), key=lambda x: x[1])[0] if mood_counts else "Unknown"
        
        return YearInReview(
            user_id=user_id,
            year=year,
            total_minutes=total_minutes,
            top_genres=[], # In a real system, we'd join with track metadata
            top_artists=[],
            dominant_mood=dominant_mood
        )
