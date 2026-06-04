# Success Metrics (KPIs)

## 1. Target Scale (100K+ Users)
- **Infrastructure Load**: API response times remain < 300ms at 10,000 concurrent users.
- **Streamlit Concurrency**: Ensuring the Streamlit server does not bottleneck under heavy user load (monitoring websocket connections).

## 2. Activation & Auth
- **Auth Success Rate**: % of users successfully linking Spotify and maintaining active refresh tokens.
- **Premium Ratio**: % of users with Spotify Premium (critical for the core value proposition of in-app playback).

## 3. Feature Usage
- **AI DJ Engagement**: Number of prompts sent to Ollama vs. Cloud providers (Grok/Gemini).
- **Recommendation Quality**: "Play-through rate" of tracks recommended in the Balanced feed (listening past the 30-second mark).

## 4. Moderation Health
- **Report Rate**: Number of reports per 1,000 active users (monitoring community health).
- **Block/Mute Usage**: Identifying if specific users or clusters are highly disruptive.
