
import streamlit as st
from dotenv import load_dotenv
import os

from modules.extractor import extract_text_from_pdf
from modules.summarizer import generate_summary
from modules.quiz_mcq import generate_mcq_quiz
from modules.quiz_mixed import generate_mixed_quiz

# Load environment variables
load_dotenv()

def main():
    st.set_page_config(layout="wide")
    st.title("📝 AI Study Notes & Quiz Generator")

    # --- API Key Check ---
    api_key = os.getenv("GEMINI_API_KEY")
    api_key_valid = api_key and api_key != "GEMINI_API_KEY"
    
    if not api_key_valid:
        st.warning(
            "⚠️ Gemini API Key is not configured. "
            "Please create a `.env` file, add your `GEMINI_API_KEY`, and restart the app. "
            "AI features will be disabled."
        )

    # Initialize session state for managing quiz answers visibility
    if 'show_answers' not in st.session_state:
        st.session_state.show_answers = {}

    st.sidebar.header("Upload PDF")
    uploaded_file = st.sidebar.file_uploader("Upload your PDF document", type=["pdf"])

    if uploaded_file is not None:
        st.session_state.show_answers = {}
        st.sidebar.success("File Uploaded Successfully!")
        
        col1, col2 = st.columns(2)

        # --- Summarizer Column ---
        with col1:
            st.header("Summary & Study Notes")
            with st.spinner("Extracting text from PDF..."):
                try:
                    extracted_text = extract_text_from_pdf(uploaded_file)
                    st.text_area("Extracted Text (Snippet)", extracted_text[:500] + "...", height=100, disabled=True)
                except Exception as e:
                    st.error(f"Error extracting text: {e}")
                    extracted_text = None

            if st.button("Generate Study Notes", disabled=(not extracted_text or not api_key_valid)):
                with st.spinner("🤖 Calling Gemini to generate summary..."):
                    summary_data = generate_summary(extracted_text, uploaded_file.name)
                
                if "error" in summary_data.get("title", "").lower():
                    st.error(f"**{summary_data['title']}**: {summary_data['summary']}")
                else:
                    st.subheader(summary_data.get("title", "Summary"))
                    st.markdown(summary_data.get("summary", "Could not generate summary."))
                    st.write("**Keywords:**", ", ".join(summary_data.get("keywords", [])))

        # --- Quiz Column ---
        with col2:
            st.header("Quiz Yourself")
            if not extracted_text:
                st.info("Upload and process a PDF to generate a quiz.")
            else:
                quiz_mode = st.radio("Select Quiz Mode:", ("MCQ", "Mixed Format"))

                if st.button("Generate Quiz", disabled=(not api_key_valid)):
                    st.session_state.quiz_data = [] # Clear previous quiz
                    if quiz_mode == "MCQ":
                        spinner_text = "🤖 Calling Gemini to generate MCQ quiz..."
                        gen_function = generate_mcq_quiz
                    else:
                        spinner_text = "🤖 Calling Gemini to generate Mixed quiz..."
                        gen_function = generate_mixed_quiz
                    
                    with st.spinner(spinner_text):
                        quiz_data = gen_function(extracted_text)
                    
                    st.session_state.quiz_data = quiz_data.get("questions", [])

                if 'quiz_data' in st.session_state and st.session_state.quiz_data:
                    first_q = st.session_state.quiz_data[0]
                    if "error" in first_q.get("type", ""):
                         st.error(f"**{first_q['question']}**")
                    else:
                        for i, q in enumerate(st.session_state.quiz_data):
                            st.markdown(f"**Question {i+1} ({q.get('type', 'mcq').upper()})**: {q['question']}")
                            
                            if q.get('type', 'mcq') == 'mcq' and 'options' in q:
                                for key, value in q['options'].items():
                                    st.write(f"&nbsp;&nbsp;&nbsp;&nbsp;**{key}:** {value}")
                            
                            show_answer_key = f"q_{i}_show"
                            if st.button(f"Show Answer for Q{i+1}", key=f"btn_q_{i}"):
                                st.session_state.show_answers[show_answer_key] = True

                            if st.session_state.show_answers.get(show_answer_key):
                                st.success(f"**Answer:** {q['answer']}")
                            st.markdown("---")

    else:
        st.info("Upload a PDF file to begin.")

if __name__ == "__main__":
    main()
