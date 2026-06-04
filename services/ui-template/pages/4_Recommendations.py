import streamlit as st
from api.client import api_client
from components.ui import track_card

st.title("Recommendations 🎶")

st.write("Get AI track recommendations based on your current vibe.")
mood = st.selectbox("Select a Mood", ["HAPPY", "SAD", "CHILL", "ENERGETIC"])

if st.button("Get Recommendations"):
    with st.spinner("Fetching from AI..."):
        recs = api_client.get_ai_recommendations(mood)
        if recs:
            for track in recs:
                track_card(track)
        else:
            st.error("Could not fetch recommendations.")
