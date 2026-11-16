# Ready gate

Proves every area has a standard, every change is a ticket, and nothing can break a contract. Changes no code. Closes no gap.

## Run

1. Draft the tickets: call `to-tickets` for the slicing and to check the breakdown with the person. A rename or retype across many callers is expand-contract: add the new form, move callers in batches, delete the old form. Write each ticket in the [rollout.md](rollout.md) shape, with its file list, not to a tracker. Do not write them to disk yet.
2. Walk every check. Print `pass` or `fail` with file, line, and what is wrong. Run all of them, even after a fail.
3. Nothing to check is a fail.
4. Any fail: status unchanged. A missing fact or decision becomes a gap. Say what to run next.

## Checks

### Map

1. Every entry [structure.md](structure.md) creates at chart exists.
2. Every header field has a value. `Branch` may be empty.
3. Every area has its section. None is blank.
4. No gap is `open`, `research`, or `waiting-on-input`.
5. Every `accepted-risk` gap has an owner and names the risk.
6. Not yet specified is `None.`
7. No survey is older than the last code commit in scope. Older: run it again.

### Standards

8. Every section is `consistent`, `n/a` with a reason, or a standard with every field.
9. Every exemplar exists in the code, or is an accepted prototype. `none` only for a rule of absence.
10. Every outcome fits [contracts.md](contracts.md).
11. Every `new-only` and `exception` has a reason.
12. Every standard a tool can check names its rule under `Checked by`, for the advice at the end. None named: fail.
13. No two standards contradict.

### Contracts

14. Every frozen surface in scope has a check, or a wave 0 ticket.
15. No ticket changes a frozen surface.
16. Every file a code-changing ticket lists is run by a check, or by a wave 0 test.

### Tickets

17. Every file under `Changes` is in exactly one ticket per standard.
18. Every ticket has every field.
19. Two tickets that share a file are in different waves, or one blocks the other.
20. Tests tickets are in the tests wave.
21. No `TBD`, `TODO`, `???`, or unfilled `<...>`.

## Pass

1. Status `ready`. `Updated` today.
2. Write `rollout.md`.
3. Log. Say the ticket count by wave and `/align-code <name> apply`.

There is no `ready anyway`. A gap the person will not decide is closed as `accepted-risk`, with them as owner.
