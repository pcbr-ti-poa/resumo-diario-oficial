# Coletor e Resumidor de Diários Oficiais

Sistema automático para coleta, processamento e resumo de diários oficiais do governo de Porto Alegre.

https://pcbr-ti-poa.github.io/resumo-diario-oficial/

## Funcionalidades

- **Coleta de PDFs**: Descoberta automática de diários diários
- **Resumos com IA**: Análise de documentos com GPT-3.5 Turbo/DeepSeek
- **Atualizações Diárias**: Geração automática de documentação com MkDocs
- **Suporte a Multiplos Provedores**: Alternância entre OpenAI e DeepSeek
- **Tolerância a Erros**: Lógica de repetição e tratamento abrangente

## Instalação

1. Clonar repositório:
```bash
git clone https://github.com/seuusuario/coletor-diarios.git
cd coletor-diarios
```

2. Instalar dependências:
```bash
pip install -r requirements.txt
```

3. Configurar variáveis de ambiente:
```bash
cp .env.example .env
# Edite .env com suas chaves de API
```

## Configuração

Variáveis de ambiente (`.env`):
```env
OPENAI_API_KEY=sk-sua-chave-aqui
DEEPSEEK_API_KEY=sk-sua-chave-aqui
```

## Uso

```bash
# Executar coletor principal
python main.py

# Atualizar índice de documentação
python -m utils.mkdocs_helper
```

## Arquitetura

```
├── config/          # Gerenciamento de configurações
├── core/            # Lógica principal e abstrações
├── scrapers/        # Coletores específicos por cidade
├── utils/           # Funções auxiliares
├── docs/            # Resumos gerados
└── main.py          # Ponto de entrada
```

## Como Contribuir

Para adicionar suporte a uma nova cidade:

1. **Criar novo coletor** no diretório `scrapers/`:
   ```python
   # scrapers/nova_cidade.py
   from core.base_scraper import BaseScraper
   from core.exceptions import PDFNotFoundError

   class NovaCidadeScraper(BaseScraper):
       INSTRUCOES_PERSONALIZADAS = "Instruções específicas para análise desta cidade..."
       
       def __init__(self, summary_provider, timezone):
           super().__init__(summary_provider, timezone)
           self.base_url = "<URL_DA_PREFEITURA_LOCAL>"

       def find_pdf_urls(self, target_date):
           # Implementar lógica específica de busca
           pass
   ```

2. **Adicionar URL base** no `config/settings.py`:
   ```python
   BASE_URLS = {
       "porto_alegre": "https://www2.portoalegre.rs.gov.br/dopa/",
       "nova_cidade": "<URL_DA_NOVA_CIDADE>"
   }
   ```

3. **Atualizar o main.py** para reconhecer a nova cidade:

4. **Enviar pull request** contendo:
   - Novo arquivo do coletor
   - Atualização do settings.py
   - Modificações no main.py
