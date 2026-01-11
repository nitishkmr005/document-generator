# Architecture Reorganization Plan

## Current Structure

```
src/doc_generator/
├── application/
│   ├── generators/        (pdf_generator, pptx_generator)
│   ├── nodes/             (workflow nodes)
│   ├── parsers/
│   └── graph_workflow.py
├── config/
│   ├── prompts/           (LLM prompts)
│   └── settings.py
├── domain/
│   ├── content_types.py
│   ├── exceptions.py
│   ├── interfaces.py
│   └── models.py
├── infrastructure/
│   ├── api/               (FastAPI routes, models, services)
│   │   ├── models/
│   │   ├── routes/
│   │   └── services/
│   ├── claude_svg_generator.py
│   ├── gemini_image_generator.py
│   ├── llm_service.py
│   ├── pdf_utils.py
│   └── ... (many files)
└── utils/
```

## Proposed Structure (Clean Architecture)

```
src/doc_generator/
├── __init__.py
├── config.py              # App configuration (moved from config/)
│
├── domain/                # DOMAIN LAYER - Pure business logic
│   ├── __init__.py
│   ├── models.py          # Domain entities (Document, Section, etc.)
│   ├── exceptions.py      # Domain exceptions
│   ├── interfaces.py      # Abstract interfaces/protocols
│   ├── content_types.py   # Enums and value objects
│   └── prompts/           # LLM prompts (domain knowledge)
│       ├── __init__.py
│       ├── content_prompts.py
│       ├── image_prompts.py
│       ├── summary_prompts.py
│       └── visual_prompts.py
│
├── application/           # APPLICATION LAYER - Use cases & orchestration
│   ├── __init__.py
│   ├── services/          # Application services
│   │   ├── __init__.py
│   │   ├── document_service.py    # Main document generation orchestration
│   │   ├── parsing_service.py     # Content parsing orchestration
│   │   └── generation_service.py  # Output generation orchestration
│   └── workflow/          # LangGraph workflow
│       ├── __init__.py
│       ├── graph.py               # Main workflow graph
│       └── nodes/                 # Workflow nodes
│           ├── __init__.py
│           ├── detect_format.py
│           ├── parse_content.py
│           ├── transform_content.py
│           ├── generate_images.py
│           ├── generate_visuals.py
│           ├── generate_output.py
│           └── validate_output.py
│
├── infrastructure/        # INFRASTRUCTURE LAYER - External concerns
│   ├── __init__.py
│   ├── settings.py        # Settings with Pydantic
│   ├── logging.py         # Logging configuration
│   │
│   ├── api/               # FastAPI HTTP layer
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── dependencies.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── generate.py
│   │   │   ├── upload.py
│   │   │   ├── download.py
│   │   │   └── cache.py
│   │   └── schemas/       # API request/response schemas
│   │       ├── __init__.py
│   │       ├── requests.py
│   │       └── responses.py
│   │
│   ├── llm/               # LLM providers
│   │   ├── __init__.py
│   │   ├── base.py        # Abstract LLM interface
│   │   ├── gemini.py      # Google Gemini provider
│   │   ├── openai.py      # OpenAI provider
│   │   └── anthropic.py   # Anthropic/Claude provider
│   │
│   ├── generators/        # Output generators
│   │   ├── __init__.py
│   │   ├── base.py        # Abstract generator
│   │   ├── pdf/
│   │   │   ├── __init__.py
│   │   │   ├── generator.py
│   │   │   └── utils.py
│   │   └── pptx/
│   │       ├── __init__.py
│   │       ├── generator.py
│   │       └── utils.py
│   │
│   ├── parsers/           # Content parsers
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── docling.py
│   │   ├── markitdown.py
│   │   └── web.py
│   │
│   ├── image/             # Image generation
│   │   ├── __init__.py
│   │   ├── gemini_generator.py
│   │   └── svg_generator.py
│   │
│   └── storage/           # File storage
│       ├── __init__.py
│       └── file_storage.py
│
└── utils/                 # Shared utilities
    ├── __init__.py
    ├── content_cache.py
    └── image_utils.py
```

## Migration Steps

### Phase 1: Move prompts to domain layer

- Move `config/prompts/` → `domain/prompts/`
- Update all imports

### Phase 2: Reorganize infrastructure

- Move `settings.py` → `infrastructure/settings.py` (already there)
- Move `logging_config.py` → `infrastructure/logging.py`
- Create `infrastructure/llm/` for LLM providers
- Create `infrastructure/generators/` for PDF/PPTX
- Create `infrastructure/parsers/` for content parsers
- Create `infrastructure/image/` for image generators
- Create `infrastructure/storage/` for file operations
- Rename `api/models/` → `api/schemas/`

### Phase 3: Reorganize application layer

- Move `graph_workflow.py` → `application/workflow/graph.py`
- Move `nodes/` → `application/workflow/nodes/`
- Create `application/services/` for orchestration services

### Phase 4: Update all imports

- Fix all import statements across the codebase
- Update `__init__.py` files with proper exports

### Phase 5: Clean up

- Remove empty directories
- Update Makefile if needed
- Test everything works

## Benefits

1. **Cleaner separation of concerns** - Each layer has clear responsibility
2. **Easier testing** - Domain and application layers can be tested independently
3. **Better maintainability** - Find files intuitively by their purpose
4. **Follows industry patterns** - Clean Architecture / Hexagonal Architecture
