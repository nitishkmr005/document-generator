"""Idea Canvas routes with SSE streaming."""

from typing import AsyncIterator

from fastapi import APIRouter, Depends
from loguru import logger
from sse_starlette.sse import EventSourceResponse

from ..dependencies import APIKeys, extract_api_keys, get_api_key_for_provider
from ..schemas.idea_canvas import (
    AnswerRequest,
    CanvasCompleteEvent,
    CanvasErrorEvent,
    CanvasProgressEvent,
    CanvasQuestionEvent,
    CanvasReadyEvent,
    GenerateApproachesRequest,
    GenerateApproachesResponse,
    GenerateReportRequest,
    GenerateReportResponse,
    RefineApproachRequest,
    RefineApproachResponse,
    StartCanvasRequest,
)
from ..services.idea_canvas import get_idea_canvas_service

router = APIRouter(tags=["idea-canvas"])


async def start_event_generator(
    request: StartCanvasRequest,
    api_key: str,
    user_id: str | None = None,
) -> AsyncIterator[dict]:
    """Generate SSE events for starting a canvas session.

    Args:
        request: Start canvas request
        api_key: API key for LLM provider
        user_id: Optional user ID

    Yields:
        SSE event dicts
    """
    service = get_idea_canvas_service()

    async for event in service.start_session(request, api_key, user_id):
        if isinstance(event, CanvasReadyEvent):
            yield {"event": "ready", "data": event.model_dump_json()}
        elif isinstance(event, CanvasQuestionEvent):
            yield {"event": "question", "data": event.model_dump_json()}
        elif isinstance(event, CanvasProgressEvent):
            yield {"event": "progress", "data": event.model_dump_json()}
        elif isinstance(event, CanvasErrorEvent):
            yield {"event": "error", "data": event.model_dump_json()}
        else:
            yield {"data": event.model_dump_json()}


async def answer_event_generator(
    request: AnswerRequest,
    api_key: str,
    user_id: str | None = None,
) -> AsyncIterator[dict]:
    """Generate SSE events for submitting an answer.

    Args:
        request: Answer request
        api_key: API key for LLM provider
        user_id: Optional user ID

    Yields:
        SSE event dicts
    """
    service = get_idea_canvas_service()

    async for event in service.submit_answer(request, api_key, user_id):
        if isinstance(event, CanvasQuestionEvent):
            yield {"event": "question", "data": event.model_dump_json()}
        elif isinstance(event, CanvasCompleteEvent):
            yield {"event": "suggest_complete", "data": event.model_dump_json()}
        elif isinstance(event, CanvasProgressEvent):
            yield {"event": "progress", "data": event.model_dump_json()}
        elif isinstance(event, CanvasErrorEvent):
            yield {"event": "error", "data": event.model_dump_json()}
        else:
            yield {"data": event.model_dump_json()}


@router.post(
    "/canvas/start",
    summary="Start an Idea Canvas session (SSE stream)",
    description=(
        "Start a new Idea Canvas session for exploring an idea through guided Q&A. "
        "Returns an SSE stream with the session ID and first question. "
        "Use the /canvas/answer endpoint to submit answers and get subsequent questions."
    ),
    response_description="SSE stream of canvas events.",
)
async def start_canvas(
    request: StartCanvasRequest,
    api_keys: APIKeys = Depends(extract_api_keys),
) -> EventSourceResponse:
    """Start a new canvas session.

    Args:
        request: Start canvas request
        api_keys: API keys from headers

    Returns:
        SSE event stream
    """
    logger.info(
        f"=== Starting Idea Canvas: template={request.template}, "
        f"provider={request.provider} ==="
    )

    api_key = get_api_key_for_provider(request.provider, api_keys)

    return EventSourceResponse(
        start_event_generator(
            request=request,
            api_key=api_key,
            user_id=api_keys.user_id,
        )
    )


@router.post(
    "/canvas/answer",
    summary="Submit an answer to continue the canvas (SSE stream)",
    description=(
        "Submit an answer to the current question and receive the next question. "
        "Returns an SSE stream with the next question or a completion suggestion."
    ),
    response_description="SSE stream of canvas events.",
)
async def submit_answer(
    request: AnswerRequest,
    api_keys: APIKeys = Depends(extract_api_keys),
) -> EventSourceResponse:
    """Submit an answer and get the next question.

    Args:
        request: Answer request with session_id and answer
        api_keys: API keys from headers

    Returns:
        SSE event stream
    """
    logger.info(f"=== Canvas answer: session={request.session_id} ===")

    # Get session to determine provider
    service = get_idea_canvas_service()
    session = service.get_session(request.session_id)

    if not session:
        # Return error stream
        async def error_generator():
            yield {
                "event": "error",
                "data": CanvasErrorEvent(
                    message=f"Session not found: {request.session_id}",
                    code="SESSION_NOT_FOUND",
                ).model_dump_json(),
            }

        return EventSourceResponse(error_generator())

    # Get API key for session's provider
    from ..schemas.requests import Provider

    provider = Provider(session.provider)
    api_key = get_api_key_for_provider(provider, api_keys)

    return EventSourceResponse(
        answer_event_generator(
            request=request,
            api_key=api_key,
            user_id=api_keys.user_id,
        )
    )


