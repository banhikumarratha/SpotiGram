from fastapi import Request, HTTPException, status
import redis
import os
import time

# Very simple sliding window/fixed window rate limiter
# Uses REDIS_URL from env
redis_client = redis.Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"))

async def rate_limit_middleware(request: Request, call_next):
    # In a real scenario, use X-Forwarded-For or authenticated user ID
    client_ip = request.client.host if request.client else "unknown"
    key = f"rate_limit:{client_ip}"
    
    # 100 requests per minute
    limit = 100
    current_time = int(time.time())
    window = current_time // 60
    
    window_key = f"{key}:{window}"
    
    try:
        requests = redis_client.incr(window_key)
        if requests == 1:
            redis_client.expire(window_key, 60)
            
        if requests > limit:
            return HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Too Many Requests")
            
    except redis.RedisError:
        # Fail open if Redis is down
        pass
        
    return await call_next(request)
