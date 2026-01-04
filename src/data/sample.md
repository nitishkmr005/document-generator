---
title: Document Generator Test
author: Claude Code
date: 2026-01-04
---

# Document Generator Test

This is a sample document to test the LangGraph-based document generator.

## Features

The document generator supports:

- **Multiple input formats**: PDF, Markdown, DOCX, PPTX, web articles
- **Multiple output formats**: PDF and PPTX
- **Advanced parsing**: Docling (IBM) and MarkItDown (Microsoft)
- **Pure Python**: No Node.js dependencies

## Architecture

### Three-Layer Clean Architecture

1. **Domain Layer**: Pure business logic
2. **Application Layer**: Use case orchestration
3. **Infrastructure Layer**: External integrations

### LangGraph Workflow

The workflow follows this pattern:

```
detect_format → parse_content → transform_content → generate_output → validate_output
```

## Code Example

Here's a simple example:

```python
from doc_generator.application.graph_workflow import run_workflow

result = run_workflow(
    input_path="sample.md",
    output_format="pdf"
)

print(f"Generated: {result['output_path']}")
```

## Table Example

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Parser | Docling | PDF/DOCX parsing |
| Converter | MarkItDown | HTML to Markdown |
| PDF | ReportLab | PDF generation |
| PPTX | python-pptx | PowerPoint |

## Lists

### Technologies Used

- Python 3.11+
- LangGraph for workflow orchestration
- Pydantic for data validation
- Loguru for logging
- Docker for containerization

### Benefits

- 100% Pure Python implementation
- Advanced document parsing with OCR
- Dockerized for portability
- Clean architecture for maintainability
- Comprehensive error handling

## Conclusion

This document generator demonstrates a modern, production-ready approach to document conversion using state-of-the-art Python libraries and clean architecture principles.

> **Note**: This is a test document. The actual implementation includes many more features and capabilities.

Happy document generating! 🚀
