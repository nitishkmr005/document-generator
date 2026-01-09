# Document Generator - Quick Start Guide

## 🎉 Implementation Complete!

A **production-ready LangGraph-based document generator** with 100% Python implementation.

## 🚀 Quick Start

### **1. Install Dependencies**

```bash
# Using make
make setup-docgen

# Or manually
uv pip install -e ".[dev]"
```

### **2. Configure API Keys (Optional)**

Create a `.env` file for LLM-enhanced features:

```bash
# Claude API (Recommended)
ANTHROPIC_API_KEY=your_key_here

# Or OpenAI API
OPENAI_API_KEY=your_key_here
```

**Note**: API keys are optional. Without them, the system uses basic transformation.

### **3. Run the Workflow**

**Simplest - Process entire folder with one command:**
```bash
make run-llm-architectures
```

This will:
- ✅ Process all files in `src/data/llm-architectures/`
- ✅ Generate both PDF and PPTX
- ✅ Use Claude/OpenAI for enhanced content (if configured)

**Alternative - Single files:**
```bash
# Single file (both formats)
bash run.sh src/data/sample/test-blog-article.md

# Or using make (one format)
make run-docgen INPUT=src/data/sample/test-blog-article.md OUTPUT=pdf
```

### **4. Check the Output**

```bash
ls -lh src/output/

# You should see:
# - llm-architectures.pdf
# - llm-architectures.pptx
```

## 🐳 Docker Deployment

```bash
# Build Docker image
make docker-build

# Run with Docker
make docker-run INPUT=src/data/sample.md OUTPUT=pdf

# Check output
ls -lh src/output/
```

## ✨ Key Features

1. ✅ **100% Pure Python** - No Node.js dependencies
2. ✅ **LLM Integration** - Claude & OpenAI support for enhanced content
3. ✅ **Advanced Parsing** - Docling (OCR, tables) + MarkItDown
4. ✅ **Folder Processing** - Process multiple files at once with intelligent merging
5. ✅ **Clean Architecture** - Domain/Application/Infrastructure separation
6. ✅ **LangGraph Workflow** - State machine with retry logic
7. ✅ **Environment Config** - .env file support for API keys
8. ✅ **Docker Ready** - Containerized for portability
9. ✅ **Production Ready** - Comprehensive error handling, logging, validation

## 📖 Documentation

- **Quickstart.md** (this file): Quick start guide
- **README.md**: Complete documentation
- **ENV_SETUP.md**: Environment configuration guide
- **docs/**: Additional documentation

## 🎉 Ready to Use!

Your document generator is fully implemented! Start with:
```bash
# Process the LLM architectures folder
make run-llm-architectures

# Or a single file
bash run.sh src/data/sample/test-blog-article.md
```
