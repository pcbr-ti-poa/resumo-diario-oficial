import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    TIMEZONE = "America/Sao_Paulo"
    OUTPUT_DIR = "docs"
    BASE_URLS = {
        "porto_alegre": "https://www2.portoalegre.rs.gov.br/dopa/"
    }


settings = Settings()