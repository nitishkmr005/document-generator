#!/usr/bin/env python3
"""
CLI entry point for document generator.

Usage:
    python scripts/run_generator.py input.md --output pdf
    python scripts/run_generator.py input.pdf --output pptx
    python scripts/run_generator.py https://example.com/article --output pdf
"""

import sys
from pathlib import Path
import argparse

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from doc_generator.application.graph_workflow import run_workflow
from doc_generator.infrastructure.logging_config import setup_logging


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="Generate PDF or PPTX from various document sources",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Markdown to PDF
  python scripts/run_generator.py src/data/article.md --output pdf

  # Web article to PPTX
  python scripts/run_generator.py https://example.com/article --output pptx

  # PDF to PPTX (extract and convert)
  python scripts/run_generator.py src/data/document.pdf --output pptx

  # With verbose logging
  python scripts/run_generator.py input.md --output pdf --verbose
        """
    )

    parser.add_argument(
        "input",
        help="Input file path or URL"
    )

    parser.add_argument(
        "--output", "-o",
        choices=["pdf", "pptx"],
        default="pdf",
        help="Output format (default: pdf)"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging (DEBUG level)"
    )

    parser.add_argument(
        "--log-file",
        help="Path to log file (optional)"
    )

    args = parser.parse_args()

    # Setup logging
    setup_logging(verbose=args.verbose, log_file=args.log_file)

    # Run workflow
    result = run_workflow(
        input_path=args.input,
        output_format=args.output
    )

    # Check for errors
    if result["errors"]:
        print(f"\n❌ Generation failed with {len(result['errors'])} error(s):", file=sys.stderr)
        for error in result["errors"]:
            print(f"  - {error}", file=sys.stderr)
        sys.exit(1)

    # Success
    output_path = result.get("output_path", "")
    if output_path:
        print(f"\n✅ Generated successfully: {output_path}")
        print(f"   Format: {args.output.upper()}")
        print(f"   Title: {result['metadata'].get('title', 'N/A')}")

        # Show file size
        file_path = Path(output_path)
        if file_path.exists():
            file_size = file_path.stat().st_size
            if file_size > 1024 * 1024:
                size_str = f"{file_size / (1024 * 1024):.2f} MB"
            elif file_size > 1024:
                size_str = f"{file_size / 1024:.2f} KB"
            else:
                size_str = f"{file_size} bytes"
            print(f"   Size: {size_str}")
    else:
        print("\n⚠️  Workflow completed but no output path was set", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
