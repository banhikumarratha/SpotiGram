import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from fastapi import FastAPI
from api.routes import router as ai_router
from libs.shared.logger import setup_structured_logger
from libs.shared.telemetry import setup_telemetry

logger = setup_structured_logger("ai-assistant-service")

app = FastAPI(title="SpotiGram AI Assistant Service", version="1.0.0")

setup_telemetry(app, "ai-assistant-service")

app.include_router(ai_router)

@app.get("/health")
async def health():
    return {"status": "ok", "service": "ai-assistant-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
