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
    GOAL_PLANNING = "goal_planning"
    PROS_CONS = "pros_cons"
    PRESENTATION_STRUCTURE = "presentation_structure"


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
            "model": "gemini-2.5-flash"
        }
    """

    sources: list[SourceItem] = Field(
        description="List of sources (file, url, or text)",
        min_length=1,
    )
    mode: MindMapMode = MindMapMode.SUMMARIZE
    provider: Provider = Provider.GEMINI
    model: str = "gemini-2.5-flash"
    # max_depth is now determined by LLM based on content complexity

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
    session_id: str | None = None  # Session ID for checkpointing/content reuse


class MindMapErrorEvent(BaseModel):
    """Error event during mind map generation."""

    type: Literal["error"] = "error"
    message: str
    code: str | None = None
