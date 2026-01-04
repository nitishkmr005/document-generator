# Review Blog Article

Review a technical blog article for quality, clarity, and correctness.

## Arguments

- `$ARTICLE`: Article name or path (e.g., "attention-mechanisms", "vllm-inference.md", or full path)

## Instructions

You are reviewing a technical ML/AI blog article. Perform a comprehensive quality review and suggest actionable improvements.

### Step 1: Locate the Article

Find the article using `$ARTICLE`:
1. If full path provided → use directly
2. If filename with `.md` → search in `content/posts/`
3. If just a name/keyword → search for matching files in `content/posts/` using partial match

```bash
# Search examples:
find content/posts -name "*$ARTICLE*" -type f
```

Read the article content and extract the title from frontmatter.

### Step 2: Concept Breakdown

Evaluate how concepts are introduced:

| Check | What to Look For |
|-------|------------------|
| Chunking | Complex ideas broken into digestible pieces |
| Progression | Simple → complex, prerequisites first |
| Definitions | Key terms bolded on first use, jargon explained |
| Context | Each concept has "why this matters" |

**Red flags:** Jargon without explanation, concepts introduced without context, assumed knowledge not stated upfront.

### Step 3: Diagrams and Flowcharts

Audit visual explanations:

| Check | What to Look For |
|-------|------------------|
| Coverage | Complex processes have visual representation |
| Accuracy | Diagrams match the text explanation |
| Clarity | Labels are clear, consistent with terminology |
| Format | Mermaid syntax used correctly |

**Identify missing visuals — suggest diagram type:**

| Content Type | Recommended Visual |
|--------------|-------------------|
| Multi-step process | Flowchart |
| System components | Architecture diagram |
| Option comparison | Table |
| If/else logic | Decision tree |
| Request/response | Sequence diagram |
| Hierarchy | Tree diagram |
| Timeline | Gantt or timeline |

### Step 4: Article Flow

Evaluate structure against target pattern:

```
✓ Problem (concrete, specific pain point)
    ↓
✓ Quick Theory (just enough to understand)
    ↓
✓ Working Code (real, runnable examples)
    ↓
✓ Practical Takeaways (decision framework, commands, checklist)
```

**Check:**
- Opens with concrete problem, NOT definitions
- Theory is minimal before showing implementation
- Transitions between sections are smooth
- Ends with actionable takeaways

### Step 5: Readability

Check formatting and presentation:

| Check | Target |
|-------|--------|
| Paragraph length | Max 4-5 sentences, then break |
| Code blocks | Labeled with filename, inline comments |
| Specifics | Real numbers: memory, benchmarks, configs |
| Voice | Active ("GPU computes" not "is computed by") |
| Tone | Direct, confident, no hedging ("does" not "might") |
| Warnings | Critical info in blockquotes |

**Red flags:** Walls of text, passive voice, hedging language, missing specifics, fluff intros.

### Step 6: Ease of Understanding

Assess reader experience:

| Check | What to Look For |
|-------|------------------|
| Target audience | Can someone with basic ML knowledge follow? |
| Analogies | Difficult concepts have relatable comparisons |
| Examples | Abstract ideas have concrete illustrations |
| Context | Reader knows WHEN to use this vs alternatives |

**Good analogies should:**
- Connect to everyday experiences (cooking, traffic, libraries)
- Highlight the KEY insight, not surface similarity
- Be brief — one sentence, not a paragraph

### Step 7: Technical Correctness

Verify accuracy:

| Check | What to Look For |
|-------|------------------|
| Concepts | Explanations are technically accurate |
| Diagrams | Visual representations are correct |
| Code | Examples are functional, follow best practices |
| Numbers | Benchmarks are realistic, sources cited |
| Limitations | Constraints and edge cases honestly stated |

**Red flags:** Incorrect explanations, misleading diagrams, broken code, unsupported performance claims.

### Step 8: Generate Review Report

Output a structured review:

```markdown
# Article Review: [Article Title]

**File:** [path/to/article.md]
**Reviewed:** [current date]

## Overall Assessment
[2-3 sentences: strengths, main issues, publication readiness]

## Scores

| Category | Score | Summary |
|----------|:-----:|---------|
| Concept Breakdown | /5 | |
| Diagrams & Visuals | /5 | |
| Article Flow | /5 | |
| Readability | /5 | |
| Ease of Understanding | /5 | |
| Technical Correctness | /5 | |
| **Overall** | **/5** | |

## Critical Issues ⚠️
> Must fix before publishing

1. ...

## Suggested Improvements 💡

1. ...

## Add These Diagrams 📊

| Location | What to Visualize | Diagram Type |
|----------|-------------------|--------------|
| Section X | ... | Flowchart |

## Add These Analogies/Examples 💬

| Concept | Suggested Analogy |
|---------|-------------------|
| ... | ... |

## Specific Edits ✏️

### [Section Name]
**Current:**
> "..."

**Suggested:**
> "..."

**Why:** [brief rationale]
```

### Step 9: Apply Fixes

After presenting the review:

1. Ask: "Would you like me to apply these fixes? (all / critical only / specific numbers)"
2. If yes:
   - Apply requested edits to the article
   - Generate and insert missing diagrams
   - Add suggested analogies where appropriate
3. Show diff summary of changes made
4. Re-run quick validation on updated article