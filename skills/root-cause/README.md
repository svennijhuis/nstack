# root-cause

Agents write comments to excuse a workaround instead of fixing the cause. "Needed because the user is sometimes undefined." "Retry because the test is flaky." The comment reads as care. It hides a bug that is still there.

This skill turns each new comment into a check. Say "find the root cause" or type `/root-cause`. The agent can also start it by itself: its description tells it to, before it writes a comment, a suppression, or a workaround.

1. [How it works](#1-how-it-works)
2. [Why a description is not enough](#2-why-a-description-is-not-enough)
3. [The hook: block and fix](#3-the-hook-block-and-fix)
4. [Install the hook](#4-install-the-hook)
5. [Make it yours](#5-make-it-yours)

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

The hook is optional. It runs on every edit of every session, so it is your choice. `setup-nstack-skills` offers it, see [Install the hook](#4-install-the-hook).

## 3. The hook: block and fix

One script, [hooks/root-cause-hook.py](hooks/root-cause-hook.py), on two Claude Code events. It needs Python 3 and nothing else.

| Event | What it does |
| --- | --- |
| `PreToolUse` on Edit, Write, MultiEdit | Refuses an edit that adds a comment or a marker with no source. The agent gets the reason and must change the code. |
| `Stop` | Before the agent finishes, reads `git diff HEAD` and new files once, for edits made another way, such as a shell command. If it finds such a comment, the agent must go back and fix it. |

**A source is the way through.** A comment passes when it carries a link, an issue (`#123`), a ticket (`ABC-123`), or an ADR (`ADR-0012`). That is the skill's rule: an outside why keeps its source, and a workaround you agreed to keeps its ticket. A what comment or an excuse has no source, so the agent has to fix the code.

What it checks:

- Comments, by the file's language: `//` and `/* */` in C-like files, `#` in Python, shell, YAML and the like, `--` in SQL, `<!-- -->` in HTML.
- Markers in any code file: `@ts-ignore`, `@ts-expect-error`, `eslint-disable`, `noqa`, `type: ignore`, `nolint`, `rubocop:disable`, `pragma warning disable`, `@SuppressWarnings`, `TODO`, `FIXME`, `HACK`, `XXX`.
- Only lines that are new. Comments already in the file pass.

What it skips: docs (`.md`, `.mdx`, `.txt`, `.rst`, `.adoc`), file types it does not know, and a shebang line.

What it cannot do: judge the source. A made-up link passes. The hook makes the agent stop and look, and the skill tells it what to look for. Review still matters.

The `Stop` check blocks once per stop. When the agent tries again, it may finish, so a false hit never traps it.

## 4. Install the hook

### With nstack

Say "set up nstack". `setup-nstack-skills` asks if you want the hook, and where: for you (`~/.claude/settings.json`) or for a repo (`.claude/settings.json`). It shows the change and writes nothing before your yes. With a home repo, `setup-home-repo` owns hooks. Say "add the root-cause hook" there instead.

### By hand

The script ships with the skill. When the skill is in `~/.claude/skills/root-cause/`, add this to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit",
        "hooks": [{ "type": "command", "command": "~/.claude/skills/root-cause/hooks/root-cause-hook.py" }]
      }
    ],
    "Stop": [
      {
        "hooks": [{ "type": "command", "command": "~/.claude/skills/root-cause/hooks/root-cause-hook.py" }]
      }
    ]
  }
}
```

For a repo, put the skill in `.claude/skills/root-cause/` and use `"$CLAUDE_PROJECT_DIR"/.claude/skills/root-cause/hooks/root-cause-hook.py` in `.claude/settings.json`. Make the script executable (`chmod +x`). Merge into the `hooks` you already have. Do not replace them. Restart the session. `/hooks` shows it.

Other harnesses with hooks can run the same script. Map the events by what they do: before a file edit, and when the agent stops. The script reads Claude Code's input, so check the fields your harness sends.

## 5. Make it yours

- Add your own markers to `MARKER`, such as a team tag for workarounds.
- Add a language: put its extension in `SLASH`, `HASH`, `DASH`, or `ANGLE`.
- Change what counts as a source in `SOURCE`, for example only your issue tracker.
- Softer: register only `Stop`. The agent works freely and fixes the comments before it finishes.
