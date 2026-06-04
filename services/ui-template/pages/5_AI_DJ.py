import streamlit as st
from api.client import api_client
from components.ui import track_card

st.title("AI DJ 🎧")

st.write("Chat with your personal AI DJ to curate the perfect playlist.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask the DJ for a vibe..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Mixing..."):
            # Simple mapping from text to a mood for MVP
            mood = "HAPPY" if "happy" in prompt.lower() else "CHILL"
            recs = api_client.get_ai_recommendations(mood)
            if recs:
                st.markdown(f"I mixed this up for your **{mood}** vibe:")
                track_card(recs[0])
                st.session_state.messages.append({"role": "assistant", "content": f"Suggested a {mood} track."})
            else:
                st.error("DJ is taking a break.")
