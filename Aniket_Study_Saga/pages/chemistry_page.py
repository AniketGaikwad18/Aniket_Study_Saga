import streamlit as st
from streamlit_lottie import st_lottie
import requests
import time
from utils.unitwise_prediction import extract_text_by_unit, predict_questions_from_text, save_unitwise_questions_as_pdf

# --- Load Lottie animations ---
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

rocket_lottie = load_lottie_url("https://assets6.lottiefiles.com/packages/lf20_w51pcehl.json")  # Rocket launch animation
thinking_lottie = load_lottie_url("https://assets4.lottiefiles.com/packages/lf20_touohxv0.json")  # Thinking animation

# --- Page config ---
st.set_page_config(page_title="Chemistry  - Aniket’s Study Saga", layout="wide")

# --- Page Heading with inline styles ---
st.markdown("""
<h1 style="
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 4rem;
    font-weight: 900;
    background: linear-gradient(90deg, #1e90ff, #00bfff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 2px 2px 5px rgba(0,0,0,0.3);
    margin-bottom: 0.5rem;
">
Chemistry
</h1>
""", unsafe_allow_html=True)

# --- Instructions ---
st.markdown("""
Upload **at least two PDF past papers** below. The app will analyze them and predict important questions **unit-wise** for your exam preparation.  
You can download the predicted questions as a PDF named **Predictionbyaniket_Physics.pdf**.  

""")
st.markdown("<h4 style='color:#9b59b6; font-weight:bold;'>📌 Every reaction matters. Chemistry is the magic of transformation – master it!</h4>", unsafe_allow_html=True)

# --- PDF Upload ---
uploaded_files = st.file_uploader(
    "Upload your Chemistry past paper PDFs (minimum 2):", type=["pdf"], accept_multiple_files=True
)

if uploaded_files and len(uploaded_files) >= 2:
    if st.button("Predict Unit-wise Questions"):
        with st.spinner("Analyzing and predicting questions for each unit..."):
            unit_texts = extract_text_by_unit(uploaded_files)
            unitwise_predictions = {}

            for unit, text in unit_texts.items():
                questions = predict_questions_from_text(text, num_questions=3)
                if questions:
                    unitwise_predictions[unit] = questions

            if unitwise_predictions:
                pdf_file_name = save_unitwise_questions_as_pdf(unitwise_predictions, subject_name="Chemistry")
                st.success(f"✅ PDF generated: {pdf_file_name}")

                # Download button
                with open(pdf_file_name, "rb") as f:
                    st.download_button(
                        label="Download Predicted Unit-wise Questions PDF",
                        data=f,
                        file_name=pdf_file_name,
                        mime="application/pdf",
                    )

                # Show predictions on screen
                st.subheader("📌 Predicted Questions by Unit")
                for unit, questions in unitwise_predictions.items():
                    st.markdown(f"### {unit}")
                    for idx, q in enumerate(questions, 1):
                        st.write(f"{idx}. {q}")
            else:
                st.warning("No unit-wise questions could be predicted. Try with better scanned or typed PDFs.")
else:
    if uploaded_files:
        st.warning("Please upload at least two PDF files for prediction.")

# --- Question & Answer Chat ---
st.subheader("Ask a Question")
question_input = st.text_input("Type your question here:")
if question_input:
    with st.spinner("Thinking..."):
        st_lottie(thinking_lottie, height=100, key="thinking_anim")
        time.sleep(2)
    st.markdown("**Answer:** Here's a placeholder answer until API is added.")

# --- Rocket animation bottom right ---
st.markdown("""
<style>
.rocket-container {
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 180px;
    height: 180px;
    z-index: 1000;
}
</style>
<div class="rocket-container"></div>
""", unsafe_allow_html=True)
st_lottie(rocket_lottie, height=180, key="rocket_anim")
