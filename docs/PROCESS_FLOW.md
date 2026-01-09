# Document Generator - Complete Process Flow

## Overview Architecture Diagram

```mermaid
graph TB
    subgraph "INPUT SOURCES"
        A1[PDF Files]
        A2[Markdown Files]
        A3[DOCX/PPTX]
        A4[TXT Files]
        A5[Web URLs]
        A6[Folders]
    end

    subgraph "ENTRY POINTS"
        B1[scripts/run_generator.py<br/>Single File]
        B2[scripts/generate_from_folder.py<br/>Folder Processing]
        B3[make commands<br/>Automation]
    end

    subgraph "LANGGRAPH WORKFLOW"
        C1[1. detect_format<br/>Detect input type]
        C2[2. parse_content<br/>Extract content]
        C3[3. transform_content<br/>LLM enhancement]
        C4[4. generate_visuals<br/>SVG diagrams]
        C5[5. generate_images<br/>Gemini infographics]
        C6[6. generate_output<br/>Create PDF/PPTX]
        C7[7. validate_output<br/>Check result]
        C8{Retry?<br/>Max 3x}
    end

    subgraph "PARSERS (Application Layer)"
        D1[UnifiedParser<br/>Docling for PDF/DOCX/PPTX]
        D2[MarkdownParser<br/>Frontmatter support]
        D3[WebParser<br/>MarkItDown for URLs]
    end

    subgraph "LLM CONTENT GENERATION"
        E1[LLMContentGenerator]
        E2[OpenAI GPT-4o<br/>Content transformation]
        E3[Claude Sonnet<br/>Visual data]
        E4[Chunked Processing<br/>Long documents]
        E5[Visual Markers<br/>Extraction]
    end

    subgraph "IMAGE GENERATION"
        F1[SVG Generator<br/>Mermaid diagrams]
        F2[Gemini Image API<br/>Decorative headers]
        F3[Gemini Image API<br/>Infographics]
        F4[Image Cache<br/>src/output/images/]
    end

    subgraph "OUTPUT GENERATORS"
        G1[PDFGenerator<br/>ReportLab]
        G2[PPTXGenerator<br/>python-pptx]
    end

    subgraph "OUTPUT FILES"
        H1[PDF Document<br/>src/output/*.pdf]
        H2[PPTX Slides<br/>src/output/*.pptx]
        H3[Generated Images<br/>src/output/images/]
    end

    subgraph "INFRASTRUCTURE"
        I1[Docling Adapter<br/>OCR + Tables]
        I2[MarkItDown Adapter<br/>Web extraction]
        I3[File System<br/>I/O operations]
        I4[Logging Config<br/>Loguru]
    end

    subgraph "CONFIGURATION"
        J1[config/settings.yaml<br/>YAML config]
        J2[.env file<br/>API keys]
        J3[Environment Variables<br/>Overrides]
    end

    %% Input to Entry Points
    A1 & A2 & A3 & A4 & A5 --> B1
    A6 --> B2
    B3 --> B1 & B2

    %% Entry Points to Workflow
    B1 & B2 --> C1

    %% Workflow Flow
    C1 --> C2
    C2 --> C3
    C3 --> C4
    C4 --> C5
    C5 --> C6
    C6 --> C7
    C7 --> C8
    C8 -->|No errors| H1 & H2 & H3
    C8 -->|Has errors & < 3 retries| C6

    %% Parsers
    C2 --> D1 & D2 & D3

    %% LLM Processing
    C3 --> E1
    E1 --> E2 & E3
    E2 --> E4
    E4 --> E5

    %% Image Generation
    C4 --> F1
    C5 --> F2 & F3
    F2 & F3 --> F4

    %% Output Generation
    C6 --> G1 & G2
    G1 --> H1
    G2 --> H2
    F4 --> G1 & G2

    %% Infrastructure
    D1 --> I1
    D3 --> I2
    G1 & G2 --> I3
    C1 & C2 & C3 --> I4

    %% Configuration
    J1 & J2 & J3 --> E1 & F2 & F3 & G1 & G2

    style C1 fill:#e1f5ff
    style C2 fill:#e1f5ff
    style C3 fill:#ffe1e1
    style C4 fill:#ffe1e1
    style C5 fill:#ffe1e1
    style C6 fill:#e1ffe1
    style C7 fill:#e1ffe1
    style C8 fill:#fff3e1
    style E1 fill:#f3e1ff
    style H1 fill:#c8e6c9
    style H2 fill:#c8e6c9
```

