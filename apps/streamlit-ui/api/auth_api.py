from api.client import APIClient
from utils.config import settings

class AuthAPI(APIClient):
    def __init__(self):
        super().__init__(settings.AUTH_SERVICE_URL)

    def login(self, email: str, password: str):
        return self.post("/api/v1/auth/login", json={"email": email, "password": password})

    def register(self, email: str, password: str, name: str):
        return self.post("/api/v1/auth/register", json={
            "email": email,
            "password": password,
            "display_name": name
        })
