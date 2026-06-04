import pytest
from fastapi.testclient import TestClient
from main import app
from core.middleware import JWT_SECRET
import jwt
import httpx

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200

def test_ready(client):
    res = client.get("/ready")
    assert res.status_code == 200

def test_metrics(client):
    res = client.get("/metrics")
    assert res.status_code == 200

def test_missing_auth(client):
    res = client.get("/api/v1/users/me")
    assert res.status_code == 401

def test_invalid_auth(client):
    res = client.get("/api/v1/users/me", headers={"Authorization": "Bearer bad"})
    assert res.status_code == 401

def test_proxy_routing(mocker, client):
    token = jwt.encode({"sub": "test-user"}, JWT_SECRET, algorithm="HS256")
    
    # Mock the httpx client inside proxy.py
    class AsyncMockResponse:
        status_code = 200
        headers = {}
        async def aiter_raw(self):
            yield b'{"message": "proxied"}'
            
    mocker.patch("httpx.AsyncClient.send", return_value=AsyncMockResponse())
    
    res = client.get("/api/v1/users/me", headers={
        "Authorization": f"Bearer {token}",
        "X-Correlation-ID": "123"
    })
    
    assert res.status_code == 200
    assert res.headers["x-correlation-id"] == "123"

def test_proxy_not_found(client):
    token = jwt.encode({"sub": "test-user"}, JWT_SECRET, algorithm="HS256")
    res = client.get("/api/v1/unknown/route", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 404
