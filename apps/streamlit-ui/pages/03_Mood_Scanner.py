import streamlit as st
from components.navigation import render_sidebar
from api.mood_api import MoodAPI
from utils.state import is_authenticated

st.set_page_config(page_title="Mood Scanner - Spotigram", page_icon="📸")

if not is_authenticated():
    st.switch_page("app.py")

render_sidebar()

st.title("Mood Scanner")
st.write("Upload an audio snippet or enter text to detect your current mood.")

tab1, tab2 = st.tabs(["Text Analysis", "Audio Analysis"])

with tab1:
    text_input = st.text_area("How are you feeling today?", placeholder="I'm feeling a bit tired but mostly relaxed...")
    if st.button("Analyze Text"):
        if text_input:
            api = MoodAPI()
            try:
                with st.spinner("Analyzing..."):
                    res = api.analyze_text(text_input)
                    if res.status_code == 200:
                        mood_data = res.json()
                        st.success(f"Detected Mood: **{mood_data.get('mood', 'Unknown').capitalize()}**")
                        st.metric("Confidence", f"{mood_data.get('confidence', 0)*100:.1f}%")
                        st.session_state["current_mood"] = mood_data.get('mood')
                    else:
                        st.error(f"Analysis failed: {res.status_code}")
            except Exception as e:
                st.error(f"Connection failed: {e}")
        else:
            st.warning("Please enter some text.")

with tab2:
    audio_file = st.file_uploader("Upload a short audio clip (WAV/MP3)", type=["wav", "mp3"])
    if st.button("Analyze Audio"):
        if audio_file is not None:
            api = MoodAPI()
            try:
                with st.spinner("Analyzing audio..."):
                    res = api.analyze_audio(audio_file.getvalue(), audio_file.name)
                    if res.status_code == 200:
                        mood_data = res.json()
                        st.success(f"Detected Mood: **{mood_data.get('mood', 'Unknown').capitalize()}**")
                        st.metric("Confidence", f"{mood_data.get('confidence', 0)*100:.1f}%")
                        st.session_state["current_mood"] = mood_data.get('mood')
                    else:
                        st.error(f"Analysis failed: {res.status_code}")
            except Exception as e:
                st.error(f"Connection failed: {e}")
        else:
            st.warning("Please upload an audio file.")

if st.session_state.get("current_mood"):
    st.divider()
    if st.button("Get Recommendations for this Mood"):
        st.switch_page("pages/04_Recommendations.py")
