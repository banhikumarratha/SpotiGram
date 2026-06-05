# Setup Guide

## Prerequisites

| Tool | Version | Purpose |
|---|---|---|
| Python | ≥ 3.11 | Runtime for all services |
| Docker & Docker Compose | Latest | Container orchestration |
| Git | Latest | Source control |
| Make | Latest | Build automation |
| Spotify Developer Account | — | OAuth credentials |

## 1. Clone the Repository

```bash
git clone https://github.com/your-org/SpotiGram.git
cd SpotiGram
```

## 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and fill in your credentials:

```env
# Required
SPOTIFY_CLIENT_ID=<your spotify client id>
SPOTIFY_CLIENT_SECRET=<your spotify client secret>
SPOTIFY_REDIRECT_URI=http://localhost:8501/callback

# Optional AI providers (Ollama is the default)
OLLAMA_BASE_URL=http://localhost:11434
# GROK_API_KEY=
# GEMINI_API_KEY=

# Defaults (change for production)
JWT_SECRET=spotigram-dev-secret
DATABASE_URL=postgresql://user:pass@localhost:5432/spotigram
```

## 3. Start the Platform

### Option A: Docker Compose (Recommended)

```bash
make local
```

This boots all services and infrastructure:
- PostgreSQL (port 5432)
- Redis (port 6379)
- Kafka (port 9092)
- ChromaDB (port 8001)
- Ollama (port 11434)
- API Gateway (port 8000)
- Streamlit UI (port 8501)
- Prometheus (port 9090), Grafana (port 3000), Loki (port 3100), Jaeger (port 16686)

### Option B: Individual Service (Development)

```bash
cd services/user-service
pip install -r requirements.txt -r requirements-dev.txt
uvicorn main:app --reload --port 8002
```

## 4. Seed Demo Data

```bash
python scripts/seed_data.py
```

Creates the `demo@spotigram.ai` user with preloaded mood history, AI DJ sessions, and recommendations.

## 5. Verify

```bash
# Smoke test
make smoke-test

# Or manually
curl http://localhost:8000/health
# → {"status": "healthy"}
```

## 6. Open the UI

Navigate to [http://localhost:8501](http://localhost:8501) and log in with:
- **Email**: `demo@spotigram.ai`
- **Password**: `demopassword`
