"""Mind map generation route with SSE streaming."""

from typing import AsyncIterator

from fastapi import APIRouter, Depends
from loguru import logger
from sse_starlette.sse import EventSourceResponse

from ..dependencies import APIKeys, extract_api_keys, get_api_key_for_provider
from ..schemas.mindmap import (
    MindMapCompleteEvent,
    MindMapErrorEvent,
    MindMapProgressEvent,
    MindMapRequest,
)
from ..services.mindmap import get_mindmap_service

router = APIRouter(tags=["mindmap"])


async def event_generator(
    request: MindMapRequest,
    api_key: str,
    user_id: str | None = None,
) -> AsyncIterator[dict]:
    """Generate SSE events for mind map creation.

    Args:
        request: Mind map generation request
        api_key: API key for LLM provider
        user_id: Optional user ID for logging

    Yields:
        SSE event dicts
    """
    service = get_mindmap_service()

    async for event in service.generate(request, api_key, user_id):
        if isinstance(event, MindMapCompleteEvent):
            yield {"event": "complete", "data": event.model_dump_json()}
        elif isinstance(event, MindMapErrorEvent):
            yield {"event": "error", "data": event.model_dump_json()}
        elif isinstance(event, MindMapProgressEvent):
            yield {"event": "progress", "data": event.model_dump_json()}
        else:
            yield {"data": event.model_dump_json()}


@router.post(
    "/generate/mindmap",
    summary="Generate a mind map (SSE stream)",
    description=(
        "Stream mind map generation progress via Server-Sent Events (SSE). "
        "Provide one or more sources (file_id, url, or text) and choose "
        "a generation mode (summarize, brainstorm, or structure). "
        "Returns a hierarchical tree structure that can be visualized as a mind map."
    ),
    response_description="SSE stream of progress events ending in complete/error.",
)
async def generate_mindmap(
    request: MindMapRequest,
    api_keys: APIKeys = Depends(extract_api_keys),
) -> EventSourceResponse:
    """Generate a mind map from sources.

    Streams progress events via SSE, ending with completion or error.

    Args:
        request: Mind map generation request
        api_keys: API keys from headers

    Returns:
        SSE event stream
    """
    logger.info(
        f"=== Mind map generation: provider={request.provider}, "
        f"mode={request.mode}, sources={len(request.sources)} ==="
    )

    # Validate API key for provider
    api_key = get_api_key_for_provider(request.provider, api_keys)
    logger.debug(f"API key validated for provider {request.provider}")

    return EventSourceResponse(
        event_generator(
            request=request,
            api_key=api_key,
            user_id=api_keys.user_id,
        )
    )
