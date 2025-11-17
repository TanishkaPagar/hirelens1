# 2_Applicant_Home.py
import streamlit as st
from utils import (
    init_session, theme_css, list_uploaded_resumes, save_resume,
    extract_text, score_resume, show_score_pie, load_logo, preview_resume
)

# -------------------------
# Initialize session & theme
# -------------------------
init_session()
theme_css()

# -------------------------
# Ensure user is logged in and is an Applicant
# -------------------------
if not st.session_state.logged_in:
    st.warning("Please login first to access the Applicant Home.")
    st.stop()

if st.session_state.user_type != 'Applicant':
    st.warning("You are not an Applicant. Access denied.")
    st.stop()

username = st.session_state.username

# -------------------------
# Page Header
# -------------------------
logo = load_logo()
if logo:
    st.image(logo, width=120)

st.title("👨‍💻 Applicant Dashboard")
st.subheader(f"Welcome, {username}!")

st.markdown("---")

# -------------------------
# Upload Resume
# -------------------------
st.subheader("Upload a New Resume")
uploaded_file = st.file_uploader("Choose PDF or DOCX file", type=["pdf", "docx"], key="upload_resume")

if uploaded_file:
    save_resume(uploaded_file, username)
    st.success(f"✅ Resume '{uploaded_file.name}' uploaded successfully!")

st.markdown("---")

# -------------------------
# List Uploaded Resumes
# -------------------------
st.subheader("Your Uploaded Resumes")
resumes = list_uploaded_resumes(username)

if not resumes:
    st.info("You have not uploaded any resumes yet.")
else:
    for idx, resume in enumerate(resumes):
        st.markdown(f"**{resume}**")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button(f"Preview 👀", key=f"preview_{idx}"):
                content = preview_resume(username, resume)
                st.text_area(f"Preview: {resume}", value=content, height=300)
        with col2:
            if st.button(f"ATS Score 📊", key=f"score_{idx}"):
                text = extract_text(open(f"uploaded_resumes/{username}/{resume}", "rb"))
                required_skills = ["Python", "Java", "SQL", "Excel", "Power BI", "Machine Learning"]
                score, skills = score_resume(text, required_skills)
                st.write(f"**ATS Score:** {score}%")
                st.write(f"**Skills Found:** {skills}")
                show_score_pie(score)

st.markdown("---")

# -------------------------
# Quick Navigation Buttons
# -------------------------
st.subheader("Quick Actions")
col1, col2 = st.columns(2)
with col1:
    if st.button("View ATS Scores 📊"):
        st.session_state['page'] = '7_ATS_Score'
        st.experimental_rerun()
with col2:
    if st.button("My Resumes 🗂️"):
        st.session_state['page'] = 'My_Resumes'
        st.experimental_rerun()

# -------------------------
# Logout
# -------------------------
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.user_type = None
    st.session_state.username = None
    st.experimental_rerun()
