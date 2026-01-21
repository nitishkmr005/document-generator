"""Pydantic response models for the API."""

from enum import Enum

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
    progress: int
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
    file_path: str
    expires_in: int = 3600
    metadata: CompletionMetadata
    pdf_base64: str | None = None  # Base64-encoded PDF data for inline preview
    markdown_content: str | None = None  # Markdown content for inline preview
    session_id: str | None = None  # Session ID for checkpointing/content reuse


class CacheHitEvent(BaseModel):
    status: GenerationStatus = GenerationStatus.CACHE_HIT
    progress: int = 100
    download_url: str
    file_path: str
    expires_in: int = 3600
    cached_at: str
    pdf_base64: str | None = None  # Base64-encoded PDF data for inline preview
    markdown_content: str | None = None  # Markdown content for inline preview
    session_id: str | None = None  # Session ID for checkpointing/content reuse


class ErrorEvent(BaseModel):
    status: GenerationStatus = GenerationStatus.ERROR
    error: str
    code: str


class UploadResponse(BaseModel):
    file_id: str
    filename: str
    size: int
    mime_type: str
    expires_in: int = 3600


class HealthResponse(BaseModel):
    status: str = "healthy"
    version: str
