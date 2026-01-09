#!/usr/bin/env python3
"""
Generate high-quality LLM architecture SVG diagrams using Claude Sonnet 4.5.

This script creates professional architecture diagrams for:
1. Transformer Architecture (Encoder-Decoder)
2. Self-Attention Mechanism
3. Multi-Head Attention
4. Position Embeddings (Sinusoidal, RoPE, ALiBi)
5. Layer Normalization comparison
"""

import os
import sys
from pathlib import Path
from anthropic import Anthropic

# Output directory for SVGs
OUTPUT_DIR = Path("src/output/llm-architecture-diagrams")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Initialize Anthropic client
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Color palette for consistent styling
COLORS = {
    "primary": "#1E5D5A",      # Teal
    "secondary": "#2E86AB",    # Blue
    "accent": "#D76B38",       # Orange
    "highlight": "#A23B72",    # Magenta
    "success": "#5C946E",      # Green
    "background": "#F6F1E7",   # Paper
    "text": "#1C1C1C",         # Dark
    "muted": "#4A4A4A",        # Gray
}


def generate_svg_with_claude(prompt: str, filename: str) -> str:
    """Generate SVG using Claude Sonnet 4.5."""

    system_prompt = f"""You are an expert SVG diagram designer specializing in technical architecture diagrams.

Create clean, professional SVG diagrams with these requirements:
1. Use this color palette:
   - Primary (teal): {COLORS['primary']}
   - Secondary (blue): {COLORS['secondary']}
   - Accent (orange): {COLORS['accent']}
   - Highlight (magenta): {COLORS['highlight']}
   - Success (green): {COLORS['success']}
   - Background: {COLORS['background']}
   - Text: {COLORS['text']}

2. Design guidelines:
   - Use rounded rectangles for components (rx="8")
   - Add subtle drop shadows for depth
   - Use arrows with proper markers for connections
   - Include clear labels with readable font sizes (14-18px)
   - Canvas size: 900x600 for landscape, 600x800 for portrait
   - Add a subtle grid or background pattern for professionalism
   - Use gradients sparingly for modern look

3. Output ONLY valid SVG code, no markdown code blocks or explanations.
   Start with <svg and end with </svg>."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8000,
        messages=[{"role": "user", "content": prompt}],
        system=system_prompt
    )

    svg_content = response.content[0].text

    # Clean up response if needed
    if "```" in svg_content:
        # Extract SVG from markdown code block
        import re
        match = re.search(r'<svg[\s\S]*?</svg>', svg_content)
        if match:
            svg_content = match.group(0)

    # Save SVG
    output_path = OUTPUT_DIR / filename
    with open(output_path, 'w') as f:
        f.write(svg_content)

    print(f"Generated: {output_path}")
    return str(output_path)


def generate_transformer_architecture():
    """Generate complete Transformer architecture diagram."""
    prompt = """Create a detailed SVG diagram of the Transformer architecture showing:

1. Left side: ENCODER stack with:
   - Input Embeddings at bottom
   - Positional Encoding (added)
   - N× stacked layers containing:
     - Multi-Head Attention (with Add & Norm)
     - Feed Forward Network (with Add & Norm)
   - Label "Encoder" on the side

2. Right side: DECODER stack with:
   - Output Embeddings (shifted right) at bottom
   - Positional Encoding (added)
   - N× stacked layers containing:
     - Masked Multi-Head Attention (with Add & Norm)
     - Multi-Head Attention (cross-attention, with Add & Norm)
     - Feed Forward Network (with Add & Norm)
   - Label "Decoder" on the side

3. Top: Linear layer → Softmax → Output Probabilities

4. Show the cross-attention connection from encoder to decoder clearly

Use a clean, modern style with the color palette provided. Make it educational and clear.
Canvas size: 900x700."""

    return generate_svg_with_claude(prompt, "01_transformer_architecture.svg")


def generate_self_attention():
    """Generate Self-Attention mechanism diagram."""
    prompt = """Create an SVG diagram explaining the Self-Attention mechanism:

1. Show the flow from Input Embeddings to Output:
   - Input X (sequence of token embeddings)
   - Three parallel paths: W_Q, W_K, W_V (weight matrices)
   - Q (Query), K (Key), V (Value) matrices

2. Show the attention computation:
   - Q × K^T (matrix multiplication)
   - Scale by √d_k
   - Softmax (attention weights)
   - Multiply by V
   - Output

3. Include the formula: Attention(Q,K,V) = softmax(QK^T / √d_k) × V

4. Add visual representation of attention weights as a small heatmap matrix

5. Use arrows to show data flow direction

Make it clear and educational. Canvas size: 900x550."""

    return generate_svg_with_claude(prompt, "02_self_attention_mechanism.svg")


def generate_multi_head_attention():
    """Generate Multi-Head Attention diagram."""
    prompt = """Create an SVG diagram showing Multi-Head Attention:

1. Show input splitting into multiple heads (h=8 heads):
   - Single input vector at top
   - Split into 8 parallel attention heads
   - Each head has its own Q, K, V projections (smaller boxes)

2. For each head show:
   - Scaled Dot-Product Attention block

3. Show concatenation of all heads:
   - All 8 outputs coming together
   - Final linear projection W_O
   - Output

4. Include labels:
   - "Head 1", "Head 2", ... "Head h"
   - "Concat"
   - "Linear"

5. Show dimensions: d_model splits into h × d_k

