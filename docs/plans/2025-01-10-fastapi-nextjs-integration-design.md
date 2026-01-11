# FastAPI + Next.js Integration Design

**Date:** 2025-01-10
**Status:** Approved
**Milestone:** v6 - FastAPI artifact generation

## Overview

Convert the document generator into a FastAPI service that integrates with a Next.js frontend. Supports multiple LLM providers, multi-source inputs with categories, streaming progress, and flexible image generation styles.

## API Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/api/generate` | Generate document (SSE streaming) |
| POST | `/api/upload` | Upload file, get file_id |
| GET | `/api/health` | Health check |

## Request Structure

### Headers (API Keys)

```
X-OpenAI-Key: sk-...        (optional)
X-Anthropic-Key: sk-ant-... (optional)
X-Google-Key: AIza...       (required if provider=google)
```

### POST /api/generate

```json
{
  "output_format": "pdf" | "pptx",

  "sources": {
    "primary": [
      {"type": "file", "file_id": "f_abc123"},
      {"type": "url", "url": "https://article.com"},
      {"type": "text", "content": "Pasted text content here..."}
    ],
    "supporting": [
      {"type": "text", "content": "User notes pasted directly..."}
    ],
    "reference": [],
    "data": [],
    "other": {
      "custom_category": [
        {"type": "file", "file_id": "f_def456"}
      ]
    }
  },

  "provider": "google" | "openai" | "anthropic",
  "model": "gemini-3-pro-preview",
  "image_model": "gemini-3-pro-image-preview",

  "preferences": {
    "audience": "technical" | "executive" | "client" | "educational",
    "image_style": "auto" | "infographic" | "handwritten" | "minimalist" | "corporate" | "educational" | "diagram" | "chart" | "mermaid" | "decorative",
    "temperature": 0.4,
    "max_tokens": 8000,
    "max_slides": 10,
    "max_summary_points": 5
  },

  "cache": {
    "reuse": true
  }
}
```

### POST /api/upload

**Request:** `multipart/form-data` with `file` field

**Response:**
```json
{
  "file_id": "f_abc123",
  "filename": "report.pdf",
  "size": 245000,
  "mime_type": "application/pdf",
  "expires_in": 3600
}
```

## Streaming Response (SSE)

**Headers:**
```
Content-Type: text/event-stream
Cache-Control: no-cache
```

**Progress Events:**
```
data: {"status": "parsing", "progress": 5, "message": "Parsing 3 sources..."}
data: {"status": "parsing", "progress": 15, "message": "Extracted content from report.pdf"}
data: {"status": "transforming", "progress": 25, "message": "Structuring content..."}
data: {"status": "generating_images", "progress": 40, "message": "Generating image 1/5..."}
data: {"status": "generating_images", "progress": 55, "message": "Generating image 3/5..."}
data: {"status": "generating_output", "progress": 80, "message": "Building PDF..."}
data: {"status": "uploading", "progress": 95, "message": "Uploading to storage..."}
data: {"status": "complete", "progress": 100, "download_url": "https://storage.../output.pdf?token=abc", "expires_in": 3600, "metadata": {"title": "Document Title", "pages": 12, "images_generated": 5}}
```

**Error Event:**
```
data: {"status": "error", "error": "Invalid API key", "code": "AUTH_ERROR"}
```

**Cache Hit Event:**
```
data: {"status": "cache_hit", "progress": 100, "download_url": "...", "cached_at": "2025-01-10T10:30:00Z"}
```

## Source Types

| Type | Description | Required Fields |
|------|-------------|-----------------|
| `file` | Uploaded file reference | `file_id` |
| `url` | Web URL to fetch | `url` |
| `text` | Direct pasted content | `content` |

## Source Categories

| Category | Purpose |
|----------|---------|
| `primary` | Main content sources |
| `supporting` | Additional context |
| `reference` | Citations, bibliography |
| `data` | Data files (CSV, XLSX) |
| `other` | Custom user-defined categories |

## Image Styles

| Style | Description | Generator |
|-------|-------------|-----------|
| `auto` | AI picks best per section | Mixed |
| `infographic` | Visual explanations | Gemini |
| `handwritten` | Whiteboard/sketch style | Gemini |
| `minimalist` | Simple, clean lines | Gemini |
| `corporate` | Professional, polished | Gemini |
| `educational` | Textbook illustrations | Gemini |
| `diagram` | Architecture/flowcharts | SVG |
| `chart` | Data visualizations | SVG |
| `mermaid` | Code-generated diagrams | Mermaid |
| `decorative` | Thematic headers | Gemini |

## Defaults

| Setting | Default Value |
|---------|---------------|
| Provider | `google` |
| Model | `gemini-3-pro-preview` |
| Image Model | `gemini-3-pro-image-preview` |
| Audience | `technical` |
| Image Style | `auto` |
| Temperature | `0.4` |
| Max Tokens | `8000` |
| Max Slides | `10` |
| Max Summary Points | `5` |
| Cache Reuse | `true` |

## File Structure

