# Wireframe Descriptions (Streamlit UI)

## 1. Global Layout
- **Sidebar**: Main navigation menu. Links to Home, Search, AI DJ, Mood Scanner, Analytics, Settings. Displays currently playing track widget at the bottom (via custom JS component).
- **Main Area**: Dynamic content area taking up the rest of the screen.

## 2. Home Feed
- **Layout**: Single central column for posts.
- **Post Structure**: 
  - User header (Avatar, Name, Timestamp).
  - Track Information (Album Art, Title, Artist).
  - Play button overlay (triggers JS playback).
  - Action row (Like, Comment, Voice React, Share).
  - "Options" dropdown (Report, Mute, Block).

## 3. AI DJ Interface
- **Layout**: Two columns.
- **Left Column (Chat)**: Streamlit `st.chat_message` interface for conversational prompts.
- **Right Column (Results)**: Displays the generated playlist with a "Play All" button.
- **Settings Toggle**: Small gear icon allowing users to switch between Ollama, Grok, and Gemini.

## 4. Profile & Music DNA
- **Layout**: Top section for user info and Follow/Following counts.
- **Music DNA**: Rendered as an interactive radar chart using `st.plotly_chart`.
- **Tabs**: `st.tabs` for "Recent Posts", "Top Tracks", "Playlists".
