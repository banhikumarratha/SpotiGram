# Spotigram: Product Requirement Document (PRD)

## 1. Product Vision & Scope
**Instagram for Music Lovers.**
Spotigram is a social platform where users share music instead of photos. It combines the catalog of Spotify, the visual social network of Instagram, the algorithmic addiction of TikTok, and the hyper-personalized recommendation systems of Netflix.
**Target Scale:** Startup-ready showcase designed to support 100K+ users.

## 2. Technical Philosophy & Constraints
- **Frontend:** Streamlit for the current iteration (rapid MVP). The backend must be designed as API-ready to support a future dedicated web application (e.g., React/Next.js).
- **Authentication:** Email/password combinations alongside Spotify OAuth. System must auto-refresh Spotify tokens when expired.
- **Music Playback:** Restricted to Spotify Premium users only. Integration utilizes the Spotify Web Playback SDK and Spotify Web API Player Endpoints, with JavaScript handling the playback integration within the Streamlit frontend.
- **Music Metadata:** Spotify serves as the primary source of truth. MusicBrainz and Last.fm serve as fallback sources when Spotify metadata is insufficient or missing.
- **AI Providers:** Ollama (local) is the default provider for privacy and cost control. Grok and Gemini are supported as optional cloud providers.
- **Recommendation Philosophy:** Balanced approach (mixing discovery of new tracks with familiar favorites).
- **Moderation:** Basic community tools including Report, Block, and Mute functionalities.

## 3. Core Features
- **User Profiles**: Displays Music DNA, top artists/tracks, recent mood scans, and pinned "Music Stories".
- **Followers/Following**: Standard asymmetric follower model.
- **Likes/Comments**: Users can like and comment on shared songs or playlists.
- **Shares/Reposts**: Share tracks to other users via DM. Repost a friend's shared track to your own feed.
- **Playlists**: Collaborative and personal playlists integrated directly with Spotify.
- **Music Stories**: 24-hour ephemeral posts featuring a song snippet.
- **Voice Reactions**: Users can record short audio reactions to songs their friends share.
- **Friend Activity**: Real-time ticker showing what friends are currently listening to.
- **Search**: Unified search for Users, Tracks, Artists, Playlists, and Moods.
- **Analytics**: Personal listening stats visible to the user.

## 4. Specific Behaviors
- **Mood Scanner**: Analyzes webcam input in Streamlit. Maps detected emotion to predefined moods and generates dynamic playlists via AI.
- **Music DNA**: Analyzes historical Spotify listening data to create a unique taste profile. Used to calculate taste overlap between users.
- **Recommendation Engine (Balanced)**: Leverages Spotify data, friend activity, and Music DNA. Balances familiar favorites with serendipitous discovery.
- **AI DJ**: Conversational interface powered by Ollama (or Gemini/Grok). Generates playlists based on text prompts and provides DJ-style commentary.
- **Spotify Integration**: Deep bidirectional sync. Requires Premium for playback. Fallbacks to MusicBrainz/Last.fm for extended metadata.
- **Social Discovery**: Surface "Music Soulmates" (users with high DNA overlap) and trending genres.
- **Feed**: Algorithmic blend of friend posts, recommendations, and trending content.
- **Monetization (Future-Ready)**: Architecture designed to support Premium plans, Advanced AI DJ (cloud LLMs), Premium Analytics, and Creator Accounts in future phases.
