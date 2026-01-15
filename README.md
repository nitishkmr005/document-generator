# DocGen

**Production-grade document generation toolkit built on LangGraph, Docling, and modern LLMs**

Transform multi-format inputs (PDF, Markdown, URLs, DOCX) into polished outputs (PDF, PPTX, Markdown, FAQ docs, podcasts) with AI-powered synthesis and image generation. Built with clean architecture, type-safety, and extensibility in mind.

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Inputs    │─────▶│  LangGraph   │─────▶│  Outputs    │
│ PDF/MD/URLs │      │  Workflow    │      │ PDF/PPTX/MP3│
└─────────────┘      └──────────────┘      └─────────────┘
                            │
                    ┌───────┴────────┐
                    │                │
              ┌─────▼─────┐   ┌─────▼─────┐
              │  Docling  │   │    LLM    │
              │ OCR+Parse │   │ Synthesis │
              └───────────┘   └─────┬─────┘
                                    │
                              ┌─────▼─────┐
                              │   Image   │
                              │ Generation│
                              └───────────┘
```

**Core Stack:**
- **Workflow:** LangGraph 0.2.55 - State machine orchestration with retry logic
- **Parsing:** Docling 2.66.0 (IBM Research) - Advanced OCR, table extraction, layout analysis
- **LLM Synthesis:** Claude/Gemini/OpenAI - Content transformation and intelligent summarization
- **Image Generation:** Gemini/DALL-E - AI-generated visuals and diagrams
- **Generation:** ReportLab 4.2.5 + python-pptx 1.0.2 - Professional PDF/PPTX rendering
- **Architecture:** Clean Architecture - Domain/Application/Infrastructure layers with zero circular dependencies

**Two Ways to Use DocGen:**

1. **Python Package** (Coming Soon) - `pip install docgen` for programmatic access
2. **Web UI + API** - FastAPI backend + Next.js frontend for UI-driven generation

---

## What DocGen Does

### Multi-Format Input Parsing
Ingest and normalize content from diverse sources with intelligent extraction:

| Format | Parser | Capabilities |
|--------|--------|--------------|
| **PDF** | Docling | OCR, table extraction, layout analysis, image extraction |
| **Markdown** | Native | Frontmatter support, code blocks, nested structures |
| **Web URLs** | MarkItDown | Article extraction, metadata parsing, link resolution |
| **Office Docs** | Docling | DOCX, PPTX, XLSX with formatting preservation |
| **Images** | Docling | PNG, JPG, TIFF with OCR and layout detection |
| **Plain Text** | Native | TXT files with encoding detection |

### AI-Powered Synthesis
- **Content Transformation:** LLM-driven summarization, restructuring, and style adaptation
- **Visual Generation:** Context-aware diagrams, charts, and illustrations via Gemini/DALL-E
- **Intelligent Merging:** Multi-source synthesis with conflict resolution and deduplication
- **Slide Generation:** Automatic PPTX layouts with bullet points, titles, and visuals

### Professional Output Formats
- **PDF:** ReportLab-based generation with custom styling, headers, footers, and TOC
- **PPTX:** python-pptx presentations with 16:9 layouts and embedded images
- **Markdown:** Structured docs with frontmatter and proper heading hierarchy
- **FAQ Docs:** Q&A format generation from input content
- **Podcasts:** MP3 audio generation (coming soon)

### Production-Ready Features
- **LangGraph Workflow:** State machine with automatic retry (max 3 attempts) on failures
- **Caching:** Content and image caching to reduce LLM costs and latency
- **Logging:** Structured logging with Loguru for observability
- **Type Safety:** Pydantic validation throughout the pipeline
- **Docker Support:** Containerized backend and frontend for easy deployment
- **BYO API Keys:** Users bring their own LLM credentials (Claude, Gemini, OpenAI)

---

## Architecture

DocGen follows **Hybrid Clean Architecture** for maintainability, testability, and extensibility.

```
backend/doc_generator/
├── domain/              # Pure business logic (zero dependencies)
│   ├── models.py        # Core entities: Document, Content, Output
│   ├── enums.py         # InputFormat, OutputFormat, ProcessingStatus
│   ├── exceptions.py    # Custom exceptions with error codes
│   └── interfaces.py    # Abstract interfaces for parsers/generators
│
├── application/         # Use case orchestration
│   ├── parsers/         # Format-specific parsing implementations
│   ├── generators/      # Output format generators
│   ├── graph_workflow.py # LangGraph state machine
│   └── nodes/           # Workflow nodes (parse, transform, generate)
│
└── infrastructure/      # External integrations
    ├── docling/         # Docling integration for parsing
    ├── markitdown/      # MarkItDown for web content
    ├── llm/             # LLM providers (Claude, Gemini, OpenAI)
    ├── image/           # Image generation services
    ├── api/             # FastAPI endpoints and routes
    └── settings.py      # Config management (YAML + env)
