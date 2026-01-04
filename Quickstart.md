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

### **2. Test the System**

```bash
# Convert the sample markdown to PDF
make run-docgen INPUT=src/data/sample.md OUTPUT=pdf

# Or directly
python scripts/run_generator.py src/data/sample.md --output pdf

# Check the output
ls -lh src/output/
```

### **3. Try Different Formats**

```bash
# Markdown to PPTX
python scripts/run_generator.py src/data/sample.md --output pptx

# Your README to PDF
python scripts/run_generator.py README.md --output pdf

# Web article to PDF
python scripts/run_generator.py https://example.com/article --output pdf
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
2. ✅ **Advanced Parsing** - Docling (OCR, tables) + MarkItDown
3. ✅ **Clean Architecture** - Domain/Application/Infrastructure separation
4. ✅ **LangGraph Workflow** - State machine with retry logic
5. ✅ **Docker Ready** - Containerized for portability
6. ✅ **Production Ready** - Comprehensive error handling, logging, validation

## 📖 Documentation

- **QUICKSTART.md** (this file): Quick start guide
- **DOC_GENERATOR_README.md**: Complete documentation

## 🎉 Ready to Use!

Your document generator is fully implemented! Start with:
```bash
make run-docgen INPUT=src/data/sample.md OUTPUT=pdf
```
