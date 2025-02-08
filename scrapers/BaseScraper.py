import os
import requests
from datetime import datetime
from io import BytesIO
from pypdf import PdfReader
from dotenv import load_dotenv

load_dotenv()

class NoPdfFoundError(Exception):
    """Raised when no PDF is found for the current day"""
    pass

class DeepSeekAPIError(Exception):
    """Raised when the DeepSeek API returns an error"""
    pass

class BaseScraper:
    def __init__(self):
        self.deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")

    class NoPdfFoundError(Exception):
        """Raised when no PDF is found for the current day"""
        pass

    class DeepSeekAPIError(Exception):
        """Raised when the DeepSeek API returns an error"""
        pass

    def fetch_pdf_content(self, url):
        """Fetch PDF bytes from URL"""
        response = requests.get(url)
        response.raise_for_status()
        return response.content

    def extract_text(self, pdf_content):
        """Extract text from in-memory PDF bytes"""
        text = ""
        reader = PdfReader(BytesIO(pdf_content))
        for page in reader.pages:
            text += page.extract_text()
        return text

    def summarize(self, text, instructions):
        """Generate summary using DeepSeek API"""
        headers = {
            "Authorization": f"Bearer {self.deepseek_api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "deepseek-chat",
            "messages": [{
                "role": "user",
                "content": f"{instructions}\n\n{text[:3000]}"  # Truncate to avoid token limits
            }]
        }

        try:
            response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers=headers,
                json=data
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            raise self.DeepSeekAPIError(f"API request failed: {str(e)}")

    def save_summary(self, summary, city, date):
        """Save the summary as an MD file."""

        filename = f"docs/{date}"""

        filename += ".md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(summary)
        print(f"Summary saved to {filename}")