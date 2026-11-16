# Ready gate

Ready proves the plan is complete: every area has a standard, every change is a ticket a subagent can do without guessing, and nothing can break a contract. Then it writes `rollout.md`. Ready changes no code and closes no gap.

## How to run the gate

Draft the tickets by [rollout.md](rollout.md) first, without writing them to disk. Then walk every check below, in order. Print one line per check: `pass` or `fail`, and for a fail the file, the line, and what is wrong. Run all checks even after a fail, so the person sees the whole list once.

A check with nothing to check is a fail: `fail: nothing to check`. Any fail stops ready and leaves the status unchanged. Each fail that is a missing fact or decision becomes a gap row. End with how many checks failed and what to run next.

## Checks

### Structure

1. The folder holds every entry [structure.md](structure.md) creates at chart.
2. The header has every field, in order, with a value. `Branch` may be empty.
3. Every area in [survey.md](survey.md), plus any added in `log.md`, has its section, and none is blank.

### Gaps

4. No row in `gaps.md` is `open`, `research`, or `waiting-on-input`.
5. Every `accepted-risk` row has an owner and names the risk.
6. Not yet specified reads `None.`
7. Every survey is newer than the last commit that changed code in the scope. When the code moved on, run that survey again first.

### Standards

8. Every area section is `consistent`, `n/a` with a reason, or a decided standard with every field filled.
9. Every decided standard names an exemplar that exists in the code, or a prototype the person accepted.
10. Every outcome is `apply`, `adapter`, `new-only`, or `exception`, and matches [contracts.md](contracts.md).
11. Every `exception` and every `new-only` has a reason on its gap row.
12. Every standard a linter, formatter, or type checker can enforce names that rule under `Checked by`. A checkable standard with no rule fails.
13. No two standards contradict each other.

### Contracts

14. Every frozen surface the scope touches has a contract check that exists, or a check ticket in the first wave.
15. No ticket's file list or rule changes a frozen surface.

### Tickets

16. Every file listed under `Changes` in a decided standard is in exactly one ticket per standard.
17. Every ticket has every field in [rollout.md](rollout.md).
18. Two tickets that share a file are never in the same wave without one listing the other under `Blocked by`.
19. Tests-area tickets sit in the last wave before the docs ticket.
20. No placeholder remains in `align.md` or the drafted tickets: `TBD`, `TODO`, `???`, or an unfilled `<...>`.

## After the gate passes

1. Set `Status: ready` and `Updated`.
2. Write the drafted tickets to `rollout.md`.
3. Append one `log.md` line. Stop. Tell the person the ticket count by wave and to run `/align-code <name> apply`.
