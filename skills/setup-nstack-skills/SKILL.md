---
name: setup-nstack-skills
description: Use when the user wants to set up nstack, an nstack skill fails because a skill it calls is missing, or the user wants an optional nstack hook such as the comment-root-cause hook. Installs the missing external skills at the pinned commit and offers the hooks.
---

nstack skills call skills that live in other repos. This skill reads the list of those skills in [external-skills.md](external-skills.md), checks which ones are installed, and installs the missing ones at the pinned commit. Then it offers the optional hooks that nstack skills ship, by [Optional hooks](#optional-hooks).

## Rules that outrank the rest

**Pin to the commit.** Install only the commit in the row. Never fetch `main` or `HEAD`. A moving branch changes the skill under the person without notice.

**Read only until the person approves.** Check and report first. Write nothing before the person approves the plan table.

**Never overwrite.** An installed skill that differs from the pinned commit is `differs`. Show the diff and ask. Never replace it without a yes.

**Copy the folder whole.** Install every file in the skill's folder, not only `SKILL.md`. Never edit what you copy.

**Never push.** This skill writes only to the local skill folder, and, after its own yes, to the settings file that registers an optional hook.

**A hook is opt-in.** Offer each hook once. Never register one without a yes. Never replace a hook that is already there.

## Steps

1. **Read the list.** Parse every row of [external-skills.md](external-skills.md). A row with a missing field is an error. Name the row and stop.
2. **Find the install folder.** The default is `~/.claude/skills/`. If the person uses another harness or a project folder, ask once and use that. Ask for nothing else you can read from disk.
3. **Check each row.** Look for `<install folder>/<name>/SKILL.md`. Also look in the project's `.claude/skills/`. Give each row one state:

   | State | Meaning | Action |
   | --- | --- | --- |
   | `installed` | The folder exists and every file matches the pinned commit | None |
   | `missing` | No folder | Install |
   | `differs` | The folder exists and a file differs from the pinned commit | Show the diff, ask |

4. **Print the plan table.** One line per row: name, state, action, and the folder it will write. End with the count of each state. If every row is `installed`, say so and go to step 8.
5. **Wait for approval.** Ask the person to approve the plan. A `differs` row needs its own yes.
6. **Install.** For each approved row, fetch only its folder at its commit into a new empty temp folder, then copy it to the install folder:

   ```sh
   tmp=$(mktemp -d)
   git -C "$tmp" init -q
   git -C "$tmp" remote add origin https://github.com/<owner>/<repo>.git
   git -C "$tmp" sparse-checkout set <folder>
   git -C "$tmp" fetch -q --depth 1 origin <commit>
   git -C "$tmp" checkout -q FETCH_HEAD
   cp -R "$tmp/<folder>" "<install folder>/<name>"
   ```

7. **Verify.** Run the check again. Every approved row must now be `installed`. Report any that is not, with the error text.
8. **Offer the hooks**, by [Optional hooks](#optional-hooks). When every row was `installed` at step 4, still do this step before you stop.

## Optional hooks

Some nstack skills ship a hook that makes the skill hard to skip. Offer a hook only when its skill is installed, in the install folder or the project's `.claude/skills/`.

| Hook | Skill | Script | Events |
| --- | --- | --- | --- |
| comment-root-cause | `comment-root-cause` | `<skill folder>/hooks/comment-root-cause-hook.py` | `PreToolUse` with matcher `Edit\|Write\|MultiEdit`, and `Stop` |

What the hook does and the settings it needs are in that skill's README.

1. **Check.** Read the settings file the hook would go in: `~/.claude/settings.json` for the person, `.claude/settings.json` for a repo. The hook is `registered` when each of its events already runs its script. Skip a registered hook.
2. **Ask.** One question per hook: what it does in one line, and the choice of for you, for this repo, or no. Recommend for you. A no is final for this run.
3. **With a home repo, hand over.** When the working directory or the person's setup has a home repo, `setup-home-repo` owns hooks. Tell the person to say "add the comment-root-cause hook" there, and stop this step.
4. **Show the change.** Print the JSON you will merge, with the full path to the script for the person's file, or `"$CLAUDE_PROJECT_DIR"/<path>` for a repo's. Wait for a yes.
5. **Merge.** Add the entries to the `hooks` that are there. Keep every other key and hook. Make the script executable. On another harness, map the events by what they do, by the skill's README. If the harness has no matching event, say so and skip it.
6. **Verify.** Read the file again and check that it is valid JSON and every event runs the script. Tell the person to restart the session and check with `/hooks`.

## Adding a skill to the list

Add one row to [external-skills.md](external-skills.md) with the repo, the folder, and the full 40-character commit. Get the commit with `git ls-remote <repo-url> HEAD`. Add a link that points at `SKILL.md` on that commit, never on a branch.