@router.post(
    "/canvas/report",
    summary="Generate a report from a canvas session",
    description=(
        "Generate a markdown and/or PDF report from a completed canvas session."
    ),
)
async def generate_canvas_report(
    request: GenerateReportRequest,
    api_keys: APIKeys = Depends(extract_api_keys),
):
    """Generate a report from a canvas session.

    Args:
        request: Report generation request
        api_keys: API keys from headers

    Returns:
        Report with download URLs and content
    """
    logger.info(f"=== Generating Canvas Report: session={request.session_id} ===")

    service = get_idea_canvas_service()

    # Get session to determine which API key to use
    session = service.get_session(request.session_id)
    if not session:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=404, detail=f"Session not found: {request.session_id}"
        )

    # Get the appropriate API key based on session provider
    api_key = get_api_key_for_provider(session.provider, api_keys)

    try:
        image_api_key = api_keys.image
        report_data = service.generate_report(
            request.session_id,
            api_key,
            image_api_key=image_api_key,
        )

        response = GenerateReportResponse(
            session_id=request.session_id,
            title=report_data["title"],
            markdown_content=report_data["markdown_content"],
            pdf_base64=report_data.get("pdf_base64"),
            image_base64=report_data.get("image_base64"),
            image_format=report_data.get("image_format"),
        )

        return response

    except ValueError as e:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail=str(e))


@router.post(
    "/canvas/mindmap",
    summary="Generate a mind map from a canvas session",
    description=(
        "Generate a mind map visualization from the canvas Q&A session. "
        "This shows a hierarchical view of the decisions made during exploration."
    ),
)
async def generate_canvas_mindmap(
    request: GenerateReportRequest,  # Reuse same request schema
    api_keys: APIKeys = Depends(extract_api_keys),
):
    """Generate a mind map from a canvas session.

    Args:
        request: Request with session_id
        api_keys: API keys from headers

    Returns:
        MindMapTree structure
    """
    logger.info(f"=== Generating Canvas MindMap: session={request.session_id} ===")

    service = get_idea_canvas_service()

    # Get session to determine which API key to use
    session = service.get_session(request.session_id)
    if not session:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=404, detail=f"Session not found: {request.session_id}"
        )

    # Get the appropriate API key based on session provider
    api_key = get_api_key_for_provider(session.provider, api_keys)

    try:
        mindmap_data = service.generate_mindmap_from_session(
            request.session_id,
            api_key,
        )

        return mindmap_data

    except ValueError as e:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail=str(e))


@router.post(
    "/canvas/approaches",
    summary="Generate implementation approaches",
    description=(
        "Generate 4 different implementation approaches based on the Q&A session. "
        "Each approach includes a mermaid diagram and task table."
    ),
    response_model=GenerateApproachesResponse,
)
async def generate_approaches(
    request: GenerateApproachesRequest,
    api_keys: APIKeys = Depends(extract_api_keys),
):
    """Generate 4 implementation approaches from a canvas session.

    Args:
        request: Request with session_id
        api_keys: API keys from headers

    Returns:
        4 approaches with mermaid diagrams and tasks
    """
    logger.info(f"=== Generating Approaches: session={request.session_id} ===")

    service = get_idea_canvas_service()

    session = service.get_session(request.session_id)
    if not session:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=404, detail=f"Session not found: {request.session_id}"
        )

    api_key = get_api_key_for_provider(session.provider, api_keys)

    try:
        result = service.generate_approaches(request.session_id, api_key)
        return GenerateApproachesResponse(approaches=result["approaches"])
    except Exception as e:
        logger.error(f"Failed to generate approaches: {e}")
        from fastapi import HTTPException

        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/canvas/refine",
    summary="Refine a specific approach",
    description=(
        "Refine a specific approach based on user feedback about a diagram element or task."
    ),
    response_model=RefineApproachResponse,
)
async def refine_approach(
    request: RefineApproachRequest,
    api_keys: APIKeys = Depends(extract_api_keys),
):
    """Refine a specific approach based on user feedback.

    Args:
        request: Refinement request with element details
        api_keys: API keys from headers

    Returns:
        Updated approach
    """
    logger.info(
        f"=== Refining Approach: session={request.session_id}, "
        f"approach={request.approach_index}, element={request.element_id} ==="
    )

    service = get_idea_canvas_service()

    session = service.get_session(request.session_id)
    if not session:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=404, detail=f"Session not found: {request.session_id}"
        )

    api_key = get_api_key_for_provider(session.provider, api_keys)

    try:
        result = service.refine_approach(
            session_id=request.session_id,
            api_key=api_key,
            approach_index=request.approach_index,
            element_id=request.element_id,
            element_type=request.element_type,
            refinement_answer=request.refinement_answer,
            current_approach=request.current_approach.model_dump(by_alias=True),
        )
        return RefineApproachResponse(approach=result)
    except Exception as e:
        logger.error(f"Failed to refine approach: {e}")
        from fastapi import HTTPException

        raise HTTPException(status_code=500, detail=str(e))
