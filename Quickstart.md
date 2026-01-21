# Document Generator - Quick Start Guide

**Production-ready LangGraph-based document generator** with 100% Python implementation.

---

## 🚀 Quick Start

### **1. Install Dependencies**

```bash
# Using make
make setup-prismdocs

# Or manually
uv pip install -e ".[dev]"
```

### **2. Configure API Keys**

Create a `.env` file:

```bash
# Required: OpenAI for LLM content generation
OPENAI_API_KEY=your_openai_key_here

# Required: Gemini for image generation
GEMINI_API_KEY=your_gemini_key_here
```

**Note**: Both API keys are required for full functionality. Without them:
- No LLM content transformation
- No image generation
- Basic markdown-to-PDF conversion only

### **3. Run the Workflow**

**Simplest - Process entire folder (RECOMMENDED):**
```bash
make process-folder FOLDER=llm-architectures
```

This will:
- ✅ Process all files in `backend/data/input/llm-architectures/`
- ✅ Generate both PDF and PPTX
- ✅ Use OpenAI for content transformation
- ✅ Use Gemini for image generation

**Alternative - Single file:**
```bash
bash run.sh backend/data/input/sample/test-blog-article.md
```

### **4. Check the Output**

```bash
ls -lh backend/data/output/

# You should see:
# - llm-architectures.pdf
# - llm-architectures.pptx
# - images/ (generated images)
```

---

## 📖 Makefile Commands

All automation ready! Just type `make <command>`.

### ⚡ Most Used Commands

```bash
# 1. Process a folder (generates images)
make process-folder FOLDER=llm-architectures

# 2. Process all folders in backend/data/input/
make batch-topics

# 3. List available folders
make list-topics

# 4. Show all commands
make help
```

### Quick Command Reference

| Command | What It Does | Output |
|---------|--------------|--------|
| `make setup-prismdocs` | Install dependencies | - |
| `make run-prismdocs` | Run main application | PDF/PPTX |
| `make process-folder FOLDER=<name>` | Process folder | PDF + PPTX |
| `make batch-topics` | Process all folders | Multiple PDFs + PPTXs |
| `make list-topics` | List available folders | List |
| `make test-prismdocs` | Run tests | Test results |
| `make lint-prismdocs` | Format + lint code | - |
| `make clean-prismdocs` | Clean outputs | - |
| `make help` | Show all commands | Command list |

### Common Scenarios

**First Time Setup:**
```bash
make setup-prismdocs                     # Install dependencies
make process-folder FOLDER=llm-architectures  # Generate everything
```

**Add New Topic:**
```bash
mkdir backend/data/input/new-topic
cp files... backend/data/input/new-topic/
make process-folder FOLDER=new-topic
```

**Process Everything:**
```bash
make batch-topics                     # Process all folders
```

**Maintenance:**
```bash
make clean-prismdocs   # Clean all generated files
make test-prismdocs    # Run tests
make lint-prismdocs    # Format and lint
```

---

## 📁 Folder-Based Processing

Process entire folders as topics - combine multiple files into one PDF/PPTX per topic.

### How It Works

```
INPUT (folder):
backend/data/input/llm-architectures/
├── slides.pdf        (File 1)
└── transcript.txt    (File 2)

PROCESSING:
1. Parse slides.pdf → extract content
2. Parse transcript.txt → extract content
3. LLM merges both → cohesive document
4. Generate images for sections
5. Create outputs

OUTPUT:
backend/data/output/
├── llm-architectures.pdf   (Combined from both files)
├── llm-architectures.pptx  (Combined from both files)
└── images/                 (Generated images)
```

### Process Your Folder

```bash
# Process llm-architectures folder
make process-folder FOLDER=llm-architectures
```

**What it does:**
1. ✅ Processes all files in the folder
2. ✅ Merges them intelligently with LLM
3. ✅ Generates images automatically
4. ✅ Creates **ONE** PDF: `backend/data/output/llm-architectures.pdf`
5. ✅ Creates **ONE** PPTX: `backend/data/output/llm-architectures.pptx`

### Adding More Topics

**1. Create New Topic Folder:**
```bash
mkdir backend/data/input/machine-learning
```

**2. Add Files:**
```bash
# Add any supported files
cp intro.pdf backend/data/input/machine-learning/
cp advanced.md backend/data/input/machine-learning/
cp notes.txt backend/data/input/machine-learning/
```

**3. Process:**
```bash
make process-folder FOLDER=machine-learning
```

**4. Get Combined Output:**
```
backend/data/output/
├── machine-learning.pdf   (All files combined)
└── machine-learning.pptx  (All files combined)
```

### Batch Process All Topics

Process **all folders** in `backend/data/input/` at once:

```bash
make batch-topics
```

**Example with 3 topics:**
```
backend/data/input/
├── llm-architectures/     → llm-architectures.pdf + .pptx
├── machine-learning/      → machine-learning.pdf + .pptx
└── python-basics/         → python-basics.pdf + .pptx

Result:
✅ 3 PDFs generated
✅ 3 PPTXs generated
✅ All in one run!
```

