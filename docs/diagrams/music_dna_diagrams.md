# Music DNA Diagrams

## What Is Music DNA?

Music DNA is a vector embedding that represents a user's unique musical fingerprint, built from their listening history, genre affinities, mood distribution, and interaction signals.

## Music DNA Data Model

```mermaid
classDiagram
    class MusicDNA {
        +str user_id
        +List~float~ embedding
        +List~str~ top_genres
        +List~str~ top_artists
        +Dict~str,float~ mood_distribution
        +int total_interactions
        +datetime last_updated
        +bool is_cold_start
        +int COLD_START_THRESHOLD = 10
    }

    class MusicInteractionEvent {
        +str user_id
        +str track_id
        +InteractionType action
        +datetime timestamp
        +str track_title
        +str track_artist
        +List~str~ track_genres
    }

    class InteractionType {
        <<enumeration>>
        PLAY
        SKIP
        LIKE
        SAVE
        SHARE
    }

    MusicInteractionEvent --> InteractionType
    MusicInteractionEvent ..> MusicDNA : updates
```

## DNA Update Pipeline

```mermaid
flowchart TD
    A["User plays/likes/skips a track"] --> B["Music Service emits music.events.v1"]
    B --> C["Kafka delivers to Recommendation Service"]
    C --> D["DNAService.process_interaction()"]
    D --> E{"total_interactions >= 10?"}
    E -->|No| F["is_cold_start = true<br/>Use generic recs"]
    E -->|Yes| G["is_cold_start = false"]
    G --> H["Update genre weights"]
    H --> I["Update artist weights"]
    I --> J["Update mood distribution"]
    J --> K["Generate new embedding via SentenceTransformer"]
    K --> L["Upsert into ChromaDB"]
    L --> M["DNA ready for similarity queries"]
```

## DNA Similarity Search

```mermaid
flowchart LR
    A["User A's DNA embedding"] --> B["ChromaDB cosine similarity query"]
    B --> C["Top N similar embeddings"]
    C --> D["Similar Users"]
    C --> E["Track Recommendations"]
```

## DNA Cold Start Strategy

| Phase | Interactions | Strategy |
|---|---|---|
| **Cold Start** | 0–9 | Generic genre-based recommendations, trending tracks |
| **Warm** | 10–50 | DNA-driven recs with high exploration factor |
| **Mature** | 50+ | Full DNA similarity, mood-filtered, socially-aware |
