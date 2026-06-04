# 🎵 SpotiGram

SpotiGram is a modern, event-driven microservices ecosystem that combines music discovery with social networking and AI-powered recommendations.

## 📖 Documentation Directory

- [Architecture Overview & Diagrams](docs/architecture_overview.md)
- [Deployment Guide](docs/deployment_guide.md)
- [Project Roadmap](docs/roadmap.md)
- [Architecture Decision Records (ADRs)](docs/adrs/)
- [Interview Talking Points](docs/interview_talking_points.md)

## 🚀 Features

- **Social Music Feed:** Share the tracks you are listening to, complete with captions and detected moods.
- **AI DJ:** Chat with a LangGraph-powered AI assistant that curates tracks based on your listening history and current vibe.
- **Emotion & Vector Analysis:** Built-in NLP heuristic scanning and text embeddings (via ChromaDB) to power intelligent recommendations.
- **Production Hardened:** Features Distributed Rate Limiting, Idempotency checks, Circuit Breakers, and the Outbox Pattern for reliable Kafka messaging.

## 🛠 Tech Stack

- **Backend:** Python 3.11, FastAPI, SQLAlchemy, Pydantic
- **Frontend:** Streamlit
- **AI/ML:** LangChain, LangGraph, Ollama, SentenceTransformers, TextBlob
- **Data & Messaging:** PostgreSQL, Redis, Apache Kafka, ChromaDB
- **Infrastructure:** Docker Compose, Kubernetes (HPA), OpenTelemetry, Prometheus, Grafana

## 🏃‍♂️ Quick Start

```bash
docker-compose -f docker-compose.dev.yml up --build
```
Navigate to `http://localhost:8501` to view the Streamlit UI.
