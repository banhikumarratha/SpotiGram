import streamlit as st
from api.auth_api import AuthAPI
from utils.state import init_session_state
import jwt

def render_login_form():
    st.subheader("Login to Spotigram")
    with st.form("login_form"):
        email = st.text_input("Email", placeholder="you@example.com")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            api = AuthAPI()
            try:
                res = api.login(email, password)
                if res.status_code == 200:
                    data = res.json()
                    st.session_state["access_token"] = data["access_token"]
                    st.session_state["refresh_token"] = data.get("refresh_token")
                    
                    # decode token to get user_id
                    try:
                        decoded = jwt.decode(data["access_token"], options={"verify_signature": False})
                        st.session_state["user_id"] = decoded.get("sub")
                        st.session_state["user_email"] = email
                        print(f"DEBUG auth_forms.py: Logged in and set user_id to {st.session_state['user_id']} and user_email to {st.session_state['user_email']}")
                    except Exception as e:
                        print(f"DEBUG auth_forms.py: Error decoding token: {e}", flush=True)
                        import traceback
                        traceback.print_exc()
                        
                    st.success("Successfully logged in!")
                    st.rerun()
                else:
                    st.error(f"Login failed: {res.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"Connection error: {str(e)}")

def render_register_form():
    st.subheader("Create an Account")
    with st.form("register_form"):
        name = st.text_input("Name", placeholder="Your Name")
        email = st.text_input("Email", placeholder="you@example.com")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Register")

        if submitted:
            api = AuthAPI()
            try:
                res = api.register(email, password, name)
                if res.status_code in (200, 201):
                    st.success("Account created successfully! Please login.")
                else:
                    st.error(f"Registration failed: {res.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"Connection error: {str(e)}")

def render_auth_gate():
    init_session_state()
    col1, col2 = st.columns(2)
    with col1:
        render_login_form()
    with col2:
        render_register_form()
