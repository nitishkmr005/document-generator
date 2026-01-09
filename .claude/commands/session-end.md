---
name: session-end
description: Update status and optionally create a retro at the end of a Claude Code session
---

# Session End

Wrap up the current session by updating status and optionally creating a retrospective.

## Process

1. **Confirm Session-End Actions**
   Ask the user to confirm before proceeding:
   - Should I update `docs/project/STATUS.md`?
   - Should I run `/commit` and `git push`?
   - Should I check for reusable prompts and run `/save-prompt`?
   - Should I create a retro?

2. **Gather Session Summary**
   Ask the user:
   - What was accomplished this session?
   - Any blockers encountered?
   - What should be worked on next?

3. **Update STATUS.md**
   - Read current `docs/project/STATUS.md`
   - Add session entry with date
   - Move completed items to "Recently Completed"
   - Update "In Progress" and "Blocked" sections
   - Add new items to "Next Up"

4. **Check for Uncommitted Work**
   - Run `git status` to check for uncommitted changes
   - Proceed to commit if there are changes

5. **Commit and Push**
   - Run `git add .`
   - Create commit using `/commit` workflow from `/commit.md`
   - Run `git push`

6. **Save Reusable Prompts**
   - If this session produced a reusable prompt, run `/save-prompt`
   - Save the generated file in `docs/pattern/slash-commands/`

7. **Offer Retrospective**
   Ask: "Would you like to create a quick retro for this session? (yes/no)"

   If yes, run `/retro` skill.

8. **Session Summary**
   Output:
   ```
   ## Session Complete

   ### Accomplished
   - [items]

   ### STATUS.md Updated
   - [changes made]

   ### Next Session
   - [suggested starting point]

   Changes committed and pushed.
   ```

## Output

Updated STATUS.md and optional retrospective.
