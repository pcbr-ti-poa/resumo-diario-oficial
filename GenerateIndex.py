import os
import yaml  # PyYAML precisa estar instalado: pip install pyyaml
from datetime import datetime

def generate_index(directory, yaml_file):
    """
    Updates the mkdocs.yml file to include all files in the given directory under the navigation menu,
    formatting dates as DD/MM/YYYY and without modifying 'Apresentação'.
    """
    if not os.path.exists(directory):
        raise FileNotFoundError(f"Directory not found: {directory}")
    
    # Get all Markdown files in the directory, excluding "index.md"
    files = [f for f in os.listdir(directory) if f.endswith(".md") and f != "index.md"]

    if not files:
        print("No Markdown files found. Nothing to update.")
        return

    # Sort files alphabetically
    files.sort()

    # Load existing mkdocs.yml content
    if os.path.exists(yaml_file):
        with open(yaml_file, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}  # Load YAML safely, defaulting to empty dict
    else:
        config = {}

    # Ensure 'nav' key exists
    if "nav" not in config:
        config["nav"] = []

    # Preserve existing entries, except "Diário oficial"
    new_nav = []
    diario_entries = []

    for item in config["nav"]:
        # Remove apenas as antigas entradas de "Diário oficial"
        if isinstance(item, dict) and any("Diário oficial" in key for key in item.keys()):
            continue
        new_nav.append(item)

    # Gerar novas entradas para "Diário oficial" com data formatada DD/MM/YYYY
    for file in files:
        try:
            file_date = datetime.strptime(file[:-3], "%Y-%m-%d").strftime("%d/%m/%Y")
            diario_entries.append({f"Diário oficial - {file_date}": f"{file}"})
        except ValueError:
            print(f"⚠️ Aviso: O arquivo '{file}' não segue o formato YYYY-MM-DD e foi ignorado.")

    # Inserir novas entradas na navegação
    new_nav.extend(diario_entries)

    # Atualizar o config
    config["nav"] = new_nav

    # Escrever de volta no mkdocs.yml
    with open(yaml_file, "w", encoding="utf-8") as f:
        yaml.dump(config, f, allow_unicode=True, default_flow_style=False)

    print(f"Updated {yaml_file} with new Diário Oficial entries.")

# Exemplo de uso
yaml_file = "./mkdocs.yml"
generate_index('./docs', yaml_file)
