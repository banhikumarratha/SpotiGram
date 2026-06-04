from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_track():
    resp = client.get("/api/v1/music/tracks/12345")
    assert resp.status_code == 200
    track = resp.json()
    assert track["spotify_id"] == "12345"
    assert "Mocked Title" in track["title"]

def test_get_track_not_found():
    resp = client.get("/api/v1/music/tracks/notfound")
    assert resp.status_code == 404
