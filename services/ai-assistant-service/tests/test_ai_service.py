from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_recommendations():
    resp = client.get("/api/v1/ai/recommendations?mood=HAPPY")
    assert resp.status_code == 200
    recs = resp.json()
    assert len(recs) > 0
    assert "HAPPY" in recs[0]["title"]
