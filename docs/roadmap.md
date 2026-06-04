# SpotiGram Roadmaps

## MVP Roadmap (v1.0.0 - Current)
- [x] Basic User Profiles and Authentication stubs.
- [x] Social Feed with Moods and Captions.
- [x] AI DJ Chatbot with mock track recommendations.
- [x] Mood Scanner using NLP text heuristics.
- [x] Event-driven Outbox pattern for publishing.
- [x] Resilient HTTP clients (Retries/Circuit Breakers).
- [x] Docker Compose deployment stack.

## Production Roadmap (v2.0.0+)
- [ ] **OAuth2 Integration:** Real Spotify authentication and token refresh handling.
- [ ] **Managed Infrastructure:** Migrate local Kafka and Postgres to managed cloud services (e.g., AWS MSK, RDS).
- [ ] **Database Sharding:** Shard the `social-service` Postgres database by `user_id` to handle high read/write feed volume.
- [ ] **Advanced RAG:** Move from `SentenceTransformers` to a more robust embedding model hosted on a dedicated GPU node.
- [ ] **Real-time Notifications:** Implement WebSockets for real-time post likes and follows.
