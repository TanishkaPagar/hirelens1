# 7_ATS_Score.py
import streamlit as st
from utils import init_session, theme_css, load_logo, list_uploaded_resumes, extract_text, score_resume, show_score_pie

# -------------------------
# Initialize session & theme
# -------------------------
init_session()
theme_css()

# -------------------------
# Ensure user is logged in and is an Applicant
# -------------------------
if not st.session_state.logged_in:
    st.warning("Please login first to view ATS scores.")
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

st.title("📊 ATS Score Dashboard")
st.subheader(f"Welcome, {username}!")

st.markdown("---")

# -------------------------
# Enter required skills
# -------------------------
st.markdown("### Enter Required Skills for ATS Evaluation")
skills_input = st.text_input(
    "Enter skills separated by commas (e.g., Python, SQL, Excel):",
    value="Python, Java, SQL, Excel, Power BI, Machine Learning"
)

required_skills = [skill.strip() for skill in skills_input.split(",") if skill.strip()]

# -------------------------
# List uploaded resumes
# -------------------------
resumes = list_uploaded_resumes(username)

if not resumes:
    st.info("You have not uploaded any resumes yet. Upload a resume to see ATS scores!")
else:
    for idx, resume in enumerate(resumes):
        st.markdown(f"**{resume}**")
        file_path = f"uploaded_resumes/{username}/{resume}"
        
        # Extract text and score
        with open(file_path, "rb") as f:
            text = extract_text(f)
        score, skills_found = score_resume(text, required_skills)
        st.write(f"Matched Skills: {', '.join(skills_found) if skills_found else 'None'}")
        st.write(f"ATS Score: {score}%")
        show_score_pie(score)
        st.markdown("---")

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
