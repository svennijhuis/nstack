# Rollout

The rollout turns the decided standards into tickets, then runs them. Each ticket is one change a subagent can make and prove alone. The main session reviews every diff before it commits. Nothing breaks, nothing is pushed.

## Waves

Tickets run in waves. A wave starts only when every ticket in the wave before it is `done` or `blocked`. Within a wave, tickets with no shared file run in parallel.

| Wave | Holds | Why this order |
| --- | --- | --- |
| 0. Checks | One ticket per missing contract check, run against the unchanged code to record the baseline | Nothing may change before it can be proven unchanged |
| 1. Tools | Linter, formatter, and type checker config for every checkable standard, then their autofix | Cheap, mechanical, and stops new copies at once |
| 2. Exemplars | Rewrite a module into the exemplar where the person accepted a prototype | Every later ticket copies the exemplar |
| 3. Spreading | Standards with danger `bad spreading` | Each day open adds copies |
| 4. Majority | Standards with danger `bad majority` | The next agent copies these first |
| 5. The rest | `bad`, then `inconsistent` | |
| 6. Markers | The frozen and exception markers from [contracts.md](contracts.md) | |
| 7. Tests | The tests area | Earlier tickets are proven by the old tests |
| 8. Docs | Trim `code-standards.md`, write the ADRs | The code now says it |

## Ticket

Each ticket in `rollout.md`:

```markdown
### T-<nnn>: <what changes, in a few words>

Wave: <n>
Gaps: <ids and questions>
Standard: <the standard sentence from align.md, word for word>
Exemplar: <module, by name>
Files: <every file this ticket may change, one per line>
Model: <cheap | mid | main>
Checks: <build, test, lint commands from AGENTS.md, plus each contract check by name>
Do not: change a frozen surface, add a dependency, add or change a migration, change a test's expected value, change any file not listed
Blocked by: <ticket ids, or none>
Status: todo
Commit:
```

- **Size.** One module, or at most about 20 files of one mechanical change. Split anything larger.
- **Files.** Listed by path. A subagent that needs another file stops and reports it. It never edits outside its list.
- **Model.** `cheap` for mechanical work: renames, imports, moving files, applying a config. `mid` for work that needs judgment: error flow, boundaries, adapters, splitting a module. `main` only when the review of a `mid` ticket failed twice and the person asks for it. In Claude Code these are `haiku`, `sonnet`, and the session's own model. In another harness, use its cheapest, middle, and main model.

`rollout.md` starts with the board, then the tickets:

```text
Wave  Ticket  Title                        Model  Status   Commit
0     T-001   API schema snapshot          mid    done     4f2a1c9
3     T-007   Errors: result type, billing mid    blocked  review failed twice: see T-007
```

Statuses: `todo`, `doing`, `review`, `done`, `blocked`.

## Apply

### Start

1. If the status is not `ready` or `applying`, say what it is and stop.
2. If the repo has uncommitted changes to tracked files outside `docs/align/` and `docs/design/`, stop and report them.
3. On the first apply, show the board, the ticket count by wave and model, and the branch name. Wait for a yes. Log `apply approved` with the date. Later sessions do not ask again.
4. Work on a local branch `align/<yyyy-mm-dd>-<name>`, made from the current branch on the first apply. Fill `Branch` in the header. Set `Status: applying`.
5. Run the build, test, lint, and contract checks once. Record anything already red in `log.md`. A ticket may not make it worse.

### Each ticket

1. **Pick.** The first `todo` tickets in the lowest open wave whose blockers are `done` and whose files no `doing` ticket holds. Run up to four at once. Set `doing`.
2. **Brief.** Start one subagent per ticket, with the ticket's model, in its own git worktree from the apply branch when the harness supports it. Otherwise run tickets one at a time in the working tree. Give it the ticket text, the full path to the exemplar, the path to [contracts.md](contracts.md), and nothing from the conversation. It returns its diff and the output of every check.
3. **Review.** In the main session, set `review` and read the diff. It passes only when:
   - every changed line follows the standard and looks like the exemplar
   - no file outside the list changed
   - nothing in the Do not line happened
   - every check passed, and every contract check shows no difference
   - `deslop` finds nothing to remove
4. **Commit or send back.** On a pass, bring the diff into the apply branch, commit only the ticket's files with the message `align: T-<nnn> <title>`, write the commit on the ticket, and set `done`. On a fail, send it back once with the reasons. On a second fail, set `blocked` with the reasons and move on.
5. **Update the board** after each ticket. Nothing lives only in the chat.

A session may stop between tickets at any point. The board says where to start again. A `doing` or `review` ticket from a session that stopped goes back to `todo`, and its worktree is removed.

### The docs ticket

The last wave. The code is the docs now, so most standards lines have nothing left to say.

1. **Trim `docs/agents/code-standards.md`.** For each line, ask: does the code, a lint rule, a type, or a marker now show this? If yes, delete the line. Keep a line only when the code cannot say it. If no line is left, propose deleting the file.
2. **Write the ADRs.** One per area with a decided standard, in `docs/adr/`, in the format of the repo's newest ADR, or the format its `AGENTS.md` Decisions section names. Title: `Code standard: <area>`. Decision is the standard. Why names the principle. Rejected lists each rejected variant and why. Name the exemplar and any frozen or excepted code.
3. **Show both as plan rows** and wait for a yes. The person maintains `code-standards.md`: never trim a line without its row.
4. Commit on a yes. Call `writing-for-agents` on each file first.
5. When the file was deleted or a line it pointed at is gone, tell the person to run `/setup-agents-md` to update the pointer in `AGENTS.md`. This skill never edits `AGENTS.md`.

### Verify and finish

1. Run each survey again on the areas with a decided standard, by [survey.md](survey.md), with the same models.
2. Each area passes when the code shows one variant, apart from the code that carries a frozen or exception marker.
3. An area that fails gets one new ticket per leftover file, in a new wave, and the run stays `applying`.
4. When every area passes and no ticket is `todo`, set `Status: aligned`. Log the counts.
5. Report: tickets done and blocked, files changed, the frozen and excepted code left as it is, and the branch to push.
6. Offer to delete the align folder, as its own question. The ADRs, the lint rules, the markers, and the code now hold every decision. Say that uncommitted files in it are not kept by git.

Never push. The person reviews the branch and pushes.
