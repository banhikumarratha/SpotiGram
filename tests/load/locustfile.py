from locust import HttpUser, task, between
import random

class SpotigramUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        """Executed when a simulated user starts."""
        self.user_email = f"loadtest_{random.randint(1000, 9999)}@spotigram.ai"
        
        # 1. Register (ignore if already exists)
        self.client.post("/api/v1/auth/register", json={
            "email": self.user_email,
            "password": "password123",
            "name": "Load Test User"
        }, catch_response=True)
        
        # 2. Login
        res = self.client.post("/api/v1/auth/login", data={
            "username": self.user_email,
            "password": "password123"
        })
        if res.status_code == 200:
            token = res.json().get("access_token")
            self.client.headers.update({"Authorization": f"Bearer {token}"})

    @task(3)
    def view_feed(self):
        self.client.get("/api/v1/music/feed")

    @task(2)
    def search_spotify(self):
        query = random.choice(["Beatles", "Drake", "Taylor Swift", "Daft Punk", "Nirvana"])
        self.client.get(f"/api/v1/spotify/search?q={query}")

    @task(1)
    def ai_dj_chat(self):
        self.client.post("/api/v1/ai/dj/chat", json={
            "session_id": f"sess_{random.randint(1,1000)}",
            "message": "Play some chill music",
            "context": {}
        })

    @task(1)
    def view_analytics(self):
        self.client.get("/api/v1/analytics/listening-stats?days=30")
