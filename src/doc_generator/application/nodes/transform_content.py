"""
Content transformation node for LangGraph workflow.

Transforms raw content into structured blog-style format for generators.
Uses LLM to generate well-structured educational content with visual markers.
"""

from loguru import logger

from ...domain.models import WorkflowState
from ...infrastructure.llm_content_generator import LLMContentGenerator, get_content_generator
from ...infrastructure.llm_service import get_llm_service
from ...utils.content_cleaner import clean_content_for_output


def _detect_content_type(input_format: str, raw_content: str) -> str:
    """
    Detect the type of content for appropriate LLM transformation.
    
    Args:
        input_format: The detected input format (txt, pdf, md, etc.)
        raw_content: The raw content string
        
    Returns:
        Content type: "transcript", "slides", or "document"
    """
    # Check for transcript indicators (timestamps)
    import re
    timestamp_pattern = r'^\d{1,2}:\d{2}(:\d{2})?\s*$'
    timestamp_count = len(re.findall(timestamp_pattern, raw_content, re.MULTILINE))
    
    # If many timestamps, it's likely a transcript
    if timestamp_count > 10:
        return "transcript"
    
    # PDF/PPTX inputs are likely slides
    if input_format in ("pdf", "pptx"):
        return "slides"
    
    # Default to document
    return "document"


def transform_content_node(state: WorkflowState) -> WorkflowState:
    """
    Transform raw content into structured blog-style format for generators.

    Uses LLM to:
    - Transform raw content (transcripts, docs) into well-structured blog posts
    - Insert visual markers where diagrams should appear
    - Generate inline mermaid diagrams for simple concepts
    - Create executive summaries and slide structures

    Args:
        state: Current workflow state

    Returns:
        Updated state with structured_content including:
        - markdown: Blog-style markdown content
        - title: Extracted/generated title
        - visual_markers: List of visual marker specifications
        - executive_summary: Brief summary (optional)
        - slides: Slide structures for PPTX (optional)
    """
    try:
        content = state.get("raw_content", "")
        metadata = state.get("metadata", {})
        output_format = state.get("output_format", "pdf")
        input_format = state.get("input_format", "txt")
        
        if not content:
            logger.warning("No content to transform")
            state["structured_content"] = {"markdown": "", "title": "Empty Document"}
            return state
        
        # Detect content type for appropriate transformation
        content_type = _detect_content_type(input_format, content)
        topic = metadata.get("title", metadata.get("topic", ""))
        
        logger.info(f"Transforming content: type={content_type}, format={input_format}, topic={topic}")
        
        # Get content generator
        content_generator = get_content_generator()
        
        # Initialize structured content
        structured = {
            "title": metadata.get("title", "Document"),
            "visual_markers": [],
        }
        
        if content_generator.is_available():
            logger.info("LLM Content Generator available - transforming to blog format")
            
            # Transform content using LLM
            generated = content_generator.generate_blog_content(
                raw_content=content,
                content_type=content_type,
                topic=topic
            )
            
            # Store generated content
            structured["markdown"] = generated.markdown
            structured["title"] = generated.title
            structured["sections"] = generated.sections
            
            # Convert visual markers to dict format for state
            structured["visual_markers"] = [
                {
                    "marker_id": m.marker_id,
                    "type": m.visual_type,
                    "title": m.title,
                    "description": m.description,
                    "position": m.position
                }
                for m in generated.visual_markers
            ]
            
            logger.info(
                f"LLM transformation complete: {len(generated.markdown)} chars, "
                f"{len(generated.visual_markers)} visual markers, "
                f"{len(generated.sections)} sections"
            )
            
            # Also get LLM service for additional enhancements
            llm = state.get("llm_service") or get_llm_service()
            
            if llm.is_available():
                # Generate executive summary from the blog content
                executive_summary = llm.generate_executive_summary(generated.markdown)
                if executive_summary:
                    structured["executive_summary"] = executive_summary
                    logger.debug("Generated executive summary")
                
                # For PPTX output, generate optimized slide structure
                if output_format == "pptx":
                    slides = llm.generate_slide_structure(generated.markdown)
                    if slides:
                        structured["slides"] = slides
                        logger.debug(f"Generated {len(slides)} slide structures")
                
                # Suggest chart data from the content
                chart_suggestions = llm.suggest_chart_data(generated.markdown)
                if chart_suggestions:
                    structured["charts"] = chart_suggestions
                    logger.debug(f"Suggested {len(chart_suggestions)} charts")
        else:
            # Fallback: Just clean the content
            logger.info("LLM not available - using basic content cleaning")
            cleaned_content = clean_content_for_output(content)
            structured["markdown"] = cleaned_content
            
            # Try to get basic enhancements from llm_service
            llm = state.get("llm_service") or get_llm_service()
            if llm.is_available():
                executive_summary = llm.generate_executive_summary(cleaned_content)
                if executive_summary:
                    structured["executive_summary"] = executive_summary
                
                if output_format == "pptx":
                    slides = llm.generate_slide_structure(cleaned_content)
                    if slides:
                        structured["slides"] = slides
        
        state["structured_content"] = structured
        
        # Update metadata with generated title
        if "title" not in metadata or not metadata["title"]:
            metadata["title"] = structured["title"]
            state["metadata"] = metadata
        
        logger.info(
            f"Transformed content: title='{structured['title']}', "
            f"{len(structured.get('markdown', ''))} chars, "
            f"{len(structured.get('visual_markers', []))} visual markers"
        )

    except Exception as e:
        error_msg = f"Transformation failed: {str(e)}"
        state["errors"].append(error_msg)
        logger.error(error_msg)
        logger.exception("Transformation error details:")
        
        # Fallback to raw content
        state["structured_content"] = {
            "markdown": state.get("raw_content", ""),
            "title": state.get("metadata", {}).get("title", "Document"),
            "visual_markers": []
        }

    return state
