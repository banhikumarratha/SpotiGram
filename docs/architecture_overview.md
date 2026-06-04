# Architecture Overview

Spotigram follows a Domain-Driven Design (DDD) and Hexagonal Architecture pattern.
It leverages an API-First approach and Event-Driven asynchronous communication.

## Microservices
- **API Gateway**: Entry point for all clients.
- **User Service**: Manages profiles and relationships.
- **Music Service**: Interfaces with Spotify and handles playback metadata.
- **Recommendation Service**: Analyzes DNA and serves feed.
- **AI Assistant Service**: Manages Ollama/LLM interactions for the DJ.
- **Analytics Service**: Captures telemetry and calculates taste metrics.

## Communication
- Sync: REST via FastAPI.
- Async: Events via Kafka (future implementation).