```

### LangGraph Workflow

```python
# State machine with automatic retry logic
START → detect_format → parse_content → transform_content → generate_output → validate_output → END
                                             ↑                                        ↓
                                             └────────── (retry on error, max 3x) ───┘
```

**Node Responsibilities:**
- `detect_format`: Identify input type (PDF, MD, URL, etc.)
- `parse_content`: Extract raw content using appropriate parser
- `transform_content`: LLM synthesis + image generation
- `generate_output`: Render PDF/PPTX/MD using templates
- `validate_output`: Check file integrity and completeness

### Configuration Management
- **YAML Config:** `backend/config/settings.yaml` for defaults (page layouts, colors, LLM params)
- **Environment Variables:** `.env` for secrets (API keys, database URLs)
- **Pydantic Settings:** Type-safe config with validation and auto-reload

---

## Getting Started

### Prerequisites
- Python 3.11+
- Docker (for containerized deployment)
- LLM API key (Claude, Gemini, or OpenAI)

### Option 1: Web UI (Fastest)

**Run with Docker Compose:**
```bash
# Clone the repo
git clone https://github.com/your-org/docgen.git
cd docgen

# Start backend + frontend
docker-compose up --build

# Open http://localhost:3000
```

**Or deploy to cloud:**
- **Backend:** Deploy to [Render](https://render.com) using `backend/render.yaml`
- **Frontend:** Deploy to [Vercel](https://vercel.com) using `vercel.json`

### Option 2: Python Package (Coming Soon)

```python
pip install docgen

from docgen import Generator

# Initialize with your API key
generator = Generator(api_key="your-claude-key")

# Generate from multiple sources
result = generator.create(
    sources=["paper.pdf", "https://blog.com/article", "notes.md"],
    output_format="pdf",
    image_generation=True
)

print(f"Generated: {result.output_path}")
```

### Option 3: Local Development

```bash
# Install dependencies with uv
make setup

# Configure API keys
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY or OPENAI_API_KEY

# Run generation
make run-docgen INPUT=sample.md OUTPUT=pdf

# Start FastAPI backend
cd backend
uvicorn doc_generator.infrastructure.api.main:app --reload

# Start Next.js frontend (separate terminal)
cd frontend
npm install && npm run dev
```

### Configuration

**Backend config** (`backend/config/settings.yaml`):
```yaml
generator:
  output_dir: "data/output"
  max_retries: 3

pdf:
  page_size: "letter"
  margin: {top: 72, bottom: 18, left: 72, right: 72}

pptx:
  layout: "LAYOUT_16x9"
  slide_width: 960
  slide_height: 540
```

**Environment variables** (`.env`):
```bash
# LLM API Keys (choose one or more)
ANTHROPIC_API_KEY=your_claude_key
OPENAI_API_KEY=your_openai_key
GOOGLE_API_KEY=your_gemini_key

