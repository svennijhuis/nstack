# Cleanup

`/setup-home-repo cleanup` fixes what advise found.

1. **Run advise** by [advise.md](advise.md), rows numbered.
2. **Ask which rows.** Recommend high and up. Answers: numbers, `all`, or `none`.
3. **Show what each picked row changes**, and for a removal, what and from where.
4. **Apply in the order below.** Stop and report at the first failure.
5. **Check again** the rows you touched.
6. **Commit and report.** One commit in the home repo unless local only, one on a new local branch in each changed child repo.

## Order

Safe fixes first.

1. Additions: a missing hook registration, a missing environment entry, a missing one-line `CLAUDE.md`.
2. Corrections: a pointer path, a script made executable.
3. Moves: a procedure out of `AGENTS.md` into a skill, pointers into `repos/` files, the lines of a `CLAUDE.md` into `AGENTS.md`.
4. Removals: a duplicate copy, a dead pointer, a merged worktree, a file for an unused harness, a `CLAUDE.md` whose lines have moved, or its text down to the one line. A `.claude/CLAUDE.md` is always removed, and a kept one-line file is written at the root.

## Ask again before each of these

A yes to the list is not a yes to these. Confirm each by name.

| Action | Before you do it |
| --- | --- |
| Remove a file or folder | Show the path. For a duplicate, confirm the kept copy has the same content. If it differs, stop and ask which wins. |
| Remove a worktree | Run `git status` in it. Any uncommitted or unpushed work means do not remove it. Report it. |
| Drop a repo pointer | Say the repo itself is not touched, only the line. Offer to remove the line that points home from that repo, on its cleanup branch. |
| Change anything in the user folder | Say it changes every session the person runs. |
| Remove a suspected secret | Say removal does not undo the leak. The token must be rotated. Offer no history rewrite unless asked. |

Never force past a refusal: report it.

## Child repos

- Work on a new local branch `home-repo/cleanup-<date>`.
- Skip and report a repo with uncommitted changes to tracked files outside `docs/design/`.
- Remove only what the picked rows name. Leave `repo-specific` items.
- A row whose Fix names `/setup-agents-md` stays: name the command.
- A rename changes every place that names the item, in the same commit.

## Report

```text
Fixed 4 of 5.
  1  mcp github          token replaced with ${GITHUB_TOKEN}. Rotate the old token.
  2  skill review-pr     kept home copy, removed from storefront on home-repo/cleanup-2026-11-12
  4  hook block-force-push  registered in .cursor/hooks.json
  5  repo legacy-importer   pointer dropped
Left
  3  repo admin-dashboard   you chose to skip

Check again: 1 finding left, 41 items clean.
Branches to review and push: storefront home-repo/cleanup-2026-11-12
```

Done when the second check is clean, or every row left has a reason beside it.
