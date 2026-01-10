# FastAPI + Next.js Integration Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create a FastAPI service with SSE streaming that integrates with a Next.js frontend for document generation.

**Architecture:** API layer under infrastructure/ with routes, models, and services. Routes handle HTTP, services orchestrate the existing graph workflow with progress callbacks. Storage service manages temp files and output URLs.

**Tech Stack:** FastAPI, sse-starlette, python-multipart, aiofiles, existing LangGraph workflow

---

## Task 1: Add FastAPI Dependencies

**Files:**
- Modify: `pyproject.toml`

**Step 1: Add dependencies to pyproject.toml**

Add to `[project.dependencies]`:

```toml
"fastapi>=0.109.0",
"sse-starlette>=1.6.0",
"python-multipart>=0.0.6",
"aiofiles>=23.2.0",
"uvicorn>=0.27.0",
```

**Step 2: Install dependencies**

Run: `uv sync`
Expected: Dependencies installed successfully

**Step 3: Commit**

```bash
git add pyproject.toml uv.lock
git commit -m "deps: add FastAPI and streaming dependencies"
```

---

## Task 2: Create Request Models

**Files:**
- Create: `src/doc_generator/infrastructure/api/__init__.py`
- Create: `src/doc_generator/infrastructure/api/models/__init__.py`
- Create: `src/doc_generator/infrastructure/api/models/requests.py`
- Test: `tests/api/test_request_models.py`

**Step 1: Create directory structure**

```bash
mkdir -p src/doc_generator/infrastructure/api/models
mkdir -p src/doc_generator/infrastructure/api/routes
mkdir -p src/doc_generator/infrastructure/api/services
mkdir -p tests/api
```

**Step 2: Create api __init__.py**

```python
"""FastAPI service for document generation."""
```

**Step 3: Create models __init__.py**

```python
"""Pydantic models for API requests and responses."""

from .requests import (
    OutputFormat,
    Provider,
    Audience,
    ImageStyle,
    FileSource,
    UrlSource,
    TextSource,
    SourceItem,
    SourceCategories,
    Preferences,
    CacheOptions,
    GenerateRequest,
)
from .responses import (
    GenerationStatus,
    ProgressEvent,
    CompletionMetadata,
    CompleteEvent,
    CacheHitEvent,
    ErrorEvent,
    UploadResponse,
    HealthResponse,
)

__all__ = [
    "OutputFormat",
    "Provider",
    "Audience",
    "ImageStyle",
    "FileSource",
    "UrlSource",
    "TextSource",
    "SourceItem",
    "SourceCategories",
    "Preferences",
    "CacheOptions",
    "GenerateRequest",
    "GenerationStatus",
    "ProgressEvent",
    "CompletionMetadata",
    "CompleteEvent",
    "CacheHitEvent",
    "ErrorEvent",
    "UploadResponse",
    "HealthResponse",
]
```

**Step 4: Write the failing test**

Create `tests/api/__init__.py`:
```python
"""API tests."""
```

Create `tests/api/test_request_models.py`:
```python
"""Tests for API request models."""

import pytest
from pydantic import ValidationError

from doc_generator.infrastructure.api.models.requests import (
    OutputFormat,
    Provider,
    Audience,
    ImageStyle,
    FileSource,
    UrlSource,
    TextSource,
    SourceCategories,
    Preferences,
    CacheOptions,
    GenerateRequest,
)


class TestSourceTypes:
    """Test source type models."""

    def test_file_source_valid(self):
        source = FileSource(file_id="f_abc123")
        assert source.type == "file"
        assert source.file_id == "f_abc123"

    def test_url_source_valid(self):
        source = UrlSource(url="https://example.com/article")
        assert source.type == "url"
        assert source.url == "https://example.com/article"

    def test_text_source_valid(self):
        source = TextSource(content="Some pasted content")
        assert source.type == "text"
        assert source.content == "Some pasted content"


class TestSourceCategories:
    """Test source categories model."""

    def test_empty_categories(self):
        categories = SourceCategories()
        assert categories.primary == []
        assert categories.supporting == []
        assert categories.other == {}

    def test_mixed_sources(self):
        categories = SourceCategories(
            primary=[
                FileSource(file_id="f_1"),
                UrlSource(url="https://example.com"),
            ],
            supporting=[
                TextSource(content="Notes here"),
            ],
            other={
                "custom": [FileSource(file_id="f_2")],
            },
        )
        assert len(categories.primary) == 2
        assert len(categories.supporting) == 1
        assert "custom" in categories.other


class TestPreferences:
    """Test preferences model."""

    def test_defaults(self):
        prefs = Preferences()
        assert prefs.audience == Audience.TECHNICAL
        assert prefs.image_style == ImageStyle.AUTO
        assert prefs.temperature == 0.4
        assert prefs.max_tokens == 8000
        assert prefs.max_slides == 10
        assert prefs.max_summary_points == 5

    def test_temperature_bounds(self):
        with pytest.raises(ValidationError):
            Preferences(temperature=1.5)
        with pytest.raises(ValidationError):
            Preferences(temperature=-0.1)

    def test_max_tokens_bounds(self):
        with pytest.raises(ValidationError):
            Preferences(max_tokens=50)
        with pytest.raises(ValidationError):
            Preferences(max_tokens=50000)


class TestGenerateRequest:
    """Test full generate request model."""

    def test_minimal_request(self):
        request = GenerateRequest(
            output_format=OutputFormat.PDF,
            sources=SourceCategories(
                primary=[TextSource(content="Test content")]
            ),
        )
        assert request.provider == Provider.GOOGLE
        assert request.model == "gemini-3-pro-preview"
        assert request.image_model == "gemini-3-pro-image-preview"
        assert request.cache.reuse is True

    def test_full_request(self):
        request = GenerateRequest(
            output_format=OutputFormat.PPTX,
            sources=SourceCategories(
                primary=[FileSource(file_id="f_1")],
                supporting=[UrlSource(url="https://example.com")],
            ),
            provider=Provider.OPENAI,
            model="gpt-4o",
            image_model="dall-e-3",
            preferences=Preferences(
                audience=Audience.EXECUTIVE,
                image_style=ImageStyle.CORPORATE,
                temperature=0.7,
                max_slides=15,
            ),
            cache=CacheOptions(reuse=False),
        )
        assert request.provider == Provider.OPENAI
        assert request.preferences.audience == Audience.EXECUTIVE
```

**Step 5: Run test to verify it fails**

Run: `pytest tests/api/test_request_models.py -v`
Expected: FAIL with import errors

**Step 6: Write implementation**

Create `src/doc_generator/infrastructure/api/models/requests.py`:

