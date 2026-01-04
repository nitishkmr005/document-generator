# Generate Blog Post from LLM Lecture

Generate a technical blog post from lecture document and transcript.

## Arguments

- `$LECTURE_NUM`: Lecture number (e.g., "2" for lecture2)

## Instructions

You are generating a technical ML/AI blog post from lecture materials. Follow these steps:

### Step 1: Locate Source Materials

Find and read the source files:
- **Document**: `data/llm/documents/lecture$LECTURE_NUM.docx` (or similar naming)
- **Transcript**: `data/llm/transcripts/lecture$LECTURE_NUM.txt` (or similar naming)

If files are named differently, search for files containing "lecture" and "$LECTURE_NUM" in the respective directories.

### Step 2: Extract Key Content

From the slides and transcript, identify:
1. **Core problem being solved** — What pain point does this lecture address?
2. **Key concepts and techniques** — Extract the main ideas with specific numbers/benchmarks
3. **Implementation details** — Any code, architectures, or configs mentioned
4. **Practical applications** — Real-world use cases and constraints
5. **Diagram opportunities** — Identify concepts that would benefit from visual explanation:
   - Any process with multiple steps → flowchart
   - Any comparison between approaches → side-by-side diagram
   - Any architecture description → block diagram
   - Any decision logic → decision tree
   - Any evolution/timeline → timeline diagram

### Step 3: Write the Blog Post

Follow this writing style strictly:

**VOICE & TONE:**
- Direct and conversational — like explaining to a smart colleague, not lecturing
- Confident without hedging ("does" not "might"), but honest about limitations
- Open with concrete problems, not definitions ("Running a 70B model on a single GPU? Not happening.")

**STRUCTURE:**
- Problem → Quick Theory → Working Code → Practical Takeaways
- Cover theory "just enough to understand," then immediately show implementation
- Include specific numbers always: memory sizes, benchmark results, config values

**FORMATTING:**
- Use tables for comparisons across multiple items
- **Use Mermaid diagrams liberally** (see MERMAID DIAGRAMS section below)
- Code blocks with file names as comments and inline explanations
- Bold key terms on first introduction only
- Blockquotes for critical warnings
- **Citations required**: When adding information from web search, always include inline citation: `([source](url))`

**MERMAID DIAGRAMS vs SVG:**
- **Use Mermaid** for: Simple flowcharts, quick decision trees, basic process flows
- **Use SVG** for: Complex architectures, detailed comparisons, polished visuals for key concepts
- **Best practice**: Start with Mermaid during drafting, then upgrade important diagrams to SVG

**MERMAID DIAGRAMS:**
Include Mermaid diagrams for simpler visualizations. Add diagrams for:

1. **Architecture flows** — How data/information flows through a system
   ```mermaid
   flowchart LR
       A[Input] --> B[Process] --> C[Output]
   ```

2. **Decision trees** — When to use what (model selection, technique choice)
   ```mermaid
   flowchart TD
       A[Task?] --> B[Generation]
       A --> C[Classification]
       B --> D[Use Decoder-Only]
       C --> E[Use BERT]
   ```

3. **Component comparisons** — Side-by-side visual of alternatives
   ```mermaid
   flowchart LR
       subgraph Old["Old Approach"]
           A1[Component A]
       end
       subgraph New["New Approach"]
           B1[Component B]
       end
   ```

4. **Process pipelines** — Training loops, inference steps, data preprocessing
5. **Timeline/evolution** — How techniques evolved over time
6. **Block architectures** — Neural network layers, transformer blocks

**Diagram guidelines:**
- Minimum 5-8 diagrams total per blog post (combination of Mermaid and SVG)
- Create 3-5 custom SVG diagrams for key concepts (see Step 5)
- Use Mermaid for simpler supporting diagrams
- Place diagrams immediately after explaining a concept (not all at the end)
- Use colors to highlight key components in Mermaid: `style NodeName fill:#28a745,color:#fff`
- Keep diagrams focused — one concept per diagram
- Add subgraphs to group related components
- Replace ASCII art with Mermaid or SVG whenever possible

**TECHNICAL DEPTH:**
- Show real model names, real GPU types, real numbers — no abstractions
- Explicitly list constraints and "what this doesn't solve"
- End with decision frameworks, quick reference commands, and checklists

**AVOID:**
- Fluff intros ("In this article, we will explore...")
- Walls of text — break up with code, diagrams, formatting
- Unsupported performance claims — back with benchmarks
- Passive voice — use active ("Each GPU computes" not "is computed by")

**TARGET:** Reader finishes knowing WHY it matters, HOW it works, has WORKING CODE to run, and knows WHEN to use it vs alternatives.

### Step 4: Generate Blog File

