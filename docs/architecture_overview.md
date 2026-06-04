# SpotiGram Architecture Overview

SpotiGram is built using a modern, event-driven, Hexagonal Architecture pattern.

## 1. System Context (C4 Model)

```mermaid
graph TD
    User([User]) --> |Visits| UI[Streamlit Frontend]
    UI --> |REST API| UserSvc[User Service]
    UI --> |REST API| SocialSvc[Social Service]
    UI --> |REST API| AISvc[AI Assistant Service]
    UI --> |REST API| EmotionSvc[Emotion Service]
    
    SocialSvc --> |Async Events| Kafka[Kafka Event Bus]
    UserSvc --> |Async Events| Kafka
    
    AISvc --> |Query| Chroma[(ChromaDB)]
    AISvc --> |Query| MusicSvc[Music Service Proxy]
    
    UserSvc --> DB[(PostgreSQL)]
    SocialSvc --> DB
```

## 2. Entity Relationship Diagram (ERD)

```mermaid
erDiagram
    USERS {
        string id PK
        string username UK
        string display_name
        datetime created_at
    }
    
    POSTS {
        string id PK
        string user_id FK
        json track
        string caption
        string mood
        datetime created_at
    }
    
    USERS ||--o{ POSTS : creates
```

## 3. Event-Driven Architecture (Kafka Flow)

We employ the **Outbox Pattern** to ensure reliable message delivery without distributed transactions.

```mermaid
sequenceDiagram
    participant API as FastAPI Route
    participant DB as Postgres (Outbox Table)
    participant Worker as Outbox Publisher
    participant Kafka as Kafka Topic

    API->>DB: 1. Save Post & Save Event (Same TX)
    DB-->>API: 2. Commit Success
    loop Every 2 Seconds
        Worker->>DB: 3. Poll FOR UPDATE SKIP LOCKED
        DB-->>Worker: 4. Pending Events
        Worker->>Kafka: 5. Publish to Topic
        Worker->>DB: 6. Mark Processed
    end
```

## 4. AI Subsystem (RAG & Music DNA)

The `ai-assistant-service` acts as the orchestrator using LangGraph.

```mermaid
graph LR
    User([User Prompt]) --> LangGraph[LangGraph State Machine]
    LangGraph --> |Tool| SocialAPI[Social Service API]
    LangGraph --> |Tool| MusicAPI[Music Service API]
    LangGraph --> |Embed| EmbedSvc[Embedding Service]
    EmbedSvc --> |Query| Chroma[(ChromaDB)]
    LangGraph --> |LLM Request| Ollama[Ollama Provider]
    Ollama --> LangGraph
    LangGraph --> Final[AI Recommendation]
```