```python
"""Pydantic request models for the API."""

from enum import Enum
from typing import Annotated, Union

from pydantic import BaseModel, Field


class OutputFormat(str, Enum):
    """Supported output formats."""

    PDF = "pdf"
    PPTX = "pptx"


class Provider(str, Enum):
    """Supported LLM providers."""

    GOOGLE = "google"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"


class Audience(str, Enum):
    """Target audience types."""

    TECHNICAL = "technical"
    EXECUTIVE = "executive"
    CLIENT = "client"
    EDUCATIONAL = "educational"


class ImageStyle(str, Enum):
    """Image generation styles."""

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
    """Source from an uploaded file."""

    type: str = "file"
    file_id: str


class UrlSource(BaseModel):
    """Source from a URL."""

    type: str = "url"
    url: str


class TextSource(BaseModel):
    """Source from pasted text."""

    type: str = "text"
    content: str


SourceItem = Annotated[
    Union[FileSource, UrlSource, TextSource],
    Field(discriminator="type"),
]


class SourceCategories(BaseModel):
    """Categorized sources for document generation."""

    primary: list[SourceItem] = Field(default_factory=list)
    supporting: list[SourceItem] = Field(default_factory=list)
    reference: list[SourceItem] = Field(default_factory=list)
    data: list[SourceItem] = Field(default_factory=list)
    other: dict[str, list[SourceItem]] = Field(default_factory=dict)


class Preferences(BaseModel):
    """Generation preferences."""

    audience: Audience = Audience.TECHNICAL
    image_style: ImageStyle = ImageStyle.AUTO
    temperature: float = Field(default=0.4, ge=0.0, le=1.0)
    max_tokens: int = Field(default=8000, ge=100, le=32000)
    max_slides: int = Field(default=10, ge=1, le=50)
    max_summary_points: int = Field(default=5, ge=1, le=20)


class CacheOptions(BaseModel):
    """Caching options."""

    reuse: bool = True


class GenerateRequest(BaseModel):
    """Full document generation request."""

    output_format: OutputFormat
    sources: SourceCategories
    provider: Provider = Provider.GOOGLE
    model: str = "gemini-3-pro-preview"
    image_model: str = "gemini-3-pro-image-preview"
    preferences: Preferences = Field(default_factory=Preferences)
    cache: CacheOptions = Field(default_factory=CacheOptions)
```

**Step 7: Run test to verify it passes**

Run: `pytest tests/api/test_request_models.py -v`
Expected: All tests PASS

**Step 8: Commit**

```bash
git add src/doc_generator/infrastructure/api/ tests/api/
git commit -m "feat(api): add request models with validation"
```

---

## Task 3: Create Response Models

**Files:**
- Create: `src/doc_generator/infrastructure/api/models/responses.py`
- Test: `tests/api/test_response_models.py`

**Step 1: Write the failing test**

Create `tests/api/test_response_models.py`:

```python
"""Tests for API response models."""

from doc_generator.infrastructure.api.models.responses import (
    GenerationStatus,
    ProgressEvent,
    CompletionMetadata,
    CompleteEvent,
    CacheHitEvent,
    ErrorEvent,
    UploadResponse,
    HealthResponse,
)


class TestProgressEvent:
    """Test progress event model."""

    def test_basic_progress(self):
        event = ProgressEvent(
            status=GenerationStatus.PARSING,
            progress=25,
            message="Parsing sources...",
        )
        assert event.status == GenerationStatus.PARSING
        assert event.progress == 25
        assert event.message == "Parsing sources..."

    def test_progress_defaults(self):
        event = ProgressEvent(
            status=GenerationStatus.TRANSFORMING,
            progress=50,
        )
        assert event.message == ""


class TestCompleteEvent:
    """Test completion event model."""

    def test_complete_event(self):
        event = CompleteEvent(
            download_url="https://storage.example.com/doc.pdf",
            expires_in=3600,
            metadata=CompletionMetadata(
                title="Test Document",
                pages=12,
                images_generated=5,
            ),
        )
        assert event.status == GenerationStatus.COMPLETE
        assert event.progress == 100
        assert event.metadata.pages == 12


class TestErrorEvent:
    """Test error event model."""

    def test_error_event(self):
        event = ErrorEvent(
            error="Invalid API key",
            code="AUTH_ERROR",
        )
        assert event.status == GenerationStatus.ERROR
        assert event.error == "Invalid API key"


class TestUploadResponse:
    """Test upload response model."""

    def test_upload_response(self):
        response = UploadResponse(
            file_id="f_abc123",
            filename="report.pdf",
            size=245000,
            mime_type="application/pdf",
        )
        assert response.file_id == "f_abc123"
        assert response.expires_in == 3600


class TestHealthResponse:
    """Test health response model."""

    def test_health_response(self):
        response = HealthResponse(version="0.1.0")
        assert response.status == "healthy"
        assert response.version == "0.1.0"
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/api/test_response_models.py -v`
Expected: FAIL with import errors

**Step 3: Write implementation**

Create `src/doc_generator/infrastructure/api/models/responses.py`:

```python
"""Pydantic response models for the API."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel


class GenerationStatus(str, Enum):
    """Status values for generation progress."""

    PARSING = "parsing"
    TRANSFORMING = "transforming"
    GENERATING_IMAGES = "generating_images"
    GENERATING_OUTPUT = "generating_output"
    UPLOADING = "uploading"
    COMPLETE = "complete"
    CACHE_HIT = "cache_hit"
    ERROR = "error"


class ProgressEvent(BaseModel):
    """Progress update event for SSE streaming."""

    status: GenerationStatus
    progress: int  # 0-100
    message: str = ""


class CompletionMetadata(BaseModel):
    """Metadata about the generated document."""

    title: str
    pages: int = 0
    slides: int = 0
    images_generated: int = 0


class CompleteEvent(BaseModel):
    """Completion event with download URL."""

    status: GenerationStatus = GenerationStatus.COMPLETE
    progress: int = 100
    download_url: str
    expires_in: int = 3600
    metadata: CompletionMetadata


class CacheHitEvent(BaseModel):
    """Cache hit event - document already generated."""

    status: GenerationStatus = GenerationStatus.CACHE_HIT
    progress: int = 100
    download_url: str
    expires_in: int = 3600
    cached_at: str


class ErrorEvent(BaseModel):
    """Error event."""

    status: GenerationStatus = GenerationStatus.ERROR
    error: str
    code: str  # AUTH_ERROR, PARSE_ERROR, GENERATION_ERROR, etc.


class UploadResponse(BaseModel):
    """Response for file upload."""

    file_id: str
    filename: str
    size: int
    mime_type: str
    expires_in: int = 3600


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = "healthy"
    version: str
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/api/test_response_models.py -v`
Expected: All tests PASS

**Step 5: Commit**

```bash
git add src/doc_generator/infrastructure/api/models/responses.py tests/api/test_response_models.py
git commit -m "feat(api): add response models for SSE streaming"
```

---

## Task 4: Create Storage Service

