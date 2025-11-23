
"""
This module contains the logic for summarizing text using the Gemini AI model.
"""
import json
from dataclasses import dataclass
from modules.gemini_client import GeminiClient

@dataclass
class FileInfo:
    filename: str
    content: str

@dataclass
class SummarizerInput:
    file_info: FileInfo

class SummaryKernel:
    """A kernel for handling summarization tasks using Gemini."""

    def __init__(self):
        try:
            self.client = GeminiClient()
        except ValueError as e:
            # Propagate the error if the client fails to initialize (e.g., no API key)
            raise e

    def summarize(self, inputs: SummarizerInput) -> dict:
        """
        Generates a summary from the provided input using the Gemini model.
        """
        if not inputs.file_info.content:
            return {"title": "Error", "summary": "No text provided.", "keywords": []}

        prompt = f"""
        Based on the following text from the document '{inputs.file_info.filename}', please perform the following tasks:
        1. Create a concise and informative title for the document.
        2. Generate a detailed, point-wise summary of the key information.
        3. List the most important keywords (as a list of strings).

        Please provide the output in a single, clean JSON object with the following structure:
        {{
          "title": "Your Generated Title",
          "summary": "Your detailed, point-wise summary here.",
          "keywords": ["keyword1", "keyword2", "keyword3"]
        }}

        Here is the text:
        ---
        {inputs.file_info.content}
        ---
        """
        
        try:
            response_text = self.client.generate_content(prompt)
            # Clean the response to ensure it's valid JSON
            cleaned_json = response_text.strip().replace("```json", "").replace("```", "")
            return json.loads(cleaned_json)
        except Exception as e:
            # If JSON parsing fails or API call fails, return an error dictionary
            error_message = f"Failed to process AI response: {e}"
            print(error_message) # Log for debugging
            return {
                "title": "Error Generating Summary",
                "summary": "Could not parse the summary from the AI model. The response may have been malformed.",
                "keywords": []
            }

def generate_summary(text: str, filename: str) -> dict:
    """
    High-level function to generate a summary.
    """
    file_info = FileInfo(filename=filename, content=text)
    summarizer_input = SummarizerInput(file_info=file_info)
    try:
        kernel = SummaryKernel()
        return kernel.summarize(summarizer_input)
    except ValueError as e:
        # Handle the case where the kernel couldn't be initialized (e.g., API key missing)
        return {"title": "Configuration Error", "summary": str(e), "keywords": []}

