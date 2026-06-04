# SpotiGram

SpotiGram is a complex, event-driven microservices ecosystem combining the domains of music streaming and social media. 

## Overview

This repository holds the entire SpotiGram platform, built using Hexagonal Architecture and Domain-Driven Design (DDD). Services communicate primarily asynchronously via Kafka (events) and synchronously via REST APIs.

## Tech Stack
- **Backend**: Python 3.12+, FastAPI
- **Frontend**: Streamlit
- **Databases**: PostgreSQL, Redis, ChromaDB
- **Event Bus**: Kafka
- **AI Models**: Ollama
- **Infrastructure**: Docker, Docker Compose (local), Kubernetes (prod)

## Quick Start
To get the project running locally:

```bash
cp .env.example .env
make run-local
```
