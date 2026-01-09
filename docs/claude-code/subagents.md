# Subagents

Specialized agents that handle specific types of tasks.

## What are Subagents?

Subagents are specialized Claude instances with:
- Focused capabilities
- Specific tool access
- Domain expertise
- Defined behaviors

## Built-in Subagents

| Agent | Purpose | Tools |
|-------|---------|-------|
| `Explore` | Codebase exploration | Glob, Grep, Read |
| `Plan` | Implementation planning | All tools |
| `Bash` | Command execution | Bash only |
| `general-purpose` | Multi-step tasks | All tools |

## Custom Subagents

### Current Custom Agents

Located in `.claude/agents/`:

| Agent | Purpose |
|-------|---------|
| `refactoring-expert` | Code refactoring and clean code |

### Creating Custom Agents

Create a file in `.claude/agents/`:

```markdown
---
name: agent-name
description: When to use this agent
tools:
  - Bash
  - Read
  - Edit
---

# Agent Name

## Purpose
What this agent does.

## Instructions
1. Step one
2. Step two

## Constraints
- What it should NOT do
- Boundaries
```

## Using Subagents

### Via Task Tool
```
Claude will automatically spawn agents via the Task tool when appropriate.
```

### Trigger Phrases
Certain phrases trigger specific agents:
- "Explore the codebase" → Explore agent
- "Plan the implementation" → Plan agent
- "Refactor this code" → refactoring-expert agent

## Agent Capabilities

### Explore Agent
- Fast codebase searching
- Pattern matching with Glob
- Content searching with Grep
- Thoroughness levels: quick, medium, thorough

### Plan Agent
- Architecture design
- Implementation planning
- Step-by-step breakdowns
- Trade-off analysis

### General-Purpose Agent
- Complex multi-step tasks
- Research and analysis
- Code modifications
- Full tool access

## Best Practices

1. **Let agents work autonomously** - Provide clear goals, not micromanagement
2. **Use appropriate thoroughness** - "quick" for simple, "thorough" for complex
3. **Trust agent outputs** - They're designed for specific tasks
4. **Create custom agents for repeated patterns** - Domain-specific expertise

## Agent Communication

Agents:
- Receive full conversation context
- Return a single result message
- Can be resumed with their agent ID
- Run in background if needed

## Example: Creating a Testing Agent

`.claude/agents/test-runner.md`:
```markdown
---
name: test-runner
description: Run tests and report results
tools:
  - Bash
  - Read
---

# Test Runner Agent

## Purpose
Run project tests and provide detailed results.

## Process
1. Identify test framework (pytest, jest, etc.)
2. Run tests with verbose output
3. Summarize results
4. Highlight failures with context

## Output Format
- Total tests: X
- Passed: X
- Failed: X
- Details for each failure
```
