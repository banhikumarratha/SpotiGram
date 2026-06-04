# Recommendation Service

The `recommendation-service` is the AI intelligence layer for Spotigram. It builds Music DNA profiles, detects mood from webcam images, and generates personalized, mood-aware recommendations using vector similarity search.

## Architecture

Follows Hexagonal Architecture (Ports & Adapters):

```
domain/          → Pure models + abstract port interfaces
application/     → Business logic (mood, DNA, ranking)
infrastructure/  → Concrete adapters (ChromaDB, Kafka, DeepFace)
api/v1/          → FastAPI routes
```

## Key Components

| Component | Technology | Purpose |
|---|---|---|
| Vector Store | ChromaDB (embedded) | Music DNA + track embeddings, similarity search |
| Embeddings | sentence-transformers `all-MiniLM-L6-v2` | 384-dim track metadata encoding |
| Mood Detection | DeepFace (local) | Webcam image → emotion → Mood bucket |
| Event Streaming | aiokafka | Consume `music.events.v1`, `user.events.v1` |
| Publishing | aiokafka | Emit `recommendation.events.v1` |

## Ranking Signals

| Signal | Weight | Description |
|---|---|---|
| Music DNA match | 40% | Cosine similarity to user's Music DNA embedding |
| Mood energy | 25% | Distance between mood energy level and track energy |
| Social | 20% | Tracks popular with similar users |
| Time of day | 15% | Energy alignment with time (morning=calm, evening=energetic) |

## Cold Start Strategy

New users (< 10 interactions) receive curated genre seeds (pop, indie, electronic, hip-hop, rock). After 10 interactions, the full DNA-based pipeline activates.

## Endpoints

| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/recommendations/mood-scan` | Analyze webcam image → mood |
| GET | `/api/v1/recommendations/feed` | Personalized track recommendations |
| GET | `/api/v1/recommendations/similar-users` | Users with similar Music DNA |
| GET | `/api/v1/recommendations/music-dna` | User's DNA insights |
| POST | `/api/v1/recommendations/feedback` | Submit interaction to update DNA |
| GET | `/health` | Liveness probe |
| GET | `/ready` | Readiness probe |
| GET | `/metrics` | Prometheus metrics |

All endpoints require `X-User-ID` header.

## Local Development

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Running Tests

Tests use `chromadb.EphemeralClient()` — no Docker or external services needed.

```bash
CHROMA_EPHEMERAL=true PYTHONPATH=. pytest tests/ --cov
```

### Running the Service

```bash
CHROMA_EPHEMERAL=true uvicorn main:app --reload --port 8002
```

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `KAFKA_URL` | `kafka:9092` | Kafka bootstrap servers |
| `CHROMA_PERSIST_DIR` | `./chroma_data` | ChromaDB persistence directory |
| `CHROMA_EPHEMERAL` | `false` | Use in-memory ChromaDB (tests only) |
| `SIGNAL_DNA_WEIGHT` | `0.40` | DNA ranking signal weight |
| `SIGNAL_MOOD_WEIGHT` | `0.25` | Mood ranking signal weight |
| `SIGNAL_SOCIAL_WEIGHT` | `0.20` | Social signal weight |
| `SIGNAL_TOD_WEIGHT` | `0.15` | Time-of-day signal weight |
