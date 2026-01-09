---
name: new-milestone
description: Add a new milestone to MILESTONES.md with a template
---

# New Milestone

Add a new milestone phase to MILESTONES.md in tabular format.

## Process

1. **Gather Information**
   Ask the user:

   **Milestone name?**
   - Example: "API Layer", "LLM Integration"

   **What are the deliverables?** (list them)
   - Example: "REST endpoints, Authentication, Rate limiting"

   **What are the acceptance criteria?**
   - Example: "All endpoints return JSON, Auth tokens validated"

2. **Determine Phase Number**
   - Read `docs/project/MILESTONES.md`
   - Find the last phase number
   - Increment for new phase

3. **Generate Milestone Row**
   - Status defaults to `Planned` unless specified
   - Use `<br>` for multi-line lists in table cells
   - Include tech stack if provided, otherwise use `_TBD_`
   ```markdown
   | N | Title | Planned | - Deliverable 1<br>- Deliverable 2<br>- Deliverable 3 | - Criterion 1<br>- Criterion 2<br>- Criterion 3 | - Tech 1<br>- Tech 2 |
   ```

4. **Update MILESTONES.md**
   - Read current file
   - Find the table row insertion point
   - Insert new milestone row
   - Write updated file

5. **Offer to Create Issues**
   Ask: "Would you like to create GitHub issues for these deliverables? (yes/no)"

   If yes, run `/create-issues` skill.

## Output

- Updated MILESTONES.md with new phase
- Optional: GitHub issues created

## Example

**User Input:**
- Name: "API Layer"
- Deliverables: REST endpoints, Authentication, Rate limiting
- Criteria: All endpoints documented, Auth tokens expire in 24h

**Generated:**
```markdown
| 6 | API Layer | Planned | - REST endpoints<br>- Authentication<br>- Rate limiting | - All endpoints documented in OpenAPI spec<br>- Auth tokens expire in 24 hours<br>- Rate limiting at 100 requests/minute | - FastAPI<br>- OpenAPI |
```

## Template

Use this structure for consistency:

```markdown
| N | Title | Status | Deliverables | Acceptance Criteria | Tech Stack |
| --- | --- | --- | --- | --- | --- |
| N | Title | Planned | - Deliverable 1<br>- Deliverable 2 | - Criterion 1<br>- Criterion 2 | - Tech 1<br>- Tech 2 |
```
