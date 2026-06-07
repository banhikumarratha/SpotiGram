import streamlit as st
from utils.state import is_authenticated, init_session_state
from components.auth_forms import render_auth_gate

st.set_page_config(
    page_title="Spotigram",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)



init_session_state()

if not is_authenticated():
    render_auth_gate()
else:
    # Restore user_id from token if missing but authenticated
    if (not st.session_state.get("user_id") or st.session_state.get("user_id") == "None") and st.session_state.get("access_token"):
        import jwt
        try:
            decoded = jwt.decode(st.session_state["access_token"], options={"verify_signature": False})
            st.session_state["user_id"] = decoded.get("sub")
            print(f"DEBUG app.py: Decoded token and set user_id to {st.session_state['user_id']}")
        except Exception as e:
            print(f"DEBUG app.py: Error decoding token: {e}", flush=True)
            import traceback
            traceback.print_exc()

    # Fetch user display name and email if missing
    user_id = st.session_state.get("user_id")
    if user_id and user_id != "None" and (not st.session_state.get("display_name") or not st.session_state.get("user_email") or st.session_state.get("user_email") == "Unknown Email"):
        from api.auth_api import AuthAPI
        auth_api = AuthAPI()
        try:
            print(f"DEBUG app.py: Fetching profile for user_id={st.session_state['user_id']}")
            res = auth_api.get_profile(st.session_state["user_id"])
            print(f"DEBUG app.py: Profile response status: {res.status_code}")
            if res.status_code == 200:
                data = res.json()
                st.session_state["display_name"] = data.get("display_name") or "User"
                st.session_state["user_email"] = data.get("email") or "Unknown Email"
                print(f"DEBUG app.py: Profile data updated to {st.session_state['display_name']} / {st.session_state['user_email']}")
            else:
                print(f"DEBUG app.py: Failed to get profile: {res.text}")
                st.session_state["display_name"] = "User"
        except Exception as e:
            print(f"DEBUG app.py: Exception fetching profile: {e}", flush=True)
            import traceback
            traceback.print_exc()
            st.session_state["display_name"] = "User"

    from components.navigation import render_sidebar
    render_sidebar()

    st.title("Welcome to Spotigram 🎵")
    
    display_name = st.session_state.get("display_name") or "User"
    user_email = st.session_state.get("user_email") or "Unknown Email"
    st.markdown(f"👤 **Name:** {display_name} &nbsp;&nbsp;|&nbsp;&nbsp; ✉️ **Username:** {user_email}")

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
