# Claude Code Instructions

## Read Order (optimize context)
1. `docs/project/STATUS.md` - current state
2. `docs/project/SPEC.md` - what we're building
3. `docs/architecture/architecture.md` - system design
4. Code files only when needed

## SPEC Format
Keep `docs/project/SPEC.md` in this structure:
- Project Name
- Overview
- Product Purpose
- Who Is This Product For
- Problems It Solves
- What the Product Does
- Functionality
- Goals
- Features (Input Formats, Output Formats, Advanced Features)
- Tech Stack
- Architecture
- Constraints
- Success Criteria

## Commands
```bash
make setup | run | test | lint | all
```

## Layout
```
src/{project}/domain|application|infrastructure/
docs/
├── architecture/architecture.md
├── claude-code/                   # hooks, mcp-servers, skills, subagents
├── guides/setup.md
├── learnings/YYYY-MM-DD-session.md
├── plans/YYYY-MM-DD-topic.md
└── project/                       # DECISIONS, MILESTONES, SPEC, STATUS
```

## Skills
- `/session-start` - read STATUS, suggest tasks
- `/session-end` - update STATUS, optional retro
- `/update-status` - update STATUS.md
- `/retro` - create learnings file

## Workflow
1. Read docs first, code only when needed
3. `make lint` after changes
4. `make test` before commit

## Principles
- Simplicity over complexity
- No premature abstraction
- Evidence before assertions
