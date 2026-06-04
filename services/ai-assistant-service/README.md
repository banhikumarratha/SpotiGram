# AI Assistant Service

The `ai-assistant-service` powers all generative AI features in Spotigram. It serves as an abstraction layer between our internal services and various LLM providers, ensuring no other service needs to communicate with an LLM directly.

## Features

- **Multi-Provider Architecture**: Supports `ollama` (default local), `grok`, and `gemini` via the `AI_PROVIDER` environment variable.
- **AI DJ**: LangGraph-powered state machine that guides users through a musical journey based on their mood and listening history.
- **RAG + Contextual Chat**: LangChain-powered conversational memory augmented with the user's Music DNA and listening history.
- **Playlist Generation**: Translates natural language requests (e.g., "Late night coding vibes") into structured playlists with specific track queries.
- **Explainable Recommendations**: Generates human-readable reasoning explaining why specific tracks were recommended based on ranking signals.

## Architecture & Constraints

- **LangChain/LangGraph Sandbox**: This is the *only* service permitted to import or use LangChain and LangGraph.
- **Data Boundaries**: This service does *not* read from the recommendation database. All contextual data (Music DNA, history) must be provided in the request payload by the client/gateway.
- **Provider Fallback**: If `grok` or `gemini` are configured but fail, the service automatically falls back to `ollama`.
- **Pure Domain**: The domain logic uses plain Python dataclasses and interfaces (`AIProviderPort`, `MemoryStorePort`). It does not depend on any LangChain models.

## Endpoints

| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/ai/chat` | Single-turn chat with conversation memory |
| POST | `/api/v1/ai/stream` | Streaming token-by-token chat via SSE |
| POST | `/api/v1/ai/dj` | AI DJ session management and track suggestions |
| POST | `/api/v1/ai/playlist` | Generate a themed playlist from natural language |
| POST | `/api/v1/ai/explain` | Explain why a track was recommended |

## Running Locally

1. Install dependencies: `uv pip install -r requirements.txt`
2. Start an Ollama server locally on `localhost:11434` with `llama3.2` installed (`ollama run llama3.2`).
3. Run the service: `uvicorn main:app --reload`
