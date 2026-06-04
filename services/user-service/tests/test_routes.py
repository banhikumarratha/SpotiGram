import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    res = client.get("/health")
    assert res.status_code == 200

def test_ready():
    res = client.get("/ready")
    assert res.status_code == 200

def test_metrics():
    res = client.get("/metrics")
    assert res.status_code == 200
