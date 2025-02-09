import os
from datetime import date
from config import settings


def save_summary(content: str, city: str, target_date: date) -> str:
    filename = f"{target_date.isoformat()}.md"
    os.makedirs(settings.Settings.OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(settings.Settings.OUTPUT_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return filepath