# Optional: Database (coming soon)
DATABASE_URL=postgresql://user:pass@localhost/docgen
```

---

## API Usage

DocGen exposes a FastAPI backend for programmatic document generation.

### Authentication (Coming Soon)
API authentication with user-managed API keys is planned. Currently, bring your own LLM keys via headers.

### Generate Documents (SSE Stream)

**Endpoint:** `POST /api/generate`

**Headers:**
```bash
Content-Type: application/json
X-Anthropic-Key: your_claude_key     # For Claude
X-OpenAI-Key: your_openai_key        # For OpenAI
X-Google-Key: your_gemini_key        # For Gemini
```

**Request Body:**
```json
{
  "output_format": "pdf",
  "provider": "gemini",
  "model": "gemini-2.0-flash-exp",
  "image_model": "imagen-3.0-generate-001",
  "sources": [
    {"type": "file", "file_id": "f_abc123"},
    {"type": "url", "url": "https://arxiv.org/pdf/2301.07041"},
    {"type": "text", "content": "Additional context to include"}
  ],
  "cache": {"reuse": true}
}
```

**Response:** Server-Sent Events (SSE) stream

```bash
curl -N -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -H "X-Google-Key: $GEMINI_API_KEY" \
  -d '{
    "output_format": "pdf",
    "provider": "gemini",
    "sources": [{"type": "url", "url": "https://example.com/article"}]
  }'
```

**Stream Events:**
```
event: progress
data: {"message": "Parsing PDF...", "progress": 20}

event: progress
data: {"message": "Generating images...", "progress": 60}

event: complete
data: {"download_url": "/api/download/f_abc/pdf/output.pdf", "file_path": "f_abc/pdf/output.pdf"}
```

### Upload Files

**Endpoint:** `POST /api/upload`

```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@paper.pdf"

# Response:
{
  "file_id": "f_abc123",
  "filename": "paper.pdf",
  "size": 245810,
  "mime_type": "application/pdf",
  "expires_in": 3600
}
```

### Download Generated Files

**Endpoint:** `GET /api/download/{file_id}/{format}/{filename}`

```bash
curl -L -o output.pdf \
  "http://localhost:8000/api/download/f_abc123/pdf/report.pdf"
```

### Health Check

**Endpoint:** `GET /api/health`

```bash
curl http://localhost:8000/api/health

# Response:
{"status": "healthy", "version": "0.1.0"}
```

---

## Roadmap

DocGen is under active development with ambitious plans for new capabilities.

### Planned Features

**🎨 Enhanced Generation**
- [ ] Podcast MP3 generation with multi-voice support
- [ ] Mind maps with visual hierarchy and relationships
- [ ] FAQ cards with structured Q&A formatting
- [ ] Advanced code blocks with syntax highlighting and Mermaid diagrams
- [ ] SVG diagram generation for technical content
- [ ] Configurable image generation toggle (on/off per request)

**🔧 UI/UX Improvements**
- [ ] API key management in UI (text + image generation keys)
- [ ] Real-time generation preview panel
- [ ] Cache/output/logs cleanup utilities
- [ ] Template marketplace with pre-built document types

**📄 Document Templates**
- [ ] Wedding cards and invitations
- [ ] Professional resumes with multiple styles
- [ ] arXiv-style research papers
- [ ] Study materials for students
- [ ] Interview Q&A preparation docs
- [ ] YouTube thumbnails with custom styles
- [ ] Excel → visual dashboards and charts

**🚀 Platform & Deployment**
- [ ] Python package on PyPI (`pip install docgen`)
- [ ] Authentication and user management
- [ ] Vercel frontend deployment optimization
- [ ] Image editing and style transfer
- [ ] Standalone image generation service

### Use Cases by Role

| Role | Use Case | Features |
|------|----------|----------|
| **Students** | Study materials, flashcards, summary PDFs | Multi-source synthesis, FAQ generation |
| **Job Seekers** | Resume generation, interview prep docs | Professional templates, Q&A formatting |
| **Executives** | Consistent brand presentations, pitch decks | Style enforcement, PPTX templates |
| **Content Creators** | YouTube thumbnails, podcast generation | Image generation, audio synthesis |
| **Researchers** | Paper formatting, literature reviews | arXiv templates, citation handling |
| **Developers** | Technical documentation, API docs | Code blocks, Mermaid diagrams, markdown |

---

## Development

### Setup Development Environment

```bash
# Clone and install
git clone https://github.com/your-org/docgen.git
cd docgen
make setup

