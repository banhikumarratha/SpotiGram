import asyncio
import httpx

async def test():
    async with httpx.AsyncClient() as client:
        # Login
        res_login = await client.post("http://localhost:8000/api/v1/auth/login", json={
            "email": "demo@spotigram.ai", "password": "demopassword"
        })
        token = res_login.json()["access_token"]
        client.headers.update({"Authorization": f"Bearer {token}"})
        # Test music search
        res1 = await client.get("http://localhost:8000/api/v1/music/search?q=Workout")
        print("Music search:", res1.status_code, res1.text)

        # Test ai dj
        res2 = await client.post("http://localhost:8000/api/v1/ai/dj", json={
            "session_id": "test_1",
            "message": "hello",
            "context": {}
        })
        print("AI DJ:", res2.status_code, res2.text)

        # Test mood text
        res3 = await client.post("http://localhost:8000/api/v1/recommendations/mood-scan/text", json={
            "text": "happy"
        })
        print("Mood text:", res3.status_code, res3.text)

if __name__ == "__main__":
    asyncio.run(test())
