# Check

Runs in a subagent with a fresh context. It reads, writes nothing, and returns only the card from [SKILL.md](../SKILL.md#check), at most 15 lines. No file dumps, no code.

Give it the ticket, the mode, and this file.

## 1. Read

Read what exists, skip what does not:

- `AGENTS.md` and `docs/agents/code-standards.md`.
- `GLOSSARY.md` (or `CONTEXT.md`): only the terms the ticket uses.
- The ADRs in `docs/adr/`: titles first, then only the ones that cover the files the ticket touches.
- A design under `docs/design/` that the ticket names. Its decisions outrank your findings.

## 2. Trace

The landing zone: the files the change touches, their direct callers, and their tests. Stop at direct callers.

## 3. Ask

Report a finding only when the ticket would make it worse, or must work around it. Other debt in the zone: leave it.

| Question | Example of a yes |
| --- | --- |
| Would the ticket add an `if`, a flag, or a boolean to code that already branches on a mode? | A fourth `if (type === ...)` in one function |
| Would the ticket add a second way to do something the code already does? | A new fetch helper next to the one in `lib/http.ts` |
| Must the ticket know something the module should hide? | Calling `init()` before `save()`, or reading a private field |
| Must the ticket copy code to reach what it needs? | The same five lines in a third file |
| Can the behaviour the ticket adds be tested where it lives? | No: the logic sits inside a request handler with no seam |
| Is there dead code in the files the ticket changes? | An unused export the ticket would have to update |
| Does the code name a thing differently from `GLOSSARY.md`? | `client` in the code, `customer` in the glossary |
| Does the zone contradict an ADR? | The ADR says one queue, the zone has two |

## 4. Verdict

- `fits`: no finding.
- `prep refactor`: every fix stays inside the files the ticket already changes and their tests, and fits one commit.
- `too big`: anything else. Also: a fix needs a choice between shapes, touches a public contract, or fights an ADR.

In `no-refactor` mode the verdict is `fits` or `too big`.
