# Documentation Guidelines

## Root Project Files

> [!WARNING]
> ONLY these `.md` files allowed in project root:
>
> - `README.md`
> - `Quickstart.md`

No other `.md` files in root. Everything else goes in `docs/`.

## docs/ Folder Structure

```
docs/
├── README.md              # Documentation index
├── project/               # Product specs and status
│   ├── SPEC.md           # Product specification
│   └── STATUS.md         # Current project status
├── plans/                 # Design plans (date-prefixed)
│   └── YYYY-MM-DD-topic.md
├── learnings/             # Session retrospectives
│   └── YYYY-MM-DD-session.md
├── claude-code/           # Claude Code integration guides
│   ├── architecture.md
│   ├── setup.md
│   ├── logging.md
│   ├── documentation.md
│   ├── model-preferences.md
│   ├── spec-template.md
│   ├── blog-template.md
│   └── config.md
└── blog/                  # Technical blog post about this current project
```

## Naming Conventions

| Folder     | Pattern                 | Example                     |
| ---------- | ----------------------- | --------------------------- |
| plans/     | `YYYY-MM-DD-topic.md`   | `2025-01-13-api-design.md`  |
| learnings/ | `YYYY-MM-DD-session.md` | `2025-01-13-refactoring.md` |
| blog/      | `topic.md`              | `implementation-guide.md`   |

## README.md

Every `README.md` should include:

1. Project title and one-line description
2. Quick start (3-5 steps max)
3. Key features
4. Installation/setup link
5. Usage examples

## Quickstart.md

Focused on getting started FAST:

1. Prerequisites
2. Installation (copy-paste commands)
3. First run example
4. Next steps (link to full docs)
