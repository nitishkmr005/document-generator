# MCP Servers

Model Context Protocol (MCP) servers extend Claude Code with additional capabilities.

## What are MCP Servers?

MCP servers provide:
- External tool integrations (databases, APIs)
- Custom resources (documentation, context)
- Specialized capabilities (file systems, git operations)

## Current Configuration

_No project-specific MCP servers configured._

## Common MCP Servers

| Server | Purpose | Install |
|--------|---------|---------|
| `filesystem` | File operations | Built-in |
| `git` | Git operations | Built-in |
| `github` | GitHub API access | `npx @anthropic/mcp-server-github` |
| `postgres` | Database queries | `npx @anthropic/mcp-server-postgres` |
| `brave-search` | Web search | `npx @anthropic/mcp-server-brave-search` |

## Adding an MCP Server

### 1. Install the Server

```bash
# Example: GitHub MCP server
npm install -g @anthropic/mcp-server-github
```

### 2. Configure in settings.json

Edit `~/.claude/settings.json` or `.claude/settings.json`:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

### 3. Set Environment Variables

```bash
export GITHUB_TOKEN=your_token_here
```

### 4. Restart Claude Code

MCP servers load at startup.

## Project-Specific vs Global

| Location | Scope |
|----------|-------|
| `~/.claude/settings.json` | All projects |
| `.claude/settings.json` | This project only |

## Debugging MCP Servers

```bash
# Check if server is running
claude --debug

# Test server directly
npx @anthropic/mcp-server-github --help
```

## Security Notes

- Never commit tokens to git
- Use environment variables for secrets
- Review server permissions before installing
- Project MCP servers override global ones

## Resources

- [MCP Specification](https://modelcontextprotocol.io/)
- [Official MCP Servers](https://github.com/anthropics/mcp-servers)
- [Claude Code MCP Docs](https://docs.anthropic.com/claude-code/mcp)
