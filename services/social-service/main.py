import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from fastapi import FastAPI
from api.routes import router as post_router
from libs.shared.logger import setup_structured_logger
from libs.shared.telemetry import setup_telemetry
from infrastructure.database.session import Base, engine

# For MVP, auto-create tables
Base.metadata.create_all(bind=engine)

logger = setup_structured_logger("social-service")

app = FastAPI(title="SpotiGram Social Service", version="1.0.0")

setup_telemetry(app, "social-service")

app.include_router(post_router)

@app.get("/health")
async def health():
    return {"status": "ok", "service": "social-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
