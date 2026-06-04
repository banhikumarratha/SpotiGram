import streamlit as st
from components.navigation import render_sidebar
from components.playback_sdk import render_spotify_player
from utils.state import is_authenticated

st.set_page_config(page_title="Home - Spotigram", page_icon="🏠")

if not is_authenticated():
    st.switch_page("app.py")

render_sidebar()

st.title("Welcome to Spotigram 🎵")
st.markdown("Your personalized music journey starts here.")

# Spotify Web Player integration (if connected)
if st.session_state.get("spotify_connected") and st.session_state.get("spotify_access_token"):
    st.subheader("Web Player")
    render_spotify_player(st.session_state["spotify_access_token"])
else:
    st.info("Connect to Spotify in the Settings page to enable web playback.")

st.divider()

col1, col2 = st.columns(2)
with col1:
    st.subheader("Your Latest Mood")
    st.write("Scan your mood in the Mood Scanner to see it here!")
    if st.button("Go to Mood Scanner"):
        st.switch_page("pages/03_Mood_Scanner.py")

with col2:
    st.subheader("AI DJ")
    st.write("Need something specific? Your DJ is ready.")
    if st.button("Chat with DJ"):
        st.switch_page("pages/05_AI_DJ.py")