**Files:**
- Create: `src/doc_generator/infrastructure/api/services/__init__.py`
- Create: `src/doc_generator/infrastructure/api/services/storage.py`
- Test: `tests/api/test_storage_service.py`

**Step 1: Write the failing test**

Create `tests/api/test_storage_service.py`:

```python
"""Tests for storage service."""

import pytest
from pathlib import Path

from doc_generator.infrastructure.api.services.storage import StorageService


@pytest.fixture
def storage_service(tmp_path):
    """Create storage service with temp directories."""
    return StorageService(
        upload_dir=tmp_path / "uploads",
        output_dir=tmp_path / "outputs",
    )


class TestStorageService:
    """Test storage service."""

    def test_save_upload(self, storage_service):
        content = b"test file content"
        file_id = storage_service.save_upload(
            content=content,
            filename="test.pdf",
            mime_type="application/pdf",
        )
        assert file_id.startswith("f_")
        assert storage_service.get_upload_path(file_id).exists()

    def test_get_upload_content(self, storage_service):
        content = b"test content"
        file_id = storage_service.save_upload(
            content=content,
            filename="test.txt",
            mime_type="text/plain",
        )
        retrieved = storage_service.get_upload_content(file_id)
        assert retrieved == content

    def test_get_nonexistent_upload(self, storage_service):
        with pytest.raises(FileNotFoundError):
            storage_service.get_upload_content("f_nonexistent")

    def test_save_output(self, storage_service):
        content = b"generated pdf content"
        output_path = storage_service.save_output(
            content=content,
            filename="output.pdf",
        )
        assert output_path.exists()
        assert output_path.read_bytes() == content

    def test_get_download_url(self, storage_service):
        content = b"pdf content"
        output_path = storage_service.save_output(
            content=content,
            filename="doc.pdf",
        )
        url = storage_service.get_download_url(output_path)
        assert "doc.pdf" in url

    def test_cleanup_expired(self, storage_service):
        file_id = storage_service.save_upload(
            content=b"temp",
            filename="temp.txt",
            mime_type="text/plain",
        )
        path = storage_service.get_upload_path(file_id)
        assert path.exists()
        storage_service.cleanup_upload(file_id)
        assert not path.exists()
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/api/test_storage_service.py -v`
Expected: FAIL with import errors

**Step 3: Write implementation**

Create `src/doc_generator/infrastructure/api/services/__init__.py`:

```python
"""API services for document generation."""

from .storage import StorageService

__all__ = ["StorageService"]
```

Create `src/doc_generator/infrastructure/api/services/storage.py`:

```python
"""Storage service for uploads and outputs."""

import hashlib
import secrets
import time
from pathlib import Path
from typing import Optional


class StorageService:
    """Manages temporary uploads and generated outputs."""

    def __init__(
        self,
        upload_dir: Path = Path("src/output/uploads"),
        output_dir: Path = Path("src/output/generated"),
        base_url: str = "/api/download",
    ):
        """Initialize storage service.

        Args:
            upload_dir: Directory for temporary uploads
            output_dir: Directory for generated outputs
            base_url: Base URL for download links
        """
        self.upload_dir = Path(upload_dir)
        self.output_dir = Path(output_dir)
        self.base_url = base_url

        # Ensure directories exist
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Track upload metadata
        self._uploads: dict[str, dict] = {}

    def save_upload(
        self,
        content: bytes,
        filename: str,
        mime_type: str,
    ) -> str:
        """Save uploaded file and return file_id.

        Args:
            content: File content bytes
            filename: Original filename
            mime_type: MIME type of file

        Returns:
            Unique file ID (f_...)
        """
        file_id = f"f_{secrets.token_hex(12)}"
        ext = Path(filename).suffix
        storage_path = self.upload_dir / f"{file_id}{ext}"

        storage_path.write_bytes(content)

        self._uploads[file_id] = {
            "filename": filename,
            "mime_type": mime_type,
            "path": storage_path,
            "created_at": time.time(),
        }

        return file_id

    def get_upload_path(self, file_id: str) -> Path:
        """Get path to uploaded file.

        Args:
            file_id: File ID from save_upload

        Returns:
            Path to the file

        Raises:
            FileNotFoundError: If file_id not found
        """
        if file_id not in self._uploads:
            raise FileNotFoundError(f"Upload not found: {file_id}")
        return self._uploads[file_id]["path"]

    def get_upload_content(self, file_id: str) -> bytes:
        """Get content of uploaded file.

        Args:
            file_id: File ID from save_upload

        Returns:
            File content bytes

        Raises:
            FileNotFoundError: If file_id not found
        """
        path = self.get_upload_path(file_id)
        return path.read_bytes()

    def get_upload_metadata(self, file_id: str) -> dict:
        """Get metadata for uploaded file.

        Args:
            file_id: File ID from save_upload

        Returns:
            Metadata dict with filename, mime_type, path, created_at

        Raises:
            FileNotFoundError: If file_id not found
        """
        if file_id not in self._uploads:
            raise FileNotFoundError(f"Upload not found: {file_id}")
        return self._uploads[file_id].copy()

    def save_output(
        self,
        content: bytes,
        filename: str,
    ) -> Path:
        """Save generated output file.

        Args:
            content: Generated file content
            filename: Output filename

        Returns:
            Path to saved file
        """
        # Add timestamp to ensure uniqueness
        timestamp = int(time.time())
        stem = Path(filename).stem
        ext = Path(filename).suffix
        unique_filename = f"{stem}_{timestamp}{ext}"

        output_path = self.output_dir / unique_filename
        output_path.write_bytes(content)

        return output_path

    def get_download_url(self, output_path: Path) -> str:
        """Generate download URL for output file.

        Args:
            output_path: Path to the output file

        Returns:
            Download URL with token
        """
        # Generate a simple token (in production, use signed URLs)
        token = secrets.token_urlsafe(16)
        filename = output_path.name
        return f"{self.base_url}/{filename}?token={token}"

    def cleanup_upload(self, file_id: str) -> None:
        """Remove uploaded file.

        Args:
            file_id: File ID to remove
        """
        if file_id in self._uploads:
            path = self._uploads[file_id]["path"]
            if path.exists():
                path.unlink()
            del self._uploads[file_id]

    def cleanup_expired_uploads(self, max_age_seconds: int = 3600) -> int:
        """Remove uploads older than max_age.

        Args:
            max_age_seconds: Maximum age in seconds (default 1 hour)

        Returns:
            Number of files cleaned up
        """
        now = time.time()
        expired = []

        for file_id, metadata in self._uploads.items():
            if now - metadata["created_at"] > max_age_seconds:
                expired.append(file_id)

        for file_id in expired:
            self.cleanup_upload(file_id)

        return len(expired)
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/api/test_storage_service.py -v`
Expected: All tests PASS

**Step 5: Commit**

