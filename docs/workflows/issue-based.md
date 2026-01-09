# Issue-Based Development Workflow

Convert project specs and milestones into GitHub issues for tracked development.

## Overview

```
SPEC.md → MILESTONES.md → GitHub Issues → Branches → PRs → Main
```

## Prerequisites

- GitHub CLI installed (`gh`)
- Authenticated: `gh auth login`
- Repository has issues enabled

## Workflow

### 1. Define Specs
Create or update `docs/project/SPEC.md` with:
- Project goals
- Features list
- Success criteria

### 2. Break Down into Milestones
Update `docs/project/MILESTONES.md`:
- Each milestone = logical phase
- List deliverables per milestone
- Define acceptance criteria

### 3. Create Issues from Milestones

**Using the skill**:
```
/create-issues
```

**Manual process**:
```bash
# Create milestone in GitHub
gh api repos/:owner/:repo/milestones -f title="Phase 1: Core Infrastructure"

# Create issues linked to milestone
gh issue create \
  --title "Set up project structure" \
  --body "Create clean architecture folder structure" \
  --milestone "Phase 1: Core Infrastructure" \
  --label "enhancement"
```

### 4. Work on Issues

```bash
# Create branch for issue
git checkout -b feature/issue-123-description

# Work on the issue
# ...

# Create PR
gh pr create --title "Fix #123: Description" --body "Closes #123"
```

### 5. Track Progress

- Issues auto-close when PR merged (if using "Closes #N")
- Update STATUS.md with `/update-status`
- Check milestone progress: `gh issue list --milestone "Phase 1"`

## Labels to Use

| Label | Purpose |
|-------|---------|
| `enhancement` | New feature |
| `bug` | Bug fix |
| `documentation` | Docs only |
| `phase-1`, `phase-2` | Milestone phases |
| `blocked` | Waiting on something |

## Tips

- One issue per deliverable
- Keep issues small and focused
- Link related issues with "Related to #N"
- Use issue templates for consistency

## Automation

The `/create-issues` skill:
1. Reads MILESTONES.md
2. Parses deliverables per phase
3. Creates GitHub issues with labels
4. Links to milestone
