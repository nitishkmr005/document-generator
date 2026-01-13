# Logging Guidelines

## Workflow Header Format

```
================================================================================
🚀 [WORKFLOW NAME] STARTED
================================================================================
Input:  [input details]
Output: [output details]
================================================================================
```

## Loguru Configuration

```yaml
# config/settings.yaml
logging:
  level: "INFO"
  format: "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
```

## Step-Based Progress

```
================================================================================
STEP 1/N: [Step Name]
================================================================================
→ [Action description]
  [Metric 1]: [value]
  [Metric 2]: [value]
✓ [Step Name] COMPLETED
[Optional result summary]
················································································

================================================================================
STEP 2/N: [Next Step]
================================================================================
→ [Action description]
  [Details]
✓ [Step Name] COMPLETED
················································································
```

## LLM Observability (Opik)

> [!IMPORTANT]
> ALL LLM calls MUST use Opik for observability.

```python
import opik
from opik.integrations.langchain import OpikTracer

opik.configure(use_local=False)
tracer = OpikTracer()
```

Log: input tokens, output tokens, latency, purpose.

## JSON Logging

Store in `src/data/logging/YYYY-MM-DD_HH-MM-SS_llm_calls.json`:

```json
{
  "timestamp": "2025-01-13T19:01:24",
  "purpose": "content_summarization",
  "model": "gemini-2.5-pro",
  "input_tokens": 1234,
  "output_tokens": 456,
  "latency_seconds": 2.34
}
```

## Summary Table (End of Run)

Include an LLM call summary table when available:

```
┌──────────────────────┬─────────┬──────────┬─────────┬──────────┐
│ Purpose              │ Model   │ Tokens   │ Latency │ Status   │
├──────────────────────┼─────────┼──────────┼─────────┼──────────┤
│ Content Summary      │ gemini  │ 1.2k/450 │ 2.34s   │ ✅       │
│ Slide Generation     │ gemini  │ 2.1k/890 │ 4.56s   │ ✅       │
│ Image Prompt         │ gemini  │ 456/123  │ 1.23s   │ ✅       │
└──────────────────────┴─────────┴──────────┴─────────┴──────────┘
```
