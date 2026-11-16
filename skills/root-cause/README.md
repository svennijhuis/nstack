# root-cause

Agents write comments to excuse a workaround instead of fixing the cause. "Needed because the user is sometimes undefined." "Retry because the test is flaky." The comment reads as care. It hides a bug that is still there.

This skill turns each new comment into a check. Say "find the root cause" or type `/root-cause`. The agent can also start it by itself: its description tells it to, before it writes a comment, a suppression, or a workaround.

1. [How it works](#1-how-it-works)
2. [Why a description is not enough](#2-why-a-description-is-not-enough)
3. [Hooks you can add](#3-hooks-you-can-add)
4. [Make them yours](#4-make-them-yours)

---

## 1. How it works

Each new comment is one of three kinds. The full rules are in [SKILL.md](SKILL.md), examples in [comment-classes.md](references/comment-classes.md).

| Kind | Example | What happens |
| --- | --- | --- |
| What | `// loop over the users` | Deleted. The code says it. |
| Outside why | `// Bank API returns 200 on failure, see <link>` | Kept, with its source. |
| Excuse | `// retry because flaky`, `@ts-ignore`, `TODO` | The agent finds the cause, fixes it, and removes the workaround and the comment. |

When the fix is bigger than the task, the agent stops and asks you. It never keeps a workaround on its own.

## 2. Why a description is not enough

A skill starts when its description matches the task. Here the trigger is the agent's own act of writing a comment, and an agent that is busy justifying a workaround does not always stop to check. The description catches most cases. A hook catches every one, because the harness runs it, not the agent.

nstack does not install hooks for you. A hook runs on every edit of every session, so it is your choice. Below are two you can copy.

## 3. Hooks you can add

These are for Claude Code. They need Python 3 and nothing else. Other harnesses with hooks take the same scripts. Change only how they are registered.

| Hook | When | What it does |
| --- | --- | --- |
| `root-cause-edit.py` | After each Edit, Write, or MultiEdit | Finds added comments and markers in the new text and tells the agent to run `root-cause`. It does not block the edit. |
| `root-cause-stop.py` | When the agent wants to finish | Reads `git diff HEAD` for added comments. If there are any, it blocks once and asks the agent to fix every excuse and list each comment it keeps. |

Use one or both. The edit hook nudges while the agent works. The stop hook is the checkpoint.

### Install

Save both scripts in `~/.claude/hooks/` (for you) or `.claude/hooks/` in a repo (for the team), and make them executable:

```bash
chmod +x ~/.claude/hooks/root-cause-*.py
```

Then add this to `~/.claude/settings.json`, or to `.claude/settings.json` in the repo. For a repo, replace `~/.claude/hooks` with `"$CLAUDE_PROJECT_DIR"/.claude/hooks`.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit",
        "hooks": [{ "type": "command", "command": "~/.claude/hooks/root-cause-edit.py" }]
      }
    ],
    "Stop": [
      {
        "hooks": [{ "type": "command", "command": "~/.claude/hooks/root-cause-stop.py" }]
      }
    ]
  }
}
```

Restart the session. `/hooks` shows them.

### `root-cause-edit.py`

Exit code 2 sends the message to the agent. The edit is already made, so the agent cannot get stuck.

```python
#!/usr/bin/env python3
"""PostToolUse hook: point the agent at root-cause when an edit adds a comment."""
import json, re, sys

DOCS = (".md", ".mdx", ".txt", ".rst", ".adoc")
COMMENT = re.compile(r"^\s*(//|#(?!!)|/\*|\*|--|<!--|;)|\s(//|#)\s")
MARKER = re.compile(
    r"@ts-ignore|@ts-expect-error|eslint-disable|noqa|type:\s*ignore|nolint"
    r"|rubocop:disable|pragma warning disable|SuppressWarnings|TODO|FIXME|HACK|workaround",
    re.I,
)

data = json.load(sys.stdin)
tool = data.get("tool_input", {})
path = tool.get("file_path", "")
if path.endswith(DOCS):
    sys.exit(0)

texts = [tool.get("new_string") or tool.get("content") or ""]
texts += [e.get("new_string", "") for e in tool.get("edits", [])]
old = tool.get("old_string", "")
old_lines = set(old.splitlines())

hits = [
    line.strip()
    for text in texts
    for line in text.splitlines()
    if line not in old_lines and (COMMENT.search(line) or MARKER.search(line))
]
if hits:
    shown = "\n".join(f"  {h[:120]}" for h in hits[:5])
    print(
        f"You added a comment or marker in {path}:\n{shown}\n"
        "Use the root-cause skill: sort each one as what, outside why, or excuse. "
        "If it is an excuse, fix the cause and remove the workaround.",
        file=sys.stderr,
    )
    sys.exit(2)
```

### `root-cause-stop.py`

It blocks once. `stop_hook_active` is true on the next try, so the agent can always finish.

```python
#!/usr/bin/env python3
"""Stop hook: before the agent finishes, ask it to account for each comment it added."""
import json, re, subprocess, sys

DOCS = (".md", ".mdx", ".txt", ".rst", ".adoc")
COMMENT = re.compile(r"^\s*(//|#(?!!)|/\*|\*|--|<!--|;)|\s(//|#)\s")
MARKER = re.compile(
    r"@ts-ignore|@ts-expect-error|eslint-disable|noqa|type:\s*ignore|nolint"
    r"|rubocop:disable|pragma warning disable|SuppressWarnings|TODO|FIXME|HACK|workaround",
    re.I,
)

data = json.load(sys.stdin)
if data.get("stop_hook_active"):
    sys.exit(0)  # block once, never loop

try:
    diff = subprocess.run(
        ["git", "diff", "HEAD", "-U0", "--no-color"],
        capture_output=True, text=True, check=True,
    ).stdout
except (OSError, subprocess.CalledProcessError):
    sys.exit(0)  # not a git repo, or no commits yet

hits, path = [], ""
for line in diff.splitlines():
    if line.startswith("+++ "):
        path = line[6:] if line.startswith("+++ b/") else ""
    elif line.startswith("+") and path and not path.endswith(DOCS):
        code = line[1:]
        if COMMENT.search(code) or MARKER.search(code):
            hits.append(f"{path}: {code.strip()[:120]}")

if hits:
    shown = "\n".join(f"  {h}" for h in hits[:10])
    print(json.dumps({
        "decision": "block",
        "reason": (
            f"This change adds comments or markers:\n{shown}\n"
            "Use the root-cause skill. Fix every excuse at its cause. In your final message, "
            "list each comment you keep, its kind, and its source."
        ),
    }))
```

### What they catch, and what they miss

They match text, not syntax. Expect a few false hits: a `#` inside a string, a `--i` in C, the word `TODO` in a name. The message only asks the agent to check, so a false hit costs one look.

They skip docs (`.md`, `.mdx`, `.txt`, `.rst`, `.adoc`), a shebang line, and comments that were already there. The stop hook sees only tracked files: a new file counts once it is added with `git add`.

## 4. Make them yours

- Add your own markers to `MARKER`, such as a team tag for workarounds.
- Skip generated folders by adding a path check next to `DOCS`.
- Make the edit hook strict: move it to `PreToolUse` and the edit is refused until the comment is gone. Expect more friction. An outside-why comment then needs a second try.
