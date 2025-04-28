# Nome do projeto
PROJECT_NAME=github-milestones-mcp

# Variáveis padrão
PYTHON=python
PIP=pip
VENV=.venv
UVICORN=uvicorn

# Arquivo principal para rodar
MAIN=main.py

# Criação do ambiente virtual
venv:
	@$(PYTHON) -m venv $(VENV)
	@echo "Virtual environment created."

# Ativar o ambiente virtual (para Linux/Mac)
activate:
	@source $(VENV)/bin/activate

# Instalar as dependências
install:
	@$(PIP) install -r requirements.txt
	@echo "Dependências instaladas."

# Rodar o servidor localmente
run:
	@$(UVICORN) mcp_server:app --host 0.0.0.0 --port 3000 --reload

# Parar o servidor (caso esteja rodando em background, customizável)
stop:
	@pkill -f "uvicorn" || echo "Nenhum servidor rodando."

# Rodar testes básicos (pode expandir futuramente)
test:
	@echo "Testando servidor..."
	@curl -X POST http://localhost:3000/v1/mcp -H "Content-Type: application/json" -d '{"input": "Olá, MCP server!"}' || echo "Servidor não está respondendo."

# Rodar lint
lint:
	@echo "Rodando flake8 para verificar padrões de código..."
	@flake8 . || echo "Linting completo."

# Limpar arquivos desnecessários
clean:
	@find . -type d -name "__pycache__" -exec rm -r {} +
	@echo "Arquivos temporários removidos."

# Atualizar pacotes
update:
	@$(PIP) install --upgrade pip
	@$(PIP) install --upgrade -r requirements.txt
	@echo "Dependências atualizadas."
test:
	PYTHONPATH=src pytest src/