## Detailed Process Flow

### Phase 1: Input & Detection

```mermaid
flowchart LR
    A[Input File/Folder] --> B{detect_format}
    B --> C1[.pdf → ContentFormat.PDF]
    B --> C2[.md → ContentFormat.MARKDOWN]
    B --> C3[.txt → ContentFormat.TEXT]
    B --> C4[.docx → ContentFormat.DOCX]
    B --> C5[.pptx → ContentFormat.PPTX]
    B --> C6[http:// → ContentFormat.WEB]
    C1 & C2 & C3 & C4 & C5 & C6 --> D[State Updated]
```

### Phase 2: Content Parsing

```mermaid
flowchart TB
    A[parse_content node] --> B{Input Format?}
    
    B -->|PDF/DOCX/PPTX| C[UnifiedParser]
    B -->|Markdown| D[MarkdownParser]
    B -->|Web URL| E[WebParser]
    B -->|Text| F[Direct Read]
    
    C --> G[Docling Library]
    G --> G1[OCR Processing]
    G --> G2[Table Extraction]
    G --> G3[Layout Analysis]
    G1 & G2 & G3 --> H[Raw Content]
    
    D --> D1[Parse Frontmatter]
    D --> D2[Parse Markdown Body]
    D1 & D2 --> H
    
    E --> E1[MarkItDown]
    E1 --> E2[HTML to Markdown]
    E2 --> H
    
    F --> H
    
    H --> I[state.raw_content]
```

### Phase 3: LLM Content Transformation

```mermaid
flowchart TB
    A[transform_content node] --> B{Content Length?}
    
    B -->|Short < 50K chars| C[Single Pass]
    B -->|Long > 50K chars| D[Chunked Processing]
    
    C --> E[LLMContentGenerator]
    D --> D1[Split into chunks]
    D1 --> D2[Process chunk 1]
    D2 --> D3[Process chunk 2]
    D3 --> D4[Process chunk N]
    D4 --> D5[Merge chunks]
    D5 --> E
    
    E --> F{Provider Selection}
    F -->|Content| G[OpenAI GPT-4o]
    F -->|Visuals| H[Claude Sonnet]
    
    G --> I[Transform to Blog Style]
    I --> I1[Remove timestamps]
    I --> I2[Add section headings]
    I --> I3[Structure content]
    I --> I4[Insert visual markers]
    
    H --> J[Generate Visual Data]
    J --> J1[Extract diagram specs]
    J --> J2[Create mermaid code]
    J --> J3[Structure for SVG]
    
    I4 & J3 --> K[Structured Content]
    K --> L[state.structured_content]
```

### Phase 4: Visual Generation

```mermaid
flowchart TB
    A[generate_visuals node] --> B[Parse Visual Markers]
    B --> C{Visual Type?}
    
    C -->|Mermaid| D[Inline Mermaid Code]
    C -->|Architecture| E[SVG Generator]
    C -->|Flowchart| E
    C -->|Comparison| E
    
    D --> F[Embed in content]
    E --> G[Generate SVG]
    
    F & G --> H[state.structured_content.visuals]
    
    I[generate_images node] --> J{Image Types?}
    
    J -->|Decorative Headers| K[Gemini API]
    J -->|Section Infographics| K
    
    K --> L[Generate prompt]
    L --> M[Call Gemini Image API]
    M --> N[Download PNG]
    N --> O[Save to src/output/images/]
    
    O --> P[state.structured_content.image_paths]
```

### Phase 5: Output Generation

```mermaid
flowchart TB
    A[generate_output node] --> B{Output Format?}
    
    B -->|PDF| C[PDFGenerator]
    B -->|PPTX| D[PPTXGenerator]
    
    C --> C1[ReportLab Setup]
    C1 --> C2[Create Document]
    C2 --> C3[Add Title Page]
    C3 --> C4[Add TOC]
    C4 --> C5{For each section}
    
    C5 --> C6[Add section heading]
    C6 --> C7[Add decorative header?]
    C7 --> C8[Add content paragraphs]
    C8 --> C9[Add infographic?]
    C9 --> C10[Add SVG diagrams]
    C10 --> C11{More sections?}
    C11 -->|Yes| C5
    C11 -->|No| C12[Build PDF]
    
    D --> D1[python-pptx Setup]
    D1 --> D2[Create Presentation]
    D2 --> D3[Title Slide]
    D3 --> D4[TOC Slide]
    D4 --> D5{For each section}
    
    D5 --> D6[Section Title Slide]
    D6 --> D7[Add decorative image?]
    D7 --> D8[Content Slides]
    D8 --> D9[Add infographic?]
    D9 --> D10[Add diagrams]
    D10 --> D11{More sections?}
    D11 -->|Yes| D5
    D11 -->|No| D12[Save PPTX]
    
    C12 --> E[state.output_path]
    D12 --> E
```