```bash
git add src/doc_generator/infrastructure/api/services/ tests/api/test_storage_service.py
git commit -m "feat(api): add storage service for uploads and outputs"
```

---

## Task 5: Create Cache Service

**Files:**
- Create: `src/doc_generator/infrastructure/api/services/cache.py`
- Test: `tests/api/test_cache_service.py`

**Step 1: Write the failing test**

Create `tests/api/test_cache_service.py`:

```python
"""Tests for cache service."""

import pytest
from pathlib import Path

from doc_generator.infrastructure.api.services.cache import CacheService
from doc_generator.infrastructure.api.models.requests import (
    GenerateRequest,
    OutputFormat,
    SourceCategories,
    TextSource,
    Preferences,
    Provider,
)


@pytest.fixture
def cache_service(tmp_path):
    """Create cache service with temp directory."""
    return CacheService(cache_dir=tmp_path / "cache")


class TestCacheService:
    """Test cache service."""

    def test_generate_cache_key(self, cache_service):
        request = GenerateRequest(
            output_format=OutputFormat.PDF,
            sources=SourceCategories(
                primary=[TextSource(content="Test content")]
            ),
        )
        key = cache_service.generate_cache_key(request)
        assert len(key) == 64  # SHA256 hex digest

    def test_same_request_same_key(self, cache_service):
        request1 = GenerateRequest(
            output_format=OutputFormat.PDF,
            sources=SourceCategories(
                primary=[TextSource(content="Test content")]
            ),
        )
        request2 = GenerateRequest(
            output_format=OutputFormat.PDF,
            sources=SourceCategories(
                primary=[TextSource(content="Test content")]
            ),
        )
        assert cache_service.generate_cache_key(request1) == cache_service.generate_cache_key(request2)

    def test_different_content_different_key(self, cache_service):
        request1 = GenerateRequest(
            output_format=OutputFormat.PDF,
            sources=SourceCategories(
                primary=[TextSource(content="Content A")]
            ),
        )
        request2 = GenerateRequest(
            output_format=OutputFormat.PDF,
            sources=SourceCategories(
                primary=[TextSource(content="Content B")]
            ),
        )
        assert cache_service.generate_cache_key(request1) != cache_service.generate_cache_key(request2)

    def test_cache_miss(self, cache_service):
        request = GenerateRequest(
            output_format=OutputFormat.PDF,
            sources=SourceCategories(
                primary=[TextSource(content="Test")]
            ),
        )
        result = cache_service.get(request)
        assert result is None

    def test_cache_hit(self, cache_service):
        request = GenerateRequest(
            output_format=OutputFormat.PDF,
            sources=SourceCategories(
                primary=[TextSource(content="Test")]
            ),
        )
        cache_service.set(
            request=request,
            output_path=Path("/output/doc.pdf"),
            metadata={"title": "Test Doc"},
        )
        result = cache_service.get(request)
        assert result is not None
        assert result["metadata"]["title"] == "Test Doc"
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/api/test_cache_service.py -v`
Expected: FAIL with import errors

**Step 3: Write implementation**

Create `src/doc_generator/infrastructure/api/services/cache.py`:

```python
"""Cache service for generated documents."""

import hashlib
import json
import time
from pathlib import Path
from typing import Optional

from ..models.requests import GenerateRequest


class CacheService:
    """Content-based cache for generated documents."""

    def __init__(
        self,
        cache_dir: Path = Path("src/output/cache"),
        ttl_seconds: int = 86400,  # 24 hours
    ):
        """Initialize cache service.

        Args:
            cache_dir: Directory for cache metadata
            ttl_seconds: Time-to-live for cache entries
        """
        self.cache_dir = Path(cache_dir)
        self.ttl_seconds = ttl_seconds
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def generate_cache_key(self, request: GenerateRequest) -> str:
        """Generate cache key from request.

        The key is a SHA256 hash of the normalized request content.

        Args:
            request: Generate request

        Returns:
            64-character hex string cache key
        """
        # Build canonical representation
        canonical = {
            "output_format": request.output_format.value,
            "sources": self._normalize_sources(request.sources),
            "provider": request.provider.value,
            "model": request.model,
            "image_model": request.image_model,
            "preferences": {
                "audience": request.preferences.audience.value,
                "image_style": request.preferences.image_style.value,
                "temperature": request.preferences.temperature,
                "max_tokens": request.preferences.max_tokens,
                "max_slides": request.preferences.max_slides,
                "max_summary_points": request.preferences.max_summary_points,
            },
        }

        # Generate hash
        canonical_json = json.dumps(canonical, sort_keys=True)
        return hashlib.sha256(canonical_json.encode()).hexdigest()

    def _normalize_sources(self, sources) -> dict:
        """Normalize sources for hashing."""
        result = {
            "primary": [self._normalize_source(s) for s in sources.primary],
            "supporting": [self._normalize_source(s) for s in sources.supporting],
            "reference": [self._normalize_source(s) for s in sources.reference],
            "data": [self._normalize_source(s) for s in sources.data],
            "other": {
                k: [self._normalize_source(s) for s in v]
                for k, v in sources.other.items()
            },
        }
        return result

    def _normalize_source(self, source) -> dict:
        """Normalize a single source for hashing."""
        if source.type == "text":
            return {"type": "text", "content": source.content}
        elif source.type == "url":
            return {"type": "url", "url": source.url}
        elif source.type == "file":
            return {"type": "file", "file_id": source.file_id}
        return {}

    def get(self, request: GenerateRequest) -> Optional[dict]:
        """Get cached result for request.

        Args:
            request: Generate request

        Returns:
            Cache entry dict or None if not found/expired
        """
        key = self.generate_cache_key(request)
        cache_file = self.cache_dir / f"{key}.json"

        if not cache_file.exists():
            return None

        try:
            data = json.loads(cache_file.read_text())

            # Check if expired
            if time.time() - data["created_at"] > self.ttl_seconds:
                cache_file.unlink()
                return None

            return data
        except (json.JSONDecodeError, KeyError):
            return None

    def set(
        self,
        request: GenerateRequest,
        output_path: Path,
        metadata: dict,
    ) -> str:
        """Store cache entry.

        Args:
            request: Generate request
            output_path: Path to generated output
            metadata: Generation metadata

        Returns:
            Cache key
        """
        key = self.generate_cache_key(request)
        cache_file = self.cache_dir / f"{key}.json"

        data = {
            "key": key,
            "output_path": str(output_path),
            "metadata": metadata,
            "created_at": time.time(),
        }

        cache_file.write_text(json.dumps(data))
        return key

    def invalidate(self, request: GenerateRequest) -> bool:
        """Invalidate cache entry.

        Args:
            request: Generate request

        Returns:
            True if entry was removed, False if not found
        """
        key = self.generate_cache_key(request)
        cache_file = self.cache_dir / f"{key}.json"

        if cache_file.exists():
            cache_file.unlink()
            return True
        return False
```

