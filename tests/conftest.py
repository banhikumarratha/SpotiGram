import pytest
import os
import httpx

@pytest.fixture(scope="session")
def base_url():
    """Base URL for the API Gateway"""
    return os.getenv("API_GATEWAY_URL", "http://localhost:8000")

@pytest.fixture(scope="session")
def e2e_client(base_url):
    """Synchronous HTTP client for E2E tests"""
    with httpx.Client(base_url=base_url) as client:
        yield client
