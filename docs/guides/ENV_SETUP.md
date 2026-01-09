# Environment Setup Guide

## Quick Start

1. **Copy the example .env file** (if it doesn't exist):
   ```bash
   # The .env file should contain your API keys
   # Example format:
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   # or
   CLAUDE_API_KEY=your_claude_api_key_here
   # or
   OPENAI_API_KEY=your_openai_api_key_here
   ```

2. **Install dependencies**:
   ```bash
   make setup-docgen
   ```

3. **Run the LLM architectures workflow**:
   ```bash
   make run-llm-architectures
   ```

## API Key Configuration

The system supports multiple LLM providers:

### Claude (Anthropic) - Recommended
- Environment variable: `ANTHROPIC_API_KEY` or `CLAUDE_API_KEY`
- Best for: Visual generation, document transformation
- Get your key: https://console.anthropic.com/

### OpenAI
- Environment variable: `OPENAI_API_KEY`
- Alternative LLM provider
- Get your key: https://platform.openai.com/api-keys

### Priority Order
1. Claude API (if `ANTHROPIC_API_KEY` or `CLAUDE_API_KEY` is set)
2. OpenAI API (if `OPENAI_API_KEY` is set)
3. No LLM (basic transformation only)

## Make Commands

### Setup
```bash
make setup-docgen          # Install all dependencies
```

### Run Workflows
```bash
make run-llm-architectures # Process LLM architectures folder (PDF + PPTX)
make run-docgen INPUT=<file> OUTPUT=<pdf|pptx>  # Process single file
```

### Examples
```bash
# Single file
make run-docgen INPUT=src/data/sample/test-blog-article.md OUTPUT=pdf

# Full folder with both PDF and PPTX
make run-llm-architectures
```

## Direct Script Usage

### Using run.sh (Recommended)
```bash
# Single file (generates both PDF and PPTX)
bash run.sh src/data/sample/test-blog-article.md --verbose

# Folder (processes all files)
bash run.sh src/data/llm-architectures --verbose
```

### Using Python directly
```bash
# Single file
python scripts/run_generator.py <input> --output <pdf|pptx>

# Folder
python scripts/generate_from_folder.py <folder>
```

## Output Location

All generated files are saved to:
```
src/output/
├── <filename>.pdf
├── <filename>.pptx
└── visuals/
    └── *.svg
```

## Troubleshooting

### No API Key Found
If you see "LLM features disabled", ensure your `.env` file exists and contains a valid API key.

### Dependencies Not Found
Run `make setup-docgen` to install all required packages.

### Permission Errors
The workflow needs to read from `src/data/` and write to `src/output/`.