**Step 4: Update services __init__.py**

```python
"""API services for document generation."""

from .storage import StorageService
from .cache import CacheService

__all__ = ["StorageService", "CacheService"]
```

**Step 5: Run test to verify it passes**

Run: `pytest tests/api/test_cache_service.py -v`
Expected: All tests PASS

**Step 6: Commit**

```bash
git add src/doc_generator/infrastructure/api/services/ tests/api/test_cache_service.py
git commit -m "feat(api): add cache service for content-based caching"
```

---

## Task 6: Create API Dependencies

**Files:**
- Create: `src/doc_generator/infrastructure/api/dependencies.py`
- Test: `tests/api/test_dependencies.py`

**Step 1: Write the failing test**

Create `tests/api/test_dependencies.py`:

```python
"""Tests for API dependencies."""

import pytest
from fastapi import HTTPException

from doc_generator.infrastructure.api.dependencies import (
    extract_api_keys,
    get_api_key_for_provider,
    APIKeys,
)
from doc_generator.infrastructure.api.models.requests import Provider


class TestExtractAPIKeys:
    """Test API key extraction from headers."""

    def test_extract_google_key(self):
        keys = extract_api_keys(
            x_google_key="AIza123",
            x_openai_key=None,
            x_anthropic_key=None,
        )
        assert keys.google == "AIza123"
        assert keys.openai is None
        assert keys.anthropic is None

    def test_extract_all_keys(self):
        keys = extract_api_keys(
            x_google_key="AIza123",
            x_openai_key="sk-abc",
            x_anthropic_key="sk-ant-xyz",
        )
        assert keys.google == "AIza123"
        assert keys.openai == "sk-abc"
        assert keys.anthropic == "sk-ant-xyz"

    def test_extract_no_keys(self):
        keys = extract_api_keys(
            x_google_key=None,
            x_openai_key=None,
            x_anthropic_key=None,
        )
        assert keys.google is None


class TestGetAPIKeyForProvider:
    """Test getting API key for specific provider."""

    def test_get_google_key(self):
        keys = APIKeys(google="AIza123", openai=None, anthropic=None)
        key = get_api_key_for_provider(Provider.GOOGLE, keys)
        assert key == "AIza123"

    def test_missing_key_raises(self):
        keys = APIKeys(google=None, openai="sk-abc", anthropic=None)
        with pytest.raises(HTTPException) as exc_info:
            get_api_key_for_provider(Provider.GOOGLE, keys)
        assert exc_info.value.status_code == 401
        assert "X-Google-Key" in exc_info.value.detail
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/api/test_dependencies.py -v`
Expected: FAIL with import errors

**Step 3: Write implementation**

Create `src/doc_generator/infrastructure/api/dependencies.py`:

```python
"""FastAPI dependencies for API routes."""

from dataclasses import dataclass
from typing import Optional

from fastapi import Header, HTTPException

from .models.requests import Provider


@dataclass
class APIKeys:
    """Container for API keys from headers."""

    google: Optional[str] = None
    openai: Optional[str] = None
    anthropic: Optional[str] = None


def extract_api_keys(
    x_google_key: Optional[str] = Header(None, alias="X-Google-Key"),
    x_openai_key: Optional[str] = Header(None, alias="X-OpenAI-Key"),
    x_anthropic_key: Optional[str] = Header(None, alias="X-Anthropic-Key"),
) -> APIKeys:
    """Extract API keys from request headers.

    Args:
        x_google_key: Google/Gemini API key
        x_openai_key: OpenAI API key
        x_anthropic_key: Anthropic/Claude API key

    Returns:
        APIKeys container with extracted keys
    """
    return APIKeys(
        google=x_google_key,
        openai=x_openai_key,
        anthropic=x_anthropic_key,
    )


def get_api_key_for_provider(provider: Provider, keys: APIKeys) -> str:
    """Get API key for the specified provider.

    Args:
        provider: The LLM provider
        keys: Extracted API keys

    Returns:
        The API key for the provider

    Raises:
        HTTPException: If the required API key is missing
    """
    key_map = {
        Provider.GOOGLE: (keys.google, "X-Google-Key"),
        Provider.OPENAI: (keys.openai, "X-OpenAI-Key"),
        Provider.ANTHROPIC: (keys.anthropic, "X-Anthropic-Key"),
    }

    key, header_name = key_map[provider]

    if not key:
        raise HTTPException(
            status_code=401,
            detail=f"Missing required header: {header_name}",
        )

    return key
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/api/test_dependencies.py -v`
Expected: All tests PASS

**Step 5: Commit**

```bash
git add src/doc_generator/infrastructure/api/dependencies.py tests/api/test_dependencies.py
git commit -m "feat(api): add dependencies for API key extraction"
```

---

## Task 7: Create Health Route

**Files:**
- Create: `src/doc_generator/infrastructure/api/routes/__init__.py`
- Create: `src/doc_generator/infrastructure/api/routes/health.py`
- Test: `tests/api/test_health_route.py`

**Step 1: Write the failing test**

Create `tests/api/test_health_route.py`:

```python
"""Tests for health route."""

import pytest
from fastapi.testclient import TestClient

from doc_generator.infrastructure.api.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


class TestHealthRoute:
    """Test health check endpoint."""

    def test_health_check(self, client):
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/api/test_health_route.py -v`
Expected: FAIL with import errors

**Step 3: Write implementation**

Create `src/doc_generator/infrastructure/api/routes/__init__.py`:

```python
"""API routes."""

from .health import router as health_router
from .upload import router as upload_router
from .generate import router as generate_router

__all__ = ["health_router", "upload_router", "generate_router"]
```

Create `src/doc_generator/infrastructure/api/routes/health.py`:

```python
"""Health check route."""

from fastapi import APIRouter

from ..models.responses import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint.

    Returns:
        Health status and version
    """
    return HealthResponse(
        status="healthy",
        version="0.1.0",
    )
```

**Step 4: Create main FastAPI app (stub for now)**

Create `src/doc_generator/infrastructure/api/main.py`:

```python
"""FastAPI application for document generation."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import health_router

app = FastAPI(
    title="Document Generator API",
    description="Generate PDF and PPTX documents from multiple sources",
    version="0.1.0",
)

# CORS middleware for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router, prefix="/api")
```

**Step 5: Run test to verify it passes**

Run: `pytest tests/api/test_health_route.py -v`
Expected: All tests PASS

**Step 6: Commit**

```bash
git add src/doc_generator/infrastructure/api/routes/ src/doc_generator/infrastructure/api/main.py tests/api/test_health_route.py
git commit -m "feat(api): add health check endpoint and FastAPI app"
```

---

## Task 8: Create Upload Route

