# ADR-004: ChromaDB for Music DNA Vector Search

**Date**: 2025-03-01
**Status**: Accepted

## Context
The recommendation engine needs to find tracks and users with similar musical fingerprints (Music DNA). This requires vector similarity search over high-dimensional embeddings.

## Decision
Use ChromaDB as the vector database for the recommendation-service. Music DNA embeddings are stored as collections in ChromaDB and queried via cosine similarity.

## Consequences
- Efficient nearest-neighbor search for recommendations
- ChromaDB supports both ephemeral (testing) and persistent (production) modes
- Embeddings are generated via SentenceTransformer models locally
- Only the recommendation-service accesses ChromaDB — other services receive recommendations via the REST API
