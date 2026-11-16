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
| 7. Tests | The tests area |

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
Do not: change a file not listed, change a frozen surface, add a dependency, add or change a migration, change or delete a test's expectation, add a comment [comments.md](comments.md) deletes
Blocked by: <ids or none>
Status: todo
Commit:
```

- **Size:** one module, or at most 20 files of one mechanical change.
- **Files:** needs another file? Stop and report. Never edit outside the list.
- **Model:** `cheap` for mechanical work: renames, imports, moves, comment deletes. `mid` for wave 0 tests. `mid` for judgment: error flow, boundaries, adapters, splits. `main` only after two failed `mid` reviews, when the person asks. In Claude Code: `haiku`, `sonnet`, the session model.

`rollout.md` starts with the board:

```text
Wave  Ticket  Title                         Model  Status   Commit
0     T-001   API schema snapshot           mid    done     4f2a1c9
3     T-007   Errors: result type, billing  mid    blocked  failed review twice
```

Statuses: `todo`, `doing`, `review`, `done`, `blocked`.

## Start

1. Status not `ready` or `applying`: say so and stop.
2. Uncommitted changes to tracked files outside `docs/align/` and `docs/design/`: stop and report.
3. First apply only: show the board, counts by wave and model, and the branch. Wait for a yes. Log `apply approved`.
4. Branch `align/<yyyy-mm-dd>-<name>` from the current branch. Fill `Branch`. Status `applying`.
5. Run every check once. Log what is already red.

## Each ticket

1. **Pick** `todo` tickets in the lowest open wave, blockers `done`, no file held by a `doing` ticket. Up to four. Set `doing`.
2. **Brief** one subagent each, with its model, in its own worktree when the harness has one, else one at a time. Give the ticket and the full paths to the exemplar, [contracts.md](contracts.md), and [comments.md](comments.md). Nothing from the conversation. It returns only: the worktree path, the files changed, one `pass` or `fail` line per check with the first error line, and anything it could not do. Never the full check output. The subagent never commits.
3. **Review.** Set `review`. Run `code-review` on the worktree: fixed point the apply branch head the ticket started from, spec the ticket, standards the area sections of `align.md` and [comments.md](comments.md). Read the diff with `git diff`. Pass only when:
   - every changed line follows the standard and looks like the exemplar
   - no file outside the list changed
   - nothing in Do not happened
   - every check passed, every contract check shows no difference
   - `code-review` reports no standards violation and no smell the ticket added
   - `deslop` finds nothing
4. **Commit** on a pass: apply the worktree diff to the apply branch, stage only the ticket's files, commit `align: T-<nnn> <title>`, write the commit, set `done`, remove the worktree. A fail goes back once with the reasons. A second fail: `blocked`, with the reasons.
5. **Update the board** after every ticket.

Stop between any two tickets. Stop the session after about ten reviewed tickets, so every review gets a clean context. On resume, `doing` and `review` go back to `todo` and their worktrees are removed.

## Finish

1. **Verify.** Run the surveys again on every area with a standard. Pass: one variant left, apart from marked code. Fail: one ticket per leftover file, in a new wave. Stay `applying`.
2. **Lint advice.** Write `lint.md` in the align folder and show it:

   ```text
   Standard        Tool    Rule and setting                                     Catches                 Hits now
   Errors: no null eslint  no-restricted-syntax ReturnStatement > Literal[raw="null"]  return null on failure  0
   Comments        eslint  no-warning-comments ["error", {"terms": ["todo"]}]     TODO                    0
   Naming          none    no tool can check it                                 the check mode covers it  -
   ```

   - One row per standard with `Checked by` set, plus every standard a rule could now check, plus every principle a rule can catch.
   - Use the repo's own linter, formatter, or type checker, or a well-known plugin for it. Name the exact rule id and setting. Never invent a rule: find it in the tool's installed docs or its source.
   - `Hits now`: run the tool once with the rule on the command line, never in a config file. Tool not installed: `-`.
   - No rule fits: say `none`, and that `/align-code check` covers it.
3. **Ask:** "Add these lint rules with a subagent?" Answers: all, the rows you name, or none. Recommend all with 0 hits.
   - On a yes: one ticket, model `cheap`, files: the tool's config only. Checks: lint passes with 0 errors. Review and commit as any ticket: `align: lint rules`.
   - On a no: nothing changes. `lint.md` and the ADRs keep the advice.
4. **Docs.**
   1. Trim `docs/agents/code-standards.md`: delete every line the code, an added lint rule, or a marker now shows. Nothing left: propose deleting the file.
   2. ADRs: one per area with a standard, in `docs/adr/`, in the repo's ADR format. Title `Code standard: <area>`. Decision, why with the principle, rejected variants, the exemplar, frozen and excepted code, and its lint rule: added, or advised and not added.
   3. Show both as plan rows. Wait for a yes. The person maintains `code-standards.md`: no line goes without its row.
   4. `writing-for-agents` on each file. Commit.
   5. File gone, or a pointer now stale: tell the person to run `/setup-agents-md`. Never edit `AGENTS.md`.
5. **Done.** Nothing `todo`: status `aligned`. Log the counts.
6. **Report** tickets done and blocked, files changed, marked code left, lint rules added and advised, and the branch.
7. **Offer** to delete the align folder, as its own question. Say git does not keep its uncommitted files.

Never push.
