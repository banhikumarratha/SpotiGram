import streamlit as st
from api.client import api_client

st.title("Mood Scanner 🎭")

st.write("Tell us how you are feeling, and we will analyze your mood!")
text = st.text_area("How was your day?", placeholder="I'm feeling really energized today...")

if st.button("Scan Mood"):
    if text:
        with st.spinner("Analyzing emotion..."):
            res = api_client.analyze_emotion(text)
            if res:
                st.success(f"Detected Mood: **{res.get('mood')}**")
    else:
        st.warning("Please enter some text.")