**Files:**
- Create: `src/doc_generator/infrastructure/api/routes/upload.py`
- Test: `tests/api/test_upload_route.py`

**Step 1: Write the failing test**

Create `tests/api/test_upload_route.py`:

```python
"""Tests for upload route."""

import pytest
from fastapi.testclient import TestClient
from io import BytesIO

from doc_generator.infrastructure.api.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


class TestUploadRoute:
    """Test file upload endpoint."""

    def test_upload_pdf(self, client):
        content = b"%PDF-1.4 fake pdf content"
        files = {"file": ("report.pdf", BytesIO(content), "application/pdf")}
        response = client.post("/api/upload", files=files)
        assert response.status_code == 200
        data = response.json()
        assert data["file_id"].startswith("f_")
        assert data["filename"] == "report.pdf"
        assert data["mime_type"] == "application/pdf"
        assert data["size"] == len(content)

    def test_upload_text(self, client):
        content = b"Plain text content"
        files = {"file": ("notes.txt", BytesIO(content), "text/plain")}
        response = client.post("/api/upload", files=files)
        assert response.status_code == 200
        data = response.json()
        assert data["filename"] == "notes.txt"

    def test_upload_no_file(self, client):
        response = client.post("/api/upload")
        assert response.status_code == 422  # Validation error
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/api/test_upload_route.py -v`
Expected: FAIL with import errors or 404

**Step 3: Write implementation**

Create `src/doc_generator/infrastructure/api/routes/upload.py`:

```python
"""File upload route."""

from fastapi import APIRouter, File, UploadFile

from ..models.responses import UploadResponse
from ..services.storage import StorageService

router = APIRouter(tags=["upload"])

# Shared storage service instance
_storage_service: StorageService | None = None


def get_storage_service() -> StorageService:
    """Get or create storage service."""
    global _storage_service
    if _storage_service is None:
        _storage_service = StorageService()
    return _storage_service


@router.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)) -> UploadResponse:
    """Upload a file for document generation.

    Args:
        file: The file to upload

    Returns:
        Upload response with file_id
    """
    storage = get_storage_service()

    content = await file.read()
    file_id = storage.save_upload(
        content=content,
        filename=file.filename or "unknown",
        mime_type=file.content_type or "application/octet-stream",
    )

    return UploadResponse(
        file_id=file_id,
        filename=file.filename or "unknown",
        size=len(content),
        mime_type=file.content_type or "application/octet-stream",
    )
```

**Step 4: Update main.py to include upload router**

Update `src/doc_generator/infrastructure/api/main.py`:

```python
"""FastAPI application for document generation."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import health_router, upload_router

app = FastAPI(
    title="Document Generator API",
    description="Generate PDF and PPTX documents from multiple sources",
    version="0.1.0",
)

# CORS middleware for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router, prefix="/api")
app.include_router(upload_router, prefix="/api")
```

**Step 5: Run test to verify it passes**

Run: `pytest tests/api/test_upload_route.py -v`
Expected: All tests PASS

**Step 6: Commit**

```bash
git add src/doc_generator/infrastructure/api/routes/upload.py src/doc_generator/infrastructure/api/main.py tests/api/test_upload_route.py
git commit -m "feat(api): add file upload endpoint"
```

---

## Task 9: Create Generation Service

**Files:**
- Create: `src/doc_generator/infrastructure/api/services/generation.py`
- Test: `tests/api/test_generation_service.py`

**Step 1: Write the failing test**

Create `tests/api/test_generation_service.py`:

```python
"""Tests for generation service."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from doc_generator.infrastructure.api.services.generation import GenerationService
from doc_generator.infrastructure.api.models.requests import (
    GenerateRequest,
    OutputFormat,
    SourceCategories,
    TextSource,
    Provider,
)
from doc_generator.infrastructure.api.models.responses import GenerationStatus


class TestGenerationService:
    """Test generation service."""

    @pytest.fixture
    def service(self, tmp_path):
        """Create generation service."""
        return GenerationService(output_dir=tmp_path)

    @pytest.mark.asyncio
    async def test_progress_callback(self, service):
        """Test that progress events are yielded."""
        events = []

        async def collect_events():
            request = GenerateRequest(
                output_format=OutputFormat.PDF,
                sources=SourceCategories(
                    primary=[TextSource(content="Test content for PDF generation")]
                ),
            )
            async for event in service.generate(
                request=request,
                api_key="test-key",
            ):
                events.append(event)
                # Stop after first few events for test
                if len(events) >= 2:
                    break

        await collect_events()
        assert len(events) >= 1
        assert events[0].status == GenerationStatus.PARSING
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/api/test_generation_service.py -v`
Expected: FAIL with import errors

**Step 3: Write implementation**

Create `src/doc_generator/infrastructure/api/services/generation.py`:

