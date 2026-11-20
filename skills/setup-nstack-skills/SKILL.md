---
name: setup-nstack-skills
description: Use when the user wants to set up nstack, or an nstack skill fails because a skill it calls is missing. Installs the missing external skills at the pinned commit.
---

Installs the external skills in [external-skills.md](external-skills.md) that are missing, at their pinned commit.

## Rules that outrank the rest

- **Pin to the commit** in the row. Never fetch `main` or `HEAD`.
- **Read only until the person approves** the plan table.
- **Never overwrite.** A skill that differs from its pin: show the diff, and replace it only on its own yes.
- **Copy the folder whole**, every file, unedited.
- **Write only to the local skill folder.** Never push.

## Steps

1. **Read the list.** A row with a missing field: name it and stop.
2. **Find the install folder**, `~/.claude/skills/` by default. For another harness or a project folder, ask once.
3. **Check each row** at `<install folder>/<name>/SKILL.md` and the project's `.claude/skills/`:

   | State | Meaning | Action |
   | --- | --- | --- |
   | `installed` | The folder exists and every file matches the pinned commit | None |
   | `missing` | No folder | Install |
   | `differs` | The folder exists and a file differs from the pinned commit | Show the diff, ask |

4. **Print the plan table**: name, state, action, target folder, then the count per state. All `installed`: say so and stop.
5. **Wait for approval.** A `differs` row needs its own yes.
6. **Install** each approved row: fetch only its folder at its commit into a new empty temp folder, then copy it:

   ```sh
   tmp=$(mktemp -d)
   git -C "$tmp" init -q
   git -C "$tmp" remote add origin https://github.com/<owner>/<repo>.git
   git -C "$tmp" sparse-checkout set <folder>
   git -C "$tmp" fetch -q --depth 1 origin <commit>
   git -C "$tmp" checkout -q FETCH_HEAD
   cp -R "$tmp/<folder>" "<install folder>/<name>"
   ```

7. **Verify.** Check again. Report any approved row that is not `installed`, with the error.

## Adding a skill to the list

One row: repo, folder, the full 40-character commit from `git ls-remote <repo-url> HEAD`, and a link to `SKILL.md` at that commit, never a branch.
