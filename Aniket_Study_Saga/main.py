import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_extras.switch_page_button import switch_page
import requests

# --- Page Config ---
st.set_page_config(page_title="Aniket’s Study Saga", layout="wide")

# --- Load Lottie animation from URL ---
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

student_lottie = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_jtbfg2nb.json")

# --- Title & Tagline ---
st.markdown("""
<h1 style='text-align: center; font-size: 4rem; color: #0072C6;'>Aniket’s Study Saga</h1>
<h3 style='text-align: center; font-family: cursive; color: #FF4B4B;'>Smart Prep for Smarter Students ✨</h3>
""", unsafe_allow_html=True)

# --- Welcome Message ---
st.success("👋 Welcome to Aniket’s Study Saga! Upload past papers, get predictions, and ask anything!")

# --- Instructions ---
with st.expander("📌 Instructions"):
    st.markdown("""
    - Choose a subject from below.
    - Upload **at least two PDFs** of previous year papers.
    - AI will predict possible exam questions.
    - You can also ask questions and get AI-generated answers.
    - Predictions are downloadable as PDF.
    """)

# --- Layout with Two Columns ---
col1, col2 = st.columns([1, 2])

# --- Subject Buttons (Left Column) ---
with col1:
    st.subheader("📚 Select a Subject")

    subject_pages = {
        "Physics": "physics_page",
        "Chemistry": "chemistry_page",
        "Maths": "maths_page",
        "BEE": "bee_page",
        "BXE": "bxe_page",
        "DBMS": "dbms_page",
        "Computer Graphics": "cg_page",
        "Fundamentals of AIML": "faiml_page",
        "OS": "os_page",
        "Analytics": "analytics_page"
    }

    for subject, page in subject_pages.items():
        if st.button(subject):
            switch_page(page)

# --- Animation (Right Column) ---
with col2:
    if student_lottie:
        st_lottie(student_lottie, height=400, key="studying")
    else:
        st.info("📎 Lottie animation could not load.")
