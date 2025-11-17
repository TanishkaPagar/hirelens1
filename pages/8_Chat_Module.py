# 8_Chat_Module.py
import streamlit as st
from utils import send_message

# -------------------------
# Ensure user is logged in
# -------------------------
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first to access the chat module.")
    st.stop()

username = st.session_state['username']

# -------------------------
# Page Header
# -------------------------
st.title("💬 Chat Module")
st.subheader("Communicate with companies or applicants in real-time")

# -------------------------
# Chat Input
# -------------------------
st.markdown("### Send a message")
message = st.text_area("Type your message here:", height=100)

col1, col2 = st.columns([1,1])
with col1:
    if st.button("Send"):
        if message.strip() != "":
            send_message(username, message)
            st.success("Message sent!")
            st.experimental_rerun()
        else:
            st.warning("Cannot send empty message.")

# -------------------------
# Display Chat History
# -------------------------
st.markdown("### Chat History")
if 'chat_history' not in st.session_state or len(st.session_state['chat_history']) == 0:
    st.info("No messages yet.")
else:
    for chat in st.session_state['chat_history']:
        sender = chat['sender']
        msg = chat['message']
        time = chat['time']
        if sender == username:
            st.markdown(f"<div style='text-align:right; background-color:#DCF8C6; padding:8px; border-radius:10px; margin:5px;'>"
                        f"<b>You:</b> {msg} <br><small>{time}</small></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align:left; background-color:#F1F0F0; padding:8px; border-radius:10px; margin:5px;'>"
                        f"<b>{sender}:</b> {msg} <br><small>{time}</small></div>", unsafe_allow_html=True)
