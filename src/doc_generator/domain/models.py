"""
Domain models for document generator.

Defines Pydantic models for workflow state, configuration, and content structures.
"""

from typing import TypedDict, Literal
from pathlib import Path
from pydantic import BaseModel, Field

from .content_types import ContentFormat, OutputFormat


class WorkflowState(TypedDict, total=False):
    """
    State object passed between nodes in the LangGraph workflow.

    Attributes:
        input_path: Path to input file or URL
        input_format: Detected input format
        output_format: Target output format
        raw_content: Extracted raw content
        structured_content: Parsed and structured content
        output_path: Path to generated file
        errors: List of errors encountered
        metadata: Additional metadata (title, author, etc.)
    """
    input_path: str
    input_format: str
    output_format: str
    raw_content: str
    structured_content: dict
    output_path: str
    errors: list[str]
    metadata: dict


class GeneratorConfig(BaseModel):
    """
    Configuration for document generator.

    Attributes:
        input_dir: Directory containing input files
        output_dir: Directory for generated files
        default_output_format: Default output format
        max_retries: Maximum generation retries
    """

    input_dir: Path = Field(default=Path("src/data"))
    output_dir: Path = Field(default=Path("src/output"))
    default_output_format: OutputFormat = Field(default=OutputFormat.PDF)
    max_retries: int = Field(default=3, ge=1, le=5)

    class Config:
        frozen = True


class ContentSection(BaseModel):
    """
    Represents a section of structured content.

    Attributes:
        type: Section type (heading, paragraph, code, image, etc.)
        text: Text content
        metadata: Additional metadata for the section
    """

    type: str
    text: str
    metadata: dict = Field(default_factory=dict)
