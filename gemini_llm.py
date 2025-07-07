import os
import requests
from dotenv import load_dotenv
from langchain_core.language_models.llms import LLM
from pydantic import Field

# Load .env variables
load_dotenv()

class GeminiFlashLLM(LLM):
    api_key: str = Field(default_factory=lambda: os.getenv("GEMINI_API_KEY"))

    @property
    def _llm_type(self) -> str:
        return "gemini-2.0-flash"

    def _call(self, prompt: str, stop=None, run_manager=None):
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")

        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        headers = {
            "Content-Type": "application/json",
            "X-goog-api-key": self.api_key
        }
        data = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ]
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code != 200:
            raise Exception(f"Gemini API failed: {response.text}")

        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
