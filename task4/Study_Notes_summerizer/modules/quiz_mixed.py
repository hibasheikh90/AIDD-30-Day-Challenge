
"""
This module contains the logic for generating mixed-format quizzes using the Gemini AI model.
"""
import json
from dataclasses import dataclass
from modules.gemini_client import GeminiClient

@dataclass
class QuizInput:
    content: str
    num_questions: int = 5 # Increased default for better quizzes

class QuizKernel:
    """A kernel for handling mixed-format quiz generation using Gemini."""

    def __init__(self):
        try:
            self.client = GeminiClient()
        except ValueError as e:
            raise e

    def generate_quiz(self, inputs: QuizInput) -> dict:
        """
        Generates a mixed-format quiz using the Gemini model.
        """
        if not inputs.content:
            return {"questions": []}

        prompt = f"""
        Based on the text provided, generate a mixed-format quiz with {inputs.num_questions} questions.
        The quiz should include a mix of "mcq", "true_false", and "short_answer" questions.

        Return the output as a single, clean JSON object with a "questions" key.
        The value should be a list of question objects. Use the following structures for each type:
        
        For "mcq":
        {{
          "type": "mcq",
          "question": "The question text?",
          "options": {{ "A": "Option A", "B": "Option B", "C": "Option C" }},
          "answer": "The letter of the correct answer (e.g., 'B')"
        }}

        For "true_false":
        {{
          "type": "true_false",
          "question": "A statement that is either true or false.",
          "answer": "True" or "False"
        }}

        For "short_answer":
        {{
          "type": "short_answer",
          "question": "A question requiring a brief explanation.",
          "answer": "A concise and correct answer."
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
            print(f"Failed to process AI response for mixed quiz: {e}")
            return {"questions": []}

def generate_mixed_quiz(text: str) -> dict:
    """
    High-level function to generate a mixed-format quiz.
    """
    quiz_input = QuizInput(content=text)
    try:
        kernel = QuizKernel()
        return kernel.generate_quiz(quiz_input)
    except ValueError as e:
        # Return an error structure that the UI can handle
        return {"questions": [{"type": "error", "question": f"Configuration Error: {e}", "answer": ""}]}

