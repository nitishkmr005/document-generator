# Workflows

How to work effectively with this project using Claude Code.

## Workflow Guides

| Guide | Purpose |
|-------|---------|
| [issue-based.md](./issue-based.md) | Convert specs/milestones to GitHub issues |
| [multi-agent.md](./multi-agent.md) | Parallel agents with git worktrees |
| [model-selection.md](./model-selection.md) | When to use Opus vs Sonnet |
| [session-checklist.md](./session-checklist.md) | Start/end session rituals |

## Quick Reference

### Starting a Session
```
/session-start
```
Reviews STATUS.md and suggests first task.

### Ending a Session
```
/session-end
```
Updates status and optionally creates a retro.

### Creating Issues from Milestones
```
/create-issues
```
Parses MILESTONES.md and creates GitHub issues.

### Model Selection
- **Opus 4.5**: Planning, complex reasoning, architecture
- **Sonnet 4.5**: Implementation, code generation, tests
