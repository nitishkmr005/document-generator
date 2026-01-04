#!/usr/bin/env python3
"""
Visualize the LangGraph workflow diagram.

Generates a PNG image of the graph structure.
"""

from src.doc_generator.application.graph_workflow import build_workflow


def main():
    """Generate and save graph visualization."""
    # Build workflow
    workflow = build_workflow()

    # Get the graph as mermaid syntax
    try:
        mermaid_graph = workflow.get_graph().draw_mermaid()
        print("Mermaid Graph Syntax:")
        print("=" * 60)
        print(mermaid_graph)
        print("=" * 60)

        # Save to file
        with open("langgraph-mermaid.txt", "w") as f:
            f.write(mermaid_graph)
        print("\n✅ Saved mermaid syntax to: langgraph-mermaid.txt")
        print("📊 Paste this into https://mermaid.live for visualization")

    except Exception as e:
        print(f"❌ Could not generate mermaid: {e}")

    # Try to generate PNG (requires graphviz)
    try:
        from IPython.display import Image
        png_data = workflow.get_graph().draw_mermaid_png()

        with open("langgraph-diagram.png", "wb") as f:
            f.write(png_data)
        print("\n✅ Saved PNG diagram to: langgraph-diagram.png")

    except ImportError:
        print("\n⚠️  PNG generation requires: pip install 'pygraphviz' or 'grandalf'")
    except Exception as e:
        print(f"\n⚠️  PNG generation failed: {e}")


if __name__ == "__main__":
    main()
