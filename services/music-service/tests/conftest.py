import pytest
import os
from unittest.mock import AsyncMock

@pytest.fixture(autouse=True)
def mock_env():
    os.environ["REDIS_URL"] = "redis://mock"
    os.environ["KAFKA_URL"] = "kafka:9092"
    os.environ["SPOTIFY_CLIENT_ID"] = "test"
    os.environ["SPOTIFY_CLIENT_SECRET"] = "test"

@pytest.fixture
def mock_publisher(mocker):
    pub = AsyncMock()
    mocker.patch("infrastructure.kafka_publisher.KafkaPublisher", return_value=pub)
    return pub

@pytest.fixture(autouse=True)
def mock_redis(mocker):
    mock_redis_client = AsyncMock()
    mock_redis_client.get.return_value = None
    mocker.patch("infrastructure.cache.get_cache", return_value=mock_redis_client)
    return mock_redis_client
