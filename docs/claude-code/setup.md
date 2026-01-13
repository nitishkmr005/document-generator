# Project Setup Guide

## Python Environment

### Requirements

- Python 3.11+ (required)
- `uv` package manager (preferred) or `pip`

### Using uv Package Manager

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment
uv venv

# Activate venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Install dependencies
uv pip install -e ".[dev]"
```

## pyproject.toml Structure

```toml
[project]
name = "project-name"
version = "0.1.0"
description = "Project description"
requires-python = ">=3.11"
dependencies = [
    # Core dependencies here
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=6.0.0",
    "ruff>=0.8.0",
    "mypy>=1.14.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 120
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W"]

[tool.mypy]
python_version = "3.11"
warn_return_any = true

[tool.pytest.ini_options]
testpaths = ["tests"]
```

## Docker Setup

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy project files
COPY pyproject.toml .
COPY src/ src/

# Install dependencies
RUN uv pip install --system -e .

CMD ["python", "-m", "project_name"]
```

### docker-compose.yaml

```yaml
services:
  app:
    build: .
    env_file: .env
    volumes:
      - ./src/data:/app/src/data
      - ./src/output:/app/src/output
    ports:
      - "8000:8000"
```

## Git Repository

### .gitignore essentials

```
.venv/
__pycache__/
*.pyc
.env
.ruff_cache/
.mypy_cache/
.pytest_cache/
*.egg-info/
dist/
build/
```

### Common Git Commands

```bash
# Setup repository
git init
git remote add origin <url>

# Pull changes from remote
git pull origin main
git fetch origin

# Create and switch branches
git checkout -b feature/new-feature
git switch -c fix/bug-fix

# Stage and commit
git add .
git commit -m "feat: add new feature"

# Push changes
git push origin feature/new-feature
git push -u origin main  # First push with upstream

# Merge branches
git checkout main
git merge feature/new-feature

# Revert to old commit
git revert <commit-hash>      # Creates new commit
git reset --hard <commit-hash>  # Destructive, use carefully

# View history
git log --oneline -n 10
git log --graph --all

# Stash changes
git stash
git stash pop
```

### Git Worktrees

```bash
# Create worktree for parallel work
git worktree add ../project-feature feature/new-feature

# List worktrees
git worktree list

# Remove worktree
git worktree remove ../project-feature
```

### GitHub CLI Commands

```bash
# Install gh CLI
brew install gh  # macOS
# or: https://cli.github.com/

# Authenticate
gh auth login

# Create repository
gh repo create project-name --public --source=. --remote=origin

# Create pull request
gh pr create --title "Add feature" --body "Description"

# Create issue
gh issue create --title "Bug report" --body "Details"

# View PRs
gh pr list
gh pr view 123

# Merge PR
gh pr merge 123 --squash
```

## Makefile Commands

> [!IMPORTANT]
> All setup and run commands should be in Makefile for single-command execution.

```makefile
.PHONY: setup run test lint all clean
.DEFAULT_GOAL := help

help:  ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

setup:  ## Setup development environment
	@if [ ! -d .venv ]; then python3 -m venv .venv; fi
	@.venv/bin/pip install -e ".[dev]"
	@echo "✅ Setup complete!"

run:  ## Run the application
	@.venv/bin/python -m project_name

test:  ## Run tests with coverage
	@pytest tests/ -v --cov=src/project_name

lint:  ## Lint and type check
	@ruff check src/
	@mypy src/

all: lint test  ## Run lint + test

clean:  ## Clean generated files
	@rm -rf __pycache__ .pytest_cache .ruff_cache .mypy_cache
```