### Phase 6: Validation & Retry

```mermaid
flowchart TB
    A[validate_output node] --> B{File exists?}
    B -->|No| C[Add error]
    B -->|Yes| D{File size > 0?}
    D -->|No| C
    D -->|Yes| E{Valid format?}
    E -->|No| C
    E -->|Yes| F[Validation passed]
    
    C --> G[state.errors.append]
    G --> H{should_retry?}
    
    H --> I{Has errors?}
    I -->|No| J[END]
    I -->|Yes| K{Retry count < 3?}
    
    K -->|No| L[Max retries - END]
    K -->|Yes| M{Error type?}
    
    M -->|Generation/Validation| N[Increment retry count]
    M -->|Other| L
    
    N --> O[Retry from generate_output]
    O --> A
    
    F --> P[state.errors = empty]
    P --> J
```

## Folder Processing Flow

```mermaid
flowchart TB
    A[Folder Input] --> B[scripts/generate_from_folder.py]
    B --> C[Discover all files]
    C --> D{For each file}
    
    D --> E[Run workflow<br/>parse only]
    E --> F[Extract content]
    F --> G[Extract metadata]
    G --> H[Collect all content]
    
    H --> I{More files?}
    I -->|Yes| D
    I -->|No| J[merge_folder_content]
    
    J --> K[LLM merge strategy]
    K --> L[Combined content]
    
    L --> M[Create temp markdown]
    M --> N[Run workflow<br/>full pipeline]
    
    N --> O[Generate PDF]
    N --> P[Generate PPTX]
    
    O & P --> Q[Output files:<br/>folder-name.pdf<br/>folder-name.pptx]
```

## Data Flow Summary

```mermaid
flowchart LR
    A[Raw Input] -->|Parsing| B[Raw Content<br/>String]
    B -->|LLM Transform| C[Structured Content<br/>JSON]
    C -->|Visual Gen| D[Content + Visuals<br/>JSON + Images]
    D -->|PDF Gen| E1[PDF File]
    D -->|PPTX Gen| E2[PPTX File]
    
    style A fill:#e3f2fd
    style B fill:#fff3e0
    style C fill:#fce4ec
    style D fill:#f3e5f5
    style E1 fill:#c8e6c9
    style E2 fill:#c8e6c9
```

## Architecture Layers

```mermaid
graph TB
    subgraph "Domain Layer (Pure Business Logic)"
        A1[models.py<br/>WorkflowState, Config]
        A2[content_types.py<br/>Enums]
        A3[exceptions.py<br/>Custom errors]
        A4[interfaces.py<br/>Protocols]
    end
    
    subgraph "Application Layer (Orchestration)"
        B1[graph_workflow.py<br/>LangGraph FSM]
        B2[nodes/<br/>7 workflow nodes]
        B3[parsers/<br/>Content parsers]
        B4[generators/<br/>Output generators]
    end
    
    subgraph "Infrastructure Layer (External)"
        C1[llm_content_generator.py<br/>OpenAI + Claude]
        C2[llm_image_generator.py<br/>Gemini Images]
        C3[docling_adapter.py<br/>PDF parsing]
        C4[markitdown_adapter.py<br/>Web extraction]
        C5[file_system.py<br/>I/O operations]
    end
    
    B1 --> A1 & A2 & A3 & A4
    B2 & B3 & B4 --> B1
    C1 & C2 & C3 & C4 & C5 --> B2 & B3 & B4
    
    style A1 fill:#e8f5e9
    style B1 fill:#e3f2fd
    style C1 fill:#fff3e0
```

## Technology Stack Flow

