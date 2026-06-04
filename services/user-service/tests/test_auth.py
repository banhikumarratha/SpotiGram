import pytest
from application.auth_service import AuthService
from infrastructure.models import UserAccount, Base
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
async def test_register_success(db_session, mock_publisher):
    service = AuthService(db_session, publisher=mock_publisher)
    res = await service.register("test@test.com", "pass123", "TestUser")
    assert res["email"] == "test@test.com"
    assert "user_id" in res
    assert mock_publisher.publish.called

@pytest.mark.asyncio
async def test_register_duplicate_email(db_session):
    service = AuthService(db_session)
    await service.register("test@test.com", "pass123", "TestUser")
    with pytest.raises(ValueError, match="Email already exists"):
        await service.register("test@test.com", "pass123", "TestUser")

@pytest.mark.asyncio
async def test_login_success(db_session):
    service = AuthService(db_session)
    await service.register("test@test.com", "pass123", "TestUser")
    res = await service.login("test@test.com", "pass123")
    assert "access_token" in res
    assert res["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_invalid_password(db_session):
    service = AuthService(db_session)
    await service.register("test@test.com", "pass123", "TestUser")
    with pytest.raises(ValueError, match="Invalid credentials"):
        await service.login("test@test.com", "wrongpass")
