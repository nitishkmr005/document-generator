"""Pydantic request and response models for mind map generation."""

from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from .requests import Provider, SourceItem


class MindMapMode(str, Enum):
    """Mind map generation modes."""
    SUMMARIZE = "summarize"
    BRAINSTORM = "brainstorm"
    STRUCTURE = "structure"


class MindMapRequest(BaseModel):
    """Request model for mind map generation.

    Example:
        {
            "sources": [
                {"type": "file", "file_id": "f_abc123"},
                {"type": "url", "url": "https://example.com/article"},
                {"type": "text", "content": "Some text content..."}
            ],
            "mode": "summarize",
            "provider": "gemini",
            "model": "gemini-2.5-flash",
            "max_depth": 5
        }
    """

    sources: list[SourceItem] = Field(
        description="List of sources (file, url, or text)",
        min_length=1,
    )
    mode: MindMapMode = MindMapMode.SUMMARIZE
    provider: Provider = Provider.GEMINI
    model: str = "gemini-2.5-flash"
    max_depth: int = Field(default=5, ge=2, le=5)

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "sources": [
                        {"type": "url", "url": "https://example.com/article"},
                        {"type": "text", "content": "Additional context"},
                    ],
                    "mode": "summarize",
                    "provider": "gemini",
                    "model": "gemini-2.5-flash",
                    "max_depth": 5,
                }
            ]
        }
    )


class MindMapNode(BaseModel):
    """A node in the mind map tree."""
    id: str
    label: str
    children: list["MindMapNode"] = Field(default_factory=list)


class MindMapTree(BaseModel):
    """Complete mind map tree structure."""
    title: str
    summary: str
    source_count: int
    mode: MindMapMode
    nodes: MindMapNode


# SSE Event Models


class MindMapProgressEvent(BaseModel):
    """Progress event during mind map generation."""
    type: Literal["progress"] = "progress"
    stage: str  # extracting, analyzing, generating
    percent: float = Field(ge=0, le=100)
    message: str | None = None


class MindMapCompleteEvent(BaseModel):
    """Completion event with mind map data."""
    type: Literal["complete"] = "complete"
    tree: MindMapTree


class MindMapErrorEvent(BaseModel):
    """Error event during mind map generation."""
    type: Literal["error"] = "error"
    message: str
    code: str | None = None
