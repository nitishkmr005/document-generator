---
name: retro
description: Create a retrospective document capturing what went well, what went poorly, and lessons learned
---

# Retrospective

Create a retrospective document for a session or milestone.

## Process

1. **Determine Context**
   Ask: "Is this retro for:"
   - A) This session
   - B) A completed milestone
   - C) A specific topic

2. **Gather Feedback**
   Ask three questions (one at a time):

   **What went well?**
   - Successes
   - Good decisions
   - Effective patterns

   **What went poorly?**
   - Challenges
   - Mistakes
   - Friction points

   **What did we learn?**
   - Insights
   - New knowledge
   - Process improvements

3. **Identify Action Items**
   Ask: "Any specific action items to carry forward?"

4. **Create Retro Document**
   Create file: `docs/learnings/YYYY-MM-session-name.md`

   ```markdown
   # Session: YYYY-MM-DD

   ## Context
   [Session/Milestone description]

   ## What Went Well
   - [items]

   ## What Went Poorly
   - [items]

   ## What We Learned
   - [items]

   ## Action Items
   - [ ] [item]

   ## Tips & Tricks for Claude Code

   Based on this session, useful patterns for future reference:

   - **Tip**: [Specific Claude Code tip discovered or reinforced]
   - **Tip**: [Another useful pattern or shortcut]

   ## Generalization Opportunities

   Consider creating reusable artifacts if this session revealed repeatable patterns. For example:

   - **Slash Command**: [If a specific workflow could be automated]
   - **Agent**: [If a specialized task could be delegated]
   - **Skill**: [If a multi-step process with assets would help]

   [Only include this section if genuinely applicable. Before generalizing, ensure the pattern is genuinely reusable across multiple contexts. Premature abstraction can add complexity without benefit.]

   ```

## Output

- New file in `docs/learnings/` with session-date naming

## Example

File: `docs/learnings/2025-01-docs-structure-session.md`

```markdown
# Session: 2025-01-09

## Context
Implementing documentation structure for MVP workflow.

## What Went Well
- Brainstorming clarified requirements
- Incremental design validation prevented rework

## What Went Poorly
- Initial scope too broad

## What We Learned
- Validate design in small sections
- Skills reduce repetitive work

## Action Items
- [ ] Test skills end-to-end
```

## Guidelines

- **Be honest and specific** - vague observations aren't actionable
- **Focus on process, not outcomes** - "we used X approach" not "we built Y feature"
- **Prioritize actionable insights** - each lesson should inform future behavior
- **Keep it concise** - quality over quantity
- **Skip sections if not applicable** - empty sections add no value
