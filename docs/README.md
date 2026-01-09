# Documentation Index

This documentation structure supports MVP development with Claude Code.

## Quick Links

| Section | Purpose |
|---------|---------|
| [project/](./project/) | Specs, milestones, status tracking |
| [architecture/](./architecture/) | System design and diagrams |
| [workflows/](./workflows/) | Issue-based, multi-agent, session rituals |
| [claude-code/](./claude-code/) | MCP, hooks, subagents, skills |
| [plans/](./plans/) | Implementation plans |
| [learnings/](./learnings/) | Retrospectives and patterns |
| [guides/](./guides/) | How-to guides |

## Skills Available

| Command | Purpose |
|---------|---------|
| `/session-start` | Review status, suggest first task |
| `/session-end` | Update status + optional retro |
| `/update-status` | Update STATUS.md with progress |
| `/retro` | Create retrospective |
| `/create-issues` | Convert milestones to GitHub issues |
| `/new-milestone` | Add milestone with template |

## Structure Overview

```
docs/
├── project/           # MVP tracking (SPEC, MILESTONES, STATUS, DECISIONS)
├── architecture/      # System design, ADRs, diagrams
├── workflows/         # How to work (issue-based, multi-agent)
├── claude-code/       # Claude Code configuration docs
├── plans/             # Implementation plans
├── learnings/         # Retros and patterns
└── guides/            # Step-by-step how-tos
```

## Portability

This structure is designed to be portable. To use in a new project:

1. Copy `docs/` folder structure
2. Copy `.claude/skills/` folder
3. Update `docs/project/SPEC.md` with new project
4. Clear `STATUS.md` and `learnings/`
5. Keep `workflows/` and `claude-code/` as-is
