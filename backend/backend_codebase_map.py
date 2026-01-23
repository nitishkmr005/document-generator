"""
This file provides a high-level map of the backend codebase structure.
It documents the role, tech stack, and key responsibilities of major Python files.
"""

codebase_map = {
    # ==========================================
    # INFRASTRUCTURE LAYER (API Routes & Main Entry)
    # ==========================================
    "backend/doc_generator/infrastructure/api/main.py": {
        "role": "Application Entry Point",
        "description": "Configures and launches the FastAPI application, CORS settings, and routes.",
        "tech_stack": ["FastAPI", "Uvicorn", "Starlette"],
        "key_components": ["create_app()", "app instance"],
    },
    "backend/doc_generator/infrastructure/api/routes/unified.py": {
        "role": "API Route",
        "description": "Unified endpoint for generating documents, podcasts, and mind maps with SSE streaming.",
        "tech_stack": ["FastAPI", "SSE-Starlette", "AsyncIO"],
        "key_components": [
            "generate_with_session",
            "generate_podcast",
            "generate_mindmap",
        ],
    },
    "backend/doc_generator/infrastructure/api/routes/upload.py": {
        "role": "API Route",
        "description": "Handles file uploads and temporary storage.",
        "tech_stack": ["FastAPI", "Aiofiles", "Shutil"],
        "key_components": ["upload_file", "upload_multiple_files"],
    },
    "backend/doc_generator/infrastructure/api/routes/download.py": {
        "role": "API Route",
        "description": "Serves generated files for download.",
        "tech_stack": ["FastAPI", "FileResponse"],
        "key_components": ["download_file"],
    },
    # ==========================================
    # INFRASTRUCTURE LAYER (Services & Integration)
    # ==========================================
    "backend/doc_generator/infrastructure/api/services/unified_generation.py": {
        "role": "Service Orchestrator",
        "description": "Bridges the API layer with the LangGraph workflow. Manages async event loops and queueing.",
        "tech_stack": ["AsyncIO", "LangGraph Bridge"],
        "key_components": [
            "UnifiedGenerationService",
            "generate_document",
            "run_unified_workflow_async",
        ],
    },
    "backend/doc_generator/infrastructure/api/services/storage.py": {
        "role": "Infrastructure Service",
        "description": "Manages file system operations, path resolution, and cleanup.",
        "tech_stack": ["Pathlib", "OS"],
        "key_components": ["StorageService", "get_download_url"],
    },
    "backend/doc_generator/infrastructure/llm/service.py": {
        "role": "Infrastructure Service",
        "description": "Wrapper around LLM providers (Gemini, OpenAI, Anthropic).",
        "tech_stack": ["LangChain", "Google Generative AI", "OpenAI SDK"],
        "key_components": ["LLMService", "generate_content", "get_model"],
    },
    "backend/doc_generator/infrastructure/image/gemini.py": {
        "role": "Infrastructure Service",
        "description": "Client for Google Gemini Vision and Imagen 3 API.",
        "tech_stack": ["Google Generative AI"],
        "key_components": ["GeminiImageClient", "generate_image", "describe_image"],
    },
    # ==========================================
    # APPLICATION LAYER (LangGraph Workflow & Nodes)
    # ==========================================
    "backend/doc_generator/application/unified_workflow.py": {
        "role": "Workflow Definition",
        "description": "Defines the StateGraph, edges, and conditions for the unified generation pipeline.",
        "tech_stack": ["LangGraph", "StateGraph"],
        "key_components": [
            "build_unified_workflow",
            "run_unified_workflow_with_session",
        ],
    },
    "backend/doc_generator/application/unified_state.py": {
        "role": "State Definition",
        "description": "TypedDict definition of the shared state passed between all workflow nodes.",
        "tech_stack": ["Python Typing", "TypedDict"],
        "key_components": ["UnifiedWorkflowState"],
    },
    "backend/doc_generator/application/checkpoint_manager.py": {
        "role": "State Management",
        "description": "Manages LangGraph MemorySaver persistence and session ID generation.",
        "tech_stack": ["LangGraph Checkpoint", "MemorySaver"],
        "key_components": ["CheckpointManager", "get_checkpoint_config"],
    },
    "backend/doc_generator/application/nodes/extract_sources.py": {
        "role": "Workflow Node",
        "description": "Extracts raw text processing from various input sources.",
        "tech_stack": ["PyMuPDF", "MarkItDown", "Firecrawl"],
        "key_components": ["extract_sources_node"],
    },
    "backend/doc_generator/application/nodes/summarize_sources.py": {
        "role": "Workflow Node",
        "description": "Generates concise summaries of extracted content.",
        "tech_stack": ["LangChain Map-Reduce"],
        "key_components": ["summarize_sources_node"],
    },
    "backend/doc_generator/application/nodes/podcast_script.py": {
        "role": "Workflow Node",
        "description": "Generates conversational scripts for podcasts.",
        "tech_stack": ["LangChain", "Pydantic"],
        "key_components": ["generate_podcast_script_node"],
    },
    # ==========================================
    # INFRASTRUCTURE LAYER (Parsers & Generators)
    # ==========================================
    "backend/doc_generator/infrastructure/parsers/markitdown.py": {
        "role": "Parser Adapter",
        "description": "Adapter for Microsoft MarkItDown library to convert files/URLs to Markdown.",
        "tech_stack": ["MarkItDown", "Requests"],
        "key_components": ["convert_url_to_markdown", "convert_to_markdown"],
    },
    "backend/doc_generator/infrastructure/parsers/firecrawl.py": {
        "role": "Parser Adapter",
        "description": "Adapter for Firecrawl API to scrape websites into clean Markdown.",
        "tech_stack": ["Firecrawl API"],
        "key_components": ["convert_url_to_markdown"],
    },
    "backend/doc_generator/infrastructure/generators/pdf/generator.py": {
        "role": "Document Generator",
        "description": "Renders HTML/CSS into PDF documents.",
        "tech_stack": ["WeasyPrint", "Jinja2"],
        "key_components": ["PDFGenerator", "generate_pdf"],
    },
    "backend/doc_generator/infrastructure/generators/pptx/generator.py": {
        "role": "Document Generator",
        "description": "Creates PowerPoint presentations from structured content.",
        "tech_stack": ["python-pptx"],
        "key_components": ["PPTXGenerator", "generate_pptx"],
    },
    # ==========================================
    # DOMAIN LAYER (Models & Prompts)
    # ==========================================
    "backend/doc_generator/domain/models.py": {
        "role": "Domain Models",
        "description": "Core Pydantic data models used throughout the application.",
        "tech_stack": ["Pydantic"],
        "key_components": ["ContentBlock", "Source"],
    },
    "backend/doc_generator/domain/prompts/podcast/prompts.py": {
        "role": "Prompt Template",
        "description": "Prompts for removing visual cues and formatting text for speech.",
        "tech_stack": ["String Templates"],
        "key_components": ["PODCAST_SCRIPT_PROMPT"],
    },
    # ==========================================
    # PROMPTS & TEMPLATES (LLM Instructions)
    # ==========================================
    "backend/doc_generator/domain/prompts/text/content_generator_prompts.py": {
        "role": "Text Prompts",
        "description": "Prompts for document content structure, enhancement, and summarization.",
        "tech_stack": ["Prompt Templates"],
        "key_components": [
            "STRUCTURE_CONTENT_PROMPT",
            "ENHANCE_CONTENT_PROMPT",
            "SUMMARY_PROMPT",
        ],
        "used_in_nodes": [
            "doc_transform_content",
            "doc_enhance_content",
            "summarize_sources",
        ],
    },
    "backend/doc_generator/domain/prompts/text/llm_service_prompts.py": {
        "role": "Text Prompts",
        "description": "Base prompts for core LLM service operations.",
        "tech_stack": ["Prompt Templates"],
        "key_components": ["BASE_SYSTEM_PROMPT"],
        "used_in_nodes": ["ALL (Base System Context)"],
    },
    "backend/doc_generator/domain/prompts/image/image_generation_prompts.py": {
        "role": "Image Prompts",
        "description": "Prompts for generating image descriptions and stable diffusion/imagen prompts.",
        "tech_stack": ["Prompt Templates"],
        "key_components": ["IMAGE_GENERATION_PROMPT", "SCENE_DESCRIPTION_PROMPT"],
        "used_in_nodes": ["doc_generate_images", "build_image_prompt"],
    },
    "backend/doc_generator/domain/prompts/image/image_prompts.py": {
        "role": "Image Prompts",
        "description": "Additional image-related prompt definitions.",
        "tech_stack": ["Prompt Templates"],
        "key_components": ["IMAGE_ANALYSIS_PROMPT"],
        "used_in_nodes": ["extract_sources (Vision)"],
    },
    "backend/doc_generator/domain/prompts/mindmap/prompts.py": {
        "role": "Mindmap Prompts",
        "description": "Prompts for extracting hierarchical concepts for mind maps.",
        "tech_stack": ["Prompt Templates"],
        "key_components": ["MINDMAP_GENERATION_PROMPT", "MINDMAP_SUMMARIZE_PROMPT"],
        "used_in_nodes": ["mindmap_generate"],
    },
    "backend/doc_generator/domain/prompts/idea_canvas/prompts.py": {
        "role": "Canvas Prompts",
        "description": "Prompts for the Idea Canvas brainstorming features.",
        "tech_stack": ["Prompt Templates"],
        "key_components": ["IDEA_EXPANSION_PROMPT", "CONNECTIONS_PROMPT"],
        "used_in_nodes": ["(External to main workflow - Idea Canvas Routes)"],
    },
}
