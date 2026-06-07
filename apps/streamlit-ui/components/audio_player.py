"""
Sidebar Now Playing panel with a small embedded YouTube player.
Renders directly inside the Streamlit sidebar to keep page content clean
and provide full native controls for play, pause, seek, and volume.
"""
import streamlit as st
import re


def _extract_video_id(url: str) -> str | None:
    """Pull the 11-char YouTube video ID out of any YouTube URL."""
    if not url:
        return None
    match = re.search(r"(?:v=|/embed/|youtu\.be/)([A-Za-z0-9_-]{11})", url)
    return match.group(1) if match else None


def render_audio_player():
    track = st.session_state.get("currently_playing")
    if not track:
        return

    # ── Resolve video_id ─────────────────────────────────────────────────────
    video_id = _extract_video_id(track.get("preview_url", ""))

    # If the track came from cold-start seeds or genre labels, search YouTube
    if not video_id:
        raw_id = track.get("id", "")
        if raw_id and len(raw_id) == 11 and not raw_id.startswith("cold_start") and not raw_id.startswith("mock"):
            video_id = raw_id
        else:
            title  = track.get("title", "")
            artist = track.get("artist", "")
            genre  = raw_id.replace("cold_start_", "") if raw_id.startswith("cold_start_") else ""
            q = f"{title} {artist}".strip() or f"top {genre} music"
            try:
                from api.music_api import MusicAPI
                res = MusicAPI().search(q)
                if res.status_code == 200:
                    items = res.json().get("tracks", {}).get("items", [])
                    if items:
                        video_id = items[0]["id"]
                        track = {**track,
                                 "id": video_id,
                                 "preview_url": f"https://www.youtube.com/watch?v={video_id}",
                                 "title": items[0].get("name", title),
                                 "artist": ", ".join(a["name"] for a in items[0].get("artists", [])) or artist}
                        st.session_state["currently_playing"] = track
            except Exception:
                pass

    title  = track.get("title", "Unknown Track")
    artist = track.get("artist", "Unknown Artist")

    # ── Sidebar Styling ───────────────────────────────────────────────────────
    st.markdown("""
    <style>
    .sidebar-player-card {
        background: linear-gradient(135deg, #0d0d1e 0%, #15152c 100%);
        border: 1px solid #2a2a4e;
        border-radius: 12px;
        padding: 12px;
        margin-top: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    .sidebar-player-header {
        font-size: 0.8rem;
        font-weight: 700;
        color: #ff4444;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .sidebar-player-title {
        font-size: 0.9rem;
        font-weight: 700;
        color: #ffffff;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        margin-top: 8px;
    }
    .sidebar-player-artist {
        font-size: 0.75rem;
        color: #a0a0c0;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        margin-bottom: 10px;
    }
    .sidebar-player-container {
        width: 100%;
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid #2a2a4e;
        background: #000;
    }
    </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.divider()
        st.markdown(f"""
        <div class="sidebar-player-card">
            <div class="sidebar-player-header">🔴 Now Playing</div>
            <div class="sidebar-player-container">
                <!-- vq=small forces a lower video quality (240p/144p) to save data -->
                <!-- rel=0, modestbranding=1, and controls=1 display complete control options -->
                <iframe 
                    width="100%" 
                    height="140" 
                    src="https://www.youtube.com/embed/{video_id}?autoplay=1&vq=small&controls=1&rel=0&modestbranding=1" 
                    frameborder="0" 
                    allow="autoplay; encrypted-media" 
                    allowfullscreen>
                </iframe>
            </div>
            <div class="sidebar-player-title" title="{title}">{title}</div>
            <div class="sidebar-player-artist">{artist}</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("⏹ Stop Playback", key="stop_sidebar_player", use_container_width=True):
            st.session_state["currently_playing"] = None
            st.rerun()
