import os

def generate_index(directory, output_file):
    """
    Generates an index.html file that lists all files in the given directory.
    """
    # Ensure the directory exists
    if not os.path.exists(directory):
        raise FileNotFoundError(f"Directory not found: {directory}")

    # Get all files in the directory
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    # Generate HTML content
    html_content = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sumários de Porto Alegre</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
                line-height: 1.6;
            }
            h1 {
                color: #333;
            }
            ul {
                list-style-type: none;
                padding: 0;
            }
            li {
                margin: 10px 0;
            }
            a {
                text-decoration: none;
                color: #007BFF;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <h1>Sumários do Diário Oficial de Porto Alegre</h1>
        <ul>
    """

    # Add links to each file
    for file in sorted(files):  # Sort files alphabetically
        html_content += f'            <li><a href="{directory}/{file}">{file}</a></li>\n'

    html_content += """
        </ul>
    </body>
    </html>
    """

    # Save the generated HTML to the output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Index file generated: {output_file}")

# Example usage
summaries_dir = "docs/summaries/PortoAlegre"
index_file = "docs/index.html"
generate_index(summaries_dir, index_file)