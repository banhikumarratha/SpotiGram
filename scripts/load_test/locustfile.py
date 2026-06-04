from locust import HttpUser, task, between
import random

class SpotiGramUser(HttpUser):
    wait_time = between(1, 5)

    @task(3)
    def view_feed(self):
        # Targeting social-service
        self.client.get("/api/v1/posts", name="Get Feed")

    @task(1)
    def create_post(self):
        self.client.post("/api/v1/posts", json={
            "user_id": f"load_user_{random.randint(1, 1000)}",
            "track": {"spotify_id": "test", "title": "Load Test", "artist": "Locust", "duration_ms": 100},
            "caption": "Testing system under load!",
            "mood": "ENERGETIC"
        }, name="Create Post")

    @task(2)
    def get_user_profile(self):
        # Targeting user-service
        self.client.get(f"/api/v1/users/user_{random.randint(1, 100)}", name="Get Profile")
