# Interview Talking Points

When presenting SpotiGram in an engineering interview, focus on these technical achievements and architectural patterns:

## 1. Resilience Engineering
- **Circuit Breakers & Retries:** Discuss how you used `tenacity` to wrap inter-service HTTP calls. Mention how preventing cascading failures is critical in microservices.
- **Rate Limiting:** Explain the sliding window Redis implementation in the FastAPI middleware to protect endpoints from abuse.
- **Idempotency:** Talk about the `Idempotency-Key` header and how Redis is used to ensure POST requests (like creating a user or post) aren't processed twice during network retries.

## 2. Event-Driven Architecture (EDA)
- **The Outbox Pattern:** This is a major talking point. Explain *why* it's needed (Dual Write problem). You write the domain data and the event payload in a single Postgres transaction. A background worker (`FOR UPDATE SKIP LOCKED`) polls and publishes to Kafka. This guarantees at-least-once delivery.
- **Kafka Dead Letter Queues (DLQ):** Mention how unprocessable messages are shunted to a DLQ topic to unblock the partition.

## 3. AI & LangGraph Orchestration
- **Agentic Workflows:** Explain how the `ai-assistant-service` acts as an agent using LangGraph. It manages state (`DJState`) and routes between tools (fetching user history from another service) and the LLM generation node.
- **Graceful Fallbacks:** Discuss the `ai_provider.py` implementation where, if the local Ollama instance crashes or times out, the service falls back to a `MockLLM` to maintain high availability for the UI.
- **Decoupled AI:** Mention ADR 002—restricting LangChain to one service and creating lightweight APIs for embeddings and emotions to prevent dependency bloat.

## 4. Observability
- Emphasize that the system isn't just code; it's observable. Mention the OpenTelemetry hooks, Jaeger tracing, and the Prometheus alerts (High Error Rate, High Latency) defined for Kubernetes.
