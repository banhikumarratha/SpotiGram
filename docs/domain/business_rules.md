# Business Rules

## Authentication

| Rule | Implementation |
|---|---|
| Duplicate email registration is rejected | `AuthService.register()` checks `UserAccount.email` uniqueness |
| Passwords are hashed with bcrypt before storage | `passlib.hash.bcrypt.hash()` in `AuthService.register()` |
| Login returns a JWT with 60-minute expiration | `jwt.encode()` with `exp` claim in `AuthService.login()` |
| Invalid credentials return 401 | `AuthService.login()` raises `ValueError("Invalid credentials")` |

## Social Graph

| Rule | Implementation |
|---|---|
| A user cannot follow themselves | `SocialService.follow_user()`: `follower_id == followed_id` → `ValueError` |
| Duplicate follows are rejected | Connection table has `UniqueConstraint("follower_id", "followed_id")` |
| Blocked users cannot be followed | `SocialService.follow_user()` checks `ConnectionStatus.BLOCKED` |
| Connection statuses: ACTIVE, BLOCKED, MUTED | `ConnectionStatus` enum in `user-service/infrastructure/models.py` |

## Mood Detection

| Rule | Implementation |
|---|---|
| Confidence below 0.6 triggers retake prompt | `recommendation-service/api/v1/router.py` returns HTTP 422 |
| Supported moods: happy, sad, energetic, calm, angry, neutral | `Mood` enum in `recommendation-service/domain/models.py` |
| Mood source can be "webcam" or "inferred" | `MoodProfile.source` field, default "webcam" |

## Music DNA

| Rule | Implementation |
|---|---|
| Cold start threshold is 10 interactions | `MusicDNA.COLD_START_THRESHOLD = 10` |
| DNA is updated on every play, skip, like, save, share | Kafka consumer processes `MusicInteractionEvent` via `DNAService.process_interaction()` |
| Cold start users get generic genre-based recommendations | `RecommendationFeed.is_cold_start` flag controls fallback logic |
| Interaction types: play, skip, like, save, share | `InteractionType` enum in domain models |

## Recommendations

| Rule | Implementation |
|---|---|
| Feed is limited to 20 results by default | `limit=20` parameter on `/feed` endpoint |
| Recommendations include explanation text | `Recommendation.explanation` field |
| Recommendations include signal breakdowns | `Recommendation.signals` dictionary |
| Similar users are found via cosine similarity in ChromaDB | `ChromaVectorStore` query in `RecommendationService` |

## AI Assistant

| Rule | Implementation |
|---|---|
| LangChain/LangGraph only in ai-assistant-service | Architecture fitness test enforces at CI time |
| Provider fallback order: Ollama → Grok → Gemini | `ProviderRegistry.get_provider()` |
| Conversation memory limited to last 20 messages | `Conversation.history_text()` slices `[-20:]` |
| DJ sessions have states: idle, playing, transitioning, paused | `DJSession.state` field |

## Analytics

| Rule | Implementation |
|---|---|
| Daily stats are materialized aggregates | `DailyUserStats` model in analytics-service |
| Year in Review requires explicit year parameter | `GET /year-in-review?year=` is a required query param |

## Infrastructure

| Rule | Implementation |
|---|---|
| Rate limit: 100 requests per 60 seconds | `RateLimiter(times=100, seconds=60)` in API Gateway |
| Kafka failures route to DLQ | `DLQKafkaConsumer` in `spotigram-shared` |
| Idempotent requests cached for 24 hours | `IdempotencyMiddleware.ttl = 86400` |
