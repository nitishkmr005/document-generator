---
name: update-status
description: Update docs/project/STATUS.md with current progress
---

# Update Status

Update the project STATUS.md file with current progress in a tabular format and supporting sections.

## Process

1. **Gather Information**
   - Run `git log --oneline -10` to see recent commits
   - Run `git status` to check current state
   - Ask user: "What was accomplished? Any blockers?"

2. **Read Current STATUS.md**
   - Read `docs/project/STATUS.md`
   - Understand current table structure and entries

3. **Update Table Row**
   - Keep the table columns: Date, Session Name, Phase Number, Summary, Status, In Progress, Blockers, Completed Tasks, Next Up, Tech Stack, Prompts Used
   - Keep most recent session as the top row
   - Update the existing row if it reflects the latest session, otherwise add a new row
   - Use `<br>` for multi-line lists in table cells
   - Keep wording concise and action-oriented
   - Fill In Progress, Blockers, Tech Stack with current details (or `_None_` / `_TBD_` if unknown)

4. **Update Supporting Sections**
   - **In Progress**: Mirror current in-progress items
   - **Blockers**: Mirror current blockers
   - **Tech Stack**: List current stack or `_TBD_`

5. **Write Updated STATUS.md**
   - Use Edit tool to update the file
   - Preserve the table and section structure

## Output

Updated STATUS.md with current progress in table format and sections.

## Example Update

```markdown
| Date | Session Name | Phase Number | Summary | Status | In Progress | Blockers | Completed Tasks | Next Up | Tech Stack | Prompts Used |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2025-01-09 | Docs Workflow Setup | 5 | Documentation structure implementation. | In Progress | - Testing skills in workflow | _None_ | - Created docs folder structure<br>- Added workflow documentation<br>- Built 6 automation skills | - Create GitHub issues from milestones | - Python<br>- Typer | - Update status table |
```

## Sections

```markdown
## In Progress
- Testing skills in workflow

## Blockers
_None_

## Tech Stack
- Python
- Typer
```
