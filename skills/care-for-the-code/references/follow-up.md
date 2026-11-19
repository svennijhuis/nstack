# Follow-up

Work that is too big for this ticket goes back into the flow: design, spec, ticket. Pick the lightest route that holds it.

## Route

| The work | Route |
| --- | --- |
| One shape, one module, no public contract, one developer can build and check it alone | Ticket |
| A choice between shapes, more than one module, a public contract, a data change, or an ADR to reverse | Spec: `/tech-design new <name>` |

In doubt: spec. Its grilling finds the shape. A ticket with a guessed shape grows in the next session too.

## Ticket

Same fields as a `tech-design` ticket:

```markdown
### <title>

- From: care-for-the-code, while building <ticket>
- Finding: <finding>. Source: <source>.
- Landing zone: <files>
- Acceptance criteria:
  - Behaviour is the same. The tests that cover <zone> pass before and after.
  - <the finding is gone, as something a reviewer can check>
- Story points: <estimate>
- Blockers: <tickets, or none>
- Work so far: <stash name or commit hash, and the tripwire that fired, or none>
```

Where it goes:

- The ticket came from a `tech-design` folder: append it under `## Follow-ups` at the end of that folder's `tickets.md`. Make the heading when it is not there. Change nothing else in that folder.
- Otherwise: in your reply, for the person's tracker. Make no ticket in a tracker unless the person asks.

## Spec

Do not start the design in this session. Write a brief the next session starts from:

```markdown
Start: /tech-design new <name>
Why: <finding>, found while building <ticket>. Source: <source>.
Landing zone: <files>
Open choices: <the shapes or decisions you saw, one line each>
Work so far: <stash name or commit hash, or none>
```

Where it goes: the same place as a ticket. Under `## Follow-ups`, it is one line linking the brief, and the brief itself in the reply.

## Handoff

When a session ends after a prep refactor and before the ticket, write one line in the reply and, for a `tech-design` ticket, under `## Follow-ups`:

```text
Handoff: <ticket>. Refactor done in <commit hash>. Next session: build the ticket on top.
```
