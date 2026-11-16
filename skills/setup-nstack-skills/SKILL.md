---
name: setup-nstack-skills
description: Use when the user wants to set up nstack, an nstack skill fails because a skill it calls is missing, or the user wants an optional nstack skill or hook such as comment-root-cause. Installs the missing external skills at the pinned commit and asks about the optional skills and hooks.
---

nstack skills call skills that live in other repos. This skill reads the list of those skills in [external-skills.md](external-skills.md), checks which ones are installed, and installs the missing ones at the pinned commit. Then it asks if the person wants each optional skill and its hook, by [Optional skills and hooks](#optional-skills-and-hooks).

## Rules that outrank the rest

**Pin to the commit.** Install only the commit in the row. Never fetch `main` or `HEAD`. A moving branch changes the skill under the person without notice.

**Read only until the person approves.** Check and report first. Write nothing before the person approves the plan table.

**Never overwrite.** An installed skill that differs from the pinned commit is `differs`. Show the diff and ask. Never replace it without a yes.

**Copy the folder whole.** Install every file in the skill's folder, not only `SKILL.md`. Never edit what you copy.

**Never push.** This skill writes only to the local skill folder, and, after its own yes, to the settings file that registers an optional hook. It removes an optional skill folder only after its own yes.

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
8. **Offer the optional skills and hooks**, by [Optional skills and hooks](#optional-skills-and-hooks). When every row was `installed` at step 4, still do this step before you stop.

## Optional skills and hooks

Some nstack skills are optional and ship a hook that reminds the agent to use them. Ask the person if they want each one. Look for the skill in the install folder and the project's `.claude/skills/`.

| Hook | Skill | Needs | Script | Events |
| --- | --- | --- | --- | --- |
| comment-root-cause | `comment-root-cause` | Python 3 | `<skill folder>/hooks/comment-root-cause-hook.py` | `PostToolUse` with matcher `Edit\|Write\|MultiEdit` |

What the hook does and the settings it needs are in that skill's README.

1. **Check what it needs.** For Python 3, try these in order and use the first that prints `Python 3`:

   | System | Try |
   | --- | --- |
   | macOS, Linux | `python3 --version`, then `python --version` |
   | Windows | `py -3 --version`, then `python --version`, then `python3 --version` |

   On macOS, run `xcode-select -p` first. When it fails, `python3` is only a stub that opens an install window: treat Python as missing. On Windows, a command that prints nothing is the Microsoft Store stub: treat it as missing.

   None works: tell the person the hook needs Python 3 (macOS: `xcode-select --install` or https://www.python.org, Windows: https://www.python.org, with "Add to PATH"). Do not install it yourself. Skip the hook, the skill can stay.
2. **Check.** Read the settings file the hook would go in: `~/.claude/settings.json` for the person, `.claude/settings.json` for a repo. The hook is `registered` when each of its events already runs its script.
3. **Ask.** One question per skill: what the skill and its hook do, one line each, and the choice:
   - **Skill and hook** (recommended), for you or for this repo.
   - **Skill only.** Register no hook.
   - **Neither.** Register no hook. When the skill is installed, offer to remove its folder, and remove it only after a yes.

   A no is final for this run. With the hook already registered, ask only whether to keep it.
4. **With a home repo, hand over.** When the working directory or the person's setup has a home repo, `setup-home-repo` owns hooks. Tell the person to say "add the comment-root-cause hook" there, and stop this step.
5. **Show the change.** Print the JSON you will merge. The command is the Python you found, then the script path in double quotes: the full path for the person's file, or `"$CLAUDE_PROJECT_DIR"/<path>` for a repo's. On Windows, write the path with forward slashes, such as `py -3 "C:/Users/<name>/.claude/skills/comment-root-cause/hooks/comment-root-cause-hook.py"`. Wait for a yes.
6. **Merge.** Add the entries to the `hooks` that are there. Keep every other key and hook. On another harness, map the events by what they do, by the skill's README. If the harness has no matching event, say so and skip it.
7. **Verify.** Read the file again and check that it is valid JSON and every event runs the script. Run the command once with `{}` on its input: it must exit without an error. Tell the person to restart the session and check with `/hooks`.

## Adding a skill to the list

Add one row to [external-skills.md](external-skills.md) with the repo, the folder, and the full 40-character commit. Get the commit with `git ls-remote <repo-url> HEAD`. Add a link that points at `SKILL.md` on that commit, never on a branch.
