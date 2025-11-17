# 0_Welcome.py
import streamlit as st
from utils import init_session, theme_css, load_logo

# -------------------------
# Initialize session & theme
# -------------------------
init_session()
theme_css()

# -------------------------
# Page layout
# -------------------------
st.set_page_config(page_title="HireLens - Welcome", page_icon="👋", layout="centered")

# Load logo if available
logo = load_logo()
if logo:
    st.image(logo, width=200)

st.markdown("<h1 style='text-align:center; color:#4CAF50;'>Welcome to HireLens</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:gray;'>Smart Resume Management & ATS Scoring</h3>", unsafe_allow_html=True)

st.markdown("---")

# -------------------------
# Welcome Buttons
# -------------------------
col1, col2 = st.columns(2)

with col1:
    if st.button("👤 Login"):
        st.session_state['page'] = '1_Login.py'
        st.experimental_rerun()  # Go to login page

with col2:
    if st.button("📝 Sign Up"):
        st.session_state['page'] = '1_SignUp.py'
        st.experimental_rerun()  # Go to sign up page

# Optional: Footer / tips
st.markdown("---")
st.markdown(
    """
    💡 Tip: If you are a new user, please sign up first.  
    🔒 Your data and resumes are private and secure.  
    🚀 Upload resumes and get ATS scores instantly!
    """
)
