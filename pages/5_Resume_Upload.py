# 5_Resume_Upload.py
import streamlit as st
from utils import init_session, theme_css, load_logo, save_resume, list_uploaded_resumes, preview_resume

# -------------------------
# Initialize session & theme
# -------------------------
init_session()
theme_css()

# -------------------------
# Ensure user is logged in and is an Applicant
# -------------------------
if not st.session_state.logged_in:
    st.warning("Please login first to upload resumes.")
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

st.title("📄 Upload Your Resume")
st.subheader(f"Hello, {username}! Upload your resume to get started.")

st.markdown("---")

# -------------------------
# File uploader
# -------------------------
uploaded_file = st.file_uploader(
    "Choose your resume (PDF or DOCX)", 
    type=["pdf", "docx"], 
    key="resume_uploader"
)

if uploaded_file:
    try:
        path = save_resume(uploaded_file, username)
        st.success(f"✅ Resume '{uploaded_file.name}' uploaded successfully!")
    except Exception as e:
        st.error(f"❌ Failed to upload resume: {e}")

st.markdown("---")

# -------------------------
# List uploaded resumes
# -------------------------
st.subheader("Your Uploaded Resumes")

resumes = list_uploaded_resumes(username)

if not resumes:
    st.info("You have not uploaded any resumes yet.")
else:
    for idx, resume in enumerate(resumes):
        col1, col2 = st.columns([3,1])
        with col1:
            st.markdown(f"**{resume}**")
        with col2:
            if st.button("Preview 👀", key=f"preview_{idx}"):
                content = preview_resume(username, resume)
                # Display content in a scrollable container
                st.markdown(f"""
                <div style="max-height:400px; overflow:auto; border:1px solid #ccc; padding:10px; border-radius:10px;">
                <pre style="white-space: pre-wrap;">{content}</pre>
                </div>
                """, unsafe_allow_html=True)

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
