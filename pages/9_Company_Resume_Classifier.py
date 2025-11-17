# 9_Company_Resume_Classifier.py
import streamlit as st
from utils import list_uploaded_resumes, extract_text, score_resume, extract_skills_from_text, preview_resume, load_logo, show_score_pie

# -------------------------
# Ensure user is logged in and is a Company
# -------------------------
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first to access Resume Classifier.")
    st.stop()

if st.session_state.get('user_type') != 'Company':
    st.warning("You are not a Company user. Access denied.")
    st.stop()

# -------------------------
# Page Header
# -------------------------
logo = load_logo()
if logo:
    st.image(logo, width=120)

st.title("🔍 Company Resume Classifier")
st.subheader(f"Welcome, {st.session_state.get('username', 'Company')}!")

st.markdown("---")
st.markdown("### Uploaded Applicant Resumes")

# -------------------------
# Collect all resumes from all applicants
# -------------------------
all_users = st.session_state.get("uploaded_resumes", {})
if not all_users:
    st.info("No resumes uploaded by applicants yet.")
else:
    resumes_data = []
    for username, files in all_users.items():
        for resume_name in files:
            resumes_data.append((username, resume_name))

    for idx, (username, resume_name) in enumerate(resumes_data):
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.markdown(f"**{resume_name}** (Applicant: {username})")
        with col2:
            if st.button("Preview 👀", key=f"preview_{idx}"):
                content = preview_resume(username, resume_name)
                st.markdown(f"""
                    <div style="position:fixed; top:10%; left:10%; width:80%; height:80%; 
                                background:white; z-index:9999; border-radius:15px; 
                                box-shadow: 0 0 10px rgba(0,0,0,0.5); overflow:auto; padding:20px;">
                        <h2>{resume_name}</h2>
                        <pre style="white-space: pre-wrap;">{content}</pre>
                        <button onclick="this.parentElement.style.display='none'" 
                            style="padding:10px 20px; margin-top:10px;">Close</button>
                    </div>
                """, unsafe_allow_html=True)
        with col3:
            required_skills_input = st.text_input(f"Skills for scoring {resume_name}", "Python,SQL,Excel", key=f"skills_{idx}")
            if st.button(f"Score 📊", key=f"score_{idx}"):
                skills_list = [s.strip() for s in required_skills_input.split(",")]
                resume_text = extract_text(open(f"uploaded_resumes/{username}/{resume_name}", "rb"))
                score, skills_found = score_resume(resume_text, skills_list)
                st.write(f"**Score:** {score}%")
                st.write(f"Skills Found: {skills_found}")
                show_score_pie(score)

# -------------------------
# Logout
# -------------------------
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.user_type = None
    st.session_state.username = None
    st.experimental_rerun()
