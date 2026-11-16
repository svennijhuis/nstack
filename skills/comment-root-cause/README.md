# comment-root-cause

Fix the root cause. Never comment it, never work around it.

An agent that cannot find a cause patches the symptom: a null check, a retry, a cast, a skipped test. Then it writes a comment that makes the patch sound reasonable. "Needed because the user is sometimes undefined." The comment reads as care. The bug is still there.

Say "find the root cause" or type `/comment-root-cause`. The agent also starts it by itself: its description names comments, suppressions, and workarounds. `/comment-root-cause <path>` cleans up the comments already in a file, folder, or repo.

1. [How it works](#1-how-it-works)
2. [Why a description is not enough](#2-why-a-description-is-not-enough)
3. [The hook](#3-the-hook)
4. [Install the hook](#4-install-the-hook)
5. [Make it yours](#5-make-it-yours)

---

## 1. How it works

| Kind | Example | What happens |
| --- | --- | --- |
| What | `// loop over the users` | Deleted. The code says it. |
| Outside why | `// Bank API returns 200 on failure: <link>` | Kept, with the source that proves it. |
| Excuse | `// retry because flaky`, `as any`, `it.skip`, `catch {}`, `TODO` | The agent finds the cause, fixes it, and removes the workaround and the comment. |

A workaround with no comment is an excuse too. So is an excuse moved into a name, a log line, a docstring, or a commit message. Only you decide to keep a workaround. The agent asks, and never decides it with a comment. Rules: [SKILL.md](SKILL.md). Examples: [comment-classes.md](references/comment-classes.md).

## 2. Why a description is not enough

A skill starts when its description matches the task. Here the trigger is the agent's own act of writing a comment or a workaround, and an agent that is busy justifying one does not always stop to check. A hook catches every one, because the harness runs it, not the agent.

The hook is optional: it runs on every edit of every session. `setup-nstack-skills` offers it.

## 3. The hook

One script, [hooks/comment-root-cause-hook.py](hooks/comment-root-cause-hook.py), for Claude Code. Python 3, nothing else.

| Event | What it does |
| --- | --- |
| `SessionStart` | Remembers the commit the session starts on. |
| `PreToolUse` on Edit, Write, MultiEdit, NotebookEdit | Refuses an edit that adds a comment, marker, or workaround with no source. |
| `Stop` | Checks everything since the session started: commits, uncommitted edits, new files, edits by shell. It blocks until each one is fixed or named in the final message with its kind, source, and your choice. |

**A source is the only way through:** a link, an issue (`#123`), an ADR (`ADR-0012`), or a ticket with a prefix you allow. That is the skill's rule. An outside why keeps the source that proves it. A workaround you agreed to keeps your ticket.

It checks, in new lines only:

- **Comments**, by language: `//` and `/* */` in C-like files, `#` in Python, shell, YAML and the like, `--` in SQL, `<!-- -->` in HTML. Python docstrings count.
- **Markers**: `@ts-ignore`, `@ts-expect-error`, `@ts-nocheck`, `eslint-disable`, `noqa`, `type: ignore`, `nolint`, `rubocop:disable`, `pragma warning disable`, `@SuppressWarnings`, `TODO`, `FIXME`, `HACK`, `XXX`.
- **Workarounds**: `as any`, `as unknown as`, an empty `catch`, `.catch(() => {})`, `except: pass`, and skipped tests (`it.skip`, `xit`, `@pytest.mark.skip`, `@Disabled`, `t.Skip()`, `#[ignore]`).

It skips docs (`.md`, `.mdx`, `.txt`, `.rst`, `.adoc`), file types it does not know, a shebang, and comments that were already there.

**What it cannot catch**, so the skill and review still matter: a workaround that is plain code (a null check, a retry, a sleep, a raised timeout, a loosened assertion), an excuse in a name or a log string, and a made-up source.

**It never traps the agent.** When the final message names every flagged file, or the transcript cannot be read, the agent may finish. Outside a git repo the `Stop` check does nothing.

## 4. Install the hook

### With nstack

Say "set up nstack". `setup-nstack-skills` asks if you want the hook, for you or for a repo, shows the change, and writes nothing before your yes. With a home repo, say "add the comment-root-cause hook" to `setup-home-repo` instead.

### By hand

With the skill in `~/.claude/skills/comment-root-cause/`, merge this into the `hooks` in `~/.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart": [
      { "hooks": [{ "type": "command", "command": "~/.claude/skills/comment-root-cause/hooks/comment-root-cause-hook.py" }] }
    ],
    "PreToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit|NotebookEdit",
        "hooks": [{ "type": "command", "command": "~/.claude/skills/comment-root-cause/hooks/comment-root-cause-hook.py" }]
      }
    ],
    "Stop": [
      { "hooks": [{ "type": "command", "command": "~/.claude/skills/comment-root-cause/hooks/comment-root-cause-hook.py" }] }
    ]
  }
}
```

For a repo, put the skill in `.claude/skills/comment-root-cause/`, use `"$CLAUDE_PROJECT_DIR"/.claude/skills/comment-root-cause/hooks/comment-root-cause-hook.py`, and merge into `.claude/settings.json`. Make the script executable. Restart the session. `/hooks` shows it.

Another harness with hooks can run the script. Map the events by what they do, and check that it sends the same fields.

## 5. Make it yours

- **Tickets:** set `COMMENT_ROOT_CAUSE_TICKETS=PAY,OPS` in the settings `env`, and `PAY-123` counts as a source. Without it, no ticket key does, so `UTF-8` or `SHA-256` never passes as one.
- **More checks:** add to `MARKER` or `WORKAROUND`, or a language to `SLASH`, `HASH`, `DASH`, or `ANGLE`.
- **Allow docstrings:** remove the `DOCSTRING` check in `unsourced`.
- **Softer:** register only `Stop`. The agent works freely, then fixes or accounts for each one before it finishes.
