# 3_Company_Home.py
import streamlit as st
from utils import (
    init_session, theme_css, load_logo,
    save_dataset, list_uploaded_resumes, preview_resume
)
import os

# -------------------------
# Initialize session & theme
# -------------------------
init_session()
theme_css()

# -------------------------
# Ensure user is logged in and is a Company
# -------------------------
if not st.session_state.logged_in:
    st.warning("Please login first to access the Company Home.")
    st.stop()

if st.session_state.user_type != 'Company':
    st.warning("You are not a Company user. Access denied.")
    st.stop()

company_name = st.session_state.username

# -------------------------
# Page Header
# -------------------------
logo = load_logo()
if logo:
    st.image(logo, width=120)

st.title("🏢 Company Dashboard")
st.subheader(f"Welcome, {company_name}!")

st.markdown("---")

# -------------------------
# Upload Candidate Dataset
# -------------------------
st.subheader("Upload Candidate CSV")
uploaded_file = st.file_uploader("Choose CSV file", type=["csv"], key="upload_dataset")

if uploaded_file:
    save_dataset(uploaded_file, company_name)
    st.success(f"✅ Dataset '{uploaded_file.name}' uploaded successfully!")

st.markdown("---")

# -------------------------
# List uploaded datasets
# -------------------------
st.subheader("Your Uploaded Candidate Datasets")

dataset_file = st.session_state.dataset_files.get(company_name, None)

if not dataset_file:
    st.info("You have not uploaded any datasets yet.")
else:
    st.write(f"**Uploaded file:** {os.path.basename(dataset_file)}")
    if st.button("Preview Dataset 📄"):
        import pandas as pd
        df = pd.read_csv(dataset_file)
        st.dataframe(df)

st.markdown("---")

# -------------------------
# Quick Actions
# -------------------------
st.subheader("Quick Actions")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Upload Another CSV 📁"):
        st.session_state['page'] = '6_Dataset_Classifier'
        st.experimental_rerun()

with col2:
    if st.button("View Applicants List 📝"):
        st.session_state['page'] = '4_Applicant_List'
        st.experimental_rerun()

with col3:
    if st.button("Resume Classifier 🔍"):
        st.session_state['page'] = '9_Company_Resume_Classifier'
        st.experimental_rerun()

# -------------------------
# Logout
# -------------------------
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.user_type = None
    st.session_state.username = None
    st.experimental_rerun()
