# SpotiGram Music Service

This service acts as a proxy to external music APIs (like Spotify).

## Architecture
It follows Hexagonal Architecture:
- `api/`: FastAPI endpoints.
- `application/`: Business use cases.

## Run Locally
```bash
uvicorn main:app --reload --port 8002
```
