import httpx
from starlette.requests import Request
from starlette.responses import StreamingResponse
from fastapi import HTTPException
import os

SERVICE_MAP = {
    "/api/v1/users": os.getenv("USER_SERVICE_URL", "http://user-service:8000"),
    "/api/v1/music": os.getenv("MUSIC_SERVICE_URL", "http://music-service:8000"),
    "/api/v1/recommendations": os.getenv("RECOMMENDATION_SERVICE_URL", "http://recommendation-service:8000"),
    "/api/v1/ai": os.getenv("AI_SERVICE_URL", "http://ai-assistant-service:8000"),
    "/api/v1/analytics": os.getenv("ANALYTICS_SERVICE_URL", "http://analytics-service:8000"),
}

client = httpx.AsyncClient()

async def forward_request(request: Request):
    path = request.url.path
    target_base = None
    for prefix, url in SERVICE_MAP.items():
        if path.startswith(prefix):
            target_base = url
            break
            
    if not target_base:
        raise HTTPException(status_code=404, detail="Route not found in API Gateway")
        
    url = httpx.URL(path=path, query=request.url.query.encode("utf-8"))
    target_url = target_base + str(url)
    
    headers = dict(request.headers)
    headers.pop("host", None)
    headers["X-Correlation-ID"] = getattr(request.state, "correlation_id", "")
    if hasattr(request.state, "user_id"):
        headers["X-User-ID"] = request.state.user_id
        
    req = client.build_request(
        method=request.method,
        url=target_url,
        headers=headers,
        content=request.stream()
    )
    try:
        response = await client.send(req, stream=True)
        return StreamingResponse(
            response.aiter_raw(),
            status_code=response.status_code,
            headers=dict(response.headers)
        )
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Bad Gateway: {str(e)}")
