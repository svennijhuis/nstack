# comment-root-cause

A comment often covers a problem. "Needed because the user is sometimes undefined." "Retry because the test is flaky." The comment reads as care, but the cause is still there.

This skill makes the agent check why a comment is there. A comment that says what the code does becomes clearer code. A business rule, a decision, or a fact outside the code stays. A comment that covers a shortcut or a workaround means: fix the root cause. When that fix is too big, the agent asks you.

Say "find the root cause" or type `/comment-root-cause`. The agent also starts it by itself when it writes a comment. `/comment-root-cause <path>` checks the comments already in a file, folder, or repo. The rules are in [SKILL.md](SKILL.md).

## The hook

An agent that is busy with a workaround does not always stop to check its own comment. The optional hook reminds it. It never blocks.

[hooks/comment-root-cause-hook.py](hooks/comment-root-cause-hook.py) runs after each Edit, Write, or MultiEdit in Claude Code. When the edit adds a comment, a `TODO`, `HACK`, or `FIXME`, a suppression such as `@ts-ignore`, `eslint-disable`, or `noqa`, or an `as any`, it tells the agent to check why with this skill. It needs Python 3 and nothing else.

It skips docs and comments that were already there. After a Write of a whole file it cannot see the old file, so it also names comments that were there before.

### Install

Say "set up nstack": `setup-nstack-skills` offers the hook and writes nothing before your yes. With a home repo, say "add the comment-root-cause hook" to `setup-home-repo`.

By hand, with the skill in `~/.claude/skills/comment-root-cause/`, merge this into `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit",
        "hooks": [{ "type": "command", "command": "~/.claude/skills/comment-root-cause/hooks/comment-root-cause-hook.py" }]
      }
    ]
  }
}
```

For a repo, put the skill in `.claude/skills/comment-root-cause/`, use `"$CLAUDE_PROJECT_DIR"/.claude/skills/comment-root-cause/hooks/comment-root-cause-hook.py`, and merge into `.claude/settings.json`. Make the script executable and restart the session.

To change what it looks for, edit `MARKER`, or add a language to `SLASH`, `HASH`, `DASH`, or `ANGLE`.
