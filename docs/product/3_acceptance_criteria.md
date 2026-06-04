# Acceptance Criteria

## Authentication & Spotify Integration
### US1.2: Spotify OAuth & Premium Check
- **Given** I am on the onboarding screen
- **When** I authenticate with Spotify
- **Then** the system checks if my account is Premium
- **And** if not Premium, displays a warning that full playback is unsupported.
- **And** the system securely stores the refresh token for background renewal.

## Playback (Streamlit & JS)
### US2.3: Seamless Playback
- **Given** I am browsing the Feed in Streamlit
- **When** I click "Play" on a track
- **Then** the injected JavaScript utilizes the Spotify Web Playback SDK
- **And** the track plays directly in the browser without opening the Spotify app.

## AI DJ & Fallbacks
### US2.2: AI DJ (Ollama Default)
- **Given** I am in the AI DJ tab
- **When** I submit a prompt and haven't overridden the AI settings
- **Then** the backend routes the prompt to the local Ollama instance
- **And** returns a generated playlist and DJ commentary.

## Moderation
### US2.4: Basic Moderation
- **Given** I am viewing a post from another user
- **When** I click the "Options" menu
- **Then** I see options to "Mute", "Block", and "Report"
- **And** selecting "Block" instantly hides all their content from my Feed and prevents them from interacting with me.
