import pdfplumber
import re
from collections import Counter

def extract_text_from_multiple_pdfs(pdf_files):
    """Extract text from multiple PDFs using pdfplumber"""
    combined_text = ""
    for pdf_file in pdf_files:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    combined_text += text + "\n"
    return combined_text

def predict_questions(text, num_questions=10):
    """
    Improved question predictor using real sentence analysis.
    """
    sentences = re.split(r'(?<=[.?!])\s+', text)

    question_starters = ["what", "why", "explain", "describe", "how", "define", "compare", "state", "discuss", "differentiate"]

    potential_questions = []
    
    for sentence in sentences:
        sentence_clean = sentence.strip()
        if (
            any(sentence_clean.lower().startswith(q) for q in question_starters) or
            sentence_clean.endswith("?")
        ) and len(sentence_clean) > 30:
            potential_questions.append(sentence_clean)

    unique_questions = list(dict.fromkeys(potential_questions))[:num_questions]

    if len(unique_questions) < num_questions:
        extras = [s for s in sentences if len(s.strip()) > 50][:num_questions - len(unique_questions)]
        unique_questions.extend(extras)

    return unique_questions
