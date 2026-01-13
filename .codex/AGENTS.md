# Codex Instructions

## Read Order (optimize context)

1. `docs/project/STATUS.md` - current state
2. `docs/project/SPEC.md` - what we're building
3. Reference guides below as needed

## Commands

```bash
make setup    # Setup environment
make run      # Run application
make test     # Run tests (before commit)
make lint     # Lint code (after changes)
make help     # Show all commands
```

## Skills

- `/session-end` - update STATUS, optional retro
- `/update-status` - update STATUS.md
- `/retro` - create learnings file
- `/brainstorm` - ALWAYS before new project/feature

## Workflow

1. **Brainstorm first** - before any new project or feature
2. **Ask questions** - before creating any `.md` file
3. **Read docs first** - code only when needed
4. **Lint and test** - `make lint` after changes, `make test` before commit

## Principles

- Simplicity over complexity
- No premature abstraction
- Evidence before assertions

## Reference Guides

Read these on first-time project setup or when starting specific tasks:

| Guide                                              | When to Use                     |
| -------------------------------------------------- | ------------------------------- |
| [Architecture](docs/claude-code/architecture.md)   | Setting up clean architecture   |
| [Setup](docs/claude-code/setup.md)                 | Python/uv/Docker/Makefile setup |
| [Logging](docs/claude-code/logging.md)             | Loguru + Opik observability     |
| [Documentation](docs/claude-code/documentation.md) | Creating any `.md` files        |
| [SPEC Template](docs/claude-code/spec-template.md) | Writing product specifications  |
| [Blog Template](docs/claude-code/blog-template.md) | Writing technical blogs         |
| [Config](docs/claude-code/config.md)               | YAML + Pydantic + .env patterns |
