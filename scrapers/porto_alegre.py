import re
from datetime import datetime, date
from typing import List
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from core.base_scraper import BaseScraper
from core.exceptions import PDFNotFoundError
from config import settings

class PortoAlegreScraper(BaseScraper):
    CUSTOM_INSTRUCTIONS = (
        "Você é um oficial do governo analisando documentos da prefeitura de Porto Alegre. "
        "Resuma este diário oficial completo de forma clara e precisa. "
        "Destaque alterações de efetivo, contratações e compras com valores, unidades e pessoas envolvidas. "
        "Revise cuidadosamente para garantir precisão absoluta das informações."
    )

    def __init__(self, summary_provider, timezone: str):
        super().__init__(summary_provider, timezone)
        self.base_url = settings.Settings.BASE_URLS["porto_alegre"]

    def find_pdf_urls(self, target_date: date) -> List[str]:
        try:
            response = requests.get(self.base_url)
            soup = BeautifulSoup(response.text, "html.parser")
            pdf_urls = []

            for link in soup.find_all("a"):
                href = link.get("href")
                link_text = link.text.strip()

                if not href or not href.lower().endswith(".pdf"):
                    continue

                if self._date_matches(link_text, target_date):
                    absolute_url = urljoin(self.base_url, href)
                    pdf_urls.append(absolute_url)

            return pdf_urls

        except Exception as e:
            raise PDFNotFoundError(f"Error finding PDFs: {str(e)}")

    def _date_matches(self, text: str, target_date: date) -> bool:
        match = re.search(r"\b(\d{1,2}/\d{1,2}/\d{4})\b", text)
        if match:
            try:
                parsed_date = datetime.strptime(match.group(1), "%d/%m/%Y").date()
                return parsed_date == target_date
            except ValueError:
                return False
        return False

    def _get_instructions(self) -> str:
        return self.CUSTOM_INSTRUCTIONS