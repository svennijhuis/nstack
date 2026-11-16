# Rollout

One ticket, one subagent, one change it can prove alone. The main session reviews every diff. Nothing breaks. Nothing is pushed.

## Waves

A wave starts when the one before it is all `done` or `blocked`. Tickets in a wave with no shared file run in parallel.

| Wave | Holds |
| --- | --- |
| 0. Checks | Every missing contract check, on the unchanged code |
| 1. Tools | Lint, format, and type config for checkable standards, then autofix |
| 2. Exemplars | Prototypes the person accepted, made real |
| 3. Spreading | `bad spreading` |
| 4. Majority | `bad majority` |
| 5. Rest | `bad`, then `inconsistent` |
| 6. Markers | Frozen and exception markers |
| 7. Comments | Deletes by [comments.md](comments.md), then each fix it calls for |
| 8. Tests | The tests area |
| 9. Docs | Trim `code-standards.md`, write the ADRs |

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
- **Model:** `cheap` for mechanical work: renames, imports, moves, config. `mid` for judgment: error flow, boundaries, adapters, splits. `main` only after two failed `mid` reviews, when the person asks. In Claude Code: `haiku`, `sonnet`, the session model.

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
2. **Brief** one subagent each, with its model, in its own worktree when the harness has one, else one at a time. Give the ticket, the exemplar path, the [contracts.md](contracts.md) path, nothing from the conversation. It returns the diff and every check's output.
3. **Review.** Set `review`. Pass only when:
   - every changed line follows the standard and looks like the exemplar
   - no file outside the list changed
   - nothing in Do not happened
   - every check passed, every contract check shows no difference
   - `deslop` finds nothing
4. **Commit** on a pass: only the ticket's files, `align: T-<nnn> <title>`, write the commit, set `done`. A fail goes back once with the reasons. A second fail: `blocked`, with the reasons.
5. **Update the board** after every ticket.

Stop between any two tickets. On resume, `doing` and `review` go back to `todo` and their worktrees are removed.

## Docs

1. **Trim `docs/agents/code-standards.md`.** Delete every line the code, a tool, or a marker now shows. Nothing left: propose deleting the file.
2. **ADRs.** One per area with a standard, in `docs/adr/`, in the repo's ADR format. Title `Code standard: <area>`. Decision, why with the principle, rejected variants, the exemplar, frozen and excepted code.
3. **Show both as plan rows. Wait for a yes.** The person maintains `code-standards.md`: no line goes without its row.
4. `writing-for-agents` on each file. Commit.
5. File gone, or a pointer now stale: tell the person to run `/setup-agents-md`. Never edit `AGENTS.md`.

## Finish

1. Run the surveys again on every area with a standard.
2. Pass: one variant left, apart from marked code.
3. Fail: one ticket per leftover file, in a new wave. Stay `applying`.
4. All pass, nothing `todo`: status `aligned`. Log the counts.
5. Report tickets done and blocked, files changed, marked code left, and the branch.
6. Offer to delete the align folder, as its own question. Say git does not keep its uncommitted files.

Never push.
