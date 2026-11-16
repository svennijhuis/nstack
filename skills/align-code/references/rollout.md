# Rollout

One ticket, one subagent, one change it can prove alone. The main session reviews every diff. Nothing breaks. Nothing is pushed.

## Waves

A wave starts when the one before it is all `done` or `blocked`. Tickets in a wave with no shared file run in parallel.

| Wave | Holds |
| --- | --- |
| 0. Checks | Every missing contract check and characterization test, on the unchanged code |
| 1. Exemplars | Prototypes the person accepted, made real |
| 2. Spreading | `bad spreading` |
| 3. Majority | `bad majority` |
| 4. Rest | `bad`, then `inconsistent` |
| 5. Markers | Frozen and exception markers |
| 6. Comments | Deletes by [comments.md](comments.md), then each fix it calls for |
| 7. Tests | Tickets that align the tests area. Never a wave 0 test. |

No ticket changes lint, format, or type checker config. Those come as advice at the end.

## Ticket

```markdown
### T-<nnn>: <title>

Wave: <n>
Gaps: <ids and questions>
Standard: <from align.md, word for word>
Exemplar: <module>
Files: <every file it may change, one per line>
Model: <cheap | mid | main>
Checks: <commands from AGENTS.md, plus each contract check>
Do not: change a file not listed, or anything under "A ticket never" in contracts.md
Blocked by: <ids or none>
Status: todo
Worktree:
Commit:
```

- **Size:** at most 20 files. One exception: an internal rename or retype is one ticket however many files, because every caller, tests included, changes in the same commit by [contracts.md](contracts.md). Past 20 files it gets model `mid`, runs alone, blocks every ticket that shares a file, and is reviewed 20 files at a time.
- **Files:** needs another file? Stop and report. Never edit outside the list. Leave existing comments: they belong to the comments wave.
- **Model:** `cheap` for mechanical work up to 20 files: renames, imports, moves, comment deletes. `mid` for wave 0 tests. `mid` for judgment: error flow, boundaries, adapters, splits. `main` only for a `blocked` ticket the person sends back. In Claude Code: `haiku`, `sonnet`, the session model.

`rollout.md` starts with the board:

```text
Wave  Ticket   Title    Model                  Status    Commit
<n>   T-<nnn>  <title>  <cheap | mid | main>  <status>  <hash, or the reason it is blocked>
```

Statuses: `todo`, `doing`, `review`, `done`, `blocked`. A `blocked` ticket goes back to `todo` only when the person asks, with model `main`.

## Start

1. Status not `ready` or `applying`: say so and stop.
2. Status `applying`: check out `Branch`. Runs before step 3. Missing: stop and report. Then each `doing` or `review` ticket:
   - `git log` has its `align: T-<nnn>` commit: write the commit, set `done`.
   - It has a `Worktree`: remove that worktree, set `todo`.
   - Neither: show `git status` and ask whether those changes are this ticket's leftovers. Yes: undo as in [Each ticket](#each-ticket) step 5, set `todo`. No: stop and report.
3. After step 2, any uncommitted changes to tracked files, or untracked files, left outside `docs/align/` and `docs/design/`: stop and report.
4. Status `ready`, the first apply: show the board, counts by wave and model, and the branch. Wait for a yes. Log `apply approved`. Create `align/<yyyy-mm-dd>-<name>` from the current branch. Fill `Branch`. Status `applying`.
5. Run every check once. Log what is already red.

## Each ticket

1. **Pick** `todo` tickets in the lowest open wave, blockers `done`, no file held by a `doing` ticket. Set `doing`. With worktrees: up to four. Without: one.
2. **Brief** one subagent each, with its model. With worktrees: each in its own, its path written to `Worktree` first. Without: on the apply branch itself. Give the ticket and the full paths to the exemplar, [contracts.md](contracts.md), and [comments.md](comments.md). Nothing from the conversation. It returns only: the worktree path or `none`, the files changed, one `pass` or `fail` line per check with the first error line, and anything it could not do. Never the full check output. The subagent never commits.
3. **Review.** Set `review`. Run `code-review` on the change: fixed point the apply branch head the ticket started from, spec the ticket, standards the area sections of `align.md` and [comments.md](comments.md). Read the diff with `git diff`. Pass only when:
   - every changed line follows the standard and looks like the exemplar
   - no file outside the list changed
   - nothing in Do not happened
   - every check passed, every contract check shows no difference
   - `code-review` reports no standards violation and no smell the ticket added
   - `deslop` finds nothing
4. **Commit** on a pass: with a worktree, apply its diff to the apply branch and remove it. Stage only the ticket's files, commit `align: T-<nnn> <title>`, write the commit, clear `Worktree`, set `done`.
5. **Fail:** undo first. With a worktree: remove it, clear `Worktree`. Without: `git restore --staged --worktree -- . ':!docs/align' ':!docs/design'`, then `git clean -fd -- . ':!docs/align' ':!docs/design'`. Start step 3 made sure nothing else was there. The first fail goes back once with the reasons. A second fail: `blocked`, with the reasons.
6. **Update the board** after every ticket.

Stop between any two tickets. Stop the session after 10 reviewed tickets, so every review gets a clean context. On resume, Start step 2 undoes `doing` and `review` tickets.

## Finish

1. **Verify.** Run the surveys again on every area with a standard. Pass: one variant left, apart from marked code. Fail, the first time: one ticket per leftover file, in one new wave. Stay `applying`. Fail after that wave: set those files' tickets `blocked` and ask the person.
2. **Lint advice.** Write `lint.md` in the align folder and show it:

   ```text
   Standard  Tool             Rule and setting                 Catches   Hits now
   <area>    <tool, or none>  <exact rule id and its setting>  <what>    <n, or ->>
   ```

   - One row per standard.
   - Use the repo's own linter, formatter, or type checker, or a well-known plugin for it. Name the exact rule id and setting. Never invent a rule: find it in the tool's installed docs or its source.
   - `Hits now`: run the tool once with the rule on the command line, never in a config file. Tool not installed: `-`.
   - No rule fits: say `none`, and that `/align-code check` covers it.
3. **Ask:** "Add these lint rules with a subagent?" Answers: all, the rows you name, or none. Recommend all with 0 hits.
   - On a yes: one ticket, model `cheap`, files: the tool's config only. Checks: lint passes with 0 errors. Review and commit as any ticket: `align: lint rules`.
   - On a no: nothing changes. `lint.md` and the ADRs keep the advice.
4. **Docs.**
   1. Trim `docs/agents/code-standards.md`: delete every line the code, an added lint rule, or a marker now shows. Nothing left: propose deleting the file.
   2. ADRs: one per area with a standard, in `docs/adr/`, in the repo's ADR format. Title `Code standard: <area>`. Decision, why with its source, rejected variants, the exemplar, frozen and excepted code, and its lint rule: added, or advised and not added.
   3. Show both as plan rows. Wait for a yes. The person maintains `code-standards.md`: no line goes without its row.
   4. `writing-for-agents` on each file. Commit.
   5. File gone, or a pointer now stale: tell the person to run `/setup-agents-md`. Never edit `AGENTS.md`.
5. **Done.** Nothing `todo` or `blocked`, and Verify passed: status `aligned`. Else stay `applying`. Log the counts.
6. **Report** tickets done and blocked, files changed, marked code left, lint rules added and advised, and the branch.
7. **Offer** to delete the align folder, as its own question. Say git does not keep its uncommitted files.

Never push.
