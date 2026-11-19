# With verify-flow

Both skills start when a ticket that changes code is picked up. `care-for-the-code` checks the shape of the code. `verify-flow` checks the stored state. They split the work so that neither reads the code twice and the session does not grow from both.

## Who does what

| Question | Skill |
| --- | --- |
| Does the code the ticket lands in hold it for the long term? | `care-for-the-code` |
| Which files, jobs, and caches write the resource? | `care-for-the-code` finds them, on the card's `State:` line |
| `skip`, `partial`, or `full`? | `verify-flow`. Never `care-for-the-code` |
| Does a refactor keep the state behaviour? | `verify-flow`: its triage on the refactor diff alone must be `skip` |
| A broken path that reproduces | `verify-flow`: a regression test |
| A finding that is too big for this ticket | `care-for-the-code`: a follow-up |

## Order

1. The `care-for-the-code` check. The card's `State:` line names the resource and its other writers, with file paths.
2. `/verify-flow before <resource>`. Hand it the `State:` line as its triage facts: the file paths are the evidence it asks for. Its rule still holds: a writer it finds that the card missed can only raise its level.
3. The prep refactor, after a yes. When the triage is `full`, the model, the refactor, and the ticket do not fit one session: route the refactor by [follow-up.md](follow-up.md), or commit it and hand off by [follow-up.md](follow-up.md#handoff) before the ticket.
4. The ticket.
5. `/verify-flow after <resource>`.
6. No worse: the last step of the flow in [SKILL.md](../SKILL.md#flow).

`State: none`: skip steps 2 and 5. `verify-flow` not installed: skip them and say so once.

## Session budget

- `verify-flow` `full`: no prep refactor in the same session.
- `verify-flow` `partial`: a prep refactor only when it is small by the rules in [SKILL.md](../SKILL.md#rules).
- `verify-flow` `skip`: nothing changes.

## Follow-ups

A `verify-flow` `after` that ends in `bug` or `blocked` is its own report, not a `care-for-the-code` finding. When the fix is too big for this ticket, route it by [follow-up.md](follow-up.md) and link the `report.md`.
