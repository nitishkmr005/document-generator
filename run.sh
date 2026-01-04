#!/bin/bash
# Helper script to run document generator with proper environment variables

# Set Cairo library path for macOS
export DYLD_LIBRARY_PATH="/opt/homebrew/opt/cairo/lib:$DYLD_LIBRARY_PATH"

# Activate virtual environment
source .venv/bin/activate

# Run the generator with all arguments passed through
python scripts/run_generator.py "$@"
