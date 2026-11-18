# Ready gate

`design.md` is the spec. Ready proves a developer can build from it without guessing, so the business and the lead developer can review it. The design is the goal. Ready closes no gap.

## How to run the gate

Walk every check below, in order. Print one line per check: `pass` or `fail`, and for a fail the file, the line, and what is wrong. Run all checks even after a fail, so the human sees the whole list once.

A check with nothing to check is a fail, not a pass. No requirements, no acceptance criteria, or a required diagram that is not drawn fails every check that reads them. Write `fail: nothing to check`.

Any fail stops ready. Leave the status unchanged. Each fail that is a missing fact or decision becomes a gap row. End by saying how many checks failed and what to run next.

## Checks

### Structure

1. The folder holds every entry in [structure.md](structure.md).
2. The `design.md` header and `state.md` have every field, in order, with a value.
3. All 15 sections are present, in order, with the exact headings.
4. No section is blank. Every `n/a` has a reason. No `n/a` sits in a section the size forbids, see [sizes.md](sizes.md).
5. `design.md` is within the line budget for its size.

### Gaps

6. No row in `gaps.md` is `open`, `research`, or `waiting-on-input`.
7. Every `accepted-risk` row has an owner and names the risk.
8. Open questions reads `None.` On `ready anyway` only, it may hold rows the human accepted.
9. The sweep in [gap-sweep.md](gap-sweep.md), run again against the finished document, finds no new gap.

### Wording

10. No placeholder remains: `TBD`, `TODO`, `???`, or an unfilled `<...>`.
11. No vague word stands without a number in a requirement or criterion row: fast, scalable, robust, secure, intuitive, user-friendly, efficient, appropriate, as needed, etc.
12. Every term used in two places means the same thing, and is in `glossary.md`.
13. Each fact, number, and decision is stated once in `design.md`, in the section that owns it. Owners: behaviour and internal numbers in Requirements, vendor limits in Dependencies, alert and log thresholds in Observability, flows in Design, failures in Failure modes, the choice and its reason in Decisions. Other sections refer to the owner by section name or by `R-` id. Restating is allowed only in these places: the Summary, one Decisions row per decision, the table or list directly under a diagram as its text twin, and an acceptance criterion, which repeats the number it tests. A restated number must match its owner. A fail names both places and says which copy to cut.
14. No em dash or en dash.

### Requirements

15. Every requirement has an `R-` id, one behaviour, and MUST in capitals. No "should".
16. Every number in a requirement is tagged `measured` or `decided`. None is `guessed`.
17. Every `R-` id is cited by at least one `AC-`. Every `AC-` cites at least one `R-` and names its test kind.
18. Every acceptance criterion can fail: it names an observable result.

### Design

19. Every diagram whose trigger fires is present, see [diagrams.md](diagrams.md).
20. Every diagram has `accTitle`, a lead-in sentence, labelled one-way arrows, and a text twin that agrees with it.
21. Every arrow that crosses a boundary carries an auth level.
22. Every sequence diagram for type `api` or `integration` shows a failure path.
23. Every actor in a diagram is in Actors. Every outside system in a diagram is in Dependencies. A system inside this codebase's boundary, such as its own database or secret store, is an actor of type system. A system outside it is a dependency. Never both.
24. Every Dependencies row has every field filled and a proof, see [dependency-contract.md](dependency-contract.md).
25. Every outside call and every dependency has a Failure modes row.
26. Alternatives includes "do nothing". Assumptions and risks has an owner on every row.
27. The type requirements in [sizes.md](sizes.md) are met for each type in `state.md`.

### Prose

28. `design.md` follows the `technical-writing` skill. Read the skill, then check each section against its rules. A fail names the file, the line, and the rule broken.
29. Run the `unslop` skill over `design.md` and every file in the folder. This check goes last. It passes when unslop finds nothing left to fix. A fail lists each file and line it would change.

When the skill a check needs is not installed, that check fails: `fail: <skill> not installed`. Name `/setup-nstack-skills`.

## Ready anyway

`/tech-design <name> ready anyway` lets the human go ready while gaps are open. Use it only when the human types it. Never suggest it. Never accept a risk for them.

1. Run the whole gate first and print it.
2. Checks 1 to 5 and 10 to 29 still stop ready. Only the gap checks 6, 8, and 9 can be accepted. If any other check fails, stop here: accept nothing, write nothing, and leave the status unchanged. Steps 3 to 7 run only when every other check passes.
3. For each open, research, or waiting gap, and each fog line, show: the question, what a builder would have to guess, what goes wrong if the guess is wrong, the possible answers (the options from the advice or research), and the follow-up action that would settle it, with who does it.
4. Ask the human to accept each one by name, one at a time. "Accept all" is not an answer.
5. For each accepted gap, set `accepted-risk`, with the human as owner, today's date, and the risk in the answer cell. A fog line they accept becomes a gap row first.
6. A gap they do not accept stops ready.
7. Add `Open at ready: <n>` to `state.md`. Fill `## Open questions` with one table row per accepted gap, written for a business reader like the rest of `design.md`, with no gap ids, in the columns of [structure.md](structure.md). The owner is who must settle it. Log who accepted the risk in `log.md`.

## After the gate passes

1. Set `Status: ready` and `Updated`.
2. Append one `log.md` line. Tell the human the design is ready for review by the business and the lead developer. Stop.

Ready is done when the status is `ready` and no gap status changed, except those the human accepted. A reviewer who rejects the design sends it back to `discussion`.
