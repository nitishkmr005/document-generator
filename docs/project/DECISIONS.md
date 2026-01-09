# Decision Log

Record of key technical and architectural decisions.

---

## DEC-001: Clean Architecture Pattern

**Date**: 2024-12 (Project Start)

**Context**: Needed to structure the codebase for maintainability and testability.

**Decision**: Use Hybrid Clean Architecture with three layers:
- Domain: Pure business logic, zero dependencies
- Application: Use case orchestration
- Infrastructure: External integrations

**Consequences**:
- Clear separation of concerns
- Easy to test domain logic in isolation
- Slightly more boilerplate than flat structure

---

## DEC-002: LangGraph for Workflow

**Date**: 2024-12

**Context**: Needed workflow orchestration for multi-step document processing.

**Decision**: Use LangGraph for state machine workflow.

**Alternatives Considered**:
- Plain Python functions: Too simple, no retry logic
- Celery: Overkill for single-process workflow
- Prefect: Heavy dependency

**Consequences**:
- Built-in retry and error handling
- Visual workflow representation possible
- Learning curve for team

---

## DEC-003: Docling for Document Parsing

**Date**: 2024-12

**Context**: Needed robust PDF/DOCX parsing with OCR support.

**Decision**: Use IBM's Docling library.

**Alternatives Considered**:
- PyPDF2: No OCR, limited table extraction
- pdfminer: Complex API
- Unstructured: Heavy, many dependencies

**Consequences**:
- Excellent table extraction
- OCR support included
- Large dependency (~500MB)

---

## DEC-004: Documentation Structure

**Date**: 2025-01-09

**Context**: Needed organized documentation for MVP workflow with Claude Code.

**Decision**: Create structured docs/ with 7 folders:
- project/ (specs, milestones, status)
- architecture/ (diagrams, ADRs)
- workflows/ (issue-based, multi-agent)
- claude-code/ (MCP, hooks, skills)
- plans/, learnings/, guides/

**Consequences**:
- Clear organization
- Portable to other projects
- Skills can automate updates

---

## Template

```markdown
## DEC-NNN: Title

**Date**: YYYY-MM-DD

**Context**: What is the issue?

**Decision**: What did we decide?

**Alternatives Considered**:
- Option A: Why not
- Option B: Why not

**Consequences**:
- Result 1
- Result 2
```
