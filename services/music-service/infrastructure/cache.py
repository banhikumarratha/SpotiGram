import os
import redis.asyncio as redis
import json
from typing import Any, Optional

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
redis_client = None

async def get_cache():
    global redis_client
    if redis_client is None:
        redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    return redis_client

async def close_cache():
    global redis_client
    if redis_client is not None:
        await redis_client.close()
        redis_client = None

async def set_cache(key: str, value: Any, expire_seconds: int = 3600):
    client = await get_cache()
    await client.set(key, json.dumps(value), ex=expire_seconds)

async def get_from_cache(key: str) -> Optional[Any]:
    client = await get_cache()
    data = await client.get(key)
    if data:
        return json.loads(data)
    return None
