#!/usr/bin/env python3
"""comment-root-cause hook for Claude Code.

Blocks a new comment, marker, or workaround that carries no source.
SessionStart: remembers the commit the session started on.
PreToolUse (Edit, Write, MultiEdit, NotebookEdit): refuses such an edit.
Stop: checks everything since the session started, edits by shell included.
  It blocks until the final message names every file that still has one.

A source is a link, an issue (#123), an ADR (ADR-0012), or a ticket whose
prefix is in COMMENT_ROOT_CAUSE_TICKETS (for example "PAY,OPS").
A comment block that starts with "Business rule:" or "Decision:" passes too.
Markers and workarounds pass only with a source.
"""
import json
import os
import re
import subprocess
import sys
import tempfile

DOCS = (".md", ".mdx", ".txt", ".rst", ".adoc")
SLASH = {"js", "jsx", "ts", "tsx", "mjs", "cjs", "java", "kt", "kts", "scala", "groovy",
         "gradle", "c", "h", "cc", "cpp", "hpp", "m", "mm", "cs", "go", "rs", "swift",
         "dart", "php", "css", "scss", "less", "zig", "sol", "proto", "jsonc"}
HASH = {"py", "ipynb", "rb", "sh", "bash", "zsh", "yml", "yaml", "toml", "r", "pl", "ex",
        "exs", "tf", "ps1", "cmake", "nix", "jl", "cr", "nim", "conf"}
DASH = {"sql", "lua", "hs", "elm"}
ANGLE = {"html", "htm", "xml", "vue", "svelte"}
SLASH_NAMES = {"Jenkinsfile"}
HASH_NAMES = {"Dockerfile", "Makefile", "Gemfile", "Rakefile", "Brewfile", "Procfile"}

MARKER = re.compile(
    r"@ts-ignore|@ts-expect-error|@ts-nocheck|eslint-disable|noqa|type:\s*ignore|nolint"
    r"|rubocop:disable|pragma warning disable|SuppressWarnings|\b(TODO|FIXME|HACK|XXX)\b",
    re.I,
)
WORKAROUND = re.compile(
    r"\bas\s+any\b|\bas\s+unknown\s+as\b"
    r"|\b(it|test|describe|context)\.(skip|todo)\s*\(|\bx(it|test|describe)\s*\("
    r"|@pytest\.mark\.(skip|xfail)|@unittest\.skip|@(Disabled|Ignore)\b|\bt\.Skip\("
    r"|#\[ignore\]|catch\s*(\([^)]*\))?\s*\{\s*\}|\.catch\(\s*\(\s*\w*\s*\)\s*=>\s*\{\s*\}\s*\)"
    r"|except\b[^:\n]*:\s*(pass|\.\.\.)\s*$|except\b[^:\n]*:\s*\n\s*(pass|\.\.\.)\s*$",
    re.M,
)
DOCSTRING = re.compile(r"^\s*[rbuRBU]?(\"\"\"|''')")
BUSINESS = re.compile(r"\b(Business rule|Decision):", re.I)


def source_pattern():
    prefixes = [p.strip() for p in os.environ.get("COMMENT_ROOT_CAUSE_TICKETS", "").split(",")]
    ticket = "|".join(re.escape(p) for p in prefixes if p)
    extra = rf"|\b({ticket})-\d+\b" if ticket else ""
    return re.compile(rf"https?://\S+|\bADR-\d+\b|(^|\s)#\d+\b{extra}")


SOURCE = source_pattern()


def comment_pattern(path):
    name = os.path.basename(path)
    ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""
    if ext in SLASH or name in SLASH_NAMES:
        return re.compile(r"^\s*(//|/\*|\*(\s|/|$))|\s(//|/\*)\s")
    if ext in HASH or name in HASH_NAMES:
        return re.compile(r"^\s*#(?!!)|\s#\s")
    if ext in DASH:
        return re.compile(r"^\s*--|\s--\s")
    if ext in ANGLE:
        return re.compile(r"<!--")
    return None


def unsourced(path, lines):
    """Return (line, text) for each new comment, marker, or workaround with no source.

    Consecutive comment lines form one block. A source anywhere in the block
    covers all of it. A business label covers its comments, never a marker
    or a workaround.
    """
    if not path or path.endswith(DOCS):
        return []
    pattern = comment_pattern(path)
    python = path.endswith((".py", ".ipynb"))

    is_comment, in_docstring = [], False
    for _, line in lines:
        opened = python and DOCSTRING.search(line)
        if opened:
            quote = opened.group(1)
            in_docstring = line.count(quote) == 1
            is_comment.append(True)
        elif in_docstring:
            in_docstring = '"""' not in line and "'''" not in line
            is_comment.append(True)
        else:
            is_comment.append(bool(pattern and pattern.search(line)))

    cover = [None] * len(lines)
    start = 0
    while start < len(lines):
        end = start
        while end < len(lines) and is_comment[end]:
            end += 1
        if end > start:
            block = [line for _, line in lines[start:end]]
            if any(SOURCE.search(l) for l in block):
                cover[start:end] = ["source"] * (end - start)
            elif any(BUSINESS.search(l) for l in block):
                cover[start:end] = ["business"] * (end - start)
        start = max(end, start + 1)

    hits = []
    for k, (number, line) in enumerate(lines):
        if SOURCE.search(line) or cover[k] == "source":
            continue
        if MARKER.search(line) or WORKAROUND.search(line) or (is_comment[k] and not cover[k]):
            hits.append((number, line.strip()))
    joined = "\n".join(line for _, line in lines)
    for match in WORKAROUND.finditer(joined):
        if "\n" in match.group(0) and not SOURCE.search(match.group(0)):
            hits.append((None, " ".join(match.group(0).split())))
    return hits


