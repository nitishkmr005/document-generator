# Claude Code Instructions

## Table of Contents
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Code Style](#code-style)
- [Documentation](#documentation)
- [Configuration](#configuration)
- [Development](#development)

## Architecture

**Three-Layer Clean Architecture** with strict dependency rules:

```
Domain (Core Logic)
  ↑
Application (Use Cases)
  ↑
Infrastructure (External)
```

**Dependency Rules:**
- Domain: ⛔ Zero dependencies on other layers
- Application: ✅ Domain only
- Infrastructure: ✅ Application + Domain

**Think of it like building blocks:** Domain is the foundation (pure business logic), Application stacks on top (orchestration), Infrastructure wraps around (external connections).

## Project Structure

```
src/{project_name}/
├── domain/          # Core logic (memory, prompts, tools)
├── application/     # Services (chat, evaluation, ingest)
└── infrastructure/  # External (API, DB, LLM, monitoring)

tests/              # All test files here
docs/               # All documentation except README/QUICKSTART
```

## Code Style

**Naming:**
- Variables/Functions: `snake_case` → `process_data()`
- Classes: `PascalCase` → `ChatService`
- Constants: `UPPER_SNAKE_CASE` → `MAX_TOKENS`

**Organization:**
- One responsibility per module
- Reusable code → `utils/` folder
- Use `loguru` for logging (never `print()`)
- Descriptive names (no abbreviations)

## Documentation

**Every `.md` file starts with Table of Contents**

**Docstrings required** for all functions/classes:
```python
def process_documents(file_path: str, batch_size: int = 10) -> list[str]:
    """
    Process documents from file in batches.
    
    Args:
        file_path: Path to input file
        batch_size: Documents per batch
        
    Returns:
        List of processed document IDs
    """
```

**README.md must include:**
1. Title & Objective
2. Implementation Plan
3. Input Data format
4. Tech Stack
5. Output Format (with examples)
6. Setup Instructions
7. Run Instructions
8. Project Structure

**Documentation placement:**
- Root: Only `README.md` + `QUICKSTART.md`
- Everything else: `docs/` subfolders

## Configuration

**Required files:**
- `docker-compose.yaml`
- `Dockerfile`
- `pyproject.toml` (dependencies here, not requirements.txt)
- `Makefile` (setup, lint, test automation)
- `tests/conftest.py` (shared fixtures)

**Environment:**
- Package manager: `uv`
- Secrets: `.env` file
- Validation: Pydantic Settings
- ⛔ Never hardcode API keys
- Pin exact dependency versions

## Development

**Workflow:**
1. Start with simplest working version
2. Build modular, testable components
3. Avoid premature abstraction
4. Keep performance high (low latency)
5. One end-to-end test in `tests/`

**Best Practices:**
- Use pre-commit hooks
- Remove unused imports
- Profile before optimizing
- Update README with every change

**Core Principle:** Simplicity > Complexity. Make it work, make it testable, make it clear.