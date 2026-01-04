#!/usr/bin/env python3
"""
Stop hook: Check if README needs updating after major changes.

Reads tracked changes from temp file and prompts Claude to update
README.md if significant logic files were modified.
"""
import json
import sys
import os

CHANGES_FILE = "/tmp/claude_readme_changes.json"
MIN_FILES_FOR_UPDATE = 1  # Minimum changed files to trigger update


def load_changes() -> dict:
    """Load tracked changes from temp file."""
    try:
        if os.path.exists(CHANGES_FILE):
            with open(CHANGES_FILE, "r") as f:
                return json.load(f)
    except (json.JSONDecodeError, IOError):
        pass
    return {"files": [], "session_id": None}


def clear_changes() -> None:
    """Clear the changes file after processing."""
    try:
        if os.path.exists(CHANGES_FILE):
            os.remove(CHANGES_FILE)
    except IOError:
        pass


def main():
    try:
        # Read hook input from stdin
        hook_input = json.load(sys.stdin)
        session_id = hook_input.get("session_id", "")

        # Load tracked changes
        changes = load_changes()

        # Check if this is the same session and has enough changes
        if changes.get("session_id") != session_id:
            sys.exit(0)

        changed_files = changes.get("files", [])

        if len(changed_files) < MIN_FILES_FOR_UPDATE:
            sys.exit(0)

        # Clear changes file (we're about to handle them)
        clear_changes()

        # Build the file list for the prompt
        files_list = "\n".join(f"  - {f}" for f in changed_files)

        # Return decision to continue with README update instruction
        result = {
            "decision": "continue",
            "reason": f"""Major logic changes detected in {len(changed_files)} file(s):
{files_list}

Please update README.md to reflect these changes:
1. Review what was changed in these files
2. Update relevant sections (features, architecture, usage) if needed
3. Keep the update concise and focused on user-facing changes"""
        }

        print(json.dumps(result))
        sys.exit(0)

    except Exception as e:
        # Non-blocking error
        sys.exit(0)


if __name__ == "__main__":
    main()
