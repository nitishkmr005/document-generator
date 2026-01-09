# Document Generator Tasks

.PHONY: setup-docgen test-docgen lint-docgen run-docgen docker-build docker-run docker-compose-up clean-docgen help-docgen

help-docgen:  ## Show all available document generator commands
	@echo "📄 Document Generator - Available Commands"
	@echo ""
	@echo "🚀 Quick Start:"
	@echo "  make run-llm-architectures     Process LLM architectures folder (PDF + PPTX)"
	@echo ""
	@echo "⚙️  Setup & Configuration:"
	@echo "  make setup-docgen              Install all dependencies"
	@echo "  Create .env file with:         ANTHROPIC_API_KEY or OPENAI_API_KEY"
	@echo ""
	@echo "📝 Single File Processing:"
	@echo "  make run-docgen INPUT=<file> OUTPUT=<pdf|pptx>"
	@echo "  bash run.sh <file>             Generate both PDF and PPTX"
	@echo ""
	@echo "🐳 Docker:"
	@echo "  make docker-build              Build Docker image"
	@echo "  make docker-run INPUT=<file> OUTPUT=<format>"
	@echo ""
	@echo "🧹 Maintenance:"
	@echo "  make test-docgen               Run tests"
	@echo "  make lint-docgen               Lint and type check"
	@echo "  make clean-docgen              Clean generated files"
	@echo ""
	@echo "📖 Documentation:"
	@echo "  README.md                      Full documentation"
	@echo "  Quickstart.md                  Quick start guide"
	@echo "  ENV_SETUP.md                   Environment setup"
	@echo "  IMPLEMENTATION_SUMMARY.md      Implementation details"
	@echo ""

setup-docgen:  ## Setup document generator environment (local development)
	@echo "Setting up document generator..."
	@uv pip install -e ".[dev]"
	@echo "✅ Setup complete!"

test-docgen:  ## Run document generator tests
	@echo "Running tests..."
	@pytest tests/ -v --cov=src/doc_generator --cov-report=term-missing

lint-docgen:  ## Lint and type check document generator code
	@echo "Linting code..."
	@ruff check src/doc_generator
	@echo "Type checking..."
	@mypy src/doc_generator

run-docgen:  ## Run document generator (make run-docgen INPUT=file.md OUTPUT=pdf)
	@if [ -z "$(INPUT)" ]; then \
		echo "Usage: make run-docgen INPUT=<file> OUTPUT=<pdf|pptx>"; \
		echo "Example: make run-docgen INPUT=src/data/sample.md OUTPUT=pdf"; \
		exit 1; \
	fi
	@python scripts/run_generator.py $(INPUT) --output $(or $(OUTPUT),pdf)

docker-build:  ## Build Docker image for document generator
	@echo "Building Docker image..."
	@docker build -t doc-generator:latest .
	@echo "✅ Docker image built successfully"

docker-run:  ## Run in Docker (make docker-run INPUT=src/data/file.md OUTPUT=pdf)
	@if [ -z "$(INPUT)" ]; then \
		echo "Usage: make docker-run INPUT=<file> OUTPUT=<pdf|pptx>"; \
		echo "Example: make docker-run INPUT=src/data/sample.md OUTPUT=pdf"; \
		exit 1; \
	fi
	@docker run --rm \
		-v $(PWD)/src/data:/app/src/data \
		-v $(PWD)/src/output:/app/src/output \
		doc-generator:latest $(INPUT) --output $(or $(OUTPUT),pdf)

docker-compose-up:  ## Run with docker-compose
	@echo "Starting docker-compose..."
	@docker-compose up

clean-docgen:  ## Clean document generator files and caches
	@echo "Cleaning generated files..."
	@rm -rf src/output/*
	@rm -rf **/__pycache__
	@rm -rf .pytest_cache
	@rm -rf .ruff_cache
	@rm -rf .mypy_cache
	@rm -rf *.egg-info
	@echo "✅ Cleaned!"

example-md-to-pdf:  ## Example: Convert markdown to PDF
	@echo "Example: Converting markdown to PDF..."
	@python scripts/run_generator.py README.md --output pdf

example-url-to-pptx:  ## Example: Convert web article to PPTX
	@echo "Example: Converting web article to PPTX..."
	@python scripts/run_generator.py https://example.com --output pptx

run-llm-architectures:  ## Process LLM architectures folder with Claude API
	@echo "🚀 Processing LLM architectures folder..."
	@if [ ! -f .env ]; then \
		echo "❌ .env file not found. Please create .env with your API keys."; \
		echo "   See .env.example for reference."; \
		exit 1; \
	fi
	@bash run.sh src/data/llm-architectures --verbose
