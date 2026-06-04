import streamlit as st
from components.navigation import render_sidebar
from api.spotify_api import SpotifyAPI
from utils.state import is_authenticated

st.set_page_config(page_title="Settings - Spotigram", page_icon="⚙️")

if not is_authenticated():
    st.switch_page("app.py")

render_sidebar()

st.title("Settings")

st.subheader("Theme")
theme = st.selectbox("Appearance", ["Dark", "Light"], index=0 if st.session_state.get("current_theme") == "dark" else 1)
if theme.lower() != st.session_state.get("current_theme"):
    st.session_state["current_theme"] = theme.lower()
    st.info("Theme preference saved. Note: Streamlit applies themes globally via config.toml, but we can use this for custom CSS.")

st.divider()

st.subheader("Spotify Integration")

if st.session_state.get("spotify_connected"):
    st.success("You are connected to Spotify.")
    if st.button("Disconnect from Spotify"):
        st.session_state["spotify_connected"] = False
        st.session_state["spotify_access_token"] = None
        st.rerun()
else:
    st.write("Connect your Spotify account to enable web playback and personalized features.")
    
    # In a real app, we'd hit the backend auth URL endpoint, then redirect the user.
    # For MVP, we simulate or provide a link.
    api = SpotifyAPI()
    try:
        res = api.get_auth_url()
        if res.status_code == 200:
            auth_url = res.json().get("auth_url")
            st.markdown(f"[Connect Spotify]({auth_url})")
            
            # Dev mock for immediate connection in UI
            with st.expander("Developer Mock Connection"):
                mock_token = st.text_input("Mock Access Token")
                if st.button("Simulate OAuth Callback"):
                    st.session_state["spotify_connected"] = True
                    st.session_state["spotify_access_token"] = mock_token if mock_token else "mock_token_123"
                    st.rerun()
        else:
            st.error("Could not fetch Spotify Auth URL from backend.")
    except Exception as e:
        st.error(f"Failed to connect to Spotify Service: {e}")