Use different shades of the primary color for different heads.
Canvas size: 900x600."""

    return generate_svg_with_claude(prompt, "03_multi_head_attention.svg")


def generate_position_embeddings():
    """Generate Position Embeddings comparison diagram."""
    prompt = """Create an SVG diagram comparing different Position Embedding methods:

Layout as 4 panels (2x2 grid):

Panel 1 - "Learned Embeddings" (top-left):
- Show lookup table E_pos with positions 1, 2, 3, ... N
- Arrow to embedding vectors
- Note: "Limited to training sequence length"

Panel 2 - "Sinusoidal Embeddings" (top-right):
- Show sine/cosine wave patterns
- Formula: PE(pos,2i) = sin(pos/10000^(2i/d))
- Show wavelength varying with dimension
- Note: "Extends to any sequence length"

Panel 3 - "ALiBi" (bottom-left):
- Show attention matrix with bias
- Diagonal pattern showing distance penalty
- Formula: softmax(QK^T + m·distance)
- Note: "Linear bias based on distance"

Panel 4 - "RoPE" (bottom-right):
- Show rotation visualization in 2D plane
- Query and Key vectors being rotated
- Formula hint: R_θ rotation matrix
- Note: "Rotates Q and K by position angle"

Add a title "Position Embedding Methods" at top.
Canvas size: 900x700."""

    return generate_svg_with_claude(prompt, "04_position_embeddings.svg")


def generate_layer_normalization():
    """Generate Layer Normalization comparison diagram."""
    prompt = """Create an SVG diagram comparing Layer Normalization variants:

Show two architecture columns side by side:

Left column - "Post-Norm (Original Transformer)":
- Input x at bottom
- Sub-layer (Attention or FFN)
- Add (residual connection shown)
- LayerNorm
- Output
- Flow: x → sublayer → add(x, sublayer(x)) → LayerNorm → output

Right column - "Pre-Norm (Modern LLMs)":
- Input x at bottom
- LayerNorm FIRST
- Sub-layer (Attention or FFN)
- Add (residual connection shown)
- Output
- Flow: x → LayerNorm → sublayer → add(x, sublayer(norm(x))) → output

Bottom section - "Normalization Formulas":
- LayerNorm: y = γ · (x - μ) / σ + β
- RMSNorm: y = γ · x / RMS(x)  [Note: No mean subtraction, fewer params]

Add arrows showing the residual skip connections clearly.
Highlight that Pre-Norm is more stable for training.
Canvas size: 900x650."""

    return generate_svg_with_claude(prompt, "05_layer_normalization.svg")


def generate_attention_patterns():
    """Generate Attention Patterns visualization."""
    prompt = """Create an SVG diagram showing different Attention Patterns:

Show 4 attention pattern matrices (heatmaps) in a row:

1. "Full Attention" (Bidirectional):
   - Complete NxN matrix filled
   - All positions attend to all positions
   - Label: "BERT-style"

2. "Causal Attention" (Autoregressive):
   - Lower triangular matrix
   - Each position only attends to previous positions
   - Label: "GPT-style"

3. "Cross Attention":
   - Rectangular matrix (decoder × encoder)
   - Decoder attends to all encoder positions
   - Label: "Encoder-Decoder"

4. "Sparse Attention":
   - Combination of local + global patterns
   - Diagonal band + vertical stripes
   - Label: "Efficient Transformers"

Use a gradient from light (low attention) to the accent color (high attention).
Add axis labels: "Query positions" (vertical) and "Key positions" (horizontal).
Canvas size: 900x400."""

    return generate_svg_with_claude(prompt, "06_attention_patterns.svg")


def generate_transformer_variants():
    """Generate Transformer Variants comparison."""
    prompt = """Create an SVG diagram showing the family of Transformer-based models:

Create a tree/hierarchy diagram:

Top center: "Transformer (2017)"
           |
    ----------------
    |              |
"Encoder-Only"  "Decoder-Only"  "Encoder-Decoder"
    |              |                  |
  BERT          GPT               T5, BART
  RoBERTa       GPT-2             mT5
  ALBERT        GPT-3             FLAN-T5
  DeBERTa       LLaMA
                Claude
                Mistral

For each branch, show:
- Model names in boxes
- Brief use case label underneath:
  - Encoder-Only: "Classification, NLU"
  - Decoder-Only: "Text Generation, Chat"
  - Encoder-Decoder: "Translation, Summarization"

Use different colors for each branch (primary, secondary, accent).
Add year annotations where relevant.
Canvas size: 900x600."""

    return generate_svg_with_claude(prompt, "07_transformer_variants.svg")


def main():
    """Generate all architecture diagrams."""
    print("=" * 60)
    print("Generating LLM Architecture SVG Diagrams")
    print("Using Claude Sonnet 4.5")
    print("=" * 60)

    diagrams = [
        ("Transformer Architecture", generate_transformer_architecture),
        ("Self-Attention Mechanism", generate_self_attention),
        ("Multi-Head Attention", generate_multi_head_attention),
        ("Position Embeddings", generate_position_embeddings),
        ("Layer Normalization", generate_layer_normalization),
        ("Attention Patterns", generate_attention_patterns),
        ("Transformer Variants", generate_transformer_variants),
    ]

    generated = []
    for name, generator in diagrams:
        print(f"\nGenerating: {name}...")
        try:
            path = generator()
            generated.append(path)
        except Exception as e:
            print(f"  Error: {e}")

    print("\n" + "=" * 60)
    print(f"Generated {len(generated)} diagrams in {OUTPUT_DIR}")
    print("=" * 60)

    for path in generated:
        print(f"  - {path}")


if __name__ == "__main__":
    main()
