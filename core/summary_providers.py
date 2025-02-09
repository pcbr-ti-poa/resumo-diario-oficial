import time
import openai
import requests
from typing import Optional
from core.exceptions import APIError


class SummaryProvider:
    def summarize(self, text: str, instructions: str) -> str:
        raise NotImplementedError


class DeepSeekProvider(SummaryProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.deepseek.com/v1/chat/completions"

    def summarize(self, text: str, instructions: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "deepseek-chat",
            "messages": [{
                "role": "user",
                "content": f"{instructions}\n\n{text}"
            }]
        }

        for attempt in range(5):
            try:
                response = requests.post(self.base_url, headers=headers, json=data)
                response.raise_for_status()
                return response.json()["choices"][0]["message"]["content"]
            except requests.exceptions.RequestException as e:
                if attempt == 4:
                    raise APIError(f"DeepSeek API failed: {str(e)}")
                time.sleep(2 ** attempt)


class OpenAiProvider(SummaryProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key
        openai.api_key = api_key

    def summarize(self, text: str, instructions: str) -> str:
        messages = [{
            "role": "user",
            "content": f"{instructions}\n\n{text}"
        }]

        for attempt in range(5):
            try:
                response = openai.chat.completions.create(
                    model="o1-mini",
                    messages=messages,
                    temperature=1
                )
                return response.choices[0].message.content.strip()
            except openai.APIError as e:
                if attempt == 4:
                    raise APIError(f"OpenAI API failed: {str(e)}")
                time.sleep(2 ** attempt)