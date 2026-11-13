# Cleanup

`/setup-home-repo cleanup` fixes what advise found. It runs advise first, lets the person pick, applies, and checks again.

## Steps

1. **Run advise** by [advise.md](advise.md). Number the rows.
2. **Ask which rows to fix.** Recommend all rows of severity high and up. The person answers with numbers, `all`, or `none`.
3. **Show what each picked row will change**: the files, and for a removal, what is removed and from where.
4. **Apply in the order below.** Stop at the first failure and report.
5. **Check again.** Run the checks for the rows you touched.
6. **Commit and report.** One commit in the home repo. One commit on a new local branch in each child repo that changed. Do not push.

## Order

Do the safe fixes first, so a stop halfway leaves nothing broken.

1. Additions: a missing `CLAUDE.md`, a missing hook registration, a missing map line, a missing environment entry.
2. Corrections: a pointer path, a renamed skill in the map, a script made executable.
3. Moves: a procedure out of `AGENTS.md` into a skill, pointers into `repos/` files.
4. Removals: a duplicate copy, a dead pointer, a merged worktree, a file for an unused harness.

## Ask again before each of these

A yes to the list is not a yes to these. Confirm each one by name.

| Action | Before you do it |
| --- | --- |
| Remove a file or folder | Show the path. For a duplicate, confirm the kept copy has the same content. If it differs, stop and ask which wins. |
| Remove a worktree | Run `git status` in it. Any uncommitted or unpushed work means do not remove it. Report it. |
| Drop a repo pointer | Say the repo itself is not touched, only the line. |
| Change anything in the user folder | Say it changes every session the person runs. |
| Remove a suspected secret | Say removal does not undo the leak. The token must be rotated. Offer no history rewrite unless asked. |

Never use a force flag to get past a refusal. A refusal is a finding to report.

## Child repos

- Work on a new local branch, `home-repo/cleanup-<date>`.
- Skip a repo with uncommitted changes and report it.
- Remove only what the picked rows name. Leave everything bucketed `repo-specific`.

## The router

Every removal and rename changes the map in the same commit. After the last row, read the map top to bottom once: no line may name an item that is gone.

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
