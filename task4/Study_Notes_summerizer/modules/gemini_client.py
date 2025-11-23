
import os
import google.generativeai as genai

class GeminiClient:
    """
    A client for interacting with the Google Gemini API.
    """
    def __init__(self):
        """
        Initializes the Gemini client.
        It configures the API key and initializes the generative model.
        Raises:
            ValueError: If the GEMINI_API_KEY environment variable is not set.
        """
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key or self.api_key == "GEMINI_API_KEY":
            raise ValueError("GEMINI_API_KEY not found. Please set it in your .env file.")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def generate_content(self, prompt: str) -> str:
        """
        Generates content using the Gemini model.
        Args:
            prompt: The prompt to send to the model.
        Returns:
            The generated text content.
        Raises:
            Exception: If the API call fails.
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            # Log the full error for debugging
            print(f"Gemini API call failed: {e}")
            # Raise a more user-friendly error
            raise Exception("Failed to generate content from Gemini. Check your API key and network connection.")

