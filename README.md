# 📋 GitHub Milestones MCP Server

Este projeto implementa um servidor **MCP** (Model Context Protocol) usando **FastAPI**, **LangChain** e **Google Gemini Flash 2**, para buscar milestones e issues de repositórios GitHub e gerar relatórios automáticos em **Markdown**.

---

## 🚀 Funcionalidades

- Buscar **milestones** de um repositório no GitHub.
- Buscar **issues** associadas a um milestone específico.
- Armazenar milestones e issues em **memória conversacional**.
- Gerar **relatórios em Markdown** automáticos usando os dados armazenados.
- Integração com **Google Gemini 1.5 Flash** para raciocínio rápido.
- Pronto para integração com agentes e fluxos inteligentes.
- Automatização de tarefas comuns com **Makefile**.

---

## 📦 Estrutura do Projeto

```
github-milestones-mcp/
├── main.py
├── mcp_server.py
├── requirements.txt
├── Makefile
├── .env
├── tools/
│   ├── __init__.py
│   ├── github_repository_tool.py
│   ├── github_issue_tool.py
│   ├── markdown_generator_tool.py
│   ├── generate_report_tool.py
```

---

## ⚙️ Pré-requisitos

- Python 3.12+
- Conta na [Google AI Studio](https://aistudio.google.com/) para obter uma **API Key do Gemini**.
- Token de acesso do GitHub (com permissão `repo` para repositórios privados, ou token classic para públicos).

---

## 🛠️ Instalação

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/github-milestones-mcp.git
cd github-milestones-mcp
```

2. Crie e ative seu ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Configure o arquivo `.env`:

```bash
GEMINI_API_KEY=your_google_gemini_api_key
GITHUB_TOKEN=your_github_token
```

---

## ▶️ Como Rodar

Execute o servidor FastAPI:

```bash
python main.py
```

O serviço estará disponível em:

```bash
http://localhost:3000/v1/mcp
```

---

## 📬 Como usar a API

### Buscar milestones de um repositório

```bash
curl -X POST http://localhost:3000/v1/mcp \
-H "Content-Type: application/json" \
-d '{"input": "Liste os milestones do repositório octocat/Hello-World"}'
```

### Buscar issues de um milestone

```bash
curl -X POST http://localhost:3000/v1/mcp \
-H "Content-Type: application/json" \
-d '{"input": "Liste as issues do milestone 1 do repositório octocat/Hello-World"}'
```

### Gerar um relatório em Markdown

```bash
curl -X POST http://localhost:3000/v1/mcp \
-H "Content-Type: application/json" \
-d '{"input": "me retone um relatório em Markdown do repositorio octocat/Hello-World"}'
```

```bash

curl -X POST http://localhost:3000/v1/mcp -H "Content-Type: application/json" -d '{"input": "me forneça o relatório do repositório octocat/Hello-World ordenado pelo numero do milestone e coloque as datas no formato brasileiro"}'
```



## ⚡ Automatização com Makefile

Este projeto inclui um **Makefile** para facilitar tarefas comuns de desenvolvimento:

### Comandos disponíveis:

| Comando          | Descrição                                      |
|:-----------------|:-----------------------------------------------|
| `make venv`      | Cria o ambiente virtual `.venv`                |
| `make install`   | Instala as dependências do projeto             |
| `make run`       | Sobe o servidor FastAPI localmente             |
| `make stop`      | Encerra o servidor (mata processos do Uvicorn) |
| `make test`      | Testa se o servidor está respondendo           |
| `make lint`      | Roda um lint (`flake8`) no código              |
| `make clean`     | Remove arquivos temporários (`__pycache__`)    |
| `make update`    | Atualiza as dependências para as versões mais recentes |

### Exemplo de uso:

```bash
make venv
make install
make run
```

E o servidor já estará rodando na porta 3000.

---

## 🧠 Memória Inteligente

O agente armazena dinamicamente:
- Todos os milestones e issues buscados.
- Ao solicitar a geração de relatório, a memória é usada automaticamente para montar o Markdown.

Não é necessário passar dados manualmente!

---

## 📋 Tecnologias Usadas

- [FastAPI](https://fastapi.tiangolo.com/) - API Server
- [LangChain](https://www.langchain.dev/) - Agente e Memory
- [Google Gemini 1.5 Flash](https://ai.google.dev/) - LLM ultra rápido
- [GitHub REST API](https://docs.github.com/en/rest) - Coleta de dados
- [Uvicorn](https://www.uvicorn.org/) - Servidor ASGI
- [Makefile](https://www.gnu.org/software/make/) - Automatização de tarefas

---

## 🛡️ Boas práticas aplicadas

- ✅ Separação de responsabilidades (cada Tool separada)
- ✅ Uso de memória conversacional (`ConversationBufferMemory`)
- ✅ Comunicação correta via `ainvoke` no LangChain
- ✅ Automatização com Makefile
- ✅ Estrutura limpa, modular e escalável

---

