#!/usr/bin/env python3
"""Checks the skills against the Agent Skills spec (agentskills.io/specification).

Fails if the set of skills changes, or if a SKILL.md breaks a frontmatter or length rule.
Run: python3 scripts/check_skills.py
"""
import json
import pathlib
import re
import sys

# The skills customers install. Adding or removing one is a deliberate change: update this list.
EXPECTED = {
    "flyweel",
    "flyweel-card-top-up",
    "flyweel-real-cash-payback",
    "flyweel-where-to-spend-next",
    "flyweel-mcp-deep-ad-analysis",
    "ad-performance-analyser-flyweel",
}
ALLOWED_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_BODY_LINES = 500


def frontmatter(text):
    """Top-level keys and their one-line values. Nested keys (under metadata) are skipped."""
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None, text
    fields = {}
    for line in m.group(1).split("\n"):
        if line and not line[0].isspace() and ":" in line:
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip().strip('"')
    return fields, text[m.end():]


def check(root, path, errors):
    rel = path.relative_to(root)
    name = path.parent.name
    fields, body = frontmatter(path.read_text())
    if fields is None:
        errors.append(f"{rel}: no frontmatter")
        return
    for key in fields.keys() - ALLOWED_KEYS:
        errors.append(f"{rel}: unknown frontmatter key '{key}'")
    if fields.get("name") != name:
        errors.append(f"{rel}: name '{fields.get('name')}' does not match folder '{name}'")
    if not NAME.match(name) or len(name) > 64:
        errors.append(f"{rel}: name must be 1-64 chars of a-z, 0-9 and single dashes")
    desc = fields.get("description", "")
    if not 1 <= len(desc) <= 1024:
        errors.append(f"{rel}: description is {len(desc)} chars, must be 1-1024")
    if "<" in desc or ">" in desc:
        errors.append(f"{rel}: description must not contain < or >")
    if len(fields.get("compatibility", "")) > 500:
        errors.append(f"{rel}: compatibility over 500 chars")
    lines = body.count("\n")
    if lines > MAX_BODY_LINES:
        errors.append(f"{rel}: body is {lines} lines, keep it under {MAX_BODY_LINES}")
    for ref in re.findall(r"`(references/[^`]+)`", body):
        if not (path.parent / ref).exists():
            errors.append(f"{rel}: points to {ref}, which does not exist")


def main():
    root = pathlib.Path(__file__).resolve().parent.parent
    errors = []
    found = {p.parent.name for p in (root / "skills").glob("*/SKILL.md")}
    if found != EXPECTED:
        errors.append(f"skills changed. Missing: {sorted(EXPECTED - found)}. New: {sorted(found - EXPECTED)}")
    for path in sorted((root / "skills").glob("*/SKILL.md")):
        check(root, path, errors)
    for manifest in sorted((root / ".claude-plugin").glob("*.json")):
        try:
            json.loads(manifest.read_text())
        except ValueError as e:
            errors.append(f"{manifest.relative_to(root)}: {e}")
    for e in errors:
        print("FAIL ", e)
    print(f"{len(found)} skills checked, {len(errors)} problems")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
