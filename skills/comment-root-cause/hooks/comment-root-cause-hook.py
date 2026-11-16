#!/usr/bin/env python3
"""comment-root-cause hook for Claude Code (PostToolUse on Edit, Write, MultiEdit).

When an edit adds a comment or a suppression, tells the agent to check why.
It never blocks: the edit is already made.
"""
import json
import os
import re
import sys

DOCS = (".md", ".mdx", ".txt", ".rst", ".adoc")
SLASH = {"js", "jsx", "ts", "tsx", "mjs", "cjs", "java", "kt", "kts", "scala", "groovy",
         "c", "h", "cc", "cpp", "hpp", "cs", "go", "rs", "swift", "dart", "php",
         "css", "scss", "less", "zig", "sol", "proto"}
HASH = {"py", "rb", "sh", "bash", "zsh", "yml", "yaml", "toml", "r", "pl", "ex", "exs",
        "tf", "ps1", "nix", "jl"}
DASH = {"sql", "lua", "hs"}
ANGLE = {"html", "htm", "xml", "vue", "svelte"}

MARKER = re.compile(
    r"@ts-ignore|@ts-expect-error|eslint-disable|noqa|type:\s*ignore|nolint"
    r"|rubocop:disable|pragma warning disable|SuppressWarnings|\bas\s+any\b"
    r"|\b(TODO|FIXME|HACK|XXX)\b",
    re.I,
)


def comment_pattern(path):
    ext = path.rsplit(".", 1)[-1].lower() if "." in os.path.basename(path) else ""
    if ext in SLASH:
        return re.compile(r"^\s*(//|/\*|\*(\s|/|$))|\s(//|/\*)\s")
    if ext in HASH:
        return re.compile(r"^\s*#(?!!)|\s#\s")
    if ext in DASH:
        return re.compile(r"^\s*--|\s--\s")
    if ext in ANGLE:
        return re.compile(r"<!--")
    return None


def old_lines(tool, path):
    if "old_string" in tool:
        return set(tool["old_string"].splitlines())
    if "edits" in tool:
        return {l for e in tool["edits"] for l in e.get("old_string", "").splitlines()}
    return set()  # Write: the hook runs after it, so the old file is gone


data = json.load(sys.stdin)
tool = data.get("tool_input", {})
path = tool.get("file_path", "")
if not path or path.endswith(DOCS):
    sys.exit(0)

pattern = comment_pattern(path)
texts = [tool.get("new_string") or tool.get("content") or ""]
texts += [e.get("new_string", "") for e in tool.get("edits", [])]
before = old_lines(tool, path)
found = [
    line.strip()
    for text in texts
    for line in text.splitlines()
    if line not in before and ((pattern and pattern.search(line)) or MARKER.search(line))
]
if found:
    shown = "\n".join(f"  {line[:120]}" for line in found[:5])
    print(
        f"New comment in {path}:\n{shown}\n"
        "Use the comment-root-cause skill. Why is this comment here? "
        "Can the code be better, or is this the best it can be? "
        "If it covers a shortcut, a workaround, or an unfixed cause, fix the root cause.",
        file=sys.stderr,
    )
    sys.exit(2)
