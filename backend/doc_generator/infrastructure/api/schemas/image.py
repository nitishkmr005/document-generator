"""
Pydantic schemas for image generation and editing API endpoints.
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, model_validator

from .requests import SourceItem, Provider


class OutputFormat(str, Enum):
    """Output format for generated images."""
    RASTER = "raster"
    SVG = "svg"


class EditMode(str, Enum):
    """Mode for image editing."""
    BASIC = "basic"
    STYLE_TRANSFER = "style_transfer"
    REGION = "region"


class Region(BaseModel):
    """Region coordinates for regional editing."""
    x: float = Field(..., ge=0, description="X coordinate (0-1 normalized)")
    y: float = Field(..., ge=0, description="Y coordinate (0-1 normalized)")
    width: float = Field(..., gt=0, description="Width (0-1 normalized)")
    height: float = Field(..., gt=0, description="Height (0-1 normalized)")


class ImageGenerateRequest(BaseModel):
    """Request schema for image generation."""
    prompt: Optional[str] = Field(
        None,
        min_length=1,
        max_length=4000,
        description="Description of the image to generate",
    )
    sources: Optional[list[SourceItem]] = Field(
        None,
        min_length=1,
        max_length=1,
        description="Single source (file, url, or text) to summarize into an image prompt",
    )
    provider: Provider = Provider.GEMINI
    model: str = "gemini-2.5-flash"
    style_category: Optional[str] = Field(None, description="Style category ID (e.g., 'diagram_and_architecture')")
    style: Optional[str] = Field(None, description="Style ID (e.g., 'system_architecture_diagram')")
    output_format: OutputFormat = Field(OutputFormat.RASTER, description="Output format (raster or svg)")
    free_text_mode: bool = Field(False, description="If true, use prompt directly without style enhancement")

    @model_validator(mode="after")
    def validate_prompt_or_sources(self) -> "ImageGenerateRequest":
        prompt = (self.prompt or "").strip()
        sources = self.sources or []
        if not prompt and not sources:
            raise ValueError("Provide a prompt or at least one source.")
        return self

    class Config:
        json_schema_extra = {
            "example": {
                "prompt": "A system architecture showing user authentication flow with OAuth2",
                "sources": [
                    {"type": "url", "url": "https://example.com/article"}
                ],
                "provider": "gemini",
                "model": "gemini-2.5-flash",
                "style_category": "diagram_and_architecture",
                "style": "system_architecture_diagram",
                "output_format": "raster",
                "free_text_mode": False
            }
        }


class ImageEditRequest(BaseModel):
    """Request schema for image editing."""
    image: str = Field(..., description="Base64 encoded image data")
    prompt: str = Field(..., min_length=1, max_length=2000, description="Edit instructions")
    edit_mode: EditMode = Field(EditMode.BASIC, description="Edit mode")
    style_category: Optional[str] = Field(None, description="Style category for style transfer mode")
    style: Optional[str] = Field(None, description="Style ID for style transfer mode")
    region: Optional[Region] = Field(None, description="Region coordinates for regional editing")

    class Config:
        json_schema_extra = {
            "example": {
                "image": "<base64_encoded_image>",
                "prompt": "Change the background color to dark blue",
                "edit_mode": "basic",
                "style_category": None,
                "style": None,
                "region": None
            }
        }


class ImageGenerateResponse(BaseModel):
    """Response schema for image generation."""
    success: bool = Field(..., description="Whether generation was successful")
    image_data: Optional[str] = Field(None, description="Base64 encoded image or SVG code")
    format: str = Field(..., description="Output format (png or svg)")
    prompt_used: str = Field(..., description="Final prompt sent to the model")
    error: Optional[str] = Field(None, description="Error message if generation failed")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "image_data": "<base64_or_svg>",
                "format": "png",
                "prompt_used": "Create a System Architecture Diagram...",
                "error": None
            }
        }


class ImageEditResponse(BaseModel):
    """Response schema for image editing."""
    success: bool = Field(..., description="Whether editing was successful")
    image_data: Optional[str] = Field(None, description="Base64 encoded edited image")
    format: str = Field("png", description="Output format (always png for edits)")
    error: Optional[str] = Field(None, description="Error message if editing failed")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "image_data": "<base64_encoded_image>",
                "format": "png",
                "error": None
            }
        }


class StyleInfo(BaseModel):
    """Style information for frontend display."""
    id: str
    name: str
    category: str
    looks_like: str
    use_cases: list[str]
    supports_svg: bool


class CategoryInfo(BaseModel):
    """Category information for frontend display."""
    id: str
    name: str


class StylesResponse(BaseModel):
    """Response schema for listing styles."""
    categories: list[CategoryInfo]
    styles: list[StyleInfo]
