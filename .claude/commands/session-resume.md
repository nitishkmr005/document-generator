---
name: session-resume
description: Review project status and suggest first task at the start of a Claude Code session
---

# Session Resume

Review current project status and suggest what to work on.

## Process

1. **Confirm What to Review**
   Ask the user to confirm what to read:
   - Project specification and Milestones: `docs/project/SPEC.md`
   - Current work status: `docs/project/STATUS.md`
   - Recent git activity: `git log --oneline -5`
   - Assigned GitHub issues: `gh issue list --assignee @me --limit 5`

2. **Read STATUS.md**
   - Read `docs/project/STATUS.md` to understand current state
   - Note what's in progress, blocked, and next up

3. **Choose Phase to Implement**
   Ask: "Which phase should we implement now based on STATUS and SPEC?"
   - Confirm the phase label (MVP, v1, v2, ...)

4. **Check Recent Commits**
   - Run `git log --oneline -5` to see recent activity
   - Understand what was done recently

5. **Review Open Issues** (if using GitHub)
   - Run `gh issue list --assignee @me --limit 5` if gh is available
   - Note any assigned issues

6. **Summarize and Suggest**
   Present a brief summary:
   ```
   ## Current Status
   - In Progress: [items]
   - Blocked: [items]
   - Next Up: [items]

   ## Recent Activity
   - [recent commits]

   ## Suggested First Task
   Based on priorities, I suggest starting with: [task]

   Ready to begin?
   ```

## Output

A concise status summary with a suggested first task for the session.
