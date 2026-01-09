# Milestones

## Overview
MVP phases for the Document Generator project.

---

## Phase 1: Core Infrastructure (Completed)

### Deliverables
- [x] Project structure with clean architecture
- [x] Domain models (WorkflowState, ContentFormat, OutputFormat)
- [x] LangGraph workflow skeleton
- [x] Basic logging with Loguru

### Acceptance Criteria
- Project runs with `make run`
- Tests pass with `make test`
- Clean architecture layers separated

---

## Phase 2: Input Parsing (Completed)

### Deliverables
- [x] Markdown parser with frontmatter support
- [x] Docling adapter for PDF/DOCX/PPTX
- [x] MarkItDown adapter for web URLs
- [x] Unified parser interface

### Acceptance Criteria
- All input formats detected correctly
- Content extracted to structured format
- Error handling for malformed inputs

---

## Phase 3: Output Generation (Completed)

### Deliverables
- [x] ReportLab PDF generator
- [x] python-pptx PPTX generator
- [x] Output validation node

### Acceptance Criteria
- PDF generates with proper styling
- PPTX generates with slides
- Retry logic works on failures

---

## Phase 4: Docker & Polish (Completed)

### Deliverables
- [x] Dockerfile
- [x] docker-compose.yaml
- [x] CLI entry point
- [x] Comprehensive tests

### Acceptance Criteria
- Docker build succeeds
- Container runs end-to-end
- Tests pass with coverage

---

## Phase 5: Documentation & Workflow (In Progress)

### Deliverables
- [ ] Comprehensive docs/ structure
- [ ] Claude Code skills for workflow automation
- [ ] Session management workflows
- [ ] Issue-based development workflow

### Acceptance Criteria
- All docs/ folders populated
- Skills functional and tested
- Workflow documentation complete

---

## Future Phases

### Phase 6: LLM Integration
- Content summarization
- Slide content generation
- Smart formatting

### Phase 7: API Layer
- REST API endpoints
- Authentication
- Rate limiting

---

## Adding a Milestone

Use `/new-milestone` or add manually:

```markdown
## Phase N: Title

### Deliverables
- [ ] Deliverable 1
- [ ] Deliverable 2

### Acceptance Criteria
- Criterion 1
- Criterion 2
```
