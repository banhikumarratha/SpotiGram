import streamlit as st
from components.navigation import render_sidebar
from api.mood_api import MoodAPI
from utils.state import is_authenticated

st.set_page_config(page_title="Recommendations - Spotigram", page_icon="🎧")

if not is_authenticated():
    st.switch_page("app.py")

render_sidebar()

# ─────────────────────────────────────────────────────────────────────────────
# Styles
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .rec-hero {
        background: linear-gradient(135deg, #1DB954 0%, #1ed760 40%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.4rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 0;
    }
    .rec-sub {
        color: #8888a8;
        font-size: 1rem;
        margin-top: 0.3rem;
        margin-bottom: 1.5rem;
    }

    /* Track card */
    div[data-testid="stHorizontalBlock"]:has(.track-rank) {
        background: linear-gradient(145deg, #12122a, #1a1a35);
        border: 1px solid #252545;
        border-radius: 14px;
        padding: 0.8rem 1.2rem;
        margin-bottom: 0.7rem;
        align-items: center !important;
        transition: border-color 0.2s ease, transform 0.2s ease;
        animation: fadeInUp 0.4s ease forwards;
    }
    div[data-testid="stHorizontalBlock"]:has(.track-rank):hover {
        border-color: rgba(29,185,84,0.4);
        transform: translateX(4px);
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(10px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .track-rank {
        font-size: 1.1rem;
        font-weight: 800;
        color: #3a3a5a;
        min-width: 28px;
        text-align: center;
    }
    .track-art {
        width: 110px;
        height: 110px;
        border-radius: 8px;
        background: linear-gradient(135deg, #1DB954, #a78bfa);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.8rem;
        flex-shrink: 0;
    }
    .track-info { flex: 1; min-width: 0; }
    .track-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: #e0e0f5;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .track-artist {
        font-size: 0.8rem;
        color: #7070a0;
        margin-top: 1px;
    }
    .track-explanation {
        font-size: 0.75rem;
        color: #5555a0;
        margin-top: 3px;
        font-style: italic;
    }
    .track-score {
        font-size: 0.8rem;
        font-weight: 600;
        color: #1DB954;
        flex-shrink: 0;
    }

    /* Mood pill selector */
    .stSelectbox > div > div {
        background: #12122a !important;
        border: 1px solid #252545 !important;
        border-radius: 10px !important;
        color: #e0e0f5 !important;
    }

    /* Primary button */
    [data-testid="stBaseButton-primary"] {
        background: linear-gradient(135deg, #1DB954, #a78bfa) !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 20px rgba(29,185,84,0.3) !important;
        transition: opacity 0.2s ease, transform 0.2s ease !important;
    }
    [data-testid="stBaseButton-primary"]:hover {
        opacity: 0.9 !important;
        transform: translateY(-1px) !important;
    }

    /* Cold-start notice */
    .cold-notice {
        background: rgba(167,139,250,0.08);
        border: 1px solid rgba(167,139,250,0.2);
        border-radius: 10px;
        padding: 0.7rem 1rem;
        color: #a78bfa;
        font-size: 0.85rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<p class="rec-hero">🎧 Recommendations</p>', unsafe_allow_html=True)
st.markdown('<p class="rec-sub">Your personalised playlist, curated by your mood.</p>', unsafe_allow_html=True)

# ── Valid moods (must match recommendation-service Mood enum) ─────────────────
VALID_MOODS = ["happy", "energetic", "calm", "sad", "angry", "neutral"]

MOOD_EMOJI = {
    "happy": "😄", "energetic": "⚡", "calm": "😌",
    "sad": "😢", "angry": "😠", "neutral": "😐",
}

GENRE_EMOJI = {
    "pop": "🎵", "indie": "🎸", "electronic": "💿", "hip-hop": "🎤",
    "rock": "🤘", "jazz": "🎷", "classical": "🎻", "r&b": "🎙️",
}

# Pre-select the mood detected by the Mood Scanner if available
detected = st.session_state.get("current_mood", "happy")
# Map detected mood to a valid enum value (e.g. "joyful" → "happy")
_mood_map = {
    "joy": "happy", "joyful": "happy", "excited": "energetic",
    "relaxed": "calm", "peaceful": "calm", "tired": "calm",
    "sadness": "sad", "anger": "angry", "fear": "calm",
    "surprised": "neutral", "melancholy": "sad", "romantic": "happy",
}
default_mood = _mood_map.get(detected.lower(), detected.lower())
if default_mood not in VALID_MOODS:
    default_mood = "happy"

# ── Controls ──────────────────────────────────────────────────────────────────
col_mood, col_btn = st.columns([3, 1])

with col_mood:
    mood_labels = [f"{MOOD_EMOJI.get(m, '🎭')} {m.capitalize()}" for m in VALID_MOODS]
    default_idx = VALID_MOODS.index(default_mood)
    mood_choice = st.selectbox(
        "Select your mood",
        options=mood_labels,
        index=default_idx,
        label_visibility="collapsed",
    )
    selected_mood = VALID_MOODS[mood_labels.index(mood_choice)]

with col_btn:
    generate = st.button("✨ Generate Playlist", type="primary", use_container_width=True)

# ── Fetch & Display ───────────────────────────────────────────────────────────
auto_generate = ("recs_playlist_data" not in st.session_state and "current_mood" in st.session_state)

if generate or auto_generate:
    api = MoodAPI()
    try:
        fetch_mood = selected_mood if generate else default_mood
        with st.spinner(f"Curating your {fetch_mood} playlist…"):
            res = api.get_feed(mood=fetch_mood, limit=20)

        if res.status_code == 200:
            st.session_state["recs_playlist_data"] = res.json()
            st.session_state["recs_playlist_mood"] = fetch_mood
            st.rerun()
        else:
            st.error(f"Failed to get recommendations: {res.status_code} — {res.text}")
    except Exception as exc:
        st.error(f"Connection failed: {exc}")

if "recs_playlist_data" in st.session_state:
    data = st.session_state["recs_playlist_data"]
    recs_mood = st.session_state["recs_playlist_mood"]
    recs = data.get("recommendations", [])
    is_cold = data.get("is_cold_start", False)

    if is_cold:
        st.markdown("""
        <div class="cold-notice">
            ✨ You're new here! We're showing popular tracks to get you started.
            Like and play tracks to personalise your feed.
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"### {MOOD_EMOJI.get(recs_mood, '🎭')} {recs_mood.capitalize()} Playlist")
    st.markdown(f"**{len(recs)} tracks** • {data.get('generated_at', '')[:10]}")
    st.markdown("---")

    if recs:
        for i, track in enumerate(recs, 1):
            title = track.get("title", "Unknown Track")
            artist = track.get("artist", "Unknown Artist")
            score = track.get("score", 0)
            explanation = track.get("explanation", "")

            # pick emoji from genre hint in track_id
            track_id = track.get("track_id", "")
            art = next(
                (v for k, v in GENRE_EMOJI.items() if k in track_id.lower()),
                "🎵"
            )

            current_playing = st.session_state.get("currently_playing") or {}
            is_playing = (current_playing.get("title") == title and current_playing.get("artist") == artist)

            # Consistent columns in both states
            col_lead, col_body, col_actions = st.columns([2.0, 3.5, 1.8])
            idx = i - 1
            is_paused = st.session_state.get("is_paused", False)
            
            with col_lead:
                if is_playing and current_playing.get("id"):
                    video_id = current_playing.get("id")
                    # Render custom interactive JS seeker player box directly in lead column
                    player_html = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <style>
                            body {{
                                margin: 0; padding: 0; background: #000; overflow: hidden;
                                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                            }}
                            #ytplayer-container {{
                                width: 100%; height: 82px; background: #000;
                            }}
                            .ctrl-bar {{
                                background: #111; padding: 4px 8px; display: flex; align-items: center; gap: 8px;
                                height: 24px; border-top: 1px solid #ff444433;
                            }}
                            .prog-slider {{
                                flex: 1; -webkit-appearance: none; height: 3px; background: #222; border-radius: 2px; outline: none;
                            }}
                            .prog-slider::-webkit-slider-thumb {{
                                -webkit-appearance: none; width: 8px; height: 8px; border-radius: 50%; background: #ff4444; cursor: pointer;
                            }}
                            .time-text {{
                                font-size: 0.65rem; color: #ff8888; font-family: monospace;
                            }}
                        </style>
                    </head>
                    <body>
                        <div id="ytplayer-container">
                            <div id="ytplayer"></div>
                        </div>
                        <div class="ctrl-bar">
                            <span class="time-text" id="time-curr">0:00</span>
                            <input type="range" class="prog-slider" id="seekBar" value="0" min="0" max="100">
                            <span class="time-text" id="time-dur">0:00</span>
                        </div>
                        <script src="https://www.youtube.com/iframe_api"></script>
                        <script>
                            var player;
                            var seekBar = document.getElementById('seekBar');
                            var timeCurr = document.getElementById('time-curr');
                            var timeDur = document.getElementById('time-dur');

                            function onYouTubeIframeAPIReady() {{
                                player = new YT.Player('ytplayer', {{
                                    height: '100%',
                                    width: '100%',
                                    videoId: '{video_id}',
                                    playerVars: {{
                                        'autoplay': 1,
                                        'vq': 'small',
                                        'controls': 1,
                                        'rel': 0,
                                        'modestbranding': 1
                                    }},
                                    events: {{
                                        'onReady': onPlayerReady
                                    }}
                                }});
                            }}

                            function onPlayerReady(event) {{
                                setInterval(updateProgress, 500);
                            }}

                            function formatTime(secs) {{
                                var m = Math.floor(secs / 60);
                                var s = Math.floor(secs % 60);
                                return m + ":" + (s < 10 ? "0" : "") + s;
                            }}

                            function updateProgress() {{
                                if (player && player.getDuration) {{
                                    var dur = player.getDuration();
                                    var curr = player.getCurrentTime();
                                    seekBar.max = dur;
                                    seekBar.value = curr;
                                    timeCurr.innerText = formatTime(curr);
                                    timeDur.innerText = formatTime(dur);
                                }}
                            }}

                            seekBar.addEventListener('input', function() {{
                                if (player && player.seekTo) {{
                                    player.seekTo(seekBar.value);
                                }}
                            }});
                        </script>
                    </body>
                    </html>
                    """
                    col_lead_rank, col_lead_player = st.columns([1, 4])
                    with col_lead_rank:
                        st.markdown(f"<div class='track-rank' style='margin-top: 35px;'>{i}</div>", unsafe_allow_html=True)
                    with col_lead_player:
                        st.components.v1.html(player_html, height=110)
                else:
                    html_lead = (
                        f'<div style="display:flex; align-items:center; gap:0.8rem; margin-top:10px;">'
                        f'<div class="track-rank">{i}</div>'
                        f'<div class="track-art">{art}</div>'
                        f'</div>'
                    )
                    st.markdown(html_lead, unsafe_allow_html=True)

            with col_body:
                st.markdown(f"**{title}**")
                st.markdown(f"<span style='color:#7070a0; font-size:0.85rem;'>🎵 {artist}</span>", unsafe_allow_html=True)
                if explanation:
                    st.markdown(f"<span style='color:#5555a0; font-style:italic; font-size:0.75rem;'>{explanation}</span>", unsafe_allow_html=True)


            with col_actions:
                st.markdown(f"<div style='text-align: right; color: #1DB954; font-size: 0.8rem; font-weight: 600; margin-bottom: 4px;'>⭐ {score:.2f}</div>", unsafe_allow_html=True)
                
                if is_playing:
                    if st.button("⏹ Stop", key=f"stop_rec_{track_id}_{i}", use_container_width=True):
                        st.session_state["currently_playing"] = None
                        st.session_state["is_paused"] = False
                        st.rerun()
                else:
                    if st.button("▶️ Play", key=f"play_rec_{track_id}_{i}", use_container_width=True):
                        from api.music_api import MusicAPI
                        music_api = MusicAPI()
                        
                        # 1. Register with backend Kafka tracker
                        try:
                            music_api.register_playback(track_id=track_id, action="play")
                        except Exception as e:
                            st.toast(f"Warning: Failed to log interaction: {e}")

                        # 2. Resolve YouTube video ID and details (like duration)
                        resolved_video_id = None
                        duration = ""
                        if track_id and len(track_id) == 11 and not track_id.startswith("cold_start") and not track_id.startswith("mock"):
                            resolved_video_id = track_id
                            try:
                                res = music_api.get_track(track_id)
                                if res.status_code == 200:
                                    duration = res.json().get("duration", "")
                            except Exception:
                                pass
                        else:
                            with st.spinner("Resolving YouTube video..."):
                                try:
                                    res = music_api.search(f"{title} {artist}")
                                    if res.status_code == 200:
                                        items = res.json().get("tracks", {}).get("items", [])
                                        if items:
                                            resolved_video_id = items[0]["id"]
                                            duration = items[0].get("duration", "")
                                except Exception:
                                    pass
                        
                        if not resolved_video_id:
                            st.error("Could not find this track on YouTube.")
                        else:
                            st.session_state["currently_playing"] = {
                                "id": resolved_video_id,
                                "title": title,
                                "artist": artist,
                                "preview_url": f"https://www.youtube.com/watch?v={resolved_video_id}",
                                "duration": duration,
                            }
                            st.session_state["is_paused"] = False
                            st.toast(f"🔊 Playing: {title}")
                            st.rerun()

            # ── Control Panel below the playing song ─────────────────────────────
            if is_playing:
                st.markdown(
                    f'<div style="background:#1a0f0f; border:1px solid #ff444444; border-radius:10px; padding:10px 16px; margin-top:4px; margin-bottom:12px;">'
                    f'<div style="font-size:0.75rem; color:#ff8888; font-weight:700; text-transform:uppercase; letter-spacing:0.5px; display:flex; align-items:center; gap:6px; justify-content:space-between;">'
                    f'<span>⚡ LIST NAVIGATION: {title}</span>'
                    f'</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )
                
                # Streamlit columns for the premium control buttons
                btn_prev, btn_next, btn_stop = st.columns([1.5, 1.5, 3])
                
                with btn_prev:
                    prev_disabled = (idx <= 0)
                    if st.button("⏮ Previous Track", key=f"prev_rec_btn_{track_id}_{i}", disabled=prev_disabled, use_container_width=True):
                        from api.music_api import MusicAPI
                        music_api = MusicAPI()
                        target_track = recs[idx - 1]
                        target_title = target_track.get("title", "Unknown Track")
                        target_artist = target_track.get("artist", "Unknown Artist")
                        target_track_id = target_track.get("track_id", "")
                        
                        resolved_video_id = None
                        target_duration = ""
                        if target_track_id and len(target_track_id) == 11 and not target_track_id.startswith("cold_start") and not target_track_id.startswith("mock"):
                            resolved_video_id = target_track_id
                            try:
                                res = music_api.get_track(target_track_id)
                                if res.status_code == 200:
                                    target_duration = res.json().get("duration", "")
                            except Exception:
                                pass
                        else:
                            with st.spinner("Resolving YouTube video..."):
                                try:
                                    res = music_api.search(f"{target_title} {target_artist}")
                                    if res.status_code == 200:
                                        items = res.json().get("tracks", {}).get("items", [])
                                        if items:
                                            resolved_video_id = items[0]["id"]
                                            target_duration = items[0].get("duration", "")
                                except Exception:
                                    pass
                        
                        if resolved_video_id:
                            st.session_state["currently_playing"] = {
                                "id": resolved_video_id,
                                "title": target_title,
                                "artist": target_artist,
                                "preview_url": f"https://www.youtube.com/watch?v={resolved_video_id}",
                                "duration": target_duration,
                            }
                            st.session_state["is_paused"] = False
                            st.rerun()
                
                with btn_next:
                    next_disabled = (idx >= len(recs) - 1)
                    if st.button("Next Track ⏭", key=f"next_rec_btn_{track_id}_{i}", disabled=next_disabled, use_container_width=True):
                        from api.music_api import MusicAPI
                        music_api = MusicAPI()
                        target_track = recs[idx + 1]
                        target_title = target_track.get("title", "Unknown Track")
                        target_artist = target_track.get("artist", "Unknown Artist")
                        target_track_id = target_track.get("track_id", "")
                        
                        resolved_video_id = None
                        target_duration = ""
                        if target_track_id and len(target_track_id) == 11 and not target_track_id.startswith("cold_start") and not target_track_id.startswith("mock"):
                            resolved_video_id = target_track_id
                            try:
                                res = music_api.get_track(target_track_id)
                                if res.status_code == 200:
                                    target_duration = res.json().get("duration", "")
                            except Exception:
                                pass
                        else:
                            with st.spinner("Resolving YouTube video..."):
                                try:
                                    res = music_api.search(f"{target_title} {target_artist}")
                                    if res.status_code == 200:
                                        items = res.json().get("tracks", {}).get("items", [])
                                        if items:
                                            resolved_video_id = items[0]["id"]
                                            target_duration = items[0].get("duration", "")
                                except Exception:
                                    pass
                        
                        if resolved_video_id:
                            st.session_state["currently_playing"] = {
                                "id": resolved_video_id,
                                "title": target_title,
                                "artist": target_artist,
                                "preview_url": f"https://www.youtube.com/watch?v={resolved_video_id}",
                                "duration": target_duration,
                            }
                            st.session_state["is_paused"] = False
                            st.rerun()
                            
                with btn_stop:
                    if st.button("⏹ Stop Audio & Controls", key=f"stop_rec_btn_stop_{track_id}_{i}", use_container_width=True):
                        st.session_state["currently_playing"] = None
                        st.session_state["is_paused"] = False
                        st.rerun()
    else:
        st.info("No recommendations found for this mood yet. Try a different mood!")
