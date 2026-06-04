# SpotiGram User Service

This service handles user profiles, registration, and user-specific data.

## Architecture
It follows Hexagonal Architecture:
- `api/`: FastAPI endpoints.
- `application/`: Business use cases.
- `domain/`: Domain logic.
- `infrastructure/`: Database, Kafka.

## Run Locally
```bash
uvicorn main:app --reload
```
