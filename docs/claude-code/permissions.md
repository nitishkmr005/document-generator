# Permissions

Control what Claude Code can and cannot do.

## Overview

Permissions control:
- Which tools Claude can use
- What files/directories are accessible
- Network access
- Command execution

## Permission Levels

| Level | Description |
|-------|-------------|
| `allow` | Permitted without asking |
| `ask` | Prompts for confirmation |
| `deny` | Blocked entirely |

## Configuration

### settings.json Format

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Glob",
      "Grep"
    ],
    "ask": [
      "Edit",
      "Write",
      "Bash"
    ],
    "deny": [
      "dangerous-command"
    ]
  }
}
```

### Path-Based Permissions

```json
{
  "permissions": {
    "allow": [
      "Read:src/**",
      "Edit:src/**"
    ],
    "deny": [
      "Read:.env",
      "Edit:node_modules/**"
    ]
  }
}
```

## Current Configuration

Check `.claude/settings.json` for project permissions.

Default behavior:
- Read operations: Usually allowed
- Write operations: Usually ask
- Bash commands: Usually ask
- Sensitive files: Usually denied

## Common Permission Patterns

### Development Mode
Allow most operations, ask for destructive:
```json
{
  "permissions": {
    "allow": ["Read", "Glob", "Grep", "Edit", "Write"],
    "ask": ["Bash"]
  }
}
```

### Strict Mode
Ask for everything except read:
```json
{
  "permissions": {
    "allow": ["Read", "Glob", "Grep"],
    "ask": ["Edit", "Write", "Bash"]
  }
}
```

### Protected Files
Block access to sensitive files:
```json
{
  "permissions": {
    "deny": [
      "Read:.env*",
      "Read:**/secrets/**",
      "Edit:package-lock.json"
    ]
  }
}
```

## Tool-Specific Permissions

### Bash Commands
```json
{
  "permissions": {
    "allow": [
      "Bash:make *",
      "Bash:npm test",
      "Bash:git status"
    ],
    "deny": [
      "Bash:rm -rf *",
      "Bash:sudo *"
    ]
  }
}
```

### File Operations
```json
{
  "permissions": {
    "allow": [
      "Edit:src/**/*.py",
      "Write:docs/**"
    ],
    "deny": [
      "Edit:*.lock",
      "Write:.github/**"
    ]
  }
}
```

## Security Best Practices

1. **Deny sensitive files** - `.env`, credentials, secrets
2. **Restrict Bash commands** - No `rm -rf`, `sudo`, etc.
3. **Protect config files** - Lock files, CI configs
4. **Use ask for destructive ops** - Deletes, overwrites
5. **Audit periodically** - Review what's allowed

## Debugging Permissions

If an operation is blocked:
1. Check permission denied message
2. Review settings.json
3. Add specific allow rule if needed
4. Use `ask` instead of `allow` for safety

## Project vs Global

| Scope | File | Priority |
|-------|------|----------|
| Project | `.claude/settings.json` | Higher |
| Global | `~/.claude/settings.json` | Lower |

Project settings override global settings.
