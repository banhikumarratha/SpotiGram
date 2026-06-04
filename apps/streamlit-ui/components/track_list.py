import streamlit as st

def render_track_list(tracks: list):
    """Render a list of Spotify tracks."""
    if not tracks:
        st.info("No tracks found.")
        return

    for t in tracks:
        col1, col2, col3 = st.columns([1, 4, 1])
        with col1:
            if "album" in t and t["album"].get("images"):
                st.image(t["album"]["images"][0]["url"], width=64)
            else:
                st.write("🎵")
        with col2:
            st.markdown(f"**{t.get('name', 'Unknown Track')}**")
            artists = ", ".join([a.get("name", "Unknown") for a in t.get("artists", [])])
            st.caption(f"by {artists}")
        with col3:
            # Just a placeholder button
            if st.button("Play", key=f"play_{t.get('id')}"):
                st.toast(f"Playback triggered for {t.get('name')} (Requires backend integration)")
        st.divider()

def render_playlist_card(playlist: dict):
    """Render a Spotify playlist as a card."""
    col1, col2 = st.columns([1, 3])
    with col1:
        if playlist.get("images"):
            st.image(playlist["images"][0]["url"], width=100)
        else:
            st.write("📁")
    with col2:
        st.subheader(playlist.get("name", "Unknown Playlist"))
        st.caption(playlist.get("description", ""))
        st.write(f"Tracks: {playlist.get('tracks', {}).get('total', 0)}")
