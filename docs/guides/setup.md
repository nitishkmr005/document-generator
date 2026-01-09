# Python Project Setup Guide

A systematic approach to setting up any Python project, based on learnings from real-world debugging sessions.

## Table of Contents
- [Prerequisites Check](#prerequisites-check)
- [Setup Workflow](#setup-workflow)
- [Common Pitfalls](#common-pitfalls)
- [System Dependencies](#system-dependencies)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

## Prerequisites Check

Before attempting installation, verify these prerequisites:

### 1. Python Version
```bash
python3 --version
```
- Check against `requires-python` in `pyproject.toml` or README
- Ensure version is compatible (not just minimum)

### 2. Package Manager
```bash
# For uv (modern, fast)
which uv

# For pip (standard)
which pip

# For poetry
which poetry
```

### 3. Project Documentation
Read in parallel to gather complete context:
```bash
cat README.md
cat QUICKSTART.md  # if exists
cat pyproject.toml  # or requirements.txt
cat CONTRIBUTING.md  # if exists
```

### 4. Test Data/Fixtures
```bash
# Check if sample data exists for testing
ls -la data/ tests/fixtures/ examples/ samples/
```

## Setup Workflow

### Step 1: Create Virtual Environment

```bash
# Using uv (recommended for speed)
uv venv

# Using standard venv
python3 -m venv .venv

# Using conda
conda create -n myproject python=3.11

# Verify creation
ls -la .venv/
```

### Step 2: Scan for System Dependencies

**Before installing Python packages**, check for libraries that need system-level dependencies:

```bash
# Search for common culprits in dependency files
grep -E "(opencv|cairo|pillow|matplotlib|psycopg2|mysqlclient|lxml)" pyproject.toml requirements.txt
```

**Known system dependency triggers:**

| Python Package | System Dependency Needed |
|---------------|-------------------------|
| `cairosvg`, `cairocffi` | cairo (graphics library) |
| `opencv-python` | opencv libraries |
| `pillow` (sometimes) | image libraries (libjpeg, zlib) |
| `psycopg2` | PostgreSQL dev libraries |
| `mysqlclient` | MySQL dev libraries |
| `lxml` | libxml2, libxslt |
| `numpy`, `scipy` | BLAS, LAPACK (usually bundled) |
| `pyaudio` | portaudio |

### Step 3: Install System Dependencies (if needed)

**macOS (Homebrew):**
```bash
# Graphics libraries
brew install cairo
brew install opencv

# Database libraries
brew install postgresql
brew install mysql

# Audio
brew install portaudio

# Check installation path
brew --prefix cairo  # Note this for later
```

**Linux (Ubuntu/Debian):**
```bash
# Graphics libraries
sudo apt-get update
sudo apt-get install libcairo2-dev
sudo apt-get install libopencv-dev

# Database libraries
sudo apt-get install libpq-dev
sudo apt-get install libmysqlclient-dev

# XML processing
sudo apt-get install libxml2-dev libxslt1-dev

# Audio
sudo apt-get install portaudio19-dev
```

**Linux (RHEL/CentOS/Fedora):**
```bash
# Graphics libraries
sudo yum install cairo-devel
sudo yum install opencv-devel

# Database libraries
sudo yum install postgresql-devel
sudo yum install mysql-devel
```

### Step 4: Check Dependency Version Constraints

Review `pyproject.toml` or `requirements.txt` for overly strict version pins:

```toml
# ❌ Fragile - exact version may not be available
"package==1.2.3"

# ✅ Better - flexible within major version
"package>=1.2.0,<2.0.0"

# ✅ Also good - minimum version only
"package>=1.2.0"

# ✅ For critical deps - pin to minor version
"package>=1.2.0,<1.3.0"
```

**When to relax constraints:**
- Non-critical dependencies (dev tools, utilities)
- Libraries with stable APIs (requests, click, etc.)
- No known breaking changes in version range

**When to keep strict pins:**
- Critical business logic dependencies
- Known breaking changes between versions
- Reproducible builds required (production, research)
- Team-wide consistency needed

### Step 5: Install Dependencies

```bash
# Activate virtual environment first
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate  # Windows

# Install with development dependencies
uv pip install -e ".[dev]"  # if using pyproject.toml with extras
# or
pip install -e ".[dev]"
# or
pip install -r requirements.txt
# or
poetry install
```

**Watch for common errors:**
- `No solution found` → version conflict, relax constraints
- `No matching distribution` → package/version doesn't exist
- `Building wheel failed` → missing system dependencies
- `error: legacy-install-failure` → compilation issues, check system libs

### Step 6: Create Environment Setup Script

If system libraries or environment variables are needed:

**For macOS:**
```bash
cat > run.sh << 'EOF'
#!/bin/bash
# Project execution wrapper with environment setup

# Set system library paths (adjust paths as needed)
export DYLD_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_LIBRARY_PATH"

# Activate virtual environment
source .venv/bin/activate

# Run command with all arguments passed through
"$@"
EOF

chmod +x run.sh
```

**For Linux:**
```bash
cat > run.sh << 'EOF'
#!/bin/bash
# Project execution wrapper with environment setup

# Set system library paths (adjust paths as needed)
export LD_LIBRARY_PATH="/usr/local/lib:/usr/lib:$LD_LIBRARY_PATH"

# Activate virtual environment
source .venv/bin/activate

# Run command with all arguments passed through
"$@"
EOF

chmod +x run.sh
```

**Usage:**
```bash
./run.sh python script.py arg1 arg2
./run.sh pytest tests/
./run.sh python -m myapp
```

### Step 7: Validate Installation

Test the installation thoroughly:

```bash
# 1. Check Python can import main modules
python -c "import mypackage; print(mypackage.__version__)"

# 2. Run test suite if available
pytest tests/ -v
# or
python -m unittest discover
# or
make test

# 3. Try example commands from README
python examples/quickstart.py
# or
python -m myapp --help

# 4. Check installed packages
pip list
pip show mypackage
```

## Common Pitfalls

### 1. Dependency Version Conflicts

**Problem:** `No solution found when resolving dependencies`

**Solutions:**
1. Relax version constraints in `pyproject.toml` or `requirements.txt`
2. Update pip/uv: `pip install --upgrade pip`
3. Check for conflicting requirements:
   ```bash
   pip check
   pipdeptree  # install with: pip install pipdeptree
   ```
4. Create fresh venv and retry
5. Use `pip install --no-deps package` for specific packages (advanced)

### 2. System Libraries Not Found

**Problem:** `OSError: no library called "X" was found` or `ImportError: cannot load library`

**Solutions:**
1. Install system package:
   ```bash
   # macOS
   brew install library-name
   brew --prefix library-name  # get install path

   # Linux
   sudo apt-get install library-name-dev
   ldconfig -p | grep library-name  # verify
   ```
2. Set library path:
   ```bash
   # macOS
   export DYLD_LIBRARY_PATH=/path/to/libs:$DYLD_LIBRARY_PATH

   # Linux
   export LD_LIBRARY_PATH=/path/to/libs:$LD_LIBRARY_PATH
   ```
3. Create wrapper script (see Step 6)
4. Add to shell profile for persistence:
   ```bash
   echo 'export DYLD_LIBRARY_PATH=/path/to/libs:$DYLD_LIBRARY_PATH' >> ~/.zshrc
   ```

### 3. Python Version Mismatch

**Problem:** Project requires Python 3.11 but you have 3.9

**Solutions:**
1. Install correct Python version:
   ```bash
   # macOS
   brew install python@3.11

   # Linux
   sudo apt-get install python3.11 python3.11-venv

   # Or use pyenv (recommended)
   pyenv install 3.11.7
   pyenv local 3.11.7
   ```
2. Create venv with specific version:
   ```bash
   python3.11 -m venv .venv
   # or
   /usr/local/bin/python3.11 -m venv .venv
   ```

### 4. Import Errors After Installation

**Problem:** `ModuleNotFoundError` despite successful installation

**Solutions:**
1. Verify venv is activated:
   ```bash
   which python  # should show .venv/bin/python
   echo $VIRTUAL_ENV  # should show path to .venv
   ```
2. Reinstall in editable mode:
   ```bash
   pip install -e .
   ```
3. Check Python path:
   ```bash
   python -c "import sys; print('\n'.join(sys.path))"
   ```
4. Clear cache and reinstall:
   ```bash
   rm -rf **/__pycache__ **/*.pyc
   pip uninstall mypackage
   pip install -e .
   ```

### 5. Compilation Errors During Install

**Problem:** `error: command 'gcc' failed` or `Microsoft Visual C++ required`

**Solutions:**
1. **macOS:** Install Xcode Command Line Tools:
   ```bash
   xcode-select --install
   ```
2. **Linux:** Install build essentials:
   ```bash
   sudo apt-get install build-essential python3-dev
   ```
3. **Windows:** Install Microsoft C++ Build Tools
4. Use pre-built wheels when available:
   ```bash
   pip install --only-binary :all: package-name
   ```

## System Dependencies Reference

### Graphics & Document Processing

| Python Package | System Dependency | macOS Install | Linux Install |
|---------------|-------------------|---------------|---------------|
| `cairosvg`, `cairocffi` | Cairo | `brew install cairo` | `apt-get install libcairo2-dev` |
| `opencv-python` | OpenCV | `brew install opencv` | `apt-get install libopencv-dev` |
| `pillow` | Image libs | Usually works | `apt-get install libjpeg-dev zlib1g-dev` |
| `matplotlib` | Usually works | May need pkg-config | `apt-get install pkg-config` |
| `reportlab` | Usually works | Sometimes needs freetype | `apt-get install libfreetype6-dev` |

### Database Connectors

| Python Package | System Dependency | macOS Install | Linux Install |
|---------------|-------------------|---------------|---------------|
| `psycopg2` | PostgreSQL dev | `brew install postgresql` | `apt-get install libpq-dev` |
| `mysqlclient` | MySQL dev | `brew install mysql` | `apt-get install libmysqlclient-dev` |
| `cx_Oracle` | Oracle Client | Download from Oracle | Download from Oracle |
| `pyodbc` | UnixODBC | `brew install unixodbc` | `apt-get install unixodbc-dev` |

### Audio/Video

| Python Package | System Dependency | macOS Install | Linux Install |
|---------------|-------------------|---------------|---------------|
| `pyaudio` | PortAudio | `brew install portaudio` | `apt-get install portaudio19-dev` |
| `pydub` | ffmpeg | `brew install ffmpeg` | `apt-get install ffmpeg` |
| `soundfile` | libsndfile | `brew install libsndfile` | `apt-get install libsndfile1` |

### Scientific Computing

| Python Package | System Dependency | Notes |
|---------------|-------------------|-------|
| `numpy`, `scipy` | BLAS, LAPACK | Usually bundled in wheels |
| `torch` | Usually self-contained | May need CUDA for GPU |
| `tensorflow` | Usually self-contained | May need CUDA for GPU |
| `h5py` | HDF5 library | Sometimes needed for compilation |

## Troubleshooting

### Debug Workflow

1. **Verify virtual environment:**
   ```bash
   which python
   # Output should be: /path/to/project/.venv/bin/python

   echo $VIRTUAL_ENV
   # Output should be: /path/to/project/.venv
   ```

2. **List installed packages:**
   ```bash
   pip list
   pip show package-name
   pip check  # find conflicts
   ```

3. **Test imports interactively:**
   ```bash
   python -c "import problematic_module"
   python -c "import problematic_module; print(problematic_module.__version__)"
   python -c "import problematic_module; print(problematic_module.__file__)"
   ```

4. **Check system libraries (advanced):**
   ```bash
   # macOS - check what libraries a .so file needs
   otool -L .venv/lib/python*/site-packages/*/*.so

   # Linux - check library dependencies
   ldd .venv/lib/python*/site-packages/*/*.so
   ```

5. **Verbose installation for debugging:**
   ```bash
   pip install package-name -v
   # or
   pip install package-name --verbose --no-cache-dir
   ```

6. **Check environment variables:**
   ```bash
   # Show all Python-related env vars
   env | grep -i python

   # Show library paths
   echo $DYLD_LIBRARY_PATH  # macOS
   echo $LD_LIBRARY_PATH    # Linux
   echo $PATH
   ```

## Best Practices

### 1. Dependency Management

✅ **DO:**
- Use flexible constraints for non-critical deps: `package>=1.0.0`
- Pin to minor version for stability: `package>=1.2.0,<1.3.0`
- Document system dependencies in README
- Test on clean environment regularly
- Use `pip-compile` or Poetry for lock files
- Keep requirements up to date (Dependabot, Renovate)

❌ **DON'T:**
- Pin everything to exact versions unnecessarily
- Mix pip and conda in same environment
- Install to system Python
- Commit `.venv/` directory to git
- Use `sudo pip install` (use venv instead)

### 2. Environment Isolation

✅ **DO:**
- Always use virtual environments
- One venv per project
- Activate before running anything
- Add `.venv/`, `venv/`, `.conda/` to `.gitignore`
- Document activation in README

❌ **DON'T:**
- Share virtual environments across projects
- Commit virtual environment to version control
- Install packages without venv activated
- Mix Python versions in same venv

### 3. Documentation

**README.md should include:**
- Python version requirements
- System dependencies (OS-specific)
- Installation commands (copy-pasteable)
- Quick start examples
- Common troubleshooting
- Environment variables needed

**Example README section:**
````markdown
## Installation

### Prerequisites

- Python 3.11 or higher
- System dependencies:
  - **macOS:** `brew install cairo`
  - **Linux:** `sudo apt-get install libcairo2-dev`

### Setup

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Verify installation
python -c "import myproject; print('Success!')"
```

### Quick Start

```bash
python script.py input.txt --output result.txt
```
````

### 4. Helper Scripts

Create automation scripts for common tasks:

**setup.sh:**
```bash
#!/bin/bash
set -e  # Exit on error

echo "Setting up project..."

# Check Python version
python3 --version | grep -q "3.1[1-9]" || {
    echo "Error: Python 3.11+ required"
    exit 1
}

# Create venv
python3 -m venv .venv
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -e ".[dev]"

echo "Setup complete! Activate with: source .venv/bin/activate"
```

**test.sh:**
```bash
#!/bin/bash
source .venv/bin/activate
pytest tests/ -v --cov --cov-report=html
```

### 5. Makefile Automation

```makefile
.PHONY: help setup install test lint clean

help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup:  ## Create virtual environment
	python3 -m venv .venv
	@echo "Run 'source .venv/bin/activate' to activate"

install:  ## Install dependencies
	pip install --upgrade pip
	pip install -e ".[dev]"

test:  ## Run tests
	pytest tests/ -v --cov

lint:  ## Run linters
	ruff check .
	mypy .

clean:  ## Clean generated files
	rm -rf .venv __pycache__ **/__pycache__ *.pyc **/*.pyc
	rm -rf .pytest_cache .coverage htmlcov
	rm -rf dist build *.egg-info
```

### 6. Docker for Portability

For complex system dependencies, consider Docker:

```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libcairo2-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY pyproject.toml ./
RUN pip install --no-cache-dir -e ".[dev]"

# Copy application code
COPY . .

# Run application
CMD ["python", "main.py"]
```

## Quick Reference Checklist

Use this checklist for any Python project setup:

```
☐ Check Python version compatibility (python3 --version)
☐ Read README, QUICKSTART, pyproject.toml
☐ Scan dependencies for system library requirements
☐ Install system libraries (cairo, opencv, postgresql, etc.)
☐ Create virtual environment (python3 -m venv .venv)
☐ Activate virtual environment (source .venv/bin/activate)
☐ Review dependency version constraints (relax if needed)
☐ Install Python dependencies (pip install -e ".[dev]")
☐ Create helper script if environment variables needed
☐ Test installation (python -c "import mypackage")
☐ Run test suite (pytest tests/)
☐ Try example commands from README
☐ Document any additional setup steps discovered
☐ Add .venv to .gitignore
☐ Commit setup scripts (setup.sh, run.sh) to repo
```

## Additional Resources

- **Virtual Environments:** https://docs.python.org/3/library/venv.html
- **pip Documentation:** https://pip.pypa.io/
- **uv (modern pip replacement):** https://github.com/astral-sh/uv
- **Poetry (dependency management):** https://python-poetry.org/
- **pyenv (Python version management):** https://github.com/pyenv/pyenv
- **Python Packaging Guide:** https://packaging.python.org/
- **Troubleshooting Guide:** https://packaging.python.org/guides/installing-scientific-packages/

---

**Golden Rule:** Fail fast and iterate. Don't try to fix everything perfectly before running - get to a working execution quickly to reveal real issues.
