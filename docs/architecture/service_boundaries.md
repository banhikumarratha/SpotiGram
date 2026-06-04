# Service Boundaries & Domain Ownership

This document defines the strict architectural boundaries, domain ownership, and dependencies across the Spotigram microservices.

## 1. Service Ownership Matrix

| Service | Domains Owned | Core Responsibilities |
|---------|---------------|-----------------------|
| **`api-gateway`** | Security, Routing | Routing, auth enforcement, rate limiting, correlation IDs, request aggregation. |
| **`user-service`** | User, Social, Notification | Auth, profiles, social graph (followers), moderation actions, notifications inbox. |
| **`music-service`** | Music | Spotify integration, playback metadata, playlists, search, token refresh. |
| **`recommendation-service`** | Recommendation, Music DNA, Mood | Mood scanning, embeddings, Music DNA calculation, feed generation, similar-user discovery. |
| **`ai-assistant-service`** | AI DJ | AI DJ orchestration, RAG, chat memory, tool calling, AI provider layer (Ollama/Grok/Gemini). |
| **`analytics-service`** | Analytics | Platform reports, dashboards, aggregated insights, Year-in-Review calculations. |

## 2. Database Ownership Matrix
*Rule: Services may not access another service's database directly.*

| Database Name | Tech Stack | Owning Service | Purpose |
|---------------|------------|----------------|---------|
| `user-db` | PostgreSQL | `user-service` | User credentials, profiles, connections (follows/blocks). |
| `music-db` | PostgreSQL | `music-service` | Cached Spotify metadata, playlist mappings, Spotify refresh tokens. |
| `recommendation-db`| ChromaDB | `recommendation-service`| Vector embeddings, Taste vectors, cached feeds. |
| `ai-dj-db` | Redis/PostgreSQL | `ai-assistant-service`| Short-term chat context, LLM memories. |
| `analytics-db`| TSDB (e.g. Timescale) | `analytics-service` | Fast ingestion of play events and mood telemetry. |

## 3. Kafka Topic Ownership Matrix
*Rule: All events must be strongly typed and versioned via contracts.*

| Topic Name | Publisher (Owner) | Subscribers | Schema Example |
|------------|-------------------|-------------|----------------|
| `users.events.v1` | `user-service` | `analytics-service`, `recommendation-service` | `UserCreatedEvent`, `UserFollowedEvent` |
| `music.events.v1` | `music-service` | `analytics-service`, `recommendation-service` | `TrackPlayedEvent`, `SpotifyAccountLinkedEvent` |
| `moods.events.v1` | `recommendation-service` | `analytics-service`, `ai-assistant-service` | `MoodScannedEvent` |
| `ai.events.v1` | `ai-assistant-service`| `analytics-service` | `PlaylistGeneratedByAIEvent` |
| `feed.events.v1` | `recommendation-service`| `analytics-service` | `FeedViewedEvent` |

## 4. API Ownership Matrix
*Rule: All APIs must be versioned.*

| Base Path | Owning Service | Example Endpoints |
|-----------|----------------|-------------------|
| `/api/v1/auth/*` | `user-service` | Login, Registration, Token Exchange |
| `/api/v1/users/*` | `user-service` | Profiles, Follows, Blocks |
| `/api/v1/notifications/*` | `user-service` | Inbox, Read Receipts |
| `/api/v1/music/*` | `music-service` | Search, Playlists, Metadata Fetch |
| `/api/v1/recommendations/*` | `recommendation-service`| Music DNA, Feed Generation |
| `/api/v1/ai/*` | `ai-assistant-service`| Chat requests, Provider Config |
| `/api/v1/analytics/*` | `analytics-service` | Dashboards, Year-in-Review Fetch |

## 5. Module/Package Ownership Matrix
*Applying Hexagonal Architecture internally.*

| Internal Module | Layer Type | Description |
|-----------------|------------|-------------|
| `api/` | Port (Primary) | FastAPI routers, request validation. |
| `domain/` | Core | Core business logic, Entities, Aggregates. Pure python. |
| `application/` | Core | Use cases orchestrating domain entities. |
| `infrastructure/` | Adapter | DB Repositories, Kafka producers/consumers, 3rd party API clients. |

## 6. Dependency Rules Document

1. **Database Isolation**: A service can only query its own database. Data joining must occur in memory (via API requests) or asynchronously (via materialized views built from Kafka events).
2. **Synchronous Communication**: Services communicate synchronously (HTTP/REST) only for real-time reads or immediate feedback loops. The `api-gateway` is the only service allowed to call multiple services and aggregate the response.
3. **Asynchronous Communication**: State changes (writes) that affect other domains must be published as Kafka events.
4. **Contract Dependency**: All services depend on `packages/spotigram-contracts`. Services must never define their own schemas for inter-service communication.
5. **AI Constraints**: `LangChain` and `LangGraph` are strictly isolated to the `ai-assistant-service`. No other service may import these libraries.
