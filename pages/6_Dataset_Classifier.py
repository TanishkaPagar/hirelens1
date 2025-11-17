# 6_Dataset_Classifier.py
import streamlit as st
import pandas as pd
from utils import save_dataset, list_uploaded_resumes, load_logo, extract_text, score_resume, extract_skills_from_text

# -------------------------
# Ensure user is logged in and is a Company
# -------------------------
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first to access Dataset Classifier.")
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

st.title("📁 Dataset Classifier")
st.subheader(f"Welcome, {st.session_state.get('username', 'Company')}!")

# -------------------------
# Upload CSV Dataset
# -------------------------
st.markdown("---")
st.markdown("### Upload Applicant Dataset (CSV)")

uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.success(f"Dataset '{uploaded_file.name}' loaded successfully!")
        st.dataframe(df.head())

        # Save the dataset for this company
        save_dataset(uploaded_file, st.session_state['username'])

        st.markdown("### ATS Score Preview (Optional)")

        # Check if resumes are uploaded
        all_resumes = list_uploaded_resumes(st.session_state['username'])
        if all_resumes:
            for resume_name in all_resumes:
                st.markdown(f"**Resume: {resume_name}**")
                path_text = extract_text(open(f"uploaded_resumes/{st.session_state['username']}/{resume_name}", "rb"))
                required_skills = st.text_input(f"Enter skills to check for {resume_name} (comma-separated)", "Python,SQL,Excel")
                if st.button(f"Score {resume_name}"):
                    skills_list = [s.strip() for s in required_skills.split(",")]
                    score, skills_found = score_resume(path_text, skills_list)
                    st.write(f"✅ **Score:** {score}%")
                    st.write(f"🔹 Skills Found: {skills_found}")
        else:
            st.info("No resumes uploaded yet for scoring. Ask applicants to upload resumes first.")

    except Exception as e:
        st.error(f"Error reading CSV file: {e}")

# -------------------------
# Logout
# -------------------------
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.user_type = None
    st.session_state.username = None
    st.experimental_rerun()
