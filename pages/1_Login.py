# 1_Login.py
import streamlit as st
from utils import init_session, hash_password, check_password, theme_css

init_session()
theme_css()

st.title("Welcome to HireLens Login")

# Temporary users (replace with DB later)
users = {
    "applicant1": {"password": hash_password("pass123"), "type": "Applicant"},
    "company1": {"password": hash_password("comp123"), "type": "Company"}
}

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if username in users and check_password(users[username]["password"], password):
        st.session_state.logged_in = True
        st.session_state.username = username
        st.session_state.user_type = users[username]["type"]
        st.success(f"Logged in as {username} ({st.session_state.user_type})")
        st.experimental_rerun()
    else:
        st.error("Invalid username or password")
