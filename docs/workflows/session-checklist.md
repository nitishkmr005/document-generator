# Session Checklist

Rituals for starting and ending Claude Code sessions.

## Starting a Session

### Quick Start
```
/session-start
```

### Manual Checklist

1. **Review STATUS.md**
   ```bash
   cat docs/project/STATUS.md
   ```
   - What's in progress?
   - What's blocked?
   - What's next up?

2. **Check Recent Commits**
   ```bash
   git log --oneline -10
   ```
   - What was done recently?
   - Any incomplete work?

3. **Review Open Issues** (if using issue-based workflow)
   ```bash
   gh issue list --assignee @me
   ```

4. **Set Session Goal**
   - Pick one main task
   - Define "done" for this session
   - Note in STATUS.md if multi-session task

5. **Create Branch** (if needed)
   ```bash
   git checkout -b feature/description
   ```

## During Session

### Progress Tracking
- Update todo list as you work
- Commit frequently with clear messages
- Note blockers immediately

### If Switching Tasks
- Commit current work (WIP commit OK)
- Update STATUS.md with context
- Note why switching

### If Stuck
1. Document what you tried
2. Check if it's a blocker (add to STATUS.md)
3. Consider switching to different task
4. Ask for help if needed

## Ending a Session

### Quick End
```
/session-end
```

### Manual Checklist

1. **Commit All Work**
   ```bash
   git status
   git add .
   git commit -m "WIP: description"  # or proper commit if complete
   ```

2. **Update STATUS.md**
   - Move completed items to "Recently Completed"
   - Update "In Progress" section
   - Add any new blockers
   - Note next steps for continuity

3. **Optional: Create Retro**
   ```
   /retro
   ```
   - What went well?
   - What went poorly?
   - What did you learn?

4. **Push to Remote** (if appropriate)
   ```bash
   git push origin HEAD
   ```

5. **Close Issue** (if completed)
   ```bash
   gh issue close 123 --comment "Completed in commit abc123"
   ```

## Session Handoff

If another session (or person) will continue:

1. **Document Context**
   - Current state of work
   - What's partially done
   - Key decisions made

2. **Leave Breadcrumbs**
   - TODO comments in code
   - Notes in STATUS.md
   - Commit messages with context

3. **Don't Leave Broken State**
   - Tests should pass
   - Code should at least compile
   - Document known issues

## Templates

### STATUS.md Session Entry
```markdown
### YYYY-MM-DD Session
**Focus**: Main task for this session
**Started**: What we began with
**Completed**: What we finished
**Next**: What continues tomorrow
**Blockers**: Any issues found
```

### WIP Commit Message
```
WIP: Brief description

- What's done
- What's remaining
- Any notes for next session
```
