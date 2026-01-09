# Project Specification

## Project Name
Document Generator

## Overview
LangGraph-based document generator for converting multiple input formats (PDF, Markdown, TXT, web articles) into PDF and PPTX outputs using 100% Python implementation.

## Goals
1. Accept multiple input formats (PDF, Markdown, TXT, DOCX, PPTX, XLSX, URLs, images)
2. Generate professional PDF and PPTX outputs
3. Pure Python implementation (no Node.js dependencies)
4. Containerized for portability

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
