---
name: care-for-the-code
description: Use when you start a ticket, issue, or task that changes code, before you write it, and when the ticket is itself a refactor. Also when the user asks to scan a path for refactor candidates. Checks whether the code the change lands in will hold it for the long term, and refactors first when it will not.
---

The ticket is the tactical goal. The codebase is the strategic one. A ticket is not done when it works but leaves the code harder to change. Make the change easy, then make the easy change.

Run this before you write code for a ticket. Show the card. Then build.

## Rules

- **Behaviour stays.** A prep refactor never changes behaviour, a public API, a schema, a config name, or a UI. It is its own commit, before the ticket's commit. Tests pass before and after it.
- **Only the landing zone.** Refactor only code the ticket touches or calls. Anything wider is `too big`.
- **ADRs win.** Never refactor against an ADR in `docs/adr/`. When the code fights an ADR, ask the person.
- **Never invent.** Every finding cites a source: a `codebase-design` term, an ADR, a glossary term, or a line in `docs/agents/code-standards.md`. No source: no finding.
- **An unknown is a question.** Ask the person. Never guess.

## 1. Read

Read what exists, skip what does not:

- `AGENTS.md` and `docs/agents/code-standards.md`.
- `GLOSSARY.md` (or `CONTEXT.md`): the terms the ticket uses.
- The ADRs in `docs/adr/` that cover the code the ticket touches.
- The design folder under `docs/design/` when the ticket came from `tech-design`. Its decisions outrank your findings.

## 2. Trace

List the landing zone: the modules the change touches, their callers, and their tests. Run `git log --oneline -20 -- <files>` on them. Many fixes in one file is a signal, not a finding.

## 3. Check

Ask each question about the landing zone. A yes is a finding, with its source.

| Question | Source |
| --- | --- |
| Is a module shallow: its interface nearly as complex as what it hides? Delete it in your head. If the complexity does not come back in its callers, it was a pass-through. | `codebase-design`: depth, deletion test |
| Does a caller have to know things the module should hide (order of calls, internal state, a flag)? | `codebase-design`: interface, locality |
| Would the ticket add an `if`, a flag, or a boolean to code that already branches on a mode? Would you build it this way if the requirement had been there from the start? | `codebase-design`: depth |
| Does the ticket add a second way to do something the code already does? | `align-code` |
| Does one piece of state have more than one owner? | `codebase-design`: locality |
| Is there dead code, an unused export, or a stale wrapper in the zone? Remove it before you add. | `codebase-design`: leverage |
| Can the behaviour the ticket adds be tested at the module's interface? No seam means no test. | `codebase-design`: seam, adapter |
| Does the code name a thing differently from `GLOSSARY.md`? | `domain-modeling` |
| Does the zone contradict an ADR? | the ADR |

## 4. Verdict

One of three:

- **`fits`**: no finding, or none the ticket makes worse. Build it.
- **`prep refactor`**: a finding inside the landing zone that the ticket would make worse, small enough to fix in this ticket. Refactor first, by [Prep refactor](#prep-refactor), then build.
- **`too big`**: the fix touches code the ticket would not, changes a public contract, or is bigger than the ticket itself. Do not start it. Ask the person, one question, three options:
  - A. Build the ticket now, leave the code no worse, and write the follow-up ticket in your reply.
  - B. Refactor first, as its own ticket.
  - C. Design it with `/tech-design`.

### The card

```text
care-for-the-code: <ticket>
Landing zone: <modules>
Findings:
- <finding>: <files>. Source: <source>.
Verdict: fits | prep refactor | too big
Plan: <the refactor in one line, then the ticket>. Or: <the question, A/B/C>.
```

`fits` with no findings is one line: `care-for-the-code: fits, <why in a few words>.`

With `prep refactor`, wait for a yes before you change code, unless the person said to go ahead without asking.

## Prep refactor

1. No test covers the behaviour you will move? Write a characterization test first: it pins what the code does today. Run it.
2. Refactor in the smallest steps that each leave the tests green.
3. Move every caller to the new interface and delete the old one in the same change. No compatibility layer for code only we call.
4. Test at the interface, not the inside. Delete tests that only pinned the old inside.
5. Commit: `refactor: <what>, to make room for <ticket>`. Then build the ticket on top.

## When the ticket is a refactor

The destination is a deeper module, with the same behaviour. Run 1 to 3 to find the shape. Sketch two interfaces and pick the one that hides the most from its callers, by `codebase-design`. Then follow [Prep refactor](#prep-refactor) for the whole ticket.

## What to keep

- The person rejects a finding for a reason that will hold next time: offer an ADR, so the next agent does not raise it again. Use the format of the newest ADR in `docs/adr/`.
- A refactor makes a real decision (a new seam, a module split, a rejected shape): write the ADR in the same change, by the repo's `AGENTS.md`.
- A new or renamed term: update `GLOSSARY.md` in the same change.

## Scan

`/care-for-the-code scan [path]` looks for candidates without a ticket. Write nothing.

1. Scope: the path, or the files with the most commits in `git log --since=3.months --name-only`.
2. Read by [1. Read](#1-read). Then a subagent with a fresh context walks the scope and asks the questions in [3. Check](#3-check).
3. List at most 10 candidates, strongest first:

```text
<n>. <module>: <finding>. Source: <source>.
   Before: <shape now, one line>. After: <shape after, one line>.
   Strength: Strong | Worth exploring | Speculative.  Size: one ticket | tech-design.
```

4. Ask which one to explore. Do not propose interfaces before the person picks one. Then call `grilling` and `codebase-design` to shape it. It ends as a ticket, or as a `/tech-design`.

## Companion skills

Call by exact name: `codebase-design`, `grilling`, `domain-modeling`, `align-code`, `tech-design`, `comment-root-cause`. If one is missing, say so once, name `/setup-nstack-skills`, and go on by these rules.

## When this is the wrong answer

- A one-line fix, a typo, or a config value: say `fits` and build.
- A hotfix in production: build the fix, and write the follow-up ticket in your reply.
