# Hooks

Hooks execute shell commands in response to Claude Code events.

## What are Hooks?

Hooks allow you to:
- Run scripts before/after tool calls
- Enforce project conventions
- Automate repetitive tasks
- Add safety checks

## Hook Types

| Hook | Trigger |
|------|---------|
| `PreToolCall` | Before a tool executes |
| `PostToolCall` | After a tool executes |
| `SessionStart` | When Claude Code starts |
| `SessionEnd` | When Claude Code exits |

## Current Configuration

Check `.claude/settings.json` or `~/.claude/settings.json` for hooks.

## Configuring Hooks

### settings.json Format

```json
{
  "hooks": {
    "PreToolCall": [
      {
        "matcher": "Bash",
        "command": "echo 'Running bash command...'"
      }
    ],
    "PostToolCall": [
      {
        "matcher": "Edit",
        "command": "make lint"
      }
    ],
    "SessionStart": [
      {
        "command": "echo 'Session started at $(date)'"
      }
    ]
  }
}
```

### Matcher Patterns

```json
{
  "matcher": "Bash",           // Exact tool name
  "matcher": "Bash|Edit",      // Multiple tools (regex)
  "matcher": ".*",             // All tools
}
```

## Common Hook Patterns

### Lint After Edit
```json
{
  "hooks": {
    "PostToolCall": [
      {
        "matcher": "Edit|Write",
        "command": "make lint 2>/dev/null || true"
      }
    ]
  }
}
```

### Log All Commands
```json
{
  "hooks": {
    "PreToolCall": [
      {
        "matcher": "Bash",
        "command": "echo \"$(date): $TOOL_INPUT\" >> ~/.claude/command.log"
      }
    ]
  }
}
```

### Session Context Loading
```json
{
  "hooks": {
    "SessionStart": [
      {
        "command": "cat docs/project/STATUS.md"
      }
    ]
  }
}
```

## Environment Variables in Hooks

Available in hook commands:
- `$TOOL_NAME` - Name of the tool
- `$TOOL_INPUT` - Tool input (JSON)
- `$TOOL_OUTPUT` - Tool output (PostToolCall only)

## Hook Failures

- If a hook returns non-zero, the operation may be blocked
- Use `|| true` to ignore failures
- Check hook output in Claude Code logs

## Best Practices

1. **Keep hooks fast** - Long hooks slow down everything
2. **Use `|| true` for optional hooks** - Don't block on non-critical checks
3. **Log sparingly** - Excessive logging clutters output
4. **Test hooks manually first** - Ensure commands work standalone

## Debugging

```bash
# Test hook command manually
echo 'test' | your-hook-command

# Check Claude Code with debug output
claude --debug
```

## Security

- Hooks run with your user permissions
- Be careful with hooks that modify files
- Never put secrets in hook commands
