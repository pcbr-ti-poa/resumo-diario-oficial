import io
import json
import re
import time
import random
import pytz
import openai
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pdfplumber
from scrapers.BaseScraper import BaseScraper

class PortoAlegreScraper(BaseScraper):
    def __init__(self, chatgpt_api_key):
        super().__init__()
        self.base_url = "https://www2.portoalegre.rs.gov.br/dopa/"
        self.tz = pytz.timezone("America/Sao_Paulo")
        self.chatgpt_api_key = chatgpt_api_key
        openai.api_key = chatgpt_api_key  # Set the API key for OpenAI

    def _extract_date_from_text(self, text):
        """Extract date from visible link text (DD/MM/YYYY format)"""
        date_pattern = r"\b(\d{1,2}/\d{1,2}/\d{4})\b"
        match = re.search(date_pattern, text)
        if match:
            try:
                return datetime.strptime(match.group(1), "%d/%m/%Y").date()
            except ValueError:
                pass
        return None

    def find_pdf_urls(self, date):
        """
        Find PDF URLs matching the date

        """
        # Uncomment the next two lines to use a fixed date for debugging
        # fixed_date = datetime.strptime("07/02/2025", "%d/%m/%Y").date()
        # today = fixed_date

        print(f"\n[DEBUG] Current Date (America/Sao_Paulo): {date.strftime('%d/%m/%Y')}")

        response = requests.get(self.base_url)
        soup = BeautifulSoup(response.text, "html.parser")
        pdf_urls = []

        print("[DEBUG] Found Links:")
        for idx, link in enumerate(soup.find_all("a")):
            link_text = link.text.strip()
            href = link.get("href")

            print(f"\nLink {idx + 1}:")
            print(f"Text: '{link_text}'")
            print(f"Href: '{href}'")

            if not href or not href.lower().endswith(".pdf"):
                print("Skipping: Not a PDF link")
                continue

            parsed_date = self._extract_date_from_text(link_text)
            print(f"Parsed Date: {parsed_date} (vs Date: {date})")

            if parsed_date == date:
                absolute_url = urljoin(self.base_url, href)
                print(f"✅ MATCH: Adding URL: {absolute_url}")
                pdf_urls.append(absolute_url)
            else:
                print("❌ Date mismatch")

        print(f"\n[DEBUG] Final PDF URLs: {pdf_urls}")
        return pdf_urls

    def fetch_pdf_content(self, url):
        """Download the PDF file from the given URL"""
        response = requests.get(url)
        response.raise_for_status()
        return response.content

    def extract_text(self, pdf_content):
        """Extract text from PDF content using pdfplumber"""
        text = ""
        with pdfplumber.open(io.BytesIO(pdf_content)) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text

    def chatgpt_summarize(self, text, prompt):
        # Combine the prompt instructions and the text into one user message.
        combined_content = f"{prompt}\n\n{text}"
        messages = [
            {"role": "user", "content": combined_content}
        ]

        max_retries = 5
        delay = 5

        for attempt in range(max_retries):
            try:
                response = openai.chat.completions.create(
                    model="o1-mini",
                    messages=messages,
                    temperature=1
                )
                # Access the message content using attribute notation
                return response.choices[0].message.content.strip()
            except openai.RateLimitError:
                wait_time = delay * (2 ** attempt)  # Exponential backoff
                print(f"Rate limit hit (attempt {attempt + 1}/{max_retries}). Sleeping for {wait_time} seconds...")
                time.sleep(wait_time)
            except openai.APIError as e:
                print(f"OpenAI API Error: {str(e)}")
                break
            except Exception as e:
                print(f"Unexpected error: {str(e)}")
                break

        raise RuntimeError("Failed to get a response from the ChatGPT API after multiple attempts.")

    def run(self):
        pages = []
        date = datetime(2025, 2, 7).date()
        """Main execution flow using the OpenAI API for summarization"""
        try:
            pdf_urls = self.find_pdf_urls(date)
            if not pdf_urls:
                raise self.NoPdfFoundError(f"No PDF found for {date}")

            for idx, url in enumerate(pdf_urls):
                try:
                    print(f"\n=== Processing PDF {idx + 1} ===")
                    print(f"URL: {url}")

                    # Process PDF content
                    pdf_content = self.fetch_pdf_content(url)
                    print(f"PDF Size: {len(pdf_content)} bytes")  # Verify download

                    # Extract text
                    text = self.extract_text(pdf_content)
                    print(f"\nExtracted Text (First 200 chars):\n{text[:200]}...")
                    print(f"Total Text Length: {len(text)} characters")

                    # Generate summary
                    print("\nCalling ChatGPT API (o1-mini)...")
                    summary = self.chatgpt_summarize(
                        text,
                        "Você é um oficial do governo e seu cargo é analizar documentos da prefeitura de Porto Alegre. "
                        "Resuma este diário oficial completo de forma que uma pessoa possa ler apenas o resumo e estar informada do seu conteúdo. "
                        "Qualquer tipo de alteração de efetivo, contratação ou compra deve estar listada com valores, unidades, pesoas envolvidas e descrição. "
                        "Preste muita atenção a precisão das informações, você é um agente do governo e não pode errar os resumos, revise-os múltiplas vezes. "
                    )
                    print(f"\nGenerated Summary:\n{summary}")
                    pages.append(summary)
                except Exception as e:
                    raise self.DeepSeekAPIError(f"Error processing {url}: {str(e)}")
            joined_summary = "\n\n".join(pages)
            self.save_summary(joined_summary, "PortoAlegre", date)
            return True

        except self.NoPdfFoundError:
            raise

        except Exception as e:
            raise RuntimeError(f"Unexpected error: {str(e)}")
