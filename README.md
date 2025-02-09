# Coletor e Resumidor de Diários Oficiais

Sistema automático para coleta, processamento e resumo de diários oficiais do governo de Porto Alegre.

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

## Contribuição

1. Crie novo coletor em `scrapers/`
2. Adicione URL base em `config/settings.py`
3. Implemente a interface BaseScraper
4. Envie um pull request