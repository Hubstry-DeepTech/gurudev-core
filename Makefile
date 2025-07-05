# Makefile para Alexandria: Biblioteca de Interoperabilidade e Programação Comparada

.PHONY: help install install-dev test lint format clean build docs run-example

# Variáveis
PYTHON = python3
PIP = pip3
PROJECT_NAME = alexandria-lang
VERSION = 0.1.0

# Cores para output
RED = \033[0;31m
GREEN = \033[0;32m
YELLOW = \033[1;33m
BLUE = \033[0;34m
NC = \033[0m # No Color

help: ## Mostra esta ajuda
	@echo "$(BLUE)🏛️ Alexandria: Biblioteca de Interoperabilidade e Programação Comparada$(NC)"
	@echo "$(YELLOW)Comandos disponíveis:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}'

install: ## Instala a biblioteca em modo desenvolvimento
	@echo "$(BLUE)📦 Instalando Alexandria em modo desenvolvimento...$(NC)"
	$(PIP) install -e .
	@echo "$(GREEN)✅ Instalação concluída!$(NC)"

install-dev: ## Instala dependências de desenvolvimento
	@echo "$(BLUE)🔧 Instalando dependências de desenvolvimento...$(NC)"
	$(PIP) install -e ".[dev]"
	@echo "$(GREEN)✅ Dependências de desenvolvimento instaladas!$(NC)"

test: ## Executa os testes
	@echo "$(BLUE)🧪 Executando testes...$(NC)"
	pytest tests/ -v --cov=alexandria --cov-report=html --cov-report=term
	@echo "$(GREEN)✅ Testes concluídos!$(NC)"

test-quick: ## Executa testes rapidamente (sem coverage)
	@echo "$(BLUE)⚡ Executando testes rápidos...$(NC)"
	pytest tests/ -v
	@echo "$(GREEN)✅ Testes rápidos concluídos!$(NC)"

lint: ## Executa verificação de código
	@echo "$(BLUE)🔍 Verificando código...$(NC)"
	flake8 alexandria/ tests/ --max-line-length=88 --ignore=E203,W503
	mypy alexandria/ --ignore-missing-imports
	@echo "$(GREEN)✅ Verificação de código concluída!$(NC)"

format: ## Formata o código
	@echo "$(BLUE)🎨 Formatando código...$(NC)"
	black alexandria/ tests/ --line-length=88
	isort alexandria/ tests/ --profile=black
	@echo "$(GREEN)✅ Formatação concluída!$(NC)"

clean: ## Limpa arquivos temporários
	@echo "$(BLUE)🧹 Limpando arquivos temporários...$(NC)"
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf build/ dist/ htmlcov/ .coverage
	@echo "$(GREEN)✅ Limpeza concluída!$(NC)"

build: ## Constrói o pacote
	@echo "$(BLUE)🔨 Construindo pacote...$(NC)"
	$(PYTHON) -m build
	@echo "$(GREEN)✅ Construção concluída!$(NC)"

docs: ## Gera documentação
	@echo "$(BLUE)📚 Gerando documentação...$(NC)"
	cd docs && make html
	@echo "$(GREEN)✅ Documentação gerada!$(NC)"

run-example: ## Executa o exemplo básico
	@echo "$(BLUE)🚀 Executando exemplo básico...$(NC)"
	$(PYTHON) examples/basic_usage.py
	@echo "$(GREEN)✅ Exemplo executado!$(NC)"

check: ## Executa todas as verificações
	@echo "$(BLUE)🔍 Executando todas as verificações...$(NC)"
	$(MAKE) format
	$(MAKE) lint
	$(MAKE) test
	@echo "$(GREEN)✅ Todas as verificações concluídas!$(NC)"

release: ## Prepara release (formata, testa, constrói)
	@echo "$(BLUE)🚀 Preparando release...$(NC)"
	$(MAKE) clean
	$(MAKE) format
	$(MAKE) lint
	$(MAKE) test
	$(MAKE) build
	@echo "$(GREEN)✅ Release preparado!$(NC)"

install-cli: ## Instala o CLI globalmente
	@echo "$(BLUE)📦 Instalando CLI globalmente...$(NC)"
	$(PIP) install -e . --force-reinstall
	@echo "$(GREEN)✅ CLI instalado! Use 'alexandria --help' para ver os comandos$(NC)"

demo: ## Executa demonstração completa
	@echo "$(BLUE)🎭 Executando demonstração completa...$(NC)"
	@echo "$(YELLOW)1. Listando linguagens disponíveis:$(NC)"
	alexandria list-languages
	@echo "$(YELLOW)2. Comparando Python e Rust:$(NC)"
	alexandria compare --source Python --target Rust
	@echo "$(YELLOW)3. Mapeando tipos Python para Rust:$(NC)"
	alexandria map-types --source python --target rust
	@echo "$(GREEN)✅ Demonstração concluída!$(NC)"

# Comandos específicos para desenvolvimento
dev-setup: ## Configuração completa para desenvolvimento
	@echo "$(BLUE)⚙️ Configurando ambiente de desenvolvimento...$(NC)"
	$(MAKE) install-dev
	$(MAKE) install-cli
	$(MAKE) run-example
	@echo "$(GREEN)✅ Ambiente de desenvolvimento configurado!$(NC)"

# Comandos para CI/CD
ci: ## Comandos para CI/CD
	@echo "$(BLUE)🔄 Executando pipeline CI/CD...$(NC)"
	$(MAKE) format
	$(MAKE) lint
	$(MAKE) test
	$(MAKE) build
	@echo "$(GREEN)✅ Pipeline CI/CD concluído!$(NC)"

# Comandos para análise
analyze: ## Análise estática do código
	@echo "$(BLUE)🔬 Análise estática do código...$(NC)"
	bandit -r alexandria/ -f json -o bandit-report.json || true
	safety check || true
	@echo "$(GREEN)✅ Análise estática concluída!$(NC)"

# Comandos para documentação
docs-serve: ## Serve documentação localmente
	@echo "$(BLUE)🌐 Servindo documentação localmente...$(NC)"
	cd docs/_build/html && python -m http.server 8000
	@echo "$(GREEN)✅ Documentação disponível em http://localhost:8000$(NC)"

# Comandos para dados
update-languages: ## Atualiza dados de linguagens
	@echo "$(BLUE)📊 Atualizando dados de linguagens...$(NC)"
	$(PYTHON) -c "from alexandria.core.analyzer import LanguageAnalyzer; analyzer = LanguageAnalyzer(); print(f'Linguagens carregadas: {len(analyzer.list_languages())}')"
	@echo "$(GREEN)✅ Dados de linguagens atualizados!$(NC)"

# Comandos para benchmark
benchmark: ## Executa benchmarks
	@echo "$(BLUE)⚡ Executando benchmarks...$(NC)"
	$(PYTHON) -m pytest tests/ -m benchmark -v || echo "$(YELLOW)⚠️ Nenhum benchmark encontrado$(NC)"
	@echo "$(GREEN)✅ Benchmarks concluídos!$(NC)" 