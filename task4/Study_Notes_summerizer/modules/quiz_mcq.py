
"""
This module contains the logic for generating MCQ quizzes using the Gemini AI model.
"""
import json
from dataclasses import dataclass
from modules.gemini_client import GeminiClient

@dataclass
class QuizInput:
    content: str
    num_questions: int = 5 # Increased default for better quizzes

class QuizKernel:
    """A kernel for handling MCQ quiz generation using Gemini."""

    def __init__(self):
        try:
            self.client = GeminiClient()
        except ValueError as e:
            raise e

    def generate_quiz(self, inputs: QuizInput) -> dict:
        """
        Generates an MCQ quiz using the Gemini model.
        """
        if not inputs.content:
            return {"questions": []}

        prompt = f"""
        Based on the text provided, generate a multiple-choice quiz with {inputs.num_questions} questions.
        For each question, provide four options (A, B, C, D) and indicate the correct answer.

        Return the output as a single, clean JSON object with a "questions" key.
        The value should be a list of question objects, each with this structure:
        {{
          "question": "The question text?",
          "options": {{
            "A": "Option A",
            "B": "Option B",
            "C": "Option C",
            "D": "Option D"
          }},
          "answer": "The letter of the correct answer (e.g., 'A')"
        }}

        Here is the text:
        ---
        {inputs.content}
        ---
        """
        
        try:
            response_text = self.client.generate_content(prompt)
            cleaned_json = response_text.strip().replace("```json", "").replace("```", "")
            return json.loads(cleaned_json)
        except Exception as e:
            print(f"Failed to process AI response for MCQ quiz: {e}")
            return {"questions": []}

def generate_mcq_quiz(text: str) -> dict:
    """
    High-level function to generate an MCQ quiz.
    """
    quiz_input = QuizInput(content=text)
    try:
        kernel = QuizKernel()
        return kernel.generate_quiz(quiz_input)
    except ValueError as e:
        # Return an error structure that the UI can handle
        return {"questions": [{"question": f"Configuration Error: {e}", "options": {}, "answer": ""}]}

