import pytest
import os
from unittest.mock import AsyncMock

@pytest.fixture(autouse=True)
def mock_redis(mocker):
    mocker.patch("redis.asyncio.from_url", return_value=AsyncMock())
    mocker.patch("fastapi_limiter.FastAPILimiter.init", new_callable=AsyncMock)
    mocker.patch("fastapi_limiter.depends.RateLimiter.__call__", new_callable=AsyncMock)
    os.environ["REDIS_URL"] = "redis://mock:6379"
