# Project Specification

## Project Name
Document Generator

## Overview
Productized document generation platform where users bring their own LLM API key to create artifacts (PDF, PPTX, Markdown, FAQ docs, podcast MP3) from multi-source inputs via a frontend app, API, or Python package.

## Product Purpose
Let users turn messy inputs into structured, reusable artifacts using their own LLM credentials, with consistent outputs across UI, API, and package interfaces.

## Who Is This Product For
- Teams and individuals who need reliable artifacts from mixed inputs
- Developers who want a Python-first package plus a hosted API
- Product teams that need UI-driven generation for non-technical users

## Problems It Solves
- Manual, time-consuming synthesis across multiple formats and sources
- Inconsistent outputs caused by ad hoc prompts and templates
- Hard-to-automate workflows without a unified API, UI, and package

## What the Product Does
- Ingests files, URLs, and folders of sources
- Normalizes and synthesizes content using an LLM (user-provided API key)
- Generates PDF, PPTX, Markdown, FAQ docs, and podcast MP3 artifacts
- Exposes generation via FastAPI and a Python package
- Provides a frontend UI for artifact creation and chat
- Supports RAG-based chat for document Q&A

## Functionality
- Multi-format input parsing with OCR support where needed
- LLM-driven synthesis, summarization, and content creation
- Artifact generation (PDF, PPTX, Markdown, FAQ, MP3)
- FastAPI service and Python package interfaces
- Frontend UI with authentication
- Logging and database-backed inputs
- Dockerized execution for portability

## Goals
1. Accept multiple input formats (PDF, Markdown, TXT, DOCX, PPTX, XLSX, URLs, images)
2. Generate professional PDF, PPTX, Markdown, FAQ, and MP3 outputs
3. Support BYO LLM API keys in frontend, API, and Python package
4. Provide a FastAPI backend with a clean, deployable interface
5. Stay Python-first and containerized for portability

## Project Phases
- MVP: End-to-end document generation
- v1: Parse documents with Docling or MarkItDown
- v2: Multi-source synthesis from a single subfolder
- v3: LLM summarization and content creation (slides/SVG)
- v4: Refactor to clean architecture, config, and env
- v5: Reorganize `docs/` and reuse Claude Code workflows
- v6: FastAPI service to generate PDF/PPT/MD via LLM synthesis
- v7: Podcast MP3 generation
- v8: FAQ-style documentation generation
- v9: Frontend integration with the API
- v10: Deploy backend and frontend (Vercel/Render)
- v11: Postgres integration for reading data
- v12: Frontend authentication
- v13: Log user data in the database
- v14: RAG ingestion + chat interface for document Q&A

## Milestones

| Phase | Title | Status | Deliverables | Acceptance Criteria | Tech Stack |
| --- | --- | --- | --- | --- | --- |
| MVP | End-to-end document generation | Complete | - Generate a document from input to output | - One sample run produces valid outputs | _TBD_ |
| v1 | Parse documents with Docling/MarkItDown | Complete | - Ingest documents via Docling or MarkItDown | - Parsed content is usable by the pipeline | _TBD_ |
| v2 | Multi-source synthesis from a subfolder | Complete | - Combine multiple sources into one document | - Single output reflects all sources | _TBD_ |
| v3 | LLM summarization and content creation | Complete | - Use LLM to summarize or generate slides/SVG | - LLM output is included in final document | _TBD_ |
| v4 | Refactor to clean architecture + config/env | Complete | - Refactor codebase and formalize config/env | - Structure is clean and config-driven | _TBD_ |
| v5 | Docs + Claude Code workflow automation | In Progress | - Reorganize `docs/` and make workflows reusable | - Session start/end flows run without gaps | _TBD_ |
| v6 | FastAPI artifact generation | Planned | - FastAPI endpoint to generate PDF/PPT/MD using LLM synthesis | - API returns requested artifacts for a sample input | _TBD_ |
| v7 | Podcast MP3 generation | Planned | - Generate podcast MP3 from input data | - MP3 output passes a basic playback check | _TBD_ |
| v8 | FAQ documentation generation | Planned | - Generate FAQ-style docs from input data | - FAQ output matches input topics | _TBD_ |
| v9 | Frontend integration | Planned | - Connect frontend to the API | - Frontend can trigger artifact generation | _TBD_ |
| v10 | Deploy backend + frontend | Planned | - Deploy services to Vercel or Render | - Public endpoints are reachable | _TBD_ |
| v11 | Postgres data integration | Planned | - Read input data from Postgres | - Pipeline runs using DB data | _TBD_ |
| v12 | Frontend authentication | Planned | - Add auth to frontend | - Protected routes require login | _TBD_ |
| v13 | User activity logging | Planned | - Log user data in the database | - Audit entries are stored per request | _TBD_ |
| v14 | RAG + chat interface | Planned | - Ingest data for RAG and add chat UI | - Users can ask questions about documents | _TBD_ |
| X | Crazy Ideas | Planned | - Prototype one experimental capability | - A short writeup captures findings | _TBD_ |
| Z | Not In Scope | Not In Scope | - Keep excluded ideas out of scope | - Items remain excluded unless re-scoped | _TBD_ |

## Features

### Input Formats
- PDF documents (with OCR support via Docling)
- Markdown files (.md) with frontmatter support
- Plain text files (.txt)
- DOCX, PPTX, XLSX documents
- Web articles (URLs)
- Images (PNG, JPG, TIFF)

### Output Formats
- PDF (ReportLab with custom styling)
- PPTX (python-pptx for PowerPoint)
- Markdown documents
- FAQ-style documentation
- Podcast MP3 output

### Advanced Features
- Advanced PDF parsing with IBM's Docling (OCR, table extraction, layout analysis)
- Web content extraction with Microsoft's MarkItDown
- LangGraph workflow orchestration
- RAG ingestion and chat interface for document Q&A
- Automatic retry on generation errors (max 3 attempts)
- Comprehensive error handling and logging
- Docker containerization

## Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Document Parsing | Docling | 2.66.0 |
| Document Conversion | MarkItDown | 0.0.1a2 |
| PDF Generation | ReportLab | 4.2.5 |
| PPTX Generation | python-pptx | 1.0.2 |
| Workflow Orchestration | LangGraph | 0.2.55 |
| Validation | Pydantic | 2.10.5 |
| Logging | Loguru | 0.7.3 |
| Package Manager | uv | latest |

## Architecture
Hybrid Clean Architecture:
- **Domain Layer**: Pure business logic (zero dependencies)
- **Application Layer**: Use case orchestration
- **Infrastructure Layer**: External integrations

## Constraints
- Python 3.11+ required
- No Node.js dependencies
- Must run in Docker container
- Users supply their own LLM API keys

## Success Criteria
- [ ] All input formats parseable
- [ ] PDF output generates correctly
- [ ] PPTX output generates correctly
- [ ] Markdown/FAQ/MP3 outputs generate correctly
- [ ] Frontend, API, and Python package can generate artifacts end-to-end
- [ ] Docker container builds and runs
- [ ] Tests pass with >80% coverage

## Future Recommendations
- Define a clear pricing model (BYO key + usage tiers) and enforce quotas
- Add template marketplace and curated presets to drive repeat usage
- Introduce team workspaces with shared assets and versioned outputs
- Provide export-ready brand themes and style packs
- Build reliability metrics and cost observability per run
- Offer one-click integrations (Google Drive, Notion, Slack, S3)
- Ship a public API with SDKs and webhooks for automation
- Improve onboarding with guided sample projects and sandbox mode
- Add human-in-the-loop review and approval before publishing
- Invest in security: secrets handling, audit logs, and role-based access
