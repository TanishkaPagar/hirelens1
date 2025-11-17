# 4_Applicant_List.py
import streamlit as st
from utils import init_session, theme_css, load_logo, list_uploaded_resumes, preview_resume, search_resumes

# -------------------------
# Initialize session & theme
# -------------------------
init_session()
theme_css()

# -------------------------
# Ensure user is logged in and is a Company
# -------------------------
if not st.session_state.logged_in:
    st.warning("Please login first to view Applicants.")
    st.stop()

if st.session_state.user_type != "Company":
    st.warning("You are not a Company user. Access denied.")
    st.stop()

# -------------------------
# Page Header
# -------------------------
logo = load_logo()
if logo:
    st.image(logo, width=120)

st.title("📝 Applicant List")
st.subheader(f"Welcome, {st.session_state.username}!")

st.markdown("---")

# -------------------------
# Search resumes
# -------------------------
keyword = st.text_input("🔍 Search resumes by keyword (skills, technologies, etc.):")

all_results = []

if keyword:
    all_results = search_resumes(keyword)
    if not all_results:
        st.info(f"No resumes found containing '{keyword}'.")
else:
    # Show all uploaded resumes
    for user, files in st.session_state.uploaded_resumes.items():
        for f in files:
            all_results.append((user, f))

# -------------------------
# Display resumes
# -------------------------
if not all_results:
    st.info("No applicant resumes available yet.")
else:
    for idx, (username, resume) in enumerate(all_results):
        col1, col2 = st.columns([3,1])
        with col1:
            st.markdown(f"**{resume}** by **{username}**")
        with col2:
            if st.button("Preview 👀", key=f"preview_{idx}"):
                content = preview_resume(username, resume)
                st.markdown(f"""
                <div style="position:fixed; top:10%; left:10%; width:80%; height:80%; 
                            background:white; z-index:9999; border-radius:15px; 
                            box-shadow: 0 0 10px rgba(0,0,0,0.5); overflow:auto; padding:20px;">
                    <h2>{resume} - {username}</h2>
                    <pre style="white-space: pre-wrap;">{content}</pre>
                    <button onclick="this.parentElement.style.display='none'" 
                        style="padding:10px 20px; margin-top:10px;">Close</button>
                </div>
                """, unsafe_allow_html=True)

# -------------------------
# Back / Home button
# -------------------------
if st.button("⬅️ Back to Dashboard"):
    st.session_state['page'] = '3_Company_Home'
    st.experimental_rerun()

# -------------------------
# Logout
# -------------------------
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.user_type = None
    st.session_state.username = None
    st.experimental_rerun()
