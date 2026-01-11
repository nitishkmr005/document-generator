#!/usr/bin/env python3
import os, re
from pathlib import Path

REPLACEMENTS = {
    r'from \.\.\.infrastructure\.gemini_image_generator import': 'from ...infrastructure.image import',
    r'from \.\.\.infrastructure\.llm_service import': 'from ...infrastructure.llm import',
    r'from \.\.\.infrastructure\.llm_content_generator import': 'from ...infrastructure.llm import',
    r'from \.\.\.infrastructure\.claude_svg_generator import': 'from ...infrastructure.image import',
    r'from \.\.\.infrastructure\.svg_generator import': 'from ...infrastructure.image import',
    r'from \.\.infrastructure\.gemini_image_generator import': 'from ..infrastructure.image import',
    r'from \.\.infrastructure\.llm_content_generator import': 'from ..infrastructure.llm import',
    r'from \.\.infrastructure\.llm_service import': 'from ..infrastructure.llm import',
}

app_dir = Path('src/doc_generator/application')
fixed = 0
for py_file in app_dir.rglob('*.py'):
    with open(py_file, 'r') as f:
        content = f.read()
    original = content
    for old, new in REPLACEMENTS.items():
        content = re.sub(old, new, content)
    if content != original:
        with open(py_file, 'w') as f:
            f.write(content)
        print(f"✓ {py_file}")
        fixed += 1
print(f"\n✅ Fixed {fixed} files")
