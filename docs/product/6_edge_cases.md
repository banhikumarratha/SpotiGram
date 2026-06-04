# Edge Cases & Error Handling

## 1. Playback & Spotify Integration
- **Non-Premium Account**: If a user connects a Spotify Free account, disable the JS Web Playback SDK integration. Display a warning: "Spotify Premium is required for in-app playback." and provide external links to Spotify.
- **Expired Refresh Token**: If the refresh token is revoked by the user on Spotify's end, force a logout on Spotigram and prompt re-authentication.

## 2. AI & Infrastructure
- **Ollama Down/Slow**: If the local Ollama instance fails or times out, seamlessly fallback to Gemini/Grok (if API keys are configured), or return a predefined error message: "The AI DJ is currently rebooting its local brain."
- **Streamlit Session State Loss**: On browser refresh, utilize browser cookies or local storage via JS to re-authenticate the user without forcing them to log in again.

## 3. Metadata
- **Missing Metadata Across All Sources**: If a track exists on Spotify but lacks detailed metadata on MusicBrainz and Last.fm, gracefully hide the extended info sections in the UI rather than displaying "Unknown".

## 4. Moderation
- **Blocking a Blocked User**: Prevent infinite loops or UI crashes if a user tries to interact with a cached post from a user they just blocked.
