# SpotiGram AI Assistant Service

This service handles recommendations and vector search using LangChain and ChromaDB.

## Architecture
It follows Hexagonal Architecture:
- `api/`: FastAPI endpoints.
- `application/`: Business use cases.
- `infrastructure/`: ChromaDB client.

## Run Locally
```bash
uvicorn main:app --reload --port 8003
```
