import pdfplumber
import re
from fpdf import FPDF
from collections import defaultdict

def extract_text_by_unit(pdf_files):
    """
    Extracts text from multiple PDFs and groups them by units (Unit I, Unit II, etc.)
    Returns a dictionary: {"Unit I": "text...", "Unit II": "text...", ...}
    """
    full_text = ""
    for pdf_file in pdf_files:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    full_text += page_text + "\n"

    # Split by units using a regex
    chunks = re.split(r'(Q[1-8][ab]?\))', full_text)



    unit_text = defaultdict(str)
    current_unit = None
    for part in chunks:
        part = part.strip()
        if re.match(r'(Q[1-8][ab]?\))', part):
            current_unit = part.upper().replace('–', '-').strip()
        elif current_unit:
            unit_text[current_unit] += part + "\n"

    return unit_text

def predict_questions_from_text(text, num_questions=3):
    """
    Improved question predictor that extracts exam-like questions from unit text.
    """
    sentences = re.split(r'(?<=[.?!])\s+', text)
    question_starters = ["what", "why", "explain", "describe", "how", "define", "compare", "state", "discuss", "differentiate"]

    potential_questions = []
    for sentence in sentences:
        sentence_clean = sentence.strip()
        if (
            any(sentence_clean.lower().startswith(q) for q in question_starters)
            or sentence_clean.endswith("?")
        ) and len(sentence_clean) > 30:
            potential_questions.append(sentence_clean)

    unique_questions = list(dict.fromkeys(potential_questions))[:num_questions]
    if len(unique_questions) < num_questions:
        extras = [s for s in sentences if len(s.strip()) > 50][:num_questions - len(unique_questions)]
        unique_questions.extend(extras)

    return unique_questions

def save_unitwise_questions_as_pdf(unit_questions_dict, subject_name):
    subject_clean = subject_name.replace(" ", "_")
    file_name = f"Predictionbyaniket.pdf"

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Predicted Questions - {subject_name}", ln=True, align='C')
    pdf.ln(5)

    for unit, questions in unit_questions_dict.items():
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(0, 10, unit, ln=True)
        pdf.set_font("Arial", size=11)
        for idx, question in enumerate(questions, 1):
            pdf.multi_cell(0, 10, f"{idx}. {question}")
        pdf.ln(3)

    pdf.output(file_name)
    return file_name
