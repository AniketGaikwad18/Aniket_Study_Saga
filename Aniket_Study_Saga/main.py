import streamlit as st
import subprocess
import sys
import requests
from PIL import Image

# ✅ Fix Lottie Import
try:
    from streamlit_lottie import st_lottie
except ModuleNotFoundError:
    subprocess.run([sys.executable, "-m", "pip", "install", "streamlit-lottie==0.0.5"])
    from streamlit_lottie import st_lottie

# ✅ Import correct switch_page from extras
from streamlit_extras.switch_page_button import switch_page

# Config
st.set_page_config(page_title="Aniket’s Study Saga", layout="wide")

# Lottie loader
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

student_lottie = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_jtbfg2nb.json")

# UI
st.markdown("""
<h1 style='text-align: center; font-size: 4rem; color: #0072C6;'>Aniket’s Study Saga</h1>
<h3 style='text-align: center; font-family: cursive; color: #FF4B4B;'>Smart Prep for Smarter Students ✨</h3>
""", unsafe_allow_html=True)

st.success("👋 Welcome to Aniket’s Study Saga! Upload papers, get predictions, and ask anything!")

with st.expander("📌 Instructions"):
    st.markdown("""
    - Choose a subject
    - Upload **2 or more PDFs**
    - Get predicted questions
    - Download PDF or ask questions
    """)

col1, col2 = st.columns([1, 2])

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

with col2:
    st_lottie(student_lottie, height=400, key="studying")
