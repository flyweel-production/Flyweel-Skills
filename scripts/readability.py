#!/usr/bin/env python3
"""Reading-ease check for the skills. Fails under a Flesch score of 70 or on a banned word.

Run: python3 scripts/readability.py
"""
import glob
import pathlib
import re
import sys

MIN_SCORE = 70
# Words we swapped out for plainer ones. See CONTRIBUTING.md.
BANNED = (
    r"streams?|pull(s|ed)?|velocity|unbilled|thresholds?|prepay|horizon|turns|float|rhythm|"
    r"rungs?|ladder|cohorts?|marginal|worst case|walk(s|ed)?|positions?"
)


def syllables(word):
    word = re.sub(r"[^a-z]", "", word.lower())
    if not word:
        return 0
    count = len(re.findall(r"[aeiouy]+", word))
    if word.endswith("e") and not word.endswith(("le", "ee")) and count > 1:
        count -= 1
    return max(count, 1)


def prose(text):
    """Drop code blocks, inline code, tables and markdown marks."""
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`[^`]*`", " it ", text)
    text = "\n".join(l for l in text.split("\n") if not l.strip().startswith("|"))
    return re.sub(r"[#*_>\[\]()]", " ", text)


def flesch(text):
    text = prose(text)
    sentences = [s for s in re.split(r"[.!?:]+\s|\n+", text) if re.search(r"[A-Za-z]", s)]
    words = re.findall(r"[A-Za-z']+", text)
    if not words or not sentences:
        return 100.0
    return 206.835 - 1.015 * len(words) / len(sentences) - 84.6 * sum(map(syllables, words)) / len(words)


def main():
    failed = False
    root = pathlib.Path(__file__).resolve().parent.parent
    files = sorted(glob.glob(str(root / "skills" / "**" / "*.md"), recursive=True)) + [str(root / "README.md")]
    for path in files:
        text = pathlib.Path(path).read_text()
        name = str(pathlib.Path(path).relative_to(root))
        parts = {"body": text}
        if text.startswith("---"):
            head, body = text.split("\n---\n", 1)
            parts["body"] = body
            match = re.search(r"^description: (.*)$", head, re.M)
            if match:
                parts["description"] = match.group(1)
        for label, part in parts.items():
            score = flesch(part)
            banned = sorted({m.group(0).lower() for m in re.finditer(rf"\b({BANNED})\b", prose(part), re.I)})
            bad = score < MIN_SCORE or banned
            failed = failed or bool(bad)
            note = f"  banned: {', '.join(banned)}" if banned else ""
            print(f"{'FAIL' if bad else 'ok  '} {score:5.1f}  {name} [{label}]{note}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
