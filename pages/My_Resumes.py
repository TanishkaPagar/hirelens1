# My_Resumes.py
import streamlit as st
from utils import init_session, theme_css, load_logo, list_uploaded_resumes, preview_resume
import os

# -------------------------
# Initialize session & theme
# -------------------------
init_session()
theme_css()

# -------------------------
# Ensure user is logged in and is an Applicant
# -------------------------
if not st.session_state.logged_in:
    st.warning("Please login first to view your resumes.")
    st.stop()

if st.session_state.user_type != "Applicant":
    st.warning("You are not an Applicant. Access denied.")
    st.stop()

username = st.session_state.username

# -------------------------
# Page Header
# -------------------------
logo = load_logo()
if logo:
    st.image(logo, width=120)

st.title("🗂️ My Resumes")
st.subheader(f"Welcome, {username}!")

st.markdown("---")

# -------------------------
# List uploaded resumes
# -------------------------
resumes = list_uploaded_resumes(username)

if not resumes:
    st.info("You have not uploaded any resumes yet. Use 'Upload Resume' to add one!")
else:
    for idx, resume in enumerate(resumes):
        col1, col2, col3 = st.columns([3,1,1])
        with col1:
            st.markdown(f"**{resume}**")
        with col2:
            if st.button("Preview 👀", key=f"preview_{idx}"):
                content = preview_resume(username, resume)
                st.markdown(f"""
                <div style="max-height:400px; overflow:auto; border:1px solid #ccc; padding:10px; border-radius:10px;">
                <pre style="white-space: pre-wrap;">{content}</pre>
                </div>
                """, unsafe_allow_html=True)
        with col3:
            if st.button("Delete ❌", key=f"delete_{idx}"):
                # Delete file from folder
                file_path = os.path.join("uploaded_resumes", username, resume)
                try:
                    os.remove(file_path)
                    st.session_state.uploaded_resumes[username].remove(resume)
                    st.success(f"Deleted '{resume}' successfully!")
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"Failed to delete '{resume}': {e}")

# -------------------------
# Back / Home button
# -------------------------
if st.button("⬅️ Back to Dashboard"):
    st.session_state['page'] = '2_Applicant_Home'
    st.experimental_rerun()

# -------------------------
# Logout
# -------------------------
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.user_type = None
    st.session_state.username = None
    st.experimental_rerun()
