import streamlit as st
from api.ai_api import AIAPI

def render_chat_interface():
    st.subheader("Chat with your AI DJ")
    
    # Initialize message history if empty
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
        
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("What would you like to listen to?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Get response from AI API
        api = AIAPI()
        session_id = st.session_state.get("user_id", "anonymous")
        try:
            with st.spinner("DJ is thinking..."):
                # context could include current mood, spotify token, etc.
                context = {"spotify_connected": st.session_state.get("spotify_connected", False)}
                res = api.chat_with_dj(session_id=session_id, message=prompt, context=context)
                
                if res.status_code == 200:
                    response_text = res.json().get("response", "I'm not sure what you mean.")
                else:
                    response_text = f"Error: {res.status_code} - {res.text}"
        except Exception as e:
            response_text = f"Failed to connect to AI DJ: {e}"

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response_text)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response_text})