```
src/doc_generator/infrastructure/api/
├── __init__.py
├── main.py                  # FastAPI app, CORS, lifespan
├── dependencies.py          # API key extraction, validation
├── routes/
│   ├── __init__.py
│   ├── generate.py          # POST /api/generate (SSE streaming)
│   ├── upload.py            # POST /api/upload
│   └── health.py            # GET /api/health
├── models/
│   ├── __init__.py
│   ├── requests.py          # Pydantic request models
│   └── responses.py         # Pydantic response models
└── services/
    ├── __init__.py
    ├── generation.py        # Orchestrates workflow with progress
    ├── storage.py           # Temp file + output storage
    └── cache.py             # Content-based cache logic
```

## Pydantic Models

### Request Models (`requests.py`)

```python
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

class OutputFormat(str, Enum):
    PDF = "pdf"
    PPTX = "pptx"

class Provider(str, Enum):
    GOOGLE = "google"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"

class Audience(str, Enum):
    TECHNICAL = "technical"
    EXECUTIVE = "executive"
    CLIENT = "client"
    EDUCATIONAL = "educational"

class ImageStyle(str, Enum):
    AUTO = "auto"
    INFOGRAPHIC = "infographic"
    HANDWRITTEN = "handwritten"
    MINIMALIST = "minimalist"
    CORPORATE = "corporate"
    EDUCATIONAL = "educational"
    DIAGRAM = "diagram"
    CHART = "chart"
    MERMAID = "mermaid"
    DECORATIVE = "decorative"

class FileSource(BaseModel):
    type: str = "file"
    file_id: str

class UrlSource(BaseModel):
    type: str = "url"
    url: str

class TextSource(BaseModel):
    type: str = "text"
    content: str

SourceItem = FileSource | UrlSource | TextSource

class SourceCategories(BaseModel):
    primary: list[SourceItem] = []
    supporting: list[SourceItem] = []
    reference: list[SourceItem] = []
    data: list[SourceItem] = []
    other: dict[str, list[SourceItem]] = {}

class Preferences(BaseModel):
    audience: Audience = Audience.TECHNICAL
    image_style: ImageStyle = ImageStyle.AUTO
    temperature: float = Field(default=0.4, ge=0, le=1)
    max_tokens: int = Field(default=8000, ge=100, le=32000)
    max_slides: int = Field(default=10, ge=1, le=50)
    max_summary_points: int = Field(default=5, ge=1, le=20)

class CacheOptions(BaseModel):
    reuse: bool = True

class GenerateRequest(BaseModel):
    output_format: OutputFormat
    sources: SourceCategories
    provider: Provider = Provider.GOOGLE
    model: str = "gemini-3-pro-preview"
    image_model: str = "gemini-3-pro-image-preview"
    preferences: Preferences = Field(default_factory=Preferences)
    cache: CacheOptions = Field(default_factory=CacheOptions)
```

### Response Models (`responses.py`)

```python
from enum import Enum
from typing import Optional
from pydantic import BaseModel

class GenerationStatus(str, Enum):
    PARSING = "parsing"
    TRANSFORMING = "transforming"
    GENERATING_IMAGES = "generating_images"
    GENERATING_OUTPUT = "generating_output"
    UPLOADING = "uploading"
    COMPLETE = "complete"
    CACHE_HIT = "cache_hit"
    ERROR = "error"

class ProgressEvent(BaseModel):
    status: GenerationStatus
    progress: int  # 0-100
    message: str = ""

class CompletionMetadata(BaseModel):
    title: str
    pages: int = 0
    slides: int = 0
    images_generated: int = 0

class CompleteEvent(BaseModel):
    status: GenerationStatus = GenerationStatus.COMPLETE
    progress: int = 100
    download_url: str
    expires_in: int = 3600
    metadata: CompletionMetadata

class CacheHitEvent(BaseModel):
    status: GenerationStatus = GenerationStatus.CACHE_HIT
    progress: int = 100
    download_url: str
    expires_in: int = 3600
    cached_at: str

class ErrorEvent(BaseModel):
    status: GenerationStatus = GenerationStatus.ERROR
    error: str
    code: str  # AUTH_ERROR, PARSE_ERROR, GENERATION_ERROR, etc.

class UploadResponse(BaseModel):
    file_id: str
    filename: str
    size: int
    mime_type: str
    expires_in: int = 3600

class HealthResponse(BaseModel):
    status: str = "healthy"
    version: str
```

## Caching Strategy

- **Cache Key:** SHA256 hash of (sources content + provider + model + preferences)
- **Storage:** Local file system or Redis (configurable)
- **TTL:** 24 hours (configurable)
- **Behavior:** If `cache.reuse=true` and cache hit, return `cache_hit` event immediately

## File Upload Flow

1. User drags/selects files in frontend
2. Frontend uploads each file to `POST /api/upload`
3. Frontend receives `file_id` for each upload
4. Frontend calls `POST /api/generate` with `file_id` references
5. Backend retrieves files from temp storage during generation
6. Temp files cleaned up after 1 hour

## Dependencies

```
fastapi>=0.109.0
sse-starlette>=1.6.0
python-multipart>=0.0.6
aiofiles>=23.2.0
```

## Next Steps

1. Create the file structure under `infrastructure/api/`
2. Implement Pydantic models
3. Implement upload endpoint with temp storage
4. Implement SSE streaming for generate endpoint
5. Integrate with existing `graph_workflow.py`
6. Add caching layer
7. Test with Next.js frontend
