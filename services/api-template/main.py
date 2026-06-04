from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os

# To allow importing from libs
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from libs.shared.utils import setup_logger, standard_response

logger = setup_logger("api-template")

app = FastAPI(title="SpotiGram API Template", version="1.0.0")

class HealthResponse(BaseModel):
    status: str
    service: str

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for the service."""
    return {"status": "ok", "service": "api-template"}

@app.get("/metrics")
async def metrics():
    """Basic metrics placeholder."""
    return standard_response(success=True, data={"metrics": "Not implemented yet"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
