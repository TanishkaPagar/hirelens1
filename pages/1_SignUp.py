# 1_SignUp.py
import streamlit as st
from utils import init_session, theme_css, hash_password

# -------------------------
# Initialize session & theme
# -------------------------
init_session()
theme_css()

st.set_page_config(page_title="HireLens - Sign Up", page_icon="📝", layout="centered")

st.title("📝 Sign Up for HireLens")

# -------------------------
# Check if already logged in
# -------------------------
if st.session_state.get('logged_in', False):
    st.warning(f"Already logged in as **{st.session_state.get('username')}**")
    if st.button("Go to Home Page"):
        st.session_state['page'] = 'Home.py'
        st.experimental_rerun()

else:
    # -------------------------
    # Sign Up form
    # -------------------------
    with st.form(key="signup_form"):
        username = st.text_input("Username / Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        user_type = st.selectbox("Sign Up as", ["Applicant", "Company"])
        submit = st.form_submit_button("Sign Up")

        if submit:
            # -------------------------
            # Temporary users DB in session (replace with actual DB)
            # -------------------------
            if 'users_db' not in st.session_state:
                st.session_state['users_db'] = {}

            users_db = st.session_state['users_db']

            if username in users_db:
                st.error("Username already exists. Please login.")
            elif password != confirm_password:
                st.error("Passwords do not match.")
            else:
                # Save user
                users_db[username] = {"password": hash_password(password), "type": user_type}
                st.session_state['users_db'] = users_db
                st.success(f"Account created successfully for **{username}**!")
                st.info("Go to Login page to continue.")
                if st.button("Go to Login"):
                    st.session_state['page'] = '1_Login.py'
                    st.experimental_rerun()














































































































