```mermaid
graph LR
    subgraph "Input Processing"
        A1[Docling 2.66.0<br/>PDF/DOCX OCR]
        A2[MarkItDown 0.0.1a2<br/>Web → Markdown]
    end
    
    subgraph "Workflow Engine"
        B1[LangGraph 0.2.55<br/>State Machine]
    end
    
    subgraph "LLM Services"
        C1[OpenAI GPT-4o<br/>Content transform]
        C2[Claude Sonnet<br/>Visual data]
        C3[Gemini Image API<br/>Image generation]
    end
    
    subgraph "Output Generation"
        D1[ReportLab 4.2.5<br/>PDF creation]
        D2[python-pptx 1.0.2<br/>PPTX creation]
    end
    
    subgraph "Support"
        E1[Pydantic 2.10.5<br/>Validation]
        E2[Loguru 0.7.3<br/>Logging]
    end
    
    A1 & A2 --> B1
    B1 --> C1 & C2 & C3
    C1 & C2 & C3 --> D1 & D2
    E1 & E2 --> B1
```

## Key Features

### 1. **Clean Architecture**
- **Domain**: Zero external dependencies (pure business logic)
- **Application**: Orchestration and use cases
- **Infrastructure**: External integrations (APIs, file I/O)

### 2. **LangGraph Workflow**
- 7-node state machine
- Automatic retry on errors (max 3 attempts)
- Conditional branching for retry logic

### 3. **Multi-Format Support**
- **Input**: PDF, DOCX, PPTX, Markdown, TXT, Web URLs
- **Output**: PDF (ReportLab) and PPTX (python-pptx)

### 4. **Advanced Parsing**
- **Docling**: OCR, table extraction, layout analysis for PDFs
- **MarkItDown**: Web content to Markdown conversion

### 5. **LLM Enhancement**
- **OpenAI GPT-4o**: Content transformation to blog style
- **Claude Sonnet**: Visual data generation
- **Chunked processing**: Handles long documents (>50K chars)

### 6. **Image Generation**
- **SVG**: Mermaid diagrams for architecture/flowcharts
- **Gemini**: Decorative headers and infographics
- **Caching**: Reuses generated images across runs

### 7. **Folder Processing**
- Combines multiple files into single output
- Intelligent content merging via LLM
- One PDF + One PPTX per folder

### 8. **Configuration**
- **settings.yaml**: Core configuration
- **.env**: API keys (never committed)
- **Environment vars**: Runtime overrides

### 9. **Error Handling**
- Comprehensive logging (Loguru)
- Automatic retry with backoff
- Validation at every step

### 10. **Docker Ready**
- Fully containerized
- Volume mounts for data and output
- Production-ready deployment

## File Locations

```
src/data/                      # Input files and folders
src/output/                    # Generated outputs
  ├── *.pdf                    # PDF documents
  ├── *.pptx                   # PowerPoint presentations
  └── images/                  # Generated images
      ├── section_*_header.png
      └── section_*_infographic.png

config/settings.yaml           # Configuration
.env                          # API keys (not committed)
scripts/                      # Entry point scripts
Makefile                      # Automation commands
```

## Command Reference

```bash
# Single file processing
make run INPUT=src/data/file.md OUTPUT=pdf

# Folder processing (combines all files)
make process-folder FOLDER=llm-architectures

# Batch process all folders
make batch-topics

# Setup and maintenance
make setup                    # Install dependencies
make test                     # Run tests
make lint                     # Format and lint
make clean                    # Clean outputs
```

## Environment Variables

```bash
# Required for LLM features
OPENAI_API_KEY=sk-...         # OpenAI for content
ANTHROPIC_API_KEY=sk-ant-...  # Claude for visuals
GEMINI_API_KEY=...            # Gemini for images

# Optional overrides
DOC_GENERATOR_LLM__MODEL=gpt-4o
DOC_GENERATOR_PDF__PAGE_SIZE=a4
DOC_GENERATOR_LOGGING__LEVEL=DEBUG
```

## Performance Notes

- **Parsing**: Fast (< 5 seconds per file)
- **LLM Transform**: ~30-60 seconds per document
- **Image Generation**: ~10-20 seconds per image
- **PDF/PPTX Creation**: ~5-10 seconds
- **Total**: ~2-5 minutes per document with images

## Future Enhancements

1. ✅ Parallel image generation
2. ✅ Streaming LLM responses
3. ✅ Image caching system
4. ⬜ Multiple LLM provider support
5. ⬜ Custom theme support
6. ⬜ Web UI for configuration
7. ⬜ API endpoint deployment
8. ⬜ Batch processing optimization
