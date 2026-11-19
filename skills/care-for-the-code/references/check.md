# Check

The check runs in a subagent with a fresh context, so the session that builds the ticket keeps its context for the ticket. The subagent reads, writes nothing, and returns only the card.

## Brief

Give the subagent:

- the ticket text, or its link and acceptance criteria
- the mode
- the path of the design folder, when the ticket came from `tech-design`
- this file

Ask for the card from [SKILL.md](../SKILL.md#the-card), at most 15 lines. No file dumps, no code.

## 1. Read

Read what exists, skip what does not:

- `AGENTS.md` and `docs/agents/code-standards.md`.
- `GLOSSARY.md` (or `CONTEXT.md`): only the terms the ticket uses.
- The ADRs in `docs/adr/` that cover the code the ticket touches. Read their titles first, then only the ones that match.
- The design folder, when given. Its decisions outrank your findings.

## 2. Trace

List the landing zone: the modules the change touches, their direct callers, and their tests. Stop at direct callers. Run `git log --oneline -20 -- <files>`. Many fixes in one file is a signal, not a finding.

## 3. Ask

A yes is a finding, with its source. Report only findings the ticket touches or would make worse. Other debt in the zone is one line at most, as a scan candidate.

| Question | Source |
| --- | --- |
| Is a module shallow: its interface nearly as complex as what it hides? Delete it in your head. If the complexity does not come back in its callers, it was a pass-through. | `codebase-design`: depth, deletion test |
| Does a caller have to know things the module should hide (order of calls, internal state, a flag)? | `codebase-design`: interface, locality |
| Would the ticket add an `if`, a flag, or a boolean to code that already branches on a mode? Would you build it this way if the requirement had been there from the start? | `codebase-design`: depth |
| Does the ticket add a second way to do something the code already does? | `align-code` |
| Does one piece of state have more than one owner? | `codebase-design`: locality |
| Is there dead code, an unused export, or a stale wrapper in the zone? | `codebase-design`: leverage |
| Can the behaviour the ticket adds be tested at the module's interface? No seam means no test. | `codebase-design`: seam, adapter |
| Does the code name a thing differently from `GLOSSARY.md`? | `domain-modeling` |
| Does the zone contradict an ADR? | the ADR |

## 4. Verdict

- `fits`: no finding the ticket makes worse.
- `prep refactor`: every fix stays inside the files the ticket already changes and their tests, fits one commit, and is smaller than the ticket.
- `too big`: anything else. Also: a fix needs a choice between shapes, touches a public contract, or fights an ADR.

In `no-refactor` mode the verdict is `fits` or `too big`, never `prep refactor`.
