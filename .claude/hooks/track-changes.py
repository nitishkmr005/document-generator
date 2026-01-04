#!/usr/bin/env python3
"""
PostToolUse hook: Track major logic changes for README update.

Monitors edits to core logic files (domain/, application/, infrastructure/)
and records them in a temp file for the Stop hook to process.
"""
import json
import sys
import os
from pathlib import Path
from datetime import datetime

# Directories containing major logic
LOGIC_DIRS = [
    "src/doc_generator/domain/",
    "src/doc_generator/application/",
    "src/doc_generator/infrastructure/",
]

# File extensions to track
TRACKED_EXTENSIONS = {".py"}

# Temp file to store tracked changes
CHANGES_FILE = "/tmp/claude_readme_changes.json"


def is_major_logic_file(file_path: str) -> bool:
    """Check if file is in a major logic directory."""
    # Normalize path
    normalized = file_path.replace("\\", "/")

    # Check extension
    if not any(normalized.endswith(ext) for ext in TRACKED_EXTENSIONS):
        return False

    # Skip test files and __pycache__
    if "__pycache__" in normalized or "test_" in normalized:
        return False

    # Check if in logic directories
    return any(logic_dir in normalized for logic_dir in LOGIC_DIRS)


def load_changes() -> dict:
    """Load existing changes from temp file."""
    try:
        if os.path.exists(CHANGES_FILE):
            with open(CHANGES_FILE, "r") as f:
                return json.load(f)
    except (json.JSONDecodeError, IOError):
        pass
    return {"files": [], "session_id": None, "timestamp": None}


def save_changes(changes: dict) -> None:
    """Save changes to temp file."""
    with open(CHANGES_FILE, "w") as f:
        json.dump(changes, f, indent=2)


def main():
    try:
        # Read hook input from stdin
        hook_input = json.load(sys.stdin)

        tool_name = hook_input.get("tool_name", "")
        tool_input = hook_input.get("tool_input", {})
        session_id = hook_input.get("session_id", "")

        # Get file path from tool input
        file_path = tool_input.get("file_path", "")

        if not file_path:
            sys.exit(0)

        # Check if this is a major logic file
        if not is_major_logic_file(file_path):
            sys.exit(0)

        # Load and update changes
        changes = load_changes()

        # Reset if new session
        if changes.get("session_id") != session_id:
            changes = {"files": [], "session_id": session_id, "timestamp": None}

        # Add file if not already tracked
        relative_path = file_path.split("src/")[-1] if "src/" in file_path else file_path
        if relative_path not in changes["files"]:
            changes["files"].append(relative_path)
            changes["timestamp"] = datetime.now().isoformat()

        save_changes(changes)

        # Output for verbose mode
        print(f"Tracked change: {relative_path}")
        sys.exit(0)

    except Exception as e:
        # Non-blocking - don't fail the edit
        sys.exit(0)


if __name__ == "__main__":
    main()
