# Study Notes Summarizer & Quiz Generator Agent

AI-powered system for converting PDFs into structured study notes and generating quizzes using **Gemini CLI**, **OpenAgents SDK**, **PyPDF**, **Streamlit**, and **Context7 MCP**.

---

##  Project Overview

This project helps students upload PDF files, extract clean text, generate well-organized summaries, and create quizzes based on the document. The app uses powerful AI tools to automate study preparation.

---

##  Main Features

### 1. PDF Summarizer

* Upload PDFs
* Text extraction using **PyPDF**
* Output includes:
  - Point-wise study notes
  - Organized summaries
  - Important concepts
  - Definitions & key ideas

### 2. Quiz Generator

Quizzes are generated from **original PDF text** (not summaries).

**Quiz Modes:**

- **MCQ Mode:** Question, four options, correct answer
- **Mixed Mode:** MCQs, True/False, Short-answer questions

---

##  Technology Stack

| Technology         | Role                                     |
| ------------------ | ---------------------------------------- |
| **Gemini CLI**     | AI orchestration                         |
| **OpenAgents SDK** | Agent logic & tool calling               |
| **Context7 MCP**   | Tool provider for filesystem & utilities |
| **PyPDF**          | PDF → Text extraction                    |
| **Streamlit**      | User interface                           |
| **Python 3.11+**   | Backend engine                           |

---

##  Project Structure

project/
│
├── gemini.md # Agent prompt for Gemini CLI
├── README.md # Documentation
├── app.py # Streamlit UI
│
├── modules/
│ ├── extractor.py # PDF text extraction
│ ├── summarizer.py # Summary generation
│ ├── quiz_mcq.py # MCQ quiz generator
│ ├── quiz_mixed.py # Mixed-format quiz generator
│
├── assets/
│ └── samples/ # Example PDF files
│
└── requirements.txt

yaml
Copy code

---

##  Workflow

1. **Upload PDF** → stored temporarily
2. **PyPDF extracts text** → cleaned and processed
3. **Agent creates summary** → structured notes
4. **"Create Quiz" button pressed** → agent generates MCQs or mixed quizzes
5. **Streamlit displays quiz** → user can review or export

---

##  How to Run

### Install Dependencies

```bash
pip install -r requirements.txt
Start Streamlit UI
bash
Copy code
streamlit run app.p
Run Gemini Agent
gemini run gemini.md

 Optional Deployment

Deploy on:

Streamlit Cloud

Railway

Vercel backend


