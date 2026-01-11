"""Generation service for document creation with progress streaming."""

import asyncio
import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import AsyncIterator, Optional

from loguru import logger

from ....application.graph_workflow import run_workflow
from ....infrastructure.llm_service import LLMService
from ..models.requests import (
    FileSource,
    GenerateRequest,
    TextSource,
    UrlSource,
)
from ..models.responses import (
    CompleteEvent,
    CompletionMetadata,
    ErrorEvent,
    GenerationStatus,
    ProgressEvent,
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
        self._executor = ThreadPoolExecutor(max_workers=2)

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
            logger.info("[1/5] Parsing sources...")
            yield ProgressEvent(
                status=GenerationStatus.PARSING,
                progress=5,
                message="[1/5] Starting to parse sources...",
            )

            input_path = await self._collect_sources(request)
            source_count = len(request.sources)
            
            logger.info(f"[1/5] Parsed {source_count} sources, input: {input_path}")
            yield ProgressEvent(
                status=GenerationStatus.PARSING,
                progress=20,
                message=f"[1/5] Parsed {source_count} sources",
            )

            # Phase 2: Transform content  
            logger.info("[2/5] Transforming content...")
            yield ProgressEvent(
                status=GenerationStatus.TRANSFORMING,
                progress=30,
                message="[2/5] Structuring content...",
            )

            # Set API key for the provider
            self._configure_api_key(request.provider.value, api_key)

            # Create LLM service with the configured provider
            llm_service = LLMService(
                provider=request.provider.value,
                model=request.model,
            )

            logger.info(f"[2/5] LLM configured: {request.provider.value}/{request.model}")
            yield ProgressEvent(
                status=GenerationStatus.TRANSFORMING,
                progress=40,
                message="[2/5] Content transformation started",
            )

            # Phase 3: Run the actual workflow
            logger.info("[3/5] Running document generation workflow...")
            yield ProgressEvent(
                status=GenerationStatus.GENERATING_IMAGES,
                progress=50,
                message="[3/5] Running generation workflow...",
            )

            # Run workflow in thread pool to not block event loop
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                self._executor,
                lambda: run_workflow(
                    input_path=str(input_path),
                    output_format=request.output_format.value,
                    llm_service=llm_service,
                    metadata={
                        "provider": request.provider.value,
                        "model": request.model,
                    },
                ),
            )

            logger.info(f"[3/5] Workflow complete: {result.get('output_path', 'N/A')}")
            yield ProgressEvent(
                status=GenerationStatus.GENERATING_IMAGES,
                progress=70,
                message="[3/5] Workflow complete",
            )

            # Phase 4: Check for errors
            errors = result.get("errors", [])
            if errors:
                logger.error(f"[4/5] Workflow errors: {errors}")
                yield ErrorEvent(
                    error="; ".join(errors),
                    code="WORKFLOW_ERROR",
                )
                return

            # Phase 4: Generate output path
            logger.info("[4/5] Generating output...")
            yield ProgressEvent(
                status=GenerationStatus.GENERATING_OUTPUT,
                progress=80,
                message=f"[4/5] Building {request.output_format.value.upper()}...",
            )

            output_path = result.get("output_path", "")

            logger.info(f"[4/5] Output generated: {output_path}")
            yield ProgressEvent(
                status=GenerationStatus.GENERATING_OUTPUT,
                progress=90,
                message="[4/5] Output generated",
            )

            # Phase 5: Finalize
            logger.info("[5/5] Finalizing...")
            yield ProgressEvent(
                status=GenerationStatus.UPLOADING,
                progress=95,
                message="[5/5] Finalizing...",
            )

            if output_path and Path(output_path).exists():
                download_url = self.storage.get_download_url(Path(output_path))
            else:
                logger.warning(f"[5/5] Output path not found: {output_path}")
                download_url = f"/api/download/{Path(output_path).name if output_path else 'error.pdf'}"

            # Extract metadata from result
            structured_content = result.get("structured_content", {})
            metadata = result.get("metadata", {})

            # Count pages/slides from structured content
            pages = 0
            slides = 0
            if request.output_format.value == "pdf":
                # Estimate pages from sections
                sections = structured_content.get("sections", [])
                pages = max(1, len(sections))
            else:
                slides = len(structured_content.get("sections", []))

            images_generated = len(structured_content.get("images", []))
            title = structured_content.get("title", metadata.get("title", "Generated Document"))

            logger.info(f"[5/5] Complete: {title} ({pages} pages, {images_generated} images)")

            # Complete
            yield CompleteEvent(
                download_url=download_url,
                expires_in=3600,
                metadata=CompletionMetadata(
                    title=title,
                    pages=pages,
                    slides=slides,
                    images_generated=images_generated,
                ),
            )

        except Exception as e:
            logger.exception(f"Generation failed: {e}")
            yield ErrorEvent(
                error=str(e),
                code="GENERATION_ERROR",
            )

    def _configure_api_key(self, provider: str, api_key: str) -> None:
        """Configure API key for the provider.

        Args:
            provider: Provider name (google, openai, anthropic)
            api_key: API key value
        """
        key_map = {
            "google": "GOOGLE_API_KEY",
            "openai": "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY",
        }
        env_var = key_map.get(provider)
        if env_var:
            os.environ[env_var] = api_key
            logger.debug(f"Configured {env_var} for provider {provider}")

    async def _collect_sources(self, request: GenerateRequest) -> Path:
        """Collect content from all sources and return input path.

        For file sources, returns the path to the first file.
        For text/URL sources, creates a temporary file with the content.

        Args:
            request: Generation request

        Returns:
            Path to input file for workflow
        """
        # Sources is now a flat list
        all_sources = request.sources

        # For file sources, use the first file's path directly
        for source in all_sources:
            if isinstance(source, FileSource):
                try:
                    file_path = self.storage.get_upload_path(source.file_id)
                    logger.info(f"Using uploaded file: {file_path}")
                    return file_path
                except FileNotFoundError:
                    # Try to find by pattern in uploads directory
                    pattern = f"{source.file_id}*"
                    matches = list(self.storage.upload_dir.glob(pattern))
                    if matches:
                        logger.info(f"Found file by pattern: {matches[0]}")
                        return matches[0]
                    logger.warning(f"File not found: {source.file_id}")
                    continue

        # For text sources, create a temporary markdown file
        contents = []
        for source in all_sources:
            if isinstance(source, TextSource):
                contents.append(source.content)
            elif isinstance(source, UrlSource):
                # TODO: Fetch URL content using web parser
                contents.append(f"# Content from URL\n\nSource: {source.url}\n\n[URL content to be fetched]")

        if contents:
            combined = "\n\n---\n\n".join(contents)
            temp_path = self.storage.upload_dir / "temp_input.md"
            temp_path.write_text(combined, encoding="utf-8")
            logger.info(f"Created temp input file: {temp_path}")
            return temp_path

        raise ValueError("No valid sources provided")