### Supported File Types

Your folder can contain any mix of:

| Type | Extensions | Example |
|------|------------|---------|
| PDF | `.pdf` | slides.pdf |
| Word | `.docx` | notes.docx |
| PowerPoint | `.pptx` | presentation.pptx |
| Markdown | `.md`, `.markdown` | readme.md |
| Text | `.txt` | transcript.txt |

**All files in the folder are merged together!**

---

## 🐳 Docker Deployment

```bash
# Run backend + frontend together
docker-compose up --build
```

Backend API image (for deployments like Render):
```bash
docker build -t prismdocs-backend:latest -f backend/Dockerfile backend
docker run --rm \
  -p 8000:8000 \
  -e PORT=8000 \
  -v $(pwd)/backend/data:/app/data \
  prismdocs-backend:latest
```

---

## ✨ Key Features

1. ✅ **Python-First Backend** - Core generation runs in FastAPI
2. ✅ **OpenAI Integration** - GPT-4o for content transformation
3. ✅ **Gemini Images** - High-quality image generation
4. ✅ **Advanced Parsing** - MarkItDown + fallback parsers
5. ✅ **Folder Processing** - Process multiple files at once with intelligent merging
6. ✅ **Clean Architecture** - Domain/Application/Infrastructure separation
7. ✅ **LangGraph Workflow** - State machine with retry logic
8. ✅ **Environment Config** - .env file support for API keys
9. ✅ **Docker Ready** - Containerized for portability
10. ✅ **Production Ready** - Comprehensive error handling, logging, validation

---

## 🎯 Project Structure

```
backend/
├── config/settings.yaml         # Backend configuration
├── data/
│   ├── input/                    # Input files and folders
│   └── output/                   # Generated PDFs and PPTXs
└── doc_generator/                # Core generator package
frontend/
├── src/                          # Next.js UI
└── public/
scripts/                          # CLI helpers
tests/api/                        # API tests
docker-compose.yml                # Backend + frontend
Makefile                          # Automation commands
```

---

## 📚 Documentation

- **Quickstart.md** (this file): Quick start guide
- **README.md**: Complete documentation
- **PROCESS_FLOW.md**: Visual process flow diagrams (see how everything works!)
- **docs/README.md**: Documentation index
- **docs/claude-code/**: Architecture and setup notes
- **docs/project/**: Project references and assets
- **docs/plans/**: Planning docs

---

## 🔧 Configuration

### Settings File

Edit `backend/config/settings.yaml` to customize:

```yaml
# LLM settings
llm:
  model: "gpt-4o-mini"
  use_claude_for_visuals: false  # Disabled (using Gemini)

# Image generation (Gemini)
image_generation:
  default_provider: "gemini"
  gemini_model: "gemini-3-pro-image-preview"
  enable_decorative_headers: true
  enable_infographics: true
```

### Environment Variables

Override settings with environment variables using `DOC_GENERATOR_` prefix:

```bash
export DOC_GENERATOR_LLM__MODEL="gpt-4o"
export DOC_GENERATOR_PDF__PAGE_SIZE="a4"
```

---

## 🎉 Ready to Use!

Your document generator is fully implemented! Start with:

```bash
# Process the LLM architectures folder
make process-folder FOLDER=llm-architectures

# Or process all folders
make batch-topics

# Or a single file
bash run.sh backend/data/input/sample/test-blog-article.md
```

---

## 🐛 Troubleshooting

### Common Issues

**1. API Key Errors**
```bash
# Check your .env file
cat .env

# Should contain:
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...
```

**2. Module Not Found**
```bash
# Reinstall dependencies
make setup-prismdocs
```

**3. Permission Errors**
```bash
# Make scripts executable
chmod +x run.sh
```

**4. No Output Generated**
```bash
# Check logs for errors
make run-prismdocs INPUT=your-file.pdf OUTPUT=pdf

# Enable verbose logging
export DOC_GENERATOR_LOGGING__LEVEL="DEBUG"
```

### Get Help

```bash
# Show all available commands
make help

# List your topic folders
make list-topics

# Test your setup
make test-prismdocs
```

---

## 💡 Pro Tips

1. **Use folder processing** for multiple related files
2. **Keep images** in `backend/data/output/images/` between runs
3. **Check `make help`** for all available commands
4. **Use `make lint-prismdocs`** before committing code
5. **Run `make test-prismdocs`** to verify everything works

---

## 📞 Support

For issues or questions:
1. Check the documentation in `docs/README.md`
2. Review the `README.md` for detailed information
3. Check logs in the output for error messages
4. Use `make help` for command reference

---

## Summary

✅ **Install:** `make setup-prismdocs`  
✅ **Configure:** Add API keys to `.env`  
✅ **Process folder:** `make process-folder FOLDER=<name>`  
✅ **Process all:** `make batch-topics`  
✅ **Get help:** `make help`  

**Ready to go!** 🚀
