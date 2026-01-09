# Project Specification

## Project Name
Document Generator

## Overview
LangGraph-based document generator for converting multiple input formats (PDF, Markdown, TXT, web articles) into PDF and PPTX outputs using 100% Python implementation.

## Product Purpose
Provide a reliable, Python-native way to transform mixed-source content into consistent, presentation-ready documents.

## Who Is This Product For
- Teams and individuals who need to generate PDFs/PPTX from mixed inputs
- Developers building document pipelines that must stay Python-only
- Technical users who want reproducible, containerized document workflows

## Problems It Solves
- Manual, time-consuming conversion from multiple formats into polished outputs
- Inconsistent formatting across input sources
- Hard-to-automate workflows that rely on GUI tools or non-Python stacks

## What the Product Does
- Ingests documents and URLs across common formats
- Normalizes content into a structured representation
- Generates PDF and PPTX outputs with consistent styling
- Validates outputs and retries on failure

## Functionality
- Multi-format input parsing with OCR support where needed
- Workflow orchestration with clear error handling and logging
- PDF/PPTX generation using Python libraries
- Dockerized execution for portability

## Goals
1. Accept multiple input formats (PDF, Markdown, TXT, DOCX, PPTX, XLSX, URLs, images)
2. Generate professional PDF and PPTX outputs
3. Pure Python implementation (no Node.js dependencies)
4. Containerized for portability

## Project Phases
- MVP: End-to-end document generation
- v1: Parse documents with Docling or MarkItDown
- v2: Multi-source synthesis from a single subfolder
- v3: LLM summarization and content creation (slides/SVG)
- v4: Refactor to clean architecture, config, and env
- v5: Reorganize `docs/` and reuse Claude Code workflows

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

### Advanced Features
- Advanced PDF parsing with IBM's Docling (OCR, table extraction, layout analysis)
- Web content extraction with Microsoft's MarkItDown
- LangGraph workflow orchestration
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

## Success Criteria
- [ ] All input formats parseable
- [ ] PDF output generates correctly
- [ ] PPTX output generates correctly
- [ ] Docker container builds and runs
- [ ] Tests pass with >80% coverage
