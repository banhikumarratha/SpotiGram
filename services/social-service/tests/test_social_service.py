from fastapi.testclient import TestClient
from main import app
from infrastructure.database.session import Base, engine
import pytest

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_and_get_feed():
    track_data = {
        "spotify_id": "123",
        "title": "Test Song",
        "artist": "Test Artist",
        "duration_ms": 200000
    }
    
    # Create
    resp = client.post("/api/v1/posts", json={
        "user_id": "user1",
        "track": track_data,
        "caption": "Love this song!",
        "mood": "HAPPY"
    })
    assert resp.status_code == 201
    post_data = resp.json()
    assert post_data["caption"] == "Love this song!"
    assert post_data["track"]["title"] == "Test Song"

    # Get Feed
    resp_get = client.get("/api/v1/posts")
    assert resp_get.status_code == 200
    feed = resp_get.json()
    assert len(feed) > 0
    assert feed[0]["id"] == post_data["id"]
