# RAG Diagrams

## RAG Architecture in AI Assistant Service

The AI Assistant Service uses **Retrieval-Augmented Generation (RAG)** to ground LLM responses in the user's actual Music DNA and listening history.

## RAG Pipeline

```mermaid
flowchart TD
    A["User message: 'Play something like what I liked last week'"]
    A --> B["AssistantService.chat()"]
    B --> C["Build UserContext from request"]
    C --> D["RAG Chain"]

    subgraph "RAG Chain (LangChain)"
        D --> E["Retrieval Step"]
        E --> F["Format context string:<br/>genres, artists, mood, recent tracks"]
        F --> G["Prompt Template:<br/>System prompt + user context + conversation history"]
        G --> H["LLM Inference (Ollama/Grok/Gemini)"]
        H --> I["Output Parser (StrOutputParser)"]
    end

    I --> J["AIResponse returned to user"]
```

## Context Sources

```mermaid
flowchart LR
    subgraph "UserContext (passed per-request)"
        A["top_genres"]
        B["top_artists"]
        C["current_mood"]
        D["recent_tracks"]
        E["preferences"]
    end

    subgraph "Conversation Memory"
        F["Last 20 messages"]
    end

    A --> CTX["Context String"]
    B --> CTX
    C --> CTX
    D --> CTX
    E --> CTX
    F --> CTX
    CTX --> PROMPT["Prompt Template"]
    PROMPT --> LLM["LLM"]
```

## RAG in AI DJ Workflow

```mermaid
flowchart TD
    subgraph "LangGraph StateGraph"
        S1["analyze_mood"]
        S2["retrieve_context (RAG)"]
        S3["generate_response"]
        S4["extract_actions"]
        S5["format_output"]
    end

    S1 --> S2
    S2 -->|"UserContext + Music DNA"| S3
    S3 -->|"LLM call"| S4
    S4 -->|"tool calls / playlist"| S5
```

## Key Design Decisions

- **No direct DB calls**: The AI service receives all context via the `UserContext` object in the API request. It never queries PostgreSQL or ChromaDB directly.
- **LangChain Core only**: Uses `langchain_core` (prompts, parsers, runnables), not the full `langchain` package.
- **Provider-agnostic**: The RAG chain works identically regardless of which LLM provider is active.
