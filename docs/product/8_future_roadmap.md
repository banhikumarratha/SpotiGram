# Future Roadmap & Architecture Migration

## Phase 1: Streamlit MVP (Current)
- Complete functionality built in Streamlit.
- Backend logic heavily modularized into API-ready services (FastAPI/Flask-like structure under the hood).
- Focus on achieving the 100K+ user scale with this setup.
- Local Ollama AI, Spotify Web Playback SDK JS injection.

## Phase 2: Headless Architecture & Web App
- Decouple the Streamlit frontend completely.
- Expose all core functions (Feed, Auth, AI DJ) via a robust REST/GraphQL API.
- Build a dedicated, highly responsive Web Application (e.g., React, Next.js, or Vite).
- Move JS playback logic natively into the new frontend framework.

## Phase 3: Advanced Monetization
- **Spotigram Plus**: Premium subscription tiers offering advanced profile customizations.
- **Premium Analytics**: Deep-dive data visualization for power users.
- **Cloud AI Upgrades**: Charging power users for unlimited Grok/Gemini AI DJ usage.
- **Creator Accounts**: Specialized tools for artists to interact with their top listeners on the platform.

## Phase 4: Mobile Native Apps
- React Native or Flutter apps consuming the same decoupled API.
- Enhanced on-device ML for faster Mood Scanning.
- Native push notifications.
