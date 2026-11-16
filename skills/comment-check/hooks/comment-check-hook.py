#!/usr/bin/env python3
"""comment-check hook for Claude Code. Blocks a new comment that has no source.

PreToolUse (Edit, Write, MultiEdit): refuses an edit that adds such a comment.
Stop: before the agent finishes, checks the whole change once, for edits made
another way (a shell command, a script).

A comment with a source passes: a link, an issue (#123), a ticket (ABC-123),
or an ADR (ADR-0012). See the comment-check skill for why.
"""
import json
import os
import re
import subprocess
import sys

DOCS = (".md", ".mdx", ".txt", ".rst", ".adoc")
SLASH = {"js", "jsx", "ts", "tsx", "mjs", "cjs", "java", "kt", "kts", "scala", "c", "h",
         "cc", "cpp", "hpp", "cs", "go", "rs", "swift", "dart", "php", "css", "scss", "less"}
HASH = {"py", "rb", "sh", "bash", "zsh", "yml", "yaml", "toml", "r", "pl", "ex", "exs",
        "tf", "ps1", "cmake"}
DASH = {"sql", "lua", "hs"}
ANGLE = {"html", "htm", "xml", "vue", "svelte"}
HASH_NAMES = {"Dockerfile", "Makefile", "Gemfile", "Rakefile"}

MARKER = re.compile(
    r"@ts-ignore|@ts-expect-error|@ts-nocheck|eslint-disable|noqa|type:\s*ignore|nolint"
    r"|rubocop:disable|pragma warning disable|SuppressWarnings|\b(TODO|FIXME|HACK|XXX)\b",
    re.I,
)
SOURCE = re.compile(r"https?://|\bADR-\d+|(^|\s)#\d+\b|\b[A-Z][A-Z0-9]+-\d+\b")


def comment_pattern(path):
    name = os.path.basename(path)
    ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""
    if ext in SLASH:
        return re.compile(r"^\s*(//|/\*|\*(\s|/|$))|\s(//|/\*)\s")
    if ext in HASH or name in HASH_NAMES:
        return re.compile(r"^\s*#(?!!)|\s#\s")
    if ext in DASH:
        return re.compile(r"^\s*--|\s--\s")
    if ext in ANGLE:
        return re.compile(r"<!--")
    return None


def unsourced(path, lines):
    if not path or path.endswith(DOCS):
        return []
    pattern = comment_pattern(path)
    return [
        line.strip()
        for line in lines
        if ((pattern and pattern.search(line)) or MARKER.search(line))
        and not SOURCE.search(line)
    ]


def read_lines(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read().splitlines()
    except OSError:
        return []


def message(hits, where):
    shown = "\n".join(f"  {h[:120]}" for h in hits[:10])
    return (
        f"Blocked by comment-check: {where} adds comments or markers with no source:\n{shown}\n"
        "Use the comment-check skill. A what comment: delete it, make the code say it. "
        "An excuse: find the cause, fix it, and remove the workaround. "
        "An outside why: add its source (a link, #123, ABC-123, ADR-0012). "
        "If the fix is bigger than the task, stop and ask the person."
    )


def pre_tool_use(data):
    tool = data.get("tool_input", {})
    path = tool.get("file_path", "")
    existing = set(read_lines(path))
    texts = [tool.get("new_string") or tool.get("content") or ""]
    texts += [e.get("new_string", "") for e in tool.get("edits", [])]
    added = [l for t in texts for l in t.splitlines() if l not in existing]
    hits = unsourced(path, added)
    if hits:
        print(message(hits, path), file=sys.stderr)
        sys.exit(2)


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout


def stop(data):
    if data.get("stop_hook_active"):
        return  # block once, never loop
    try:
        diff = git("diff", "HEAD", "-U0", "--no-color")
        new_files = git("ls-files", "--others", "--exclude-standard").splitlines()
    except (OSError, subprocess.CalledProcessError):
        return  # not a git repo, or no commit yet

    added, path = {}, ""
    for line in diff.splitlines():
        if line.startswith("+++ "):
            path = line[6:] if line.startswith("+++ b/") else ""
        elif line.startswith("+") and path:
            added.setdefault(path, []).append(line[1:])
    for path in new_files:
        added[path] = read_lines(path)

    hits = [f"{p}: {h}" for p, lines in added.items() for h in unsourced(p, lines)]
    if hits:
        print(json.dumps({"decision": "block", "reason": message(hits, "this change")}))


data = json.load(sys.stdin)
event = data.get("hook_event_name")
if event == "PreToolUse":
    pre_tool_use(data)
elif event == "Stop":
    stop(data)
