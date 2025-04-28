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
.
├── docker-compose.yml
├── Dockerfile
├── LICENSE
├── makefile
├── README.md
├── requirements.txt
├── src
│   ├── agents
│   │   ├── agent.py
│   │   ├── __init__.py
│   ├── application.py
│   ├── __init__.py
│   ├── mcp_server.py
│   ├── repository
│   │   ├── github_issue_repository.py
│   │   ├── github_milestone_repository.py
│   │   ├── github_project_repository.py
│   │   ├── __init__.py
│   ├── service
│   │   ├── github_issue_service.py
│   │   ├── github_milestone_service.py
│   │   ├── github_project_service.py
│   │   ├── github_repository_service.py
│   │   ├── __init__.py
│   ├── test
│   │   ├── __init__.py
│   │   ├── test_repository_project.py
│   │   ├── test_repositoy_issue.py
│   │   ├── test_repositoy_milestone.py
│   │   ├── test_service_issue .py
│   │   ├── test_service_milestone .py
│   │   └── test_service_project.py
│   └── tools
│       ├── __init__.py
│       ├── project
│       │   ├── generate_projects_report_tool.py
│       │   ├── github_projects_tool.py
│       │   ├── __init__.py
│       │   ├── list_projects_cards_milestones_tool.py
│       └── repository
│           ├── generate_developer_report_tool.py
│           ├── generate_report_tool.py
│           ├── github_issue_tool.py
│           ├── github_milestones_tool.py
│           ├── __init__.py
│           ├── list_all_milestones_and_issues_tool.py
│   
```

### 📁 Estrutura do Projeto

O projeto está organizado da seguinte maneira:

| Pasta/Arquivo | Descrição |
|:---|:---|
| `src/application.py` | Arquivo principal que inicia o servidor da aplicação. |
| `src/mcp_server.py` | Define o servidor FastAPI e as rotas da aplicação. |
| `src/agents/` | Código dos agentes responsáveis por orquestrar tarefas automáticas. |
| `src/repository/` | Código para buscar dados diretamente da API do GitHub (issues, projetos, milestones). |
| `src/service/` | Regras de negócio e processamento dos dados obtidos do GitHub. |
| `src/test/` | Testes automáticos para validar os repositórios e serviços. |
| `src/tools/` | Ferramentas para gerar relatórios e consultas específicas nos dados do GitHub. |

### 📄 Tabela de Arquivos do Projeto

| Arquivo | Explicação |
|:--------------|:-----------|
| `docker-compose.yml` | Define como rodar a aplicação em containers Docker, mapeando porta e volumes. |
| `Dockerfile` | Descreve como construir a imagem Docker da aplicação. |
| `LICENSE` | Arquivo de licença legal do projeto (ex: MIT, Apache 2.0). |
| `makefile` | Define comandos simplificados como `make build`, `make up`, `make test`. |
| `README.md` | Documentação principal do projeto, explicando instalação e uso. |
| `requirements.txt` | Lista todas as bibliotecas Python necessárias para instalar a aplicação. |
| `src/application.py` | Arquivo que inicia o servidor FastAPI usando Uvicorn. |
| `src/mcp_server.py` | Contém a instância `app` da FastAPI e as configurações de rotas. |
| `src/agents/agent.py` | Define agentes que executam tarefas automáticas ou fluxos inteligentes. |
| `src/repository/github_issue_repository.py` | Código para buscar dados de **issues** diretamente da API do GitHub. |
| `src/repository/github_milestone_repository.py` | Código para buscar dados de **milestones** da API do GitHub. |
| `src/repository/github_project_repository.py` | Código para buscar dados de **projetos** da API do GitHub. |
| `src/service/github_issue_service.py` | Aplica regras de negócio sobre **issues** obtidas do repositório. |
| `src/service/github_milestone_service.py` | Aplica regras de negócio sobre **milestones**. |
| `src/service/github_project_service.py` | Aplica regras de negócio sobre **projetos**. |
| `src/service/github_repository_service.py` | Regras sobre operações relacionadas a **repositórios** GitHub. |
| `src/test/test_repository_project.py` | Testes automáticos para o repositório de projetos. |
| `src/test/test_repositoy_issue.py` | Testes automáticos para o repositório de issues. |
| `src/test/test_repositoy_milestone.py` | Testes automáticos para o repositório de milestones. |
| `src/test/test_service_issue.py` | Testes das regras de negócio aplicadas a issues. |
| `src/test/test_service_milestone.py` | Testes das regras de negócio aplicadas a milestones. |
| `src/test/test_service_project.py` | Testes das regras de negócio aplicadas a projetos. |
| `src/tools/project/generate_projects_report_tool.py` | Ferramenta para gerar relatórios automáticos de projetos GitHub. |
| `src/tools/project/github_projects_tool.py` | Ferramenta para consultar dados detalhados de projetos. |
| `src/tools/project/list_projects_cards_milestones_tool.py` | Ferramenta para listar cartões e milestones de projetos. |
| `src/tools/repository/generate_developer_report_tool.py` | Gera relatórios focados nos desenvolvedores. |
| `src/tools/repository/generate_report_tool.py` | Ferramenta genérica para criar relatórios a partir dos dados. |
| `src/tools/repository/github_issue_tool.py` | Operações específicas para issues do GitHub. |
| `src/tools/repository/github_milestones_tool.py` | Operações específicas para milestones do GitHub. |
| `src/tools/repository/list_all_milestones_and_issues_tool.py` | Lista todas milestones e issues associadas de um projeto. |


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

## 🧪 Rodando os Testes

Para rodar todos os testes automatizados do projeto, basta usar o comando:

```bash
make test
```

Esse comando executa todos os testes localizados na pasta `src/test/`, validando o funcionamento dos repositórios, serviços e ferramentas da aplicação.

✅ Antes de rodar, certifique-se de:
- Ter o ambiente configurado (bibliotecas instaladas via `requirements.txt`).
- Estar dentro do diretório raiz do projeto.
- Ter o Docker (caso alguns testes dependam de serviços externos).

---

## 📋 Sobre o comando `make test`

No `makefile`, o comando `make test` provavelmente executa algo como:

```bash
pytest src/test
```
ou
```bash
python -m unittest discover src/test
```

Assim, todos os arquivos de teste que seguem o padrão `test_*.py` serão automaticamente encontrados e executados.

---


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

