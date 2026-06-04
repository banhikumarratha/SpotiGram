import os
from datetime import date, datetime
from typing import List
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import Integer, String, Date, DateTime, select
from sqlalchemy.sql import func

from domain.models import DailyUserStats
from domain.ports import AnalyticsRepositoryPort

Base = declarative_base()


class DailyUserStatsModel(Base):
    __tablename__ = "daily_user_stats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String, index=True)
    stat_date: Mapped[date] = mapped_column(Date, index=True)
    total_plays: Mapped[int] = mapped_column(Integer, default=0)
    total_skips: Mapped[int] = mapped_column(Integer, default=0)
    total_likes: Mapped[int] = mapped_column(Integer, default=0)
    total_shares: Mapped[int] = mapped_column(Integer, default=0)
    dominant_mood: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class PostgresAnalyticsRepository(AnalyticsRepositoryPort):
    def __init__(self, db_url: str = None):
        if not db_url:
            db_url = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/analytics")
        self.engine = create_async_engine(db_url, echo=False)
        self.session_factory = async_sessionmaker(bind=self.engine, expire_on_commit=False, class_=AsyncSession)

    async def _get_or_create(self, session: AsyncSession, user_id: str, stat_date: date) -> DailyUserStatsModel:
        result = await session.execute(
            select(DailyUserStatsModel)
            .where(DailyUserStatsModel.user_id == user_id, DailyUserStatsModel.stat_date == stat_date)
        )
        record = result.scalars().first()
        if not record:
            record = DailyUserStatsModel(
                user_id=user_id, 
                stat_date=stat_date,
                total_plays=0,
                total_skips=0,
                total_likes=0,
                total_shares=0
            )
            session.add(record)
        return record

    async def increment_interaction(self, user_id: str, stat_date: date, action: str) -> None:
        async with self.session_factory() as session:
            async with session.begin():
                record = await self._get_or_create(session, user_id, stat_date)
                
                if action == "play" or action == "complete":
                    record.total_plays += 1
                elif action == "skip":
                    record.total_skips += 1
                elif action == "like":
                    record.total_likes += 1
                elif action == "share":
                    record.total_shares += 1
                
                # SQLAlchemy onupdate triggers updated_at automatically

    async def update_dominant_mood(self, user_id: str, stat_date: date, mood: str) -> None:
        async with self.session_factory() as session:
            async with session.begin():
                record = await self._get_or_create(session, user_id, stat_date)
                record.dominant_mood = mood

    async def get_daily_stats_range(self, user_id: str, start_date: date, end_date: date) -> List[DailyUserStats]:
        async with self.session_factory() as session:
            result = await session.execute(
                select(DailyUserStatsModel)
                .where(
                    DailyUserStatsModel.user_id == user_id,
                    DailyUserStatsModel.stat_date >= start_date,
                    DailyUserStatsModel.stat_date <= end_date
                )
                .order_by(DailyUserStatsModel.stat_date.asc())
            )
            records = result.scalars().all()
            
            return [
                DailyUserStats(
                    user_id=r.user_id,
                    stat_date=r.stat_date,
                    total_plays=r.total_plays,
                    total_skips=r.total_skips,
                    total_likes=r.total_likes,
                    total_shares=r.total_shares,
                    dominant_mood=r.dominant_mood,
                    created_at=r.created_at,
                    updated_at=r.updated_at
                ) for r in records
            ]
