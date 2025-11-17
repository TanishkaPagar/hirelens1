# Home.py
import streamlit as st
from utils import init_session, theme_css, load_logo

# Initialize session
init_session()
theme_css()

# Ensure user is logged in
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first to access the Home Page.")
    st.stop()

# Load app logo
logo = load_logo()
if logo:
    st.sidebar.image(logo, width=150)

# Page title
st.title(f"🏠 Welcome to HireLens, {st.session_state.get('username', 'User')}!")

st.markdown("---")
st.subheader("Quick Actions")

# Quick navigation buttons
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Upload Resume 📄"):
        st.session_state['page'] = '5_Resume_Upload'
        st.experimental_rerun()

with col2:
    if st.button("View My Resumes 🗂️"):
        st.session_state['page'] = 'My_Resumes'
        st.experimental_rerun()

with col3:
    if st.button("ATS Score 📊"):
        st.session_state['page'] = '7_ATS_Score'
        st.experimental_rerun()

# Company-specific actions
if st.session_state.get("user_type") == "Company":
    st.markdown("---")
    st.subheader("Company Actions")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Upload Candidate CSV 📁"):
            st.session_state['page'] = '6_Dataset_Classifier'
            st.experimental_rerun()
    with col2:
        if st.button("View Applicants List 📝"):
            st.session_state['page'] = '4_Applicant_List'
            st.experimental_rerun()

# Info / Tips section
st.markdown("---")
st.markdown(
    """
    💡 **Tip:** Use the menu or buttons above to quickly navigate.  
    🌙 Switch themes and fonts in Settings to personalize your experience.  
    🚀 Upload resumes, evaluate ATS scores, and manage applicants efficiently!
    """
)

# Logout button
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.user_type = None
    st.session_state.username = None
    st.experimental_rerun()
