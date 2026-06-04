import streamlit as st
from components.navigation import render_sidebar
from components.track_list import render_playlist_card
from api.ai_api import AIAPI
from utils.state import is_authenticated

st.set_page_config(page_title="Recommendations - Spotigram", page_icon="🎧")

if not is_authenticated():
    st.switch_page("app.py")

render_sidebar()

st.title("Recommendations")

current_mood = st.session_state.get("current_mood", "chill")
mood_input = st.text_input("Mood", value=current_mood)

if st.button("Generate Playlist"):
    api = AIAPI()
    try:
        with st.spinner("Curating your playlist..."):
            res = api.get_recommendations(mood=mood_input)
            if res.status_code == 200:
                data = res.json()
                st.success("Here are your recommendations!")
                # Assuming the response has a list of playlists or tracks
                playlists = data.get("playlists", [])
                for p in playlists:
                    render_playlist_card(p)
                
                tracks = data.get("tracks", [])
                if tracks:
                    from components.track_list import render_track_list
                    st.subheader("Tracks")
                    render_track_list(tracks)
                    
            else:
                st.error(f"Failed to get recommendations: {res.status_code}")
    except Exception as e:
        st.error(f"Connection failed: {e}")
