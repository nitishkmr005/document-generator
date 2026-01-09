# Milestones

## Overview
MVP phases for the Document Generator project.

| Phase | Title | Status | Deliverables | Acceptance Criteria | Tech Stack |
| --- | --- | --- | --- | --- | --- |
| MVP | End-to-end document generation | Complete | - Generate a document from input to output | - One sample run produces valid outputs | _TBD_ |
| v1 | Parse documents with Docling/MarkItDown | Complete | - Ingest documents via Docling or MarkItDown | - Parsed content is usable by the pipeline | _TBD_ |
| v2 | Multi-source synthesis from a subfolder | Complete | - Combine multiple sources into one document | - Single output reflects all sources | _TBD_ |
| v3 | LLM summarization and content creation | Complete | - Use LLM to summarize or generate slides/SVG | - LLM output is included in final document | _TBD_ |
| v4 | Refactor to clean architecture + config/env | Complete | - Refactor codebase and formalize config/env | - Structure is clean and config-driven | _TBD_ |
| v5 | Docs + Claude Code workflow automation | In Progress | - Reorganize `docs/` and make workflows reusable | - Session start/end flows run without gaps | _TBD_ |
| X | Crazy Ideas | Planned | - Prototype one experimental capability | - A short writeup captures findings | _TBD_ |
| Z | Not In Scope | Not In Scope | - Keep excluded ideas out of scope | - Items remain excluded unless re-scoped | _TBD_ |

## Adding a Milestone

Use `/new-milestone` or add a new row:

```markdown
| Phase | Title | Status | Deliverables | Acceptance Criteria | Tech Stack |
| --- | --- | --- | --- | --- | --- |
| vN | Title | Planned | - Deliverable 1<br>- Deliverable 2 | - Criterion 1<br>- Criterion 2 | - Tech 1<br>- Tech 2 |
```