```python
"""Generation service for document creation with progress streaming."""

import asyncio
import tempfile
from pathlib import Path
from typing import AsyncIterator, Optional

from loguru import logger

from ..models.requests import (
    GenerateRequest,
    Provider,
    FileSource,
    UrlSource,
    TextSource,
)
from ..models.responses import (
    GenerationStatus,
    ProgressEvent,
    CompleteEvent,
    CompletionMetadata,
    ErrorEvent,
)
from .storage import StorageService


class GenerationService:
    """Orchestrates document generation with progress streaming."""

    def __init__(
        self,
        output_dir: Path = Path("src/output/generated"),
        storage_service: Optional[StorageService] = None,
    ):
        """Initialize generation service.

        Args:
            output_dir: Directory for generated outputs
            storage_service: Storage service for file operations
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.storage = storage_service or StorageService()

    async def generate(
        self,
        request: GenerateRequest,
        api_key: str,
    ) -> AsyncIterator[ProgressEvent | CompleteEvent | ErrorEvent]:
        """Generate document with progress streaming.

        Args:
            request: Generation request
            api_key: API key for LLM provider

        Yields:
            Progress events, then completion or error event
        """
        try:
            # Phase 1: Parse sources
            yield ProgressEvent(
                status=GenerationStatus.PARSING,
                progress=5,
                message="Starting to parse sources...",
            )

            content = await self._collect_sources(request)

            yield ProgressEvent(
                status=GenerationStatus.PARSING,
                progress=20,
                message=f"Parsed {len(request.sources.primary)} primary sources",
            )

            # Phase 2: Transform content
            yield ProgressEvent(
                status=GenerationStatus.TRANSFORMING,
                progress=30,
                message="Structuring content...",
            )

            # Run the workflow
            result = await self._run_workflow(
                content=content,
                request=request,
                api_key=api_key,
                progress_callback=lambda status, progress, msg: None,  # TODO: wire up
            )

            yield ProgressEvent(
                status=GenerationStatus.TRANSFORMING,
                progress=50,
                message="Content structured",
            )

            # Phase 3: Generate images (if applicable)
            yield ProgressEvent(
                status=GenerationStatus.GENERATING_IMAGES,
                progress=60,
                message="Generating images...",
            )

            await asyncio.sleep(0.1)  # Placeholder for actual image generation

            yield ProgressEvent(
                status=GenerationStatus.GENERATING_IMAGES,
                progress=70,
                message="Images generated",
            )

            # Phase 4: Generate output
            yield ProgressEvent(
                status=GenerationStatus.GENERATING_OUTPUT,
                progress=80,
                message=f"Building {request.output_format.value.upper()}...",
            )

            output_path = result.get("output_path", "")

            yield ProgressEvent(
                status=GenerationStatus.GENERATING_OUTPUT,
                progress=90,
                message="Output generated",
            )

            # Phase 5: Upload/finalize
            yield ProgressEvent(
                status=GenerationStatus.UPLOADING,
                progress=95,
                message="Finalizing...",
            )

            download_url = self.storage.get_download_url(Path(output_path)) if output_path else ""

            # Complete
            yield CompleteEvent(
                download_url=download_url,
                expires_in=3600,
                metadata=CompletionMetadata(
                    title=result.get("metadata", {}).get("title", "Generated Document"),
                    pages=result.get("metadata", {}).get("pages", 0),
                    slides=result.get("metadata", {}).get("slides", 0),
                    images_generated=result.get("metadata", {}).get("images_generated", 0),
                ),
            )

        except Exception as e:
            logger.error(f"Generation failed: {e}")
            yield ErrorEvent(
                error=str(e),
                code="GENERATION_ERROR",
            )

    async def _collect_sources(self, request: GenerateRequest) -> str:
        """Collect content from all sources.

        Args:
            request: Generation request

        Returns:
            Combined content string
        """
        contents = []

        all_sources = (
            request.sources.primary
            + request.sources.supporting
            + request.sources.reference
            + request.sources.data
        )

        for category_sources in request.sources.other.values():
            all_sources.extend(category_sources)

        for source in all_sources:
            if isinstance(source, TextSource):
                contents.append(source.content)
            elif isinstance(source, UrlSource):
                # TODO: Fetch URL content using web parser
                contents.append(f"[Content from: {source.url}]")
            elif isinstance(source, FileSource):
                # TODO: Get file content from storage
                contents.append(f"[Content from file: {source.file_id}]")

        return "\n\n".join(contents)

    async def _run_workflow(
        self,
        content: str,
        request: GenerateRequest,
        api_key: str,
        progress_callback,
    ) -> dict:
        """Run the document generation workflow.

        Args:
            content: Combined source content
            request: Generation request
            api_key: API key for LLM
            progress_callback: Callback for progress updates

        Returns:
            Workflow result dict
        """
        # Import here to avoid circular imports
        from doc_generator.application.graph_workflow import run_workflow

        # Write content to temp file
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".md",
            delete=False,
        ) as f:
            f.write(content)
            temp_path = f.name

        try:
            # Run workflow
            result = run_workflow(
                input_path=temp_path,
                output_format=request.output_format.value,
            )
            return result
        finally:
            # Cleanup temp file
            Path(temp_path).unlink(missing_ok=True)
```

**Step 4: Update services __init__.py**

```python
"""API services for document generation."""

from .storage import StorageService
from .cache import CacheService
from .generation import GenerationService

__all__ = ["StorageService", "CacheService", "GenerationService"]
```

**Step 5: Run test to verify it passes**

Run: `pytest tests/api/test_generation_service.py -v`
Expected: All tests PASS

**Step 6: Commit**

```bash
git add src/doc_generator/infrastructure/api/services/ tests/api/test_generation_service.py
git commit -m "feat(api): add generation service with progress streaming"
```

---

## Task 10: Create Generate Route with SSE

**Files:**
- Create: `src/doc_generator/infrastructure/api/routes/generate.py`
- Test: `tests/api/test_generate_route.py`

**Step 1: Write the failing test**

Create `tests/api/test_generate_route.py`:

```python
"""Tests for generate route."""

import pytest
from fastapi.testclient import TestClient

from doc_generator.infrastructure.api.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


class TestGenerateRoute:
    """Test document generation endpoint."""

    def test_generate_missing_api_key(self, client):
        """Test that missing API key returns 401."""
        response = client.post(
            "/api/generate",
            json={
                "output_format": "pdf",
                "sources": {
                    "primary": [{"type": "text", "content": "Test content"}],
                },
            },
        )
        assert response.status_code == 401

    def test_generate_with_api_key(self, client):
        """Test generation with API key returns SSE stream."""
        response = client.post(
            "/api/generate",
            json={
                "output_format": "pdf",
                "sources": {
                    "primary": [{"type": "text", "content": "Test content"}],
                },
            },
            headers={"X-Google-Key": "test-key"},
        )
        # Should return streaming response
        assert response.status_code == 200
        assert "text/event-stream" in response.headers.get("content-type", "")

    def test_generate_invalid_format(self, client):
        """Test that invalid output format returns error."""
        response = client.post(
            "/api/generate",
            json={
                "output_format": "invalid",
                "sources": {
                    "primary": [{"type": "text", "content": "Test"}],
                },
            },
            headers={"X-Google-Key": "test-key"},
        )
        assert response.status_code == 422  # Validation error
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/api/test_generate_route.py -v`
Expected: FAIL with 404 or import errors

**Step 3: Write implementation**

Create `src/doc_generator/infrastructure/api/routes/generate.py`:

