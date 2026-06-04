import streamlit as st

def track_card(track: dict):
    with st.container():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.image(track.get("album_art_url") or "https://via.placeholder.com/150", width=80)
        with col2:
            st.markdown(f"**{track.get('title', 'Unknown Title')}**")
            st.markdown(f"*{track.get('artist', 'Unknown Artist')}*")
        st.divider()

def post_card(post: dict):
    with st.container():
        st.markdown(f"**@{post.get('user_id', 'User')}** was feeling **{post.get('mood', 'CHILL')}**")
        st.markdown(f"> {post.get('caption', '')}")
        track_card(post.get("track", {}))

def loading_state():
    with st.spinner('Loading...'):
        pass
