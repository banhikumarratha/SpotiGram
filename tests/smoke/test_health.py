import pytest

# Smoke tests just hit the endpoints to see if they return 200 OK.
# We test the gateway, which routes to internal services if necessary,
# but we can also test internal service health if exposed directly.

def test_api_gateway_health(e2e_client):
    res = e2e_client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "healthy"}

def test_api_gateway_ready(e2e_client):
    res = e2e_client.get("/ready")
    assert res.status_code == 200
    assert res.json() == {"status": "ready"}

def test_api_gateway_metrics(e2e_client):
    res = e2e_client.get("/metrics")
    assert res.status_code == 200
    assert "process_cpu_seconds_total" in res.text
