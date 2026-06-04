import streamlit as st
from components.navigation import render_sidebar
from components.track_list import render_track_list, render_playlist_card
from api.spotify_api import SpotifyAPI
from utils.state import is_authenticated

st.set_page_config(page_title="Discover - Spotigram", page_icon="🔍")

if not is_authenticated():
    st.switch_page("app.py")

render_sidebar()

st.title("Discover")

search_query = st.text_input("Search for tracks or artists...", placeholder="e.g. The Beatles")

if search_query:
    api = SpotifyAPI()
    try:
        with st.spinner("Searching..."):
            res = api.search(search_query)
            if res.status_code == 200:
                data = res.json()
                tracks = data.get("tracks", {}).get("items", [])
                
                if tracks:
                    st.subheader("Tracks")
                    render_track_list(tracks)
                else:
                    st.write("No tracks found.")
            else:
                st.error(f"Search failed: {res.status_code} - {res.text}")
    except Exception as e:
        st.error(f"Failed to connect to Spotify Service: {e}")
