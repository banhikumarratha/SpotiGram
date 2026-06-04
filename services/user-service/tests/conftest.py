import pytest
import os
from unittest.mock import AsyncMock

@pytest.fixture(autouse=True)
def mock_env():
    os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
    os.environ["KAFKA_URL"] = "kafka:9092"
    os.environ["JWT_SECRET"] = "test-secret"

@pytest.fixture
def mock_publisher(mocker):
    pub = AsyncMock()
    mocker.patch("infrastructure.kafka_publisher.KafkaPublisher", return_value=pub)
    return pub
