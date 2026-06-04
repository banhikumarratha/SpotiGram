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

def test_create_and_get_user():
    # Create
    resp = client.post("/api/v1/users", json={"username": "testuser", "display_name": "Test User"})
    assert resp.status_code == 201
    user_data = resp.json()
    assert user_data["username"] == "testuser"
    user_id = user_data["id"]

    # Get
    resp_get = client.get(f"/api/v1/users/{user_id}")
    assert resp_get.status_code == 200
    assert resp_get.json()["id"] == user_id