def read_lines(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read().splitlines()
    except OSError:
        return []


def message(hits, where, extra=""):
    shown = "\n".join(f"  {h[:140]}" for h in hits[:15])
    more = f"\n  ... and {len(hits) - 15} more" if len(hits) > 15 else ""
    return (
        f"Blocked by comment-root-cause: {where} adds comments, markers, or workarounds "
        f"with no source:\n{shown}{more}\n"
        "Use the comment-root-cause skill. A what comment: delete it, make the code say it. "
        "An excuse or a workaround: find the cause, fix it, remove both. "
        "An outside why: add the source that proves it. "
        "A business rule or decision: start the comment with 'Business rule:' or 'Decision:'. "
        "Never add a source or a label only to pass. "
        "If the fix is bigger than the task, ask the person." + extra
    )


def state_file(data):
    session = re.sub(r"[^\w-]", "", str(data.get("session_id", ""))) or "unknown"
    folder = os.path.join(tempfile.gettempdir(), "comment-root-cause")
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, session)


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout


def session_start(data):
    try:
        base = git("rev-parse", "HEAD").strip()
    except (OSError, subprocess.CalledProcessError):
        return
    with open(state_file(data), "w") as f:
        f.write(base)


def pre_tool_use(data):
    tool = data.get("tool_input", {})
    path = tool.get("file_path") or tool.get("notebook_path") or ""
    existing = set(read_lines(path))
    texts = [tool.get("new_string") or tool.get("content") or tool.get("new_source") or ""]
    texts += [e.get("new_string", "") for e in tool.get("edits", [])]
    added = [(None, l) for t in texts for l in t.splitlines() if l not in existing]
    hits = unsourced(path, added)
    if hits:
        print(message([h for _, h in hits], path), file=sys.stderr)
        sys.exit(2)


def changes_since_start(data):
    base = "HEAD"
    try:
        with open(state_file(data)) as f:
            base = f.read().strip() or "HEAD"
    except OSError:
        pass
    diff = git("diff", base, "-U0", "--no-color")
    added, path, number = {}, "", 0
    for line in diff.splitlines():
        if line.startswith("+++ "):
            path = line[6:] if line.startswith("+++ b/") else ""
        elif line.startswith("@@"):
            number = int(re.search(r"\+(\d+)", line).group(1))
        elif line.startswith("+") and path:
            added.setdefault(path, []).append((number, line[1:]))
            number += 1
    for path in git("ls-files", "--others", "--exclude-standard").splitlines():
        added[path] = list(enumerate(read_lines(path), 1))
    return added


def last_reply(data):
    """Text of the assistant's turn that is ending, or None when it cannot be read."""
    try:
        with open(data["transcript_path"], encoding="utf-8") as f:
            entries = [json.loads(l) for l in f if l.strip()]
    except (KeyError, OSError, ValueError):
        return None
    texts = []
    for entry in reversed(entries):
        if entry.get("type") == "user" and not entry.get("toolUseResult"):
            content = entry.get("message", {}).get("content")
            if isinstance(content, str) or any(
                c.get("type") == "text" for c in content or [] if isinstance(c, dict)
            ):
                break
        if entry.get("type") == "assistant":
            for c in entry.get("message", {}).get("content", []):
                if isinstance(c, dict) and c.get("type") == "text":
                    texts.append(c["text"])
    return "\n".join(texts)


def stop(data):
    try:
        added = changes_since_start(data)
    except (OSError, subprocess.CalledProcessError):
        return  # not a git repo, or no commit yet
    hits = {
        p: [f"{p}:{n or '?'}: {t}" for n, t in unsourced(p, lines)]
        for p, lines in added.items()
    }
    hits = {p: h for p, h in hits.items() if h}
    if not hits:
        return
    if data.get("stop_hook_active"):
        reply = last_reply(data)
        if reply is None:
            return  # cannot read the reply: never trap the agent
        hits = {p: h for p, h in hits.items() if p not in reply}
        if not hits:
            return  # the final message accounts for every file
    flat = [h for group in hits.values() for h in group]
    extra = (
        " To finish, fix them, or name each of these files in your final message with "
        "each line's kind, source, and the person's choice."
    )
    print(json.dumps({"decision": "block", "reason": message(flat, "this session", extra)}))


data = json.load(sys.stdin)
event = data.get("hook_event_name")
if event == "SessionStart":
    session_start(data)
elif event == "PreToolUse":
    pre_tool_use(data)
elif event == "Stop":
    stop(data)
