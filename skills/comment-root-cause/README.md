# comment-root-cause

A comment often covers a problem. "Needed because the user is sometimes undefined." "Retry because the test is flaky." The comment reads as care, but the cause is still there.

This skill makes the agent ask two questions: why is this comment here, and can the code be better? When code needs a comment to explain what it does, it is often not the best code, so the agent makes the code better and the comment goes. A business rule, a decision, or a fact outside the code stays. A comment that covers a shortcut or a workaround means: fix the root cause. When that fix is too big, the agent asks you.

Say "find the root cause" or type `/comment-root-cause`. The agent also starts it by itself when it writes a comment. `/comment-root-cause <path>` checks the comments already in a file, folder, or repo. The rules are in [SKILL.md](SKILL.md).

## The hook

An agent that is busy with a workaround does not always stop to check its own comment. The optional hook reminds it. It never blocks.

[hooks/comment-root-cause-hook.py](hooks/comment-root-cause-hook.py) runs after each Edit, Write, or MultiEdit in Claude Code. When the edit adds a comment, a `TODO`, `HACK`, or `FIXME`, a suppression such as `@ts-ignore`, `eslint-disable`, or `noqa`, or an `as any`, it asks the agent why the comment is there and whether the code can be better. It needs Python 3 and nothing else.

It skips docs and comments that were already there. After a Write of a whole file it cannot see the old file, so it also names comments that were there before.

### Install

Say "set up nstack": `setup-nstack-skills` asks if you want this skill and its hook, the skill only, or neither, and writes nothing before your yes. With a home repo, say "add the comment-root-cause hook" to `setup-home-repo`.

By hand, with the skill in `~/.claude/skills/comment-root-cause/`, merge this into `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit",
        "hooks": [{ "type": "command", "command": "python3 ~/.claude/skills/comment-root-cause/hooks/comment-root-cause-hook.py" }]
      }
    ]
  }
}
```

The command differs per system:

| System | Command |
| --- | --- |
| macOS, Linux | `python3 ~/.claude/skills/comment-root-cause/hooks/comment-root-cause-hook.py` |
| Windows | `py -3 "C:/Users/<name>/.claude/skills/comment-root-cause/hooks/comment-root-cause-hook.py"` |

On macOS, Python 3 comes with the Xcode command line tools (`xcode-select --install`) or from https://www.python.org. On Windows, install it from https://www.python.org, which also installs `py`. Without `py`, use `python`.

For a repo, put the skill in `.claude/skills/comment-root-cause/`, use `"$CLAUDE_PROJECT_DIR"/.claude/skills/comment-root-cause/hooks/comment-root-cause-hook.py` as the path, and merge into `.claude/settings.json`. Restart the session.

To change what it looks for, edit `MARKER`, or add a language to `SLASH`, `HASH`, `DASH`, or `ANGLE`.
