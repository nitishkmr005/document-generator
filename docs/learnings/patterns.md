# Patterns

Recurring patterns and insights to carry forward to future MVPs.

---

## Architecture Patterns

### Clean Architecture Works
**Pattern**: Three-layer separation (Domain → Application → Infrastructure)
**Why It Works**: Clear dependencies, testable domain logic, swappable infrastructure
**Apply When**: Building any non-trivial application

### LangGraph for Multi-Step Workflows
**Pattern**: State machine with nodes for each processing step
**Why It Works**: Built-in retry, clear visualization, easy to extend
**Apply When**: Document processing, data pipelines, any multi-step orchestration

---

## Claude Code Patterns

### Session Rituals
**Pattern**: `/session-start` at beginning, `/session-end` at end
**Why It Works**: Maintains context, tracks progress, captures learnings
**Apply When**: Every Claude Code session

### Issue-Based Development
**Pattern**: Specs → Milestones → GitHub Issues → PRs
**Why It Works**: Clear tracking, parallel work possible, audit trail
**Apply When**: Any project with multiple features/tasks

### Git Worktrees for Parallel Work
**Pattern**: Create worktree per feature, multiple Claude instances
**Why It Works**: Isolation, no merge conflicts during development
**Apply When**: Large features that can be parallelized

---

## Anti-Patterns to Avoid

### Over-Engineering Early
**Anti-Pattern**: Building abstractions before they're needed
**Better**: Start concrete, abstract when you see repetition

### Skipping Status Updates
**Anti-Pattern**: Not updating STATUS.md, losing track of progress
**Better**: Update at end of every session, even briefly

### Ignoring Retros
**Anti-Pattern**: Not capturing what went well/poorly
**Better**: Quick retro per milestone, patterns feed next MVP

---

## Template

```markdown
### Pattern Name
**Pattern**: Brief description
**Why It Works**: Explanation
**Apply When**: Situations
```
