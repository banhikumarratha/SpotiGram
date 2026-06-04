from fastapi import Request, HTTPException, status
import redis
import os

redis_client = redis.Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"))

async def idempotency_middleware(request: Request, call_next):
    if request.method in ["POST", "PUT", "PATCH"]:
        idem_key = request.headers.get("Idempotency-Key")
        if idem_key:
            redis_key = f"idempotency:{idem_key}"
            try:
                # If key exists, it means we already processed this. Return 409 Conflict.
                # A more robust system would store the exact previous HTTP response.
                if redis_client.exists(redis_key):
                    from fastapi.responses import JSONResponse
                    return JSONResponse(status_code=409, content={"detail": "Duplicate request detected"})
                
                # Mark as processing/done (store for 24h)
                redis_client.setex(redis_key, 86400, "done")
            except redis.RedisError:
                pass # Fail open
                
    return await call_next(request)
