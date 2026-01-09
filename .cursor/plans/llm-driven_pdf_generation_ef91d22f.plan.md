---
name: LLM-Driven PDF Generation
overview: Refactor the document generator to use LLM for transforming raw content (transcripts, slides) into well-structured blog-like markdown, and generate contextual SVG/mermaid visualizations that are embedded inline in the PDF.
todos:
  - id: create-llm-content-gen
    content: Create new `llm_content_generator.py` with methods to transform raw content to structured blog markdown with visual markers
    status: completed
  - id: update-transform-node
    content: Update `transform_content.py` to use new LLM content generator and extract visual specifications
    status: completed
  - id: update-visuals-node
    content: Update `generate_visuals.py` to generate visualizations from markers, not raw content analysis
    status: completed
  - id: update-pdf-generator
    content: Update `pdf_generator.py` to replace visual markers with actual images and render mermaid inline
    status: completed
  - id: update-content-merger
    content: Update `content_merger.py` to use LLM for intelligent content merging instead of concatenation
    status: completed
  - id: test-and-verify
    content: Test with llm-architectures folder and verify blog-like PDF output
    status: completed
---

