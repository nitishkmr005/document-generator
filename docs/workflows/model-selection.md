# Model Selection Guide

When to use Opus 4.5 vs Sonnet 4.5 in Claude Code.

## Quick Reference

| Task Type | Model | Why |
|-----------|-------|-----|
| Planning | Opus 4.5 | Better at architecture, trade-offs |
| Complex reasoning | Opus 4.5 | Deeper analysis |
| Implementation | Sonnet 4.5 | Fast, good at code generation |
| Bug fixes | Sonnet 4.5 | Quick iteration |
| Refactoring | Sonnet 4.5 | Efficient for repetitive changes |
| Code review | Opus 4.5 | Catches subtle issues |

## Opus 4.5 - The Planner

**Strengths**:
- Architectural decisions
- Breaking down complex problems
- Considering trade-offs
- Writing design documents
- Code review and analysis

**Use for**:
```
- "Design the authentication system"
- "Break this feature into parallel tasks"
- "Review this PR for issues"
- "What's the best approach for X?"
- "Analyze this codebase structure"
```

**Cost**: Higher tokens, slower response

## Sonnet 4.5 - The Implementer

**Strengths**:
- Fast code generation
- Following established patterns
- Implementing defined tasks
- Writing tests
- Fixing bugs

**Use for**:
```
- "Implement the login endpoint"
- "Write tests for UserService"
- "Fix the null pointer in auth.py"
- "Refactor these functions to use async"
- "Add validation to this form"
```

**Cost**: Lower tokens, faster response

## Workflow Pattern

### 1. Plan with Opus
```bash
claude --model opus
> Plan the implementation of user authentication
```

Opus outputs:
- Architecture overview
- Component breakdown
- Implementation order
- Risk areas

### 2. Implement with Sonnet
```bash
claude --model sonnet
> Implement step 1: Create User model as specified in the plan
```

### 3. Review with Opus
```bash
claude --model opus
> Review the authentication implementation for security issues
```

## Switching Models

**In Claude Code**:
```
/model opus     # Switch to Opus
/model sonnet   # Switch to Sonnet
```

**Via CLI**:
```bash
claude --model opus
claude --model sonnet
```

## Cost Optimization

1. **Start cheap**: Begin with Sonnet for exploration
2. **Escalate when stuck**: Switch to Opus for complex reasoning
3. **Batch planning**: Do all planning in one Opus session
4. **Implement in Sonnet**: All coding tasks in Sonnet

## Anti-Patterns

**Don't use Opus for**:
- Simple file edits
- Running commands
- Repetitive refactoring
- Well-defined implementation tasks

**Don't use Sonnet for**:
- Architectural decisions without a plan
- Complex debugging without understanding
- Trade-off analysis
- Design review

## Decision Flowchart

```
Is this a planning/design task?
├── Yes → Opus 4.5
└── No
    └── Is this complex reasoning?
        ├── Yes → Opus 4.5
        └── No
            └── Is this implementation/coding?
                ├── Yes → Sonnet 4.5
                └── No → Start with Sonnet, escalate if needed
```
