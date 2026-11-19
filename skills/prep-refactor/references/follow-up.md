# Follow-up

Work too big for this ticket goes back as a ticket or a spec. It is written to a file, so it outlives the session.

## Route

| The work | Route |
| --- | --- |
| One shape, the files are known, no public contract, one developer can build and check it alone | Ticket |
| A choice between shapes, a public contract, a data change, or an ADR to reverse | Spec |

In doubt: spec. A ticket with a guessed shape grows in the next session too.

## Where

One file per follow-up: `docs/follow-ups/<yyyy-mm-dd>-<slug>.md`. One file each, so two agents at once do not conflict. Commit it with the ticket. Once the follow-up is in the person's tracker or in a design, delete the file.

Make no ticket in a tracker unless the person asks.

## Ticket

```markdown
# <title>

Route: ticket
From: prep-refactor, while building <ticket>
Finding: <finding>. <file:line>.
Landing zone: <files>
Acceptance criteria:
- Behaviour is the same. The tests that cover <zone> pass before and after.
- <the finding is gone, as something a reviewer can check>
Work so far: <branch refactor/<slug>, the tripwire that fired, or none>
```

## Spec

```markdown
# <title>

Route: spec
From: prep-refactor, while building <ticket>
Finding: <finding>. <file:line>.
Landing zone: <files>
Open choices:
- <a shape or decision you saw>
Start: /tech-design new <name>, or a spec in the person's own format
Work so far: <branch, or none>
```

Do not start the spec in this session.

## Handoff

A session that ends after a prep refactor, before the ticket, says one line:

```text
Handoff: <ticket>. Refactor done in <commit hash> on <ticket branch>. Next session: build the ticket on top.
```