Create the blog post as a markdown file:
- **Location**: `content/posts/`
- **Filename**: Use kebab-case based on the lecture topic (e.g., `attention-mechanisms-deep-dive.md`)
- Include appropriate frontmatter (title, date, tags, description)

### Step 5: Create SVG Diagrams

**IMPORTANT**: Create custom SVG diagrams to illustrate key concepts in the article. These should complement or replace Mermaid diagrams for better visual quality.

**When to Create SVG Diagrams:**
- Complex architectural diagrams (transformers, neural networks)
- Visual comparisons (before/after, multiple approaches side-by-side)
- Data flow diagrams with detailed annotations
- Charts showing performance comparisons
- Timeline or evolution diagrams
- Any concept that benefits from professional-quality visuals

**SVG Creation Guidelines:**

1. **File Organization:**
   - Create directory: `static/images/posts/[article-slug]/`
   - Example: For article `transformer-internals.md` → `static/images/posts/transformer-internals/`
   - Name files descriptively: `diagram_1_architecture.svg`, `diagram_2_attention_comparison.svg`
   - Create overview diagram: `article-overview.svg` (shows all topics covered)

2. **Design Principles:**
   - **Viewbox sizing**: Use appropriate dimensions (1200-1600 width, adjust height as needed)
   - **Color scheme**: Use professional, consistent colors
     - Primary: `#3b82f6` (blue), `#10b981` (green), `#f59e0b` (orange)
     - Backgrounds: `#f8fafc` (light gray), white for cards
     - Text: `#1e293b` (dark), `#64748b` (gray for subtitles)
   - **Typography**: Arial or sans-serif, sizes 12-36px depending on hierarchy
   - **Spacing**: Generous padding and margins for clarity
   - **Gradients**: Use linear gradients for depth and professional appearance

3. **Required Elements:**
   - **Title**: Clear, large title at top (32-36px)
   - **Subtitle**: Context or explanation below title (16-18px)
   - **Labels**: All components clearly labeled
   - **Legends**: Include legend for colors/symbols used
   - **Annotations**: Brief explanations where needed
   - **Modern markers**: Use ⭐ to highlight modern/recommended approaches

4. **Technical Structure:**
   ```svg
   <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1400 800">
     <defs>
       <!-- Define gradients, markers, etc. -->
     </defs>
     <rect width="1400" height="800" fill="#f8fafc"/>
     <!-- Content groups -->
   </svg>
   ```

5. **Common Diagram Types to Create:**
   - **Overview diagram** - Shows all 5-7 main topics at article start
   - **Architecture diagrams** - System components and data flow
   - **Comparison diagrams** - Side-by-side feature/approach comparisons
   - **Process flow** - Step-by-step workflows
   - **Evolution timeline** - How technology changed over time
   - **Summary diagram** - Quick reference table/visual at article end

6. **Reference in Markdown:**
   ```markdown
   ![Description of diagram](/images/posts/article-slug/diagram_name.svg)
   ```

7. **Quality Checklist:**
   - ☐ SVG is resolution-independent and scales well
   - ☐ File size is reasonable (typically 10-20KB per diagram)
   - ☐ Colors are consistent across all diagrams
   - ☐ Text is readable at all zoom levels
   - ☐ Diagram accurately represents the concept
   - ☐ All diagrams follow same design language
   - ☐ Diagrams are placed near relevant content in article

**Example SVG Pattern:**
Create diagrams that match the quality of `diagram_2_attention_sharing.svg`, `diagram_6_sliding_window.svg` in the transformers article - professional, clear, and informative.

### Step 6: Generate Thumbnail

Create a thumbnail image for the blog post:
- Generate a visually appealing thumbnail that represents the lecture topic
- Save to the appropriate assets/images directory used by the portfolio
- Reference the thumbnail in the blog post frontmatter

### Step 7: Update Portfolio Ordering

Ensure the new post appears at the top:
- **Home section**: Update the home page to display this post first in the recent posts/featured section
- **Posts section**: Verify posts are sorted by date (newest first) or manually update ordering if needed
- Check frontmatter date is set to current date to ensure proper sorting

### Step 8: Confirm Output

After creating the file:
1. Confirm the blog post file was created successfully
2. Confirm SVG diagrams were created and saved to `static/images/posts/[article-slug]/`
3. Verify all SVG images are properly referenced in the markdown
4. Confirm the thumbnail was generated and linked
5. Verify the post appears at the top in both home and posts sections
6. Summarize the key topics covered and diagrams created
7. Note any areas where the source material was unclear or could use additional research

**SVG Diagram Summary Template:**
```
Created [X] SVG diagrams:
- article-overview.svg: Overview of all topics
- diagram_1_[name].svg: [description]
- diagram_2_[name].svg: [description]
...
Total size: ~[XX]KB
All diagrams saved to: static/images/posts/[article-slug]/
```