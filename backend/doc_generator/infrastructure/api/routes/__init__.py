"""API routes."""

from .cache import router as cache_router
from .download import router as download_router
from .generate import router as generate_router
from .health import router as health_router
from .image import router as image_router
from .mindmap import router as mindmap_router
from .upload import router as upload_router

__all__ = [
    "health_router",
    "upload_router",
    "generate_router",
    "download_router",
    "cache_router",
    "image_router",
    "mindmap_router",
]