```python
"""Document generation route with SSE streaming."""

import json
from typing import AsyncIterator

from fastapi import APIRouter, Depends
from sse_starlette.sse import EventSourceResponse

from ..dependencies import APIKeys, extract_api_keys, get_api_key_for_provider
from ..models.requests import GenerateRequest
from ..models.responses import ProgressEvent, CompleteEvent, ErrorEvent
from ..services.generation import GenerationService
from ..services.cache import CacheService

router = APIRouter(tags=["generate"])

# Shared service instances
_generation_service: GenerationService | None = None
_cache_service: CacheService | None = None


def get_generation_service() -> GenerationService:
    """Get or create generation service."""
    global _generation_service
    if _generation_service is None:
        _generation_service = GenerationService()
    return _generation_service


def get_cache_service() -> CacheService:
    """Get or create cache service."""
    global _cache_service
    if _cache_service is None:
        _cache_service = CacheService()
    return _cache_service


async def event_generator(
    request: GenerateRequest,
    api_key: str,
    generation_service: GenerationService,
    cache_service: CacheService,
) -> AsyncIterator[dict]:
    """Generate SSE events for document creation.

    Args:
        request: Generation request
        api_key: API key for LLM provider
        generation_service: Generation service
        cache_service: Cache service

    Yields:
        SSE event dicts
    """
    # Check cache first if reuse enabled
    if request.cache.reuse:
        cached = cache_service.get(request)
        if cached:
            from ..models.responses import CacheHitEvent, GenerationStatus
            import datetime

            event = CacheHitEvent(
                download_url=cached["output_path"],
                cached_at=datetime.datetime.fromtimestamp(
                    cached["created_at"]
                ).isoformat(),
            )
            yield {"data": event.model_dump_json()}
            return

    # Generate document
    async for event in generation_service.generate(
        request=request,
        api_key=api_key,
    ):
        yield {"data": event.model_dump_json()}

        # Cache successful completions
        if isinstance(event, CompleteEvent):
            from pathlib import Path

            cache_service.set(
                request=request,
                output_path=Path(event.download_url),
                metadata=event.metadata.model_dump(),
            )


@router.post("/generate")
async def generate_document(
    request: GenerateRequest,
    api_keys: APIKeys = Depends(extract_api_keys),
) -> EventSourceResponse:
    """Generate a document from sources.

    Streams progress events via SSE, ending with completion or error.

    Args:
        request: Generation request
        api_keys: API keys from headers

    Returns:
        SSE event stream
    """
    # Validate API key for provider
    api_key = get_api_key_for_provider(request.provider, api_keys)

    generation_service = get_generation_service()
    cache_service = get_cache_service()

    return EventSourceResponse(
        event_generator(
            request=request,
            api_key=api_key,
            generation_service=generation_service,
            cache_service=cache_service,
        )
    )
```

**Step 4: Update main.py to include generate router**

Update `src/doc_generator/infrastructure/api/main.py`:

```python
"""FastAPI application for document generation."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import health_router, upload_router, generate_router

app = FastAPI(
    title="Document Generator API",
    description="Generate PDF and PPTX documents from multiple sources",
    version="0.1.0",
)

# CORS middleware for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router, prefix="/api")
app.include_router(upload_router, prefix="/api")
app.include_router(generate_router, prefix="/api")
```

**Step 5: Run test to verify it passes**

Run: `pytest tests/api/test_generate_route.py -v`
Expected: All tests PASS

**Step 6: Commit**

```bash
git add src/doc_generator/infrastructure/api/ tests/api/test_generate_route.py
git commit -m "feat(api): add generate endpoint with SSE streaming"
```

---

## Task 11: Add Run Script

**Files:**
- Create: `scripts/run_api.py`
- Modify: `Makefile`

**Step 1: Create run script**

Create `scripts/run_api.py`:

```python
#!/usr/bin/env python3
"""Run the FastAPI server."""

import uvicorn


def main():
    """Start the API server."""
    uvicorn.run(
        "doc_generator.infrastructure.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    main()
```

**Step 2: Add Makefile target**

Add to `Makefile`:

```makefile
run-api:  ## Run the FastAPI server
	@echo "Starting API server on http://localhost:8000"
	@$(PYTHON) scripts/run_api.py
```

**Step 3: Test the server starts**

Run: `make run-api`
Expected: Server starts on http://localhost:8000

**Step 4: Test health endpoint**

Run: `curl http://localhost:8000/api/health`
Expected: `{"status":"healthy","version":"0.1.0"}`

**Step 5: Commit**

```bash
git add scripts/run_api.py Makefile
git commit -m "feat(api): add run script and Makefile target"
```

---

## Task 12: Final Integration Test

**Files:**
- Test: `tests/api/test_integration.py`

**Step 1: Write integration test**

Create `tests/api/test_integration.py`:

```python
"""Integration tests for the full API."""

import pytest
from fastapi.testclient import TestClient
from io import BytesIO

from doc_generator.infrastructure.api.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


class TestFullWorkflow:
    """Test full document generation workflow."""

    def test_upload_then_generate(self, client):
        """Test uploading a file then generating a document."""
        # Step 1: Upload a file
        content = b"# Test Document\n\nThis is test content."
        files = {"file": ("test.md", BytesIO(content), "text/markdown")}
        upload_response = client.post("/api/upload", files=files)
        assert upload_response.status_code == 200
        file_id = upload_response.json()["file_id"]

        # Step 2: Generate document (will fail without real API key, but should stream)
        generate_response = client.post(
            "/api/generate",
            json={
                "output_format": "pdf",
                "sources": {
                    "primary": [{"type": "file", "file_id": file_id}],
                },
            },
            headers={"X-Google-Key": "test-key"},
        )
        assert generate_response.status_code == 200
        assert "text/event-stream" in generate_response.headers.get("content-type", "")

    def test_text_source_generation(self, client):
        """Test generating from pasted text."""
        response = client.post(
            "/api/generate",
            json={
                "output_format": "pptx",
                "sources": {
                    "primary": [
                        {"type": "text", "content": "# Presentation\n\n- Point 1\n- Point 2"}
                    ],
                },
                "preferences": {
                    "audience": "executive",
                    "max_slides": 5,
                },
            },
            headers={"X-Google-Key": "test-key"},
        )
        assert response.status_code == 200
```

**Step 2: Run integration test**

Run: `pytest tests/api/test_integration.py -v`
Expected: All tests PASS

**Step 3: Run all API tests**

Run: `pytest tests/api/ -v`
Expected: All tests PASS

**Step 4: Final commit**

```bash
git add tests/api/test_integration.py
git commit -m "test(api): add integration tests for full workflow"
```

---

## Summary

**Total Tasks:** 12

**Files Created:**
- `src/doc_generator/infrastructure/api/__init__.py`
- `src/doc_generator/infrastructure/api/main.py`
- `src/doc_generator/infrastructure/api/dependencies.py`
- `src/doc_generator/infrastructure/api/models/__init__.py`
- `src/doc_generator/infrastructure/api/models/requests.py`
- `src/doc_generator/infrastructure/api/models/responses.py`
- `src/doc_generator/infrastructure/api/routes/__init__.py`
- `src/doc_generator/infrastructure/api/routes/health.py`
- `src/doc_generator/infrastructure/api/routes/upload.py`
- `src/doc_generator/infrastructure/api/routes/generate.py`
- `src/doc_generator/infrastructure/api/services/__init__.py`
- `src/doc_generator/infrastructure/api/services/storage.py`
- `src/doc_generator/infrastructure/api/services/cache.py`
- `src/doc_generator/infrastructure/api/services/generation.py`
- `scripts/run_api.py`
- `tests/api/__init__.py`
- `tests/api/test_request_models.py`
- `tests/api/test_response_models.py`
- `tests/api/test_storage_service.py`
- `tests/api/test_cache_service.py`
- `tests/api/test_dependencies.py`
- `tests/api/test_health_route.py`
- `tests/api/test_upload_route.py`
- `tests/api/test_generate_route.py`
- `tests/api/test_integration.py`

**Files Modified:**
- `pyproject.toml` (dependencies)
- `Makefile` (run-api target)
