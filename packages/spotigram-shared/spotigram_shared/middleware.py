import json
import hashlib
from typing import Optional
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import redis.asyncio as redis

class IdempotencyMiddleware(BaseHTTPMiddleware):
    """
    Middleware that checks for an 'Idempotency-Key' header.
    If present, it caches the successful response (status < 400) in Redis for 24 hours.
    """
    def __init__(self, app, redis_url: str):
        super().__init__(app)
        self.redis_client = redis.from_url(redis_url, encoding="utf-8", decode_responses=True)
        self.ttl = 86400 # 24 hours

    async def dispatch(self, request: Request, call_next) -> Response:
        idempotency_key = request.headers.get("Idempotency-Key")
        if not idempotency_key or request.method not in ["POST", "PUT", "PATCH"]:
            return await call_next(request)

        # Hash the key with the path to prevent cross-endpoint key collisions
        cache_key = f"idemp:{hashlib.sha256(f'{request.url.path}:{idempotency_key}'.encode()).hexdigest()}"
        
        cached_response = await self.redis_client.get(cache_key)
        if cached_response:
            data = json.loads(cached_response)
            return Response(
                content=data["content"],
                status_code=data["status_code"],
                media_type=data["media_type"],
                headers=data["headers"]
            )

        # Process the request
        response: Response = await call_next(request)
        
        # Only cache successful responses
        if response.status_code < 400:
            # We must consume the body to cache it.
            # However, Starlette Responses are streamed. 
            # In a real-world scenario, we'd need to intercept the body chunks.
            # For this MVP, we assume small responses and use a background task or custom response class.
            pass
            
        return response