# Or manually with uv
uv pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests with coverage
make test

# Or manually
pytest tests/ -v --cov=backend/doc_generator --cov-report=term-missing
```

### Linting & Type Checking

```bash
# Lint and type check
make lint

# Or manually
ruff check backend/doc_generator
mypy backend/doc_generator
```

### Project Commands

```bash
make setup       # Install dependencies
make run         # Run sample generation
make test        # Run test suite
make lint        # Lint and type check
make clean       # Clean output/cache files
make help        # Show all commands
```

### Project Structure

```
docgen/
├── backend/
│   ├── Dockerfile                    # FastAPI backend container
│   ├── config/settings.yaml          # Configuration
│   ├── doc_generator/                # Core package
│   │   ├── domain/                   # Business logic
│   │   ├── application/              # Use cases
│   │   └── infrastructure/           # External integrations
│   └── requirements-docker.txt
│
├── frontend/
│   ├── Dockerfile                    # Next.js frontend container
│   ├── src/app/                      # App router pages
│   └── package.json
│
├── scripts/                          # CLI utilities
├── tests/                            # Test suite
├── docs/                             # Documentation
├── docker-compose.yml                # Multi-container setup
└── Makefile                          # Automation tasks
```

### Contributing

We welcome contributions! Please follow these guidelines:

1. **Architecture:** Follow clean architecture patterns (domain/application/infrastructure)
2. **Type Safety:** Add type hints to all functions
3. **Documentation:** Write comprehensive docstrings
4. **Testing:** Add unit tests for new features (aim for >80% coverage)
5. **Linting:** Run `make lint` before committing
6. **Commits:** Use conventional commits (feat, fix, docs, refactor, test)

**Before submitting a PR:**
```bash
make lint        # Ensure code passes linting
make test        # Ensure tests pass
```

---

## Troubleshooting

### Common Issues

**Port already in use (Docker)**
```bash
# Stop existing containers
docker-compose down

# Or change port in docker-compose.yml
```

**Module not found errors**
```bash
# Reinstall dependencies
make setup

# Or manually
uv pip install -e ".[dev]"
```

**Docker build fails**
```bash
# Rebuild without cache
docker-compose build --no-cache
```

**LLM API errors**
```bash
# Verify API key in .env
cat .env | grep API_KEY

# Check API key validity
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01"
```

**Permission denied on output directory**
```bash
chmod 755 backend/data/output
```

### Getting Help

- **Issues:** [GitHub Issues](https://github.com/your-org/docgen/issues)
- **Discussions:** [GitHub Discussions](https://github.com/your-org/docgen/discussions)
- **Documentation:** See `docs/` for architecture and guides

---

## Acknowledgments

DocGen is built on the shoulders of giants:

- **[Docling](https://github.com/DS4SD/docling)** by IBM Research - Advanced document parsing with OCR and layout analysis
- **[MarkItDown](https://github.com/microsoft/markitdown)** by Microsoft - Document-to-markdown conversion
- **[LangGraph](https://github.com/langchain-ai/langgraph)** by LangChain - Workflow orchestration and state machines
- **[ReportLab](https://www.reportlab.com/)** - Professional PDF generation
- **[python-pptx](https://github.com/scanny/python-pptx)** - PowerPoint presentation generation
- **[Loguru](https://github.com/Delgan/loguru)** - Beautiful and powerful logging

## License

MIT License - See [LICENSE](LICENSE) file for details.

---

**Built with ❤️ for developers who value clean architecture, type safety, and extensibility.**

⭐ Star this repo if you find it useful!
