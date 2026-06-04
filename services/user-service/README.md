# User Service

The User Service is responsible for managing authentication, profile metadata, and the social graph (follows/blocks/mutes) for Spotigram.

## Architecture
- **Hexagonal Architecture**: Isolates the domain from infrastructure concerns.
- **Async-First**: Built with FastAPI, SQLAlchemy 2.0 (async), and aiokafka.
- **Database**: PostgreSQL
- **Messaging**: Kafka (publishes to `user.events.v1`)

## Local Development

### Requirements
- Python 3.11+
- Postgres
- Kafka

### Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Running Tests
Tests use an in-memory SQLite database via `aiosqlite`.
```bash
pytest tests/
```

### Running the Service
```bash
uvicorn main:app --reload --port 8000
```
