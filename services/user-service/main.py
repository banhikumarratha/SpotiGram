import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from fastapi import FastAPI
from api.routes import router as user_router
from libs.shared.logger import setup_structured_logger
from libs.shared.telemetry import setup_telemetry
from infrastructure.database.session import Base, engine

# For MVP, auto-create tables if Alembic isn't run
Base.metadata.create_all(bind=engine)

logger = setup_structured_logger("user-service")

app = FastAPI(title="SpotiGram User Service", version="1.0.0")

setup_telemetry(app, "user-service")

app.include_router(user_router)

@app.get("/health")
async def health():
    return {"status": "ok", "service": "user-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
