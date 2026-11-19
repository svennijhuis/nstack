---
name: implement
description: Use when you implement a ticket, issue, spec, feature, or bug fix in code. Builds it so the codebase gets better, not worse: refactors first where the change needs it, builds test-first, gets an independent review, and proves it works.
---

The ticket is the tactical goal. The codebase is the strategic one. Make the change easy, then make the easy change. Every ticket leaves the code it touches:

- **deeper**: modules that hide more behind a smaller interface
- **better tested**: behaviour you touch has a test through its interface
- **cleaner**: no comment that covers a shortcut
- **in the domain's words**: names from the glossary, choices that follow the ADRs

Be the colleague who says "we need to refactor this first", out loud and before the code. One ticket per session.

A companion skill below is missing: read [fallbacks.md](references/fallbacks.md) once, and follow it for each missing one.

## 1. Read

- **The ticket.** A reference: fetch it by `docs/agents/issue-tracker.md`, or from `.scratch/<feature>/issues/`. Say its title. It matches more than one: ask which.
- **Its spec**, only the one the ticket names or its parent. Its decisions outrank your taste. A spec the ticket does not name does not bind it. Which sections hold decisions: [spec.md](references/spec.md).
- **The repo.** `AGENTS.md`, `docs/agents/code-standards.md`, the glossary terms the ticket uses (`GLOSSARY.md`, `CONTEXT.md`, or by `GLOSSARY-MAP.md`), the ADRs whose titles match the code you change.
- **The code.** Where the change lands, its direct callers, their tests. Stop there. `git log --oneline -20 -- <files>`.
- **Git.** On the default branch: branch first. Note the start commit. Never push.

A bug: [bug.md](references/bug.md) before 2. A ticket that is itself a refactor: [refactor-ticket.md](references/refactor-ticket.md). Stored state written and `verify-flow` installed: [stored-state.md](references/stored-state.md).

## 2. Shape

If this requirement had been there from the start, what would this code look like? A refactor comes first when, without one, you would:

- add an `if` or a flag to code that already branches on a mode
- add a second way to do something the code already does, or copy code
- make a caller know what a module should hide
- put logic where no test can reach it through an interface
- work around a name, type, or module that no longer fits

On a signal, shape it with `codebase-design`. Put code where its meaning belongs: the module its name, glossary term, or ADR covers.

Caring is not adding layers. No new module that fails the deletion test. No seam (a place tests or adapters swap behaviour) unless the spec names it or two things vary across it. No option nothing uses.

**Say the call** in one line, then go on: "Refactor first: <what>, because <signal>." or "Fits as it is: <why>."

## 3. Refactor first

Only the code the change lands in. Same behaviour, API, schema, and UI. Pin untested behaviour first, then small green steps. Move every caller and delete the old shape, unless the ticket is an expand step. Commit it green as `refactor: <what>` before you build.

## 4. Build

`tdd` at the spec's seams. It asks you to confirm seams when the spec names none: propose the public functions the ticket changes. Tests go through the interface; testing past it means the shape is wrong. Behaviour you touched without a test gets one. Run the test file often. Every comment, `TODO`, or suppression you write or edit goes through `comment-root-cause`.

## 5. Review with fresh eyes

You do not judge your own code. Start at once, each in a fresh subagent, given only the diff from the start commit, the ticket, and the paths to the spec and the docs, never your reasoning:

- `code-review`: Standards and Spec
- the design reviewer: [design-review.md](references/design-review.md)

No subagent tool: say the review is not independent, and run both yourself.

## 6. Fix

- A claimed bug counts only when a test or command shows it. It does not: drop it and name it. It does: keep the test, fix it.
- Other findings in the ticket's files: fix, behaviour the same. A fix to the feature's code goes in the feature commit, a fix to older code in its own `refactor:` commit.
- Outside the ticket's files, or against the spec or an ADR: name it, do not fix it.
- One you think is wrong: say why. Never drop one silently.
- One round. A second only when the fixes changed the shape.

## 7. Finish

1. A real decision: an ADR. A new term: the glossary. Both by `AGENTS.md`, in the same change.
2. Full suite and typecheck. Then run the real thing the ticket changed and read its output: green tests are not the proof.
3. Commit the feature on top of the refactor commit.
4. Summary, by [finish.md](references/finish.md): the call, the safety fact, `/blast-radius` or not, findings, what you saw outside the ticket.

## Decide, or ask

Ask only for: a behaviour or contract change the ticket and spec do not cover, a shape against an ADR or the spec, a new seam the spec did not name, the seams `tdd` asks for, two shapes equal for the long term. Decide everything else and name it: a test the ticket changes on purpose, a detail the ticket leaves open (match the code around it), whether a choice is an ADR.

## Companion skills

`codebase-design`, `tdd`, `comment-root-cause`, `code-review`, `diagnosing-bugs`, `verify-flow`, by exact name, each only on its step. `blast-radius` and `pr` are the person's: suggest `blast-radius`, never call either.
