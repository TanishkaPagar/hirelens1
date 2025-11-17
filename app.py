# app.py
import streamlit as st
from utils import init_session, theme_css, load_logo

# -------------------------
# Initialize session and theme
# -------------------------
init_session()
theme_css()

# -------------------------
# Sidebar Logo
# -------------------------
logo = load_logo()
if logo:
    st.sidebar.image(logo, width=150)

# -------------------------
# App title and settings
# -------------------------
st.title("HireLens - Smart Resume Management & ATS")
st.sidebar.header("Settings")

# Theme toggle
theme_option = st.sidebar.radio("Select Theme", ["Light", "Dark"])
if theme_option.lower() != st.session_state.theme:
    st.session_state.theme = theme_option.lower()
    theme_css()

# -------------------------
# Pages mapping
# -------------------------
pages = {
    "Home": "pages/Home.py",
    "Login": "pages/1_Login.py",
    "Applicant Home": "pages/2_Applicant_Home.py",
    "Company Home": "pages/3_Company_Home.py",
    "Applicant List": "pages/4_Applicant_List.py",
    "Resume Upload": "pages/5_Resume_Upload.py",
    "Dataset Classifier": "pages/6_Dataset_Classifier.py",
    "ATS Score": "pages/7_ATS_Score.py",
    "Chat Module": "pages/8_Chat_Module.py",
    "My Resumes": "pages/My_Resumes.py",
    "Company Resume Classifier": "pages/9_Company_Resume_Classifier.py",
    "Settings": "pages/10_Settings.py"
}

# -------------------------
# Initialize current page
# -------------------------
if 'current_page' not in st.session_state:
    # Default to Login page if not logged in
    st.session_state.current_page = "Login" if not st.session_state.logged_in else "Home"

# -------------------------
# Sidebar Navigation
# -------------------------
st.sidebar.header("Navigation")
page_names = list(pages.keys())

# Only show allowed pages based on login
if st.session_state.logged_in:
    if st.session_state.user_type == "Applicant":
        allowed_pages = [
            "Home", "Applicant Home", "Resume Upload",
            "My Resumes", "ATS Score", "Chat Module", "Settings"
        ]
    elif st.session_state.user_type == "Company":
        allowed_pages = [
            "Home", "Company Home", "Applicant List",
            "Dataset Classifier", "Company Resume Classifier", "Settings", "Chat Module"
        ]
    else:
        allowed_pages = ["Home", "Settings"]
else:
    allowed_pages = ["Login", "Home", "SignUp"]

selected_page = st.sidebar.selectbox("Go to page:", allowed_pages, index=allowed_pages.index(st.session_state.current_page))

# Update current page
st.session_state.current_page = selected_page

# -------------------------
# Load page dynamically
# -------------------------
def load_page(page_file):
    try:
        with open(page_file, "r", encoding="utf-8") as f:
            code = f.read()
        exec(code, globals())
    except FileNotFoundError:
        st.error(f"Page {page_file} not found.")
    except Exception as e:
        st.error(f"Error loading {page_file}: {str(e)}")

# Load the selected page
load_page(pages[st.session_state.current_page])

# -------------------------
# Logout button
# -------------------------
if st.session_state.logged_in and st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.user_type = None
    st.session_state.current_page = "Login"  # Redirect to Login
