# Architecture

System design documentation and architectural decisions.

## Contents

| Path | Purpose |
|------|---------|
| [diagrams/](./diagrams/) | Visual diagrams (Mermaid, flowcharts) |
| [decisions/](./decisions/) | Architecture Decision Records (ADRs) |

## Current Architecture

See main [README.md](../../README.md) for architecture overview.

**Key Pattern**: Hybrid Clean Architecture
- Domain Layer: Pure business logic
- Application Layer: Use case orchestration
- Infrastructure Layer: External integrations

## Diagrams

- [LangGraph Workflow](./diagrams/langgraph-diagram.md)
- [Workflow Visualization](./diagrams/WORKFLOW-VISUALIZATION.md)

## Adding ADRs

Use format: `decisions/NNNN-title.md`

```markdown
# NNNN. Title

## Status
Accepted | Deprecated | Superseded

## Context
What is the issue?

## Decision
What did we decide?

## Consequences
What are the results?
```
