# Product Specification

## Vision

Spotigram is **Instagram for Music Lovers** — a social music discovery platform where your taste, mood, and musical DNA drive every interaction.

## Target Users

- Music enthusiasts who want personalized discovery beyond Spotify's built-in algorithms
- Social listeners who share playlists and follow friends' musical journeys
- AI-curious users who want an intelligent DJ that understands their mood and taste

## Core Features

### 1. Identity & Social Graph
- User registration and authentication (JWT-based)
- Profile management with display name, bio, avatar
- Follow/Unfollow, Block, Mute, Report user flows
- Privacy controls (PUBLIC/PRIVATE profiles)

### 2. Spotify Integration
- Spotify OAuth for connecting user accounts
- Music search (tracks, artists, albums)
- In-browser playback via Spotify Web Playback SDK (Premium only)
- Playlist import from Spotify
- Playlist creation and track saving
- Automatic token refresh handling

### 3. Mood Detection
- Webcam-based emotion detection via DeepFace
- Supported moods: Happy, Sad, Energetic, Calm, Angry, Neutral
- Confidence threshold (≥ 0.6 required, otherwise prompts retake)
- Manual mood correction
- Full mood history timeline

### 4. Music DNA
- A vector embedding representing a user's musical fingerprint
- Built from: genre affinities, artist preferences, mood distribution, interaction signals
- Updates with every play, like, save, skip, and share
- Cold start detection (< 10 interactions → generic recommendations)
- Historical DNA snapshots for taste evolution comparison

### 5. Recommendation Engine
- Personalized feed powered by Music DNA similarity search (ChromaDB)
- Mood-filtered recommendations
- Ranked by composite score: DNA similarity × mood alignment × social signals
- Each recommendation includes a human-readable explanation
- Similar user discovery via DNA vector proximity

### 6. AI DJ
- Conversational AI assistant powered by LangGraph state machine
- Multi-provider: Ollama (default), Grok, Gemini
- RAG retrieval from user's Music DNA and listening history
- Tool calling for real-time Spotify search integration
- Themed playlist generation from natural language prompts
- Persistent conversation memory per session

### 7. Analytics Dashboard
- Listening statistics (plays, skips, completion rate)
- Mood trend analysis over time
- Music personality profiling (derived traits)
- Year in Review / Spotigram Wrapped

### 8. Web UI
- Multi-page Streamlit application
- 8 pages: Home, Discover, Mood Scanner, Recommendations, AI DJ, Profile, Analytics, Settings
- Dark theme with premium music platform aesthetics
- Real-time AI DJ chat interface

## Non-Functional Requirements

- **Performance**: < 200ms p95 latency for feed and search APIs
- **Scale**: Support 100 concurrent users (validated via Locust)
- **Reliability**: Circuit breakers, retries, DLQ for Kafka, MusicBrainz/Last.fm fallbacks
- **Observability**: Prometheus metrics, Grafana dashboards, structured logging, OpenTelemetry tracing
- **Security**: bcrypt password hashing, JWT with configurable secrets, rate limiting (100 req/min)
