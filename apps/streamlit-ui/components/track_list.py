import streamlit as st

def _parse_duration_to_seconds(dur_str: str) -> int:
    if not dur_str:
        return 180
    clean = "".join(c for c in dur_str if c.isdigit() or c == ":")
    parts = clean.split(":")
    try:
        if len(parts) == 1:
            return int(parts[0])
        elif len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1])
        elif len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    except Exception:
        pass
    return 180

def render_track_list(tracks: list):
    """Render a list of YouTube music tracks as rich cards."""
    if not tracks:
        st.info("No tracks found.")
        return

    # Custom styling
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    .yt-thumb-placeholder {
        width: 100%;
        height: 110px;
        border-radius: 8px;
        background: linear-gradient(135deg, #ff0000 0%, #aa0000 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

    current_playing = st.session_state.get("currently_playing") or {}
    playing_id = current_playing.get("id")
    is_paused = st.session_state.get("is_paused", False)

    for idx, t in enumerate(tracks):
        video_id = t.get("id", "")
        title = t.get("name", "Unknown Track")
        artists = ", ".join(a.get("name", "Unknown") for a in t.get("artists", []))
        duration = t.get("duration", "")
        preview_url = t.get("preview_url", f"https://www.youtube.com/watch?v={video_id}")
        thumbnail = ""
        if t.get("album", {}).get("images"):
            thumbnail = t["album"]["images"][0].get("url", "")

        is_playing = (playing_id == video_id)

        # ── Render Card using Streamlit layout columns ────────────────
        col_media, col_info, col_btn = st.columns([1.5, 3.5, 1])

        with col_media:
            if is_playing:
                # Load custom player containing YouTube embed and interactive seek slider controls
                # The height is locked to exactly 110px to match the static thumbnail size
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
                st.components.v1.html(player_html, height=110)
            else:
                if thumbnail:
                    st.markdown(
                        f'<img src="{thumbnail}" style="width:100%; height:110px; object-fit:cover; border-radius:8px; border:1px solid #333;" />',
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown('<div class="yt-thumb-placeholder">▶</div>', unsafe_allow_html=True)

        with col_info:
            st.markdown(f"**{title}**")
            st.markdown(f"<span style='color:#7070a0; font-size:0.85rem;'>🎵 {artists}</span>", unsafe_allow_html=True)
            if duration:
                st.markdown(f"<span style='color:#ff4444; font-size:0.75rem; font-weight:600;'>⏱ {duration}</span>", unsafe_allow_html=True)

        with col_btn:
            st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
            if is_playing:
                if st.button("⏹ Stop", key=f"stop_{video_id}", use_container_width=True):
                    st.session_state["currently_playing"] = None
                    st.session_state["is_paused"] = False
                    st.rerun()
            else:
                if st.button("▶ Play", key=f"play_{video_id}", use_container_width=True):
                    from api.music_api import MusicAPI
                    try:
                        MusicAPI().register_playback(track_id=video_id, action="play")
                    except Exception:
                        pass

                    st.session_state["currently_playing"] = {
                        "id": video_id,
                        "title": title,
                        "artist": artists,
                        "preview_url": preview_url,
                        "thumbnail": thumbnail,
                        "duration": duration,
                    }
                    st.session_state["is_paused"] = False
                    st.rerun()

        # ── Control Panel below the playing song ─────────────────────────────
        if is_playing:
            status_text = "⏸ PAUSED" if is_paused else "🔊 NOW PLAYING"
            st.markdown(
                f'<div style="background:#1a0f0f; border:1px solid #ff444444; border-radius:10px; padding:10px 16px; margin-top:4px; margin-bottom:12px;">'
                f'<div style="font-size:0.75rem; color:#ff8888; font-weight:700; text-transform:uppercase; letter-spacing:0.5px; display:flex; align-items:center; gap:6px; justify-content:space-between;">'
                f'<span>🔴 {status_text}: {title}</span>'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True
            )
            
            # Streamlit columns for the premium control buttons
            btn_prev, btn_playpause, btn_replay, btn_next, btn_stop = st.columns([1, 1.2, 1, 1, 1.2])
            
            with btn_prev:
                prev_disabled = (idx <= 0)
                if st.button("⏮ Prev", key=f"prev_btn_{video_id}", disabled=prev_disabled, use_container_width=True):
                    prev_track = tracks[idx - 1]
                    st.session_state["currently_playing"] = {
                        "id": prev_track.get("id"),
                        "title": prev_track.get("name"),
                        "artist": ", ".join(a.get("name", "Unknown") for a in prev_track.get("artists", [])),
                        "preview_url": prev_track.get("preview_url"),
                        "thumbnail": prev_track.get("album", {}).get("images", [{}])[0].get("url", ""),
                        "duration": prev_track.get("duration", ""),
                    }
                    st.session_state["is_paused"] = False
                    st.rerun()
            
            with btn_playpause:
                playpause_label = "▶ Resume" if is_paused else "⏸ Pause"
                if st.button(playpause_label, key=f"playpause_btn_{video_id}", use_container_width=True):
                    st.session_state["is_paused"] = not is_paused
                    st.rerun()
            
            with btn_replay:
                if st.button("🔁 Replay", key=f"replay_btn_{video_id}", use_container_width=True):
                    st.session_state["is_paused"] = False
                    st.rerun()
            
            with btn_next:
                next_disabled = (idx >= len(tracks) - 1)
                if st.button("⏭ Next", key=f"next_btn_{video_id}", disabled=next_disabled, use_container_width=True):
                    next_track = tracks[idx + 1]
                    st.session_state["currently_playing"] = {
                        "id": next_track.get("id"),
                        "title": next_track.get("name"),
                        "artist": ", ".join(a.get("name", "Unknown") for a in next_track.get("artists", [])),
                        "preview_url": next_track.get("preview_url"),
                        "thumbnail": next_track.get("album", {}).get("images", [{}])[0].get("url", ""),
                        "duration": next_track.get("duration", ""),
                    }
                    st.session_state["is_paused"] = False
                    st.rerun()
                    
            with btn_stop:
                if st.button("⏹ Stop Play", key=f"stop_btn_{video_id}", use_container_width=True):
                    st.session_state["currently_playing"] = None
                    st.session_state["is_paused"] = False
                    st.rerun()

        st.divider()
