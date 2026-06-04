import pytest
from fastapi.testclient import TestClient
from main import app
from application.analytics_service import AnalyticsService
import api.v1.router as router_module

client = TestClient(app)


@pytest.fixture(autouse=True)
def override_service(mock_repo):
    svc = AnalyticsService(mock_repo)
    router_module._analytics_service = svc
    yield
    router_module._analytics_service = None


def test_health_check():
    res = client.get("/health")
    assert res.status_code == 200


def test_ready_check():
    res = client.get("/ready")
    assert res.status_code == 200


def test_metrics_check():
    res = client.get("/metrics")
    assert res.status_code == 200


def test_get_listening_stats():
    res = client.get("/api/v1/analytics/listening-stats?days=30", headers={"X-User-ID": "u1"})
    assert res.status_code == 200
    assert "completion_rate" in res.json()


def test_get_mood_trends():
    res = client.get("/api/v1/analytics/mood-trends?days=30", headers={"X-User-ID": "u1"})
    assert res.status_code == 200
    assert "dominant_mood" in res.json()


def test_get_music_personality():
    res = client.get("/api/v1/analytics/personality", headers={"X-User-ID": "u1"})
    assert res.status_code == 200
    assert "traits" in res.json()


def test_get_year_in_review():
    res = client.get("/api/v1/analytics/year-in-review?year=2023", headers={"X-User-ID": "u1"})
    assert res.status_code == 200
    assert "total_minutes" in res.json()


def test_missing_header():
    res = client.get("/api/v1/analytics/year-in-review?year=2023")
    assert res.status_code == 422
