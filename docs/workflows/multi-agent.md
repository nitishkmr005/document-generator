# Multi-Agent Workflow with Git Worktrees

Run multiple Claude Code instances in parallel using git worktrees.

## Overview

Git worktrees allow multiple working directories from the same repository. Each Claude instance works in its own worktree, preventing conflicts.

```
main-repo/
├── .git/                    # Shared git database
├── src/                     # Main working directory
└── ...

../main-repo-feature-auth/   # Worktree 1: Auth feature
../main-repo-feature-api/    # Worktree 2: API feature
```

## Prerequisites

- Git 2.5+ (worktree support)
- Multiple terminal windows/tabs
- Clear task breakdown (independent tasks)

## Setup

### 1. Identify Parallel Tasks

Tasks must be **independent**:
- Different files/modules
- No shared state during development
- Can be merged separately

Good candidates:
- Feature A in `src/features/auth/`
- Feature B in `src/features/api/`

Bad candidates:
- Both modifying `src/models.py`
- One depends on the other's output

### 2. Create Worktrees

```bash
# From main repository
git worktree add ../project-feature-auth feature/auth
git worktree add ../project-feature-api feature/api

# Or create with new branch
git worktree add -b feature/auth ../project-feature-auth main
```

### 3. Start Claude Instances

**Terminal 1**:
```bash
cd ../project-feature-auth
claude
# Work on auth feature
```

**Terminal 2**:
```bash
cd ../project-feature-api
claude
# Work on API feature
```

## Coordination

### Communication Between Instances

Instances don't share context. Coordinate via:
1. **STATUS.md** - Each updates their section
2. **Git commits** - Fetch to see other's progress
3. **Shared docs** - Read common documentation

### Merging Work

```bash
# In main repo, after both features complete
git checkout main
git merge feature/auth
git merge feature/api

# Or use PRs for review
```

### Handling Conflicts

If worktrees touch same files:
1. Complete one feature first
2. Merge to main
3. Rebase second feature: `git rebase main`
4. Complete second feature

## Cleanup

```bash
# List worktrees
git worktree list

# Remove worktree (after merging)
git worktree remove ../project-feature-auth

# Prune stale worktrees
git worktree prune
```

## Best Practices

1. **Clear boundaries** - Each worktree owns specific modules
2. **Frequent commits** - Small commits in each worktree
3. **Sync periodically** - `git fetch` to see progress
4. **Merge promptly** - Don't let worktrees diverge too long
5. **Document in STATUS.md** - Track what each worktree is doing

## Model Selection

- **Planning agent (Opus 4.5)**: Designs overall architecture, breaks down tasks
- **Implementation agents (Sonnet 4.5)**: Each worktree uses Sonnet for coding

## Example Session

```bash
# Opus: Plan the work
claude --model opus
> Break down the user service into parallel tasks

# Result: Auth module, API endpoints, Database layer

# Create worktrees
git worktree add -b feature/auth ../proj-auth main
git worktree add -b feature/api ../proj-api main
git worktree add -b feature/db ../proj-db main

# Sonnet: Implement in parallel (3 terminals)
cd ../proj-auth && claude --model sonnet
cd ../proj-api && claude --model sonnet
cd ../proj-db && claude --model sonnet
```
