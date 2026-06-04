# SpotiGram Social Service

This service handles the social graph (follows) and feeds (posts).

## Architecture
It follows Hexagonal Architecture:
- `api/`: FastAPI endpoints.
- `application/`: Business use cases.
- `domain/`: Domain logic.
- `infrastructure/`: Database, Kafka.

## Run Locally
```bash
uvicorn main:app --reload --port 8001
```
