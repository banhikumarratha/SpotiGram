import streamlit as st
from components.navigation import render_sidebar
from api.mood_api import MoodAPI
from utils.state import is_authenticated

st.set_page_config(page_title="Mood Scanner - Spotigram", page_icon="📸")

if not is_authenticated():
    st.switch_page("app.py")

render_sidebar()


# ─────────────────────────────────────────────────────────────────────────────
# Helper
# ─────────────────────────────────────────────────────────────────────────────
def _mood_emoji(mood: str) -> str:
    mapping = {
        "happy": "😄", "joy": "😄", "joyful": "😄",
        "sad": "😢", "sadness": "😢",
        "angry": "😠", "anger": "😠",
        "calm": "😌", "relaxed": "😌", "peaceful": "😌",
        "excited": "🤩", "energetic": "⚡",
        "fearful": "😨", "fear": "😨",
        "surprised": "😲", "surprise": "😲",
        "neutral": "😐",
        "tired": "😴", "sleepy": "😴",
        "romantic": "😍", "love": "❤️",
        "melancholy": "🌧️",
    }
    return mapping.get(mood.lower(), "🎭")


# ─────────────────────────────────────────────────────────────────────────────
# Styles
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .mood-hero {
        background: linear-gradient(135deg, #1DB954 0%, #1ed760 40%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.6rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 0;
        line-height: 1.2;
    }
    .mood-sub {
        color: #8888a8;
        font-size: 1.05rem;
        margin-top: 0.4rem;
        margin-bottom: 1.8rem;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: #0d0d1c;
        border-radius: 14px;
        padding: 6px;
        border: 1px solid #1e1e3a;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 10px 26px;
        font-weight: 600;
        font-size: 0.95rem;
        color: #8888a8;
        background: transparent;
        transition: all 0.25s ease;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1DB954, #a78bfa) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(29,185,84,0.25);
    }

    /* Mode info card */
    .mode-card {
        background: linear-gradient(145deg, #12122a, #1a1a35);
        border: 1px solid #252545;
        border-radius: 18px;
        padding: 2.2rem;
        margin-bottom: 1.8rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    .mode-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle at center, rgba(29,185,84,0.04) 0%, transparent 60%);
        pointer-events: none;
    }
    .mode-icon {
        font-size: 3.8rem;
        margin-bottom: 0.75rem;
        display: block;
        animation: float 3s ease-in-out infinite;
    }
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-6px); }
    }
    .mode-title {
        font-size: 1.35rem;
        font-weight: 700;
        color: #e0e0f5;
        margin-bottom: 0.5rem;
    }
    .mode-desc {
        color: #7070a0;
        font-size: 0.9rem;
        line-height: 1.5;
    }

    /* Mood result */
    .mood-result {
        background: linear-gradient(135deg, rgba(29,185,84,0.1), rgba(167,139,250,0.1));
        border: 1px solid rgba(29,185,84,0.25);
        border-radius: 18px;
        padding: 2rem;
        text-align: center;
        margin-top: 1.2rem;
        animation: fadeInUp 0.5s ease forwards;
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(15px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .mood-result-emoji { font-size: 3rem; margin-bottom: 0.3rem; display: block; }
    .mood-result-label {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1DB954, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .mood-result-conf { color: #7070a0; font-size: 0.9rem; margin-top: 0.3rem; }

    /* Override Streamlit's default button in primary mode */
    [data-testid="stBaseButton-primary"] {
        background: linear-gradient(135deg, #1DB954, #a78bfa) !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        transition: opacity 0.2s ease, transform 0.2s ease !important;
        box-shadow: 0 4px 20px rgba(29,185,84,0.3) !important;
    }
    [data-testid="stBaseButton-primary"]:hover {
        opacity: 0.9 !important;
        transform: translateY(-1px) !important;
    }
</style>
""", unsafe_allow_html=True)

# ── Page header ───────────────────────────────────────────────────────────────
st.markdown('<p class="mood-hero">🎭 Mood Scanner</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="mood-sub">Let your voice or face reveal the perfect playlist for your vibe.</p>',
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# Tabs
# ─────────────────────────────────────────────────────────────────────────────
tab_voice, tab_face = st.tabs(["🎙️  Voice Recording", "📸  Face Scanner"])


# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 – VOICE RECORDING
# st.audio_input() activates the browser microphone directly — no file upload.
# ─────────────────────────────────────────────────────────────────────────────
with tab_voice:
    st.markdown("""
    <div class="mode-card">
        <span class="mode-icon">🎙️</span>
        <div class="mode-title">Speak Your Mind</div>
        <div class="mode-desc">
            Hit the microphone button and talk about how you feel.<br>
            We'll read the emotion in your voice to find your perfect soundtrack.
        </div>
    </div>
    """, unsafe_allow_html=True)

    audio_value = st.audio_input(
        "Click the mic to start — speak freely, then stop recording",
        key="voice_recorder",
    )

    if audio_value is not None:
        st.audio(audio_value, format="audio/wav")
        st.markdown("&nbsp;")

        col_l, col_btn, col_r = st.columns([1, 2, 1])
        with col_btn:
            analyze_voice = st.button(
                "✨ Analyze Voice Mood",
                key="analyze_voice",
                use_container_width=True,
                type="primary",
            )

        if analyze_voice:
            api = MoodAPI()
            try:
                with st.spinner("🎵 Reading your vibe…"):
                    audio_bytes = audio_value.read()
                    res = api.analyze_audio(audio_bytes, "voice_recording.wav")
                if res.status_code == 200:
                    mood_data = res.json()
                    mood = mood_data.get("mood", "neutral").capitalize()
                    confidence = mood_data.get("confidence", 0) * 100
                    emoji = _mood_emoji(mood)

                    st.markdown(f"""
                    <div class="mood-result">
                        <span class="mood-result-emoji">{emoji}</span>
                        <div class="mood-result-label">{mood}</div>
                        <div class="mood-result-conf">Confidence: {confidence:.1f}%</div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.session_state["current_mood"] = mood_data.get("mood")
                    st.balloons()
                else:
                    st.error(f"Analysis failed ({res.status_code}): {res.text}")
            except Exception as exc:
                st.error(f"Connection error: {exc}")
    else:
        st.info("🎤 Press **Start recording** above to capture your voice.")


# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 – FACE SCANNER
# st.camera_input() activates the system camera directly — no file upload.
# ─────────────────────────────────────────────────────────────────────────────
with tab_face:
    st.markdown("""
    <div class="mode-card">
        <span class="mode-icon">📸</span>
        <div class="mode-title">Show Your Emotion</div>
        <div class="mode-desc">
            Allow camera access and take a quick selfie.<br>
            We'll read your facial expression to match the perfect playlist to your mood.
        </div>
    </div>
    """, unsafe_allow_html=True)

    img_snapshot = st.camera_input(
        "Take a selfie to scan your mood",
        key="face_scanner",
    )

    if img_snapshot is not None:
        st.markdown("&nbsp;")
        col_l, col_btn, col_r = st.columns([1, 2, 1])
        with col_btn:
            analyze_face = st.button(
                "✨ Analyze Face Mood",
                key="analyze_face",
                use_container_width=True,
                type="primary",
            )

        if analyze_face:
            api = MoodAPI()
            try:
                with st.spinner("🔍 Scanning your expression…"):
                    image_bytes = img_snapshot.getvalue()
                    res = api.analyze_image(image_bytes, "face_snapshot.jpg")
                if res.status_code == 200:
                    mood_data = res.json()
                    mood = mood_data.get("mood", "neutral").capitalize()
                    confidence = mood_data.get("confidence", 0) * 100
                    emoji = _mood_emoji(mood)

                    st.markdown(f"""
                    <div class="mood-result">
                        <span class="mood-result-emoji">{emoji}</span>
                        <div class="mood-result-label">{mood}</div>
                        <div class="mood-result-conf">Confidence: {confidence:.1f}%</div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.session_state["current_mood"] = mood_data.get("mood")
                    st.balloons()
                else:
                    st.error(f"Analysis failed ({res.status_code}): {res.text}")
            except Exception as exc:
                st.error(f"Connection error: {exc}")
    else:
        st.info("📷 Click **Take photo** once the camera initializes above.")


# ─────────────────────────────────────────────────────────────────────────────
# Bottom CTA – navigate to Recommendations
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.get("current_mood"):
    st.divider()
    mood_display = st.session_state["current_mood"].capitalize()
    emoji = _mood_emoji(mood_display)
    st.markdown(f"**Current mood:** {emoji} {mood_display}")

    col_l, col_btn, col_r = st.columns([1, 2, 1])
    with col_btn:
        if st.button(
            "🎵 Get Recommendations for this Mood",
            use_container_width=True,
            type="primary",
        ):
            st.switch_page("pages/04_Recommendations.py")
