# Troubleshooting

Common issues and their solutions.

---

## Installation Issues

### ImportError: Docling not available

**Symptom**: `ImportError: Docling not installed`

**Solution**:
```bash
uv pip install docling==2.66.0
```

### ImportError: MarkItDown not available

**Symptom**: `ImportError: MarkItDown not installed`

**Solution**:
```bash
uv pip install "markitdown[all]==0.0.1a2"
```

### uv not found

**Symptom**: `command not found: uv`

**Solution**:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## Docker Issues

### Docker build fails

**Symptom**: Build fails with dependency errors

**Solution**:
```bash
docker build --no-cache -t doc-generator:latest .
```

### Permission denied on output directory

**Symptom**: `Permission denied: /app/src/output`

**Solution**:
```bash
chmod 755 src/output
```

### Container exits immediately

**Symptom**: Container starts and exits with no output

**Solution**: Check logs:
```bash
docker logs <container_id>
```

---

## Runtime Issues

### PDF generation fails

**Symptom**: `ReportLabError` or blank PDF

**Possible Causes**:
1. Font not found - ensure fonts are installed
2. Content too long - check page margins
3. Invalid characters - sanitize input

**Debug**:
```bash
python scripts/run_generator.py input.md --output pdf --verbose
```

### PPTX has no content

**Symptom**: Empty slides

**Possible Causes**:
1. Parsing failed - check input format
2. Content structure missing sections

**Debug**: Check the parsed content structure in logs.

---

## Claude Code Issues

### Skill not found

**Symptom**: `/skill-name` not recognized

**Solution**: Check `.claude/skills/` for the skill file. Ensure it has correct YAML frontmatter.

### Hook fails

**Symptom**: Command blocked by hook

**Solution**: Check `.claude/settings.json` for hook configuration. Review hook output for specific error.

---

## Adding New Issues

When you encounter and solve a new issue:
1. Add it to this file
2. Include symptom, cause, and solution
3. Add code examples where helpful
