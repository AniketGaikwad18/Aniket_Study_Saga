# pages/analytics_page.py

import streamlit as st
import os
import re
from collections import Counter
import PyPDF2
import spacy

# Load spaCy English NLP model
nlp = spacy.load("en_core_web_sm")

st.set_page_config(page_title="Analytics - Aniket’s Study Saga", layout="wide")

st.markdown(
    "<h1 style='text-align: center; color: #FF5733;'>📊 Exam Concept Analytics</h1>",
    unsafe_allow_html=True,
)

st.markdown("""
This page analyzes predicted questions across subjects and extracts the most repeated **concepts**, not just keywords.
Make sure you've already generated prediction PDFs in each subject page.
""")

# Subjects to scan
subjects = [
    "Physics", "Chemistry", "Maths", "BEE", "BXE",
    "DBMS", "Computer Graphics", "Fundamentals of AIML", "Operating System"
]

def extract_text_from_pdf(file_path):
    text = ""
    try:
        reader = PyPDF2.PdfReader(file_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception as e:
        st.error(f"Error reading {file_path}: {e}")
    return text

# Collect all question text
all_questions = []

for subject in subjects:
    file_name = f"Predictionbyaniket_{subject.replace(' ', '_')}.pdf"
    if os.path.exists(file_name):
        st.subheader(f"📘 {subject}")
        pdf_text = extract_text_from_pdf(file_name)
        if not pdf_text.strip():
            st.warning("No readable text found in this PDF.")
            continue

        st.code(pdf_text, language="markdown")
        all_questions.extend([line.strip() for line in pdf_text.split("\n") if line.strip()])
    else:
        st.info(f"No prediction PDF found for **{subject}** yet.")

# ---------- Concept Extraction Using spaCy ----------
def extract_concepts(questions):
    all_noun_phrases = []
    for q in questions:
        doc = nlp(q)
        for chunk in doc.noun_chunks:
            concept = chunk.text.strip().lower()
            # Basic cleanup
            if len(concept) >= 4 and not concept.startswith("the "):
                all_noun_phrases.append(concept.title())
    return all_noun_phrases

concepts = extract_concepts(all_questions)
concept_freq = Counter(concepts)

# ---------- Display Top Concepts ----------
if concept_freq:
    st.subheader("🔍 Top 10 Repeated Concepts Across Subjects")
    for i, (concept, count) in enumerate(concept_freq.most_common(10), 1):
        st.write(f"{i}. **{concept}** — {count} times")
else:
    st.warning("⚠️ No concepts found. Try generating more meaningful predictions first.")
