import asyncio
import httpx
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("seed_data")

API_URL = os.getenv("API_GATEWAY_URL", "http://localhost:8000")

async def seed_data():
    async with httpx.AsyncClient(base_url=API_URL, timeout=10.0) as client:
        logger.info("Starting database seed...")
        
        # 1. Create Demo User
        demo_user = {
            "email": "demo@spotigram.ai",
            "password": "demopassword",
            "name": "Demo User"
        }
        logger.info("Registering demo user...")
        # Ignore if it exists
        await client.post("/api/v1/auth/register", json=demo_user)
        
        # 2. Login
        logger.info("Logging in...")
        res = await client.post("/api/v1/auth/login", data={
            "username": demo_user["email"],
            "password": demo_user["password"]
        })
        
        if res.status_code != 200:
            logger.error(f"Login failed! Ensure API gateway is running. {res.text}")
            return
            
        token = res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        client.headers.update(headers)
        logger.info("Authenticated.")

        # 3. Trigger Mood Scans (Updates Mood History -> Recommendation embeddings)
        logger.info("Sending mood logs...")
        await client.post("/api/v1/mood/analyze/text", json={"text": "I am feeling very happy and energetic today!"})
        await client.post("/api/v1/mood/analyze/text", json={"text": "Just want to relax and chill."})

        # 4. Trigger AI DJ Conversation (Updates DJ History)
        logger.info("Chatting with AI DJ...")
        await client.post("/api/v1/ai/dj/chat", json={
            "session_id": "demo_session_1",
            "message": "Can you give me something upbeat for a workout?",
            "context": {}
        })

        # 5. Simulate track plays (Updates Music DNA & Analytics)
        # Note: Depending on the API design, this might be a direct event or an API endpoint.
        # Let's hit the search to populate some caches.
        logger.info("Running searches...")
        await client.get("/api/v1/spotify/search?q=Workout")
        
        logger.info("Seed data generated successfully!")

if __name__ == "__main__":
    asyncio.run(seed_data())
