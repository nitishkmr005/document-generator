# Documentation Index

Welcome to the Document Generator documentation. This directory contains comprehensive guides, architecture documentation, and implementation details.

## Quick Navigation

### 📊 Process & Architecture
- **[PROCESS_FLOW.md](./PROCESS_FLOW.md)** - Complete visual process flow with diagrams
- **[architecture.md](./architecture/architecture.md)** - System architecture overview

### 📖 User Guides
- **[FOLDER_BASED_PROCESSING.md](./guides/FOLDER_BASED_PROCESSING.md)** - Process multiple files as topics
- **[MAKEFILE_COMMANDS.md](./guides/MAKEFILE_COMMANDS.md)** - Complete command reference
- **[ENV_SETUP.md](./guides/ENV_SETUP.md)** - Environment configuration guide
- **[REUSING_IMAGES.md](./guides/REUSING_IMAGES.md)** - Image caching and reuse
- **[setup.md](./guides/setup.md)** - Initial setup instructions

### 🔧 Implementation Details
- **[IMPLEMENTATION_SUMMARY.md](./guides/IMPLEMENTATION_SUMMARY.md)** - Technical implementation summary
- **[FIXED_PYTHON_ISSUE.md](./guides/FIXED_PYTHON_ISSUE.md)** - Troubleshooting guide

### 📋 Project Status
- **[STATUS.md](./project/STATUS.md)** - Current project status
- **[SPEC.md](./project/SPEC.md)** - Project specifications

### 🎯 Design Plans
- **[gemini-image-generation-design.md](./plans/2025-01-10-gemini-image-generation-design.md)** - Gemini image integration
- **[docs-structure-design.md](./plans/2025-01-09-docs-structure-design.md)** - Documentation structure

### 🧠 Learnings
- **[refactoring-session.md](./learnings/2024-12-refactoring-session.md)** - Lessons from refactoring

### 🤖 Claude Code Integration
- **[hooks.md](./claude-code/hooks.md)** - Pre-commit hooks
- **[mcp-servers.md](./claude-code/mcp-servers.md)** - MCP server integration
- **[skills.md](./claude-code/skills.md)** - Claude skills
- **[subagents.md](./claude-code/subagents.md)** - Subagent patterns

### 📝 Patterns
- **[commands.md](./pattern/commands.md)** - Command patterns

## Getting Started

1. Start with the **[Quickstart Guide](../Quickstart.md)** in the root directory
2. Review **[PROCESS_FLOW.md](./PROCESS_FLOW.md)** to understand how the system works
3. Read **[FOLDER_BASED_PROCESSING.md](./guides/FOLDER_BASED_PROCESSING.md)** for the main use case
4. Check **[ENV_SETUP.md](./guides/ENV_SETUP.md)** for API key configuration

## Documentation Structure

```
docs/
├── README.md (this file)          # Documentation index
├── PROCESS_FLOW.md                # Visual process diagrams
├── architecture/                  # Architecture docs
├── guides/                        # User and developer guides
├── project/                       # Project specs and status
├── plans/                         # Design plans
├── learnings/                     # Development learnings
├── claude-code/                   # Claude integration
└── pattern/                       # Code patterns
```

## Contributing to Documentation

When adding new documentation:
1. Place files in the appropriate subdirectory
2. Update this README.md index
3. Use clear, descriptive filenames with dates for plans/learnings
4. Include diagrams where helpful (Mermaid syntax preferred)
5. Keep the root directory clean (only README.md and Quickstart.md)
