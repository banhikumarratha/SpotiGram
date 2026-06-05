# Spotigram Interview Guide

## For Interviewers & Candidates

This document helps anyone presenting or discussing the Spotigram project in a technical interview, portfolio review, or architecture walkthrough.

---

## 1. Architecture & Design (System Design Interview)

### Q: Describe the high-level architecture of Spotigram.
**A**: Spotigram is a microservices platform with 6 backend services (API Gateway, User, Music, Recommendation, AI Assistant, Analytics) plus a Streamlit frontend. Services communicate via REST APIs (synchronous) and Apache Kafka (asynchronous events). Each service follows Hexagonal Architecture internally with domain/application/infrastructure layers. Data stores include PostgreSQL, Redis, ChromaDB (vector DB), and Ollama (local LLM).

### Q: Why microservices instead of a monolith?
**A**: Each bounded context (Identity, Music Catalog, Recommendations, AI, Analytics) has distinct scaling characteristics and technology requirements. The AI service needs LangChain/LangGraph which shouldn't pollute other services. The recommendation service needs a vector database. Microservices let each team own their full stack.

### Q: How do you prevent services from breaking each other?
**A**: (1) Database isolation — no cross-service DB access. (2) Versioned API contracts and Kafka event schemas. (3) Automated architecture fitness tests that parse Python AST and fail CI if boundaries are violated. (4) Circuit breakers and DLQ for resilience.

---

## 2. Domain-Driven Design

### Q: What are the bounded contexts?
**A**:
- **Identity & Social**: User accounts, profiles, follows, blocks (user-service)
- **Music Catalog**: Spotify integration, search, playback events (music-service)
- **Discovery & DNA**: Mood detection, Music DNA fingerprinting, recommendations (recommendation-service)
- **Conversational AI**: AI DJ, RAG, playlist generation (ai-assistant-service)
- **Analytics**: Listening stats, mood trends, personality profiling (analytics-service)

### Q: What is Music DNA?
**A**: A 384-dimensional vector embedding representing a user's musical fingerprint. Built from genre weights, artist affinities, mood distribution, and interaction signals (play/skip/like/save/share). Cold start requires 10+ interactions. Stored in ChromaDB and used for cosine similarity searches to find similar users and generate recommendations.

---

## 3. AI & ML

### Q: How does the AI DJ work?
**A**: It uses a LangGraph StateGraph with states: analyze_mood → retrieve_context (RAG) → generate_response → extract_actions → format_output. The RAG step injects the user's Music DNA, recent tracks, and mood into the prompt. The LLM (Ollama by default) generates contextual responses with optional tool calls for Spotify search.

### Q: Why isolate LangChain to one service?
**A**: LangChain evolves rapidly. Isolating it prevents version conflicts across the codebase and keeps domain models as pure Python dataclasses. The AI service's domain layer has zero LangChain imports — it uses interfaces (`AIProviderPort`, `MemoryStorePort`) that the LangChain adapters implement.

### Q: How does RAG work without cross-service DB access?
**A**: The `UserContext` object is passed in every API request. The frontend or API gateway assembles it from the recommendation service's output and passes it to the AI service. This respects the architectural rule that no service queries another service's database.

---

## 4. Event-Driven Architecture

### Q: What happens when a user plays a track?
**A**: Music Service publishes a `music.events.v1` event to Kafka. Two consumers receive it: (1) Recommendation Service updates the user's Music DNA embedding in ChromaDB. (2) Analytics Service increments the daily play count in PostgreSQL. Both happen asynchronously. If processing fails, the message is sent to `spotigram.dlq`.

### Q: How do you handle message processing failures?
**A**: The `DLQKafkaConsumer` base class wraps all message processing in a try/except. Failed messages are published to `spotigram.dlq` with the original topic, error message, and full payload for manual inspection and replay.

---

## 5. Resilience & Production Readiness

### Q: What resilience patterns are implemented?
**A**:
- **Retry with exponential backoff** (tenacity) for inter-service HTTP calls
- **Circuit breakers** for downstream services (Spotify API, Ollama)
- **Idempotency middleware** caching successful responses in Redis for 24 hours
- **DLQ** for Kafka consumer failures
- **Outbox pattern** for atomic event emission
- **Rate limiting** at 100 req/min via Redis-backed fastapi-limiter
- **Fallbacks**: MusicBrainz and Last.fm when Spotify is unavailable

### Q: How do you verify architecture rules in CI?
**A**: `tests/architecture/test_fitness.py` uses Python's `ast` module to statically analyze the codebase. It checks for LangChain isolation, database boundary violations, hardcoded credentials, API versioning, and health probe presence. It runs in < 100ms and fails the build on any violation.

---

## 6. Testing Strategy

### Q: What types of tests do you have?
**A**:
- **Unit**: Per-service, mocking infrastructure (pytest)
- **Architecture fitness**: AST-based static analysis (pytest)
- **E2E**: Full user journey scenarios hitting the API Gateway (pytest + httpx)
- **Load**: 100 concurrent users via Locust
- **Smoke**: Health/ready/metrics probe verification

---

## 7. Key Technical Decisions (ADRs)

| Decision | Rationale |
|---|---|
| Hexagonal Architecture | Testable, framework-agnostic business logic |
| LangChain sandbox | Prevent framework coupling, isolate AI complexity |
| Kafka for events | Temporal decoupling, replay capability, DLQ support |
| ChromaDB for vectors | Efficient cosine similarity for Music DNA matching |
| Multi-provider AI | No single-point-of-failure for LLM inference |
