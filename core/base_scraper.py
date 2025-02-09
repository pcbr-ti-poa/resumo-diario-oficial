import io
from abc import ABC, abstractmethod
from datetime import date
import pdfplumber
import requests
from core.exceptions import PDFNotFoundError, PDFProcessingError

class BaseScraper(ABC):
    def __init__(self, summary_provider, timezone: str):
        self.summary_provider = summary_provider
        self.timezone = timezone

    @abstractmethod
    def find_pdf_urls(self, target_date: date) -> list[str]:
        pass

    def process_pdf(self, pdf_content: bytes) -> str:
        try:
            text = ""
            with pdfplumber.open(io.BytesIO(pdf_content)) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            raise PDFProcessingError(f"PDF processing failed: {str(e)}")

    def fetch_pdf(self, url: str) -> bytes:
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            raise PDFProcessingError(f"Failed to fetch PDF: {str(e)}")

    def run(self, target_date: date) -> str:
        pdf_urls = self.find_pdf_urls(target_date)
        if not pdf_urls:
            raise PDFNotFoundError(f"No PDFs found for {target_date}")

        summaries = []
        for url in pdf_urls:
            try:
                content = self.fetch_pdf(url)
                text = self.process_pdf(content)
                summary = self.summary_provider.summarize(
                    text, self._get_instructions()
                )
                summaries.append(summary)
            except Exception as e:
                raise PDFProcessingError(f"Error processing {url}: {str(e)}")

        return "\n\n".join(summaries)

    def _get_instructions(self) -> str:
        return "Resume this document accurately:"