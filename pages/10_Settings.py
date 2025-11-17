# 10_Settings.py
import streamlit as st
from utils import init_session

# -------------------------
# Initialize session
# -------------------------
init_session()

st.title("⚙️ Settings")

# -------------------------
# Theme toggle
# -------------------------
st.subheader("Theme")
theme = st.radio("Select Theme", options=["light", "dark"], index=0 if st.session_state.theme=="light" else 1)
st.session_state.theme = theme
st.success(f"Theme set to {theme} mode")

# -------------------------
# Account info / Logout
# -------------------------
st.subheader("Account")
if 'username' in st.session_state:
    st.write(f"Logged in as: **{st.session_state['username']}**")
    if st.button("Logout"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.success("Logged out successfully!")
else:
    st.info("You are not logged in.")

# -------------------------
# Other Preferences
# -------------------------
st.subheader("Preferences")
st.checkbox("Enable notifications", value=True)
st.checkbox("Show tips on homepage", value=True)
