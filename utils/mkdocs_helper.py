import os
import yaml
from datetime import datetime
from config import settings


def update_index():
    yaml_file = "mkdocs.yml"
    files = [
        f for f in os.listdir(settings.Settings.OUTPUT_DIR)
        if f.endswith(".md") and f != "index.md"
    ]

    try:
        with open(yaml_file, "r") as f:
            config = yaml.safe_load(f) or {}
    except FileNotFoundError:
        config = {}

    nav = config.get("nav", [])

    # Remove existing diary entries
    nav = [item for item in nav if not (
            isinstance(item, dict) and any("Diário oficial" in key for key in item)
    )]

    # Add new entries
    for file in sorted(files):
        try:
            date_str = file[:-3]
            formatted_date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%d/%m/%Y")
            nav.append({f"Diário oficial - {formatted_date}": f"{file}"})
        except ValueError:
            continue

    config["nav"] = nav

    with open(yaml_file, "w") as f:
        yaml.dump(config, f, allow_unicode=True, default_flow_style=False)