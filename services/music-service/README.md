# Music Service

The Music Service manages the playback, orchestration, and metadata retrieval for Spotigram, integrating heavily with Spotify's Web API and Playback SDK logic.

## Architecture
- **Hexagonal Architecture**: Isolates the domain from infrastructure concerns.
- **Async-First**: Built with FastAPI, `httpx`, `tenacity` (retries), and `aiokafka`.
- **Cache**: Redis (via `redis.asyncio`)
- **Messaging**: Kafka (publishes to `music.events.v1`)

## Resilience & Caching
- **Tenacity**: External HTTP requests to Spotify are wrapped in `@retry` decorators using exponential backoff to handle rate limits and temporary outages.
- **Redis Cache**: OAuth tokens and search/track metadata are aggressively cached to reduce external API footprints and latency.

## Local Development

### Requirements
- Python 3.11+
- Redis
- Kafka

### Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Running Tests
Tests use `respx` and `pytest-mock` to isolate the service from the external internet, ensuring stable and fast executions.
```bash
pytest tests/
```

### Running the Service
```bash
uvicorn main:app --reload --port 8000
```
