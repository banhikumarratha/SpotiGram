import pytest
from application.social_service import SocialService
from infrastructure.models import Base, ConnectionStatus
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

@pytest.fixture
async def db_session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    session_maker = async_sessionmaker(engine, expire_on_commit=False)
    async with session_maker() as session:
        yield session

@pytest.mark.asyncio
async def test_follow_user(db_session, mock_publisher):
    service = SocialService(db_session, publisher=mock_publisher)
    res = await service.follow_user("user1", "user2")
    assert res["status"] == "success"
    assert mock_publisher.publish.called

@pytest.mark.asyncio
async def test_follow_self_fails(db_session):
    service = SocialService(db_session)
    with pytest.raises(ValueError, match="Cannot follow yourself"):
        await service.follow_user("user1", "user1")

@pytest.mark.asyncio
async def test_follow_already_following(db_session):
    service = SocialService(db_session)
    await service.follow_user("user1", "user2")
    with pytest.raises(ValueError, match="Already following"):
        await service.follow_user("user1", "user2")
