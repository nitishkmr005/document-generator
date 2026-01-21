"""API routes."""

from .cache import router as cache_router
from .download import router as download_router
from .health import router as health_router
from .idea_canvas import router as idea_canvas_router
from .image import router as image_router
from .upload import router as upload_router

__all__ = [
    "health_router",
    "upload_router",
    "download_router",
    "cache_router",
    "image_router",
    "idea_canvas_router",
]
