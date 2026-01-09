# Claude Code Configuration

Documentation for Claude Code setup in this project.

## Configuration Files

| File | Purpose |
|------|---------|
| [mcp-servers.md](./mcp-servers.md) | MCP server configurations |
| [hooks.md](./hooks.md) | Pre/post command hooks |
| [subagents.md](./subagents.md) | Custom subagent definitions |
| [skills.md](./skills.md) | Available skills/commands |
| [permissions.md](./permissions.md) | Permission settings |

## Key Locations

| Path | Purpose |
|------|---------|
| `.claude/CLAUDE.md` | Project instructions |
| `.claude/settings.json` | Claude Code settings |
| `.claude/skills/` | Custom skills |

## Quick Setup

1. Review `.claude/CLAUDE.md` for project conventions
2. Check `mcp-servers.md` for available integrations
3. Use `/session-start` to begin work

## Adding New Configuration

When adding new MCP servers, hooks, or skills:
1. Implement the configuration
2. Document in the appropriate file here
3. Update `skills.md` if adding new commands
