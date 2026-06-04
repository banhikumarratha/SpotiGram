import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from datetime import date
from infrastructure.postgres_repo import PostgresAnalyticsRepository, Base


@pytest_asyncio.fixture
async def repo():
    # Use SQLite in-memory instead of TestContainers because Docker is unavailable in this environment
    async_url = "sqlite+aiosqlite:///:memory:"
    
    # Initialize repo
    repository = PostgresAnalyticsRepository(db_url=async_url)
    
    # Create tables
    async with repository.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    yield repository
    
    # Drop tables
    async with repository.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.mark.asyncio
async def test_increment_interaction(repo):
    d = date(2023, 1, 1)
    await repo.increment_interaction("u1", d, "play")
    await repo.increment_interaction("u1", d, "play")
    await repo.increment_interaction("u1", d, "skip")
    
    stats = await repo.get_daily_stats_range("u1", d, d)
    assert len(stats) == 1
    assert stats[0].total_plays == 2
    assert stats[0].total_skips == 1


@pytest.mark.asyncio
async def test_update_dominant_mood(repo):
    d = date(2023, 1, 1)
    await repo.update_dominant_mood("u1", d, "happy")
    await repo.update_dominant_mood("u1", d, "sad") # Overwrites
    
    stats = await repo.get_daily_stats_range("u1", d, d)
    assert stats[0].dominant_mood == "sad"


@pytest.mark.asyncio
async def test_get_daily_stats_range(repo):
    await repo.increment_interaction("u1", date(2023, 1, 1), "play")
    await repo.increment_interaction("u1", date(2023, 1, 2), "play")
    await repo.increment_interaction("u2", date(2023, 1, 1), "play") # Different user
    
    stats = await repo.get_daily_stats_range("u1", date(2023, 1, 1), date(2023, 1, 3))
    assert len(stats) == 2
