---
name: implement
description: Use when you implement a ticket, issue, spec, feature, or fix in code. Builds it so the codebase gets better over time, not worse. Reads the ticket and its spec, shapes the code the change lands in as if the requirement had been there from the start, refactors where the change needs it, builds with tdd at the agreed seams, and ends with a review and a commit.
---

The ticket is the tactical goal. The codebase is the strategic one. A ticket is not done when it works but leaves the code harder to change. Make the change easy, then make the easy change.

## 1. Read

- **The ticket.** A ticket reference: fetch it from the issue tracker, or from `.scratch/<feature>/issues/` when `to-tickets` wrote local files. Say its title before you start. A reference that matches more than one ticket: ask which.
- **Its spec.** The parent issue, the spec from `to-spec`, or the `docs/design/` folder from `tech-design`. Its Implementation Decisions, Testing Decisions, and seams are decided. They outrank your own shape choices.
- **The repo.** `AGENTS.md`, `docs/agents/code-standards.md`, the terms in `GLOSSARY.md` (or `CONTEXT.md`) the ticket uses, and the ADRs in `docs/adr/` that cover the code you will change. Titles first, then the ones that match. Skip what does not exist.
- **The code.** Where the change lands, its direct callers, and its tests. Stop at direct callers. `git log --oneline -20 -- <files>`: a file with many recent fixes is where the shape hurts most.
- **The start commit.** `git rev-parse HEAD`. The review reads the diff from here.

## 2. Shape

Ask: if this requirement had been there from the start, what would this code look like? Build toward that shape, not on top of the current one.

The change needs a refactor first when, without one, you would:

- add an `if`, a flag, or a boolean to code that already branches on a mode
- add a second way to do something the code already does
- copy code to reach what you need
- make a caller know what a module should hide (call order, internal state)
- put logic where no agreed seam can test it
- work around a name, a type, or a module that no longer fits

Pick the shape that hides the most from its callers, by `codebase-design`. The spec already decided the modules and interfaces: follow it. The code fights the spec, or two shapes are equal and the spec does not choose: ask the person in one question with the options.

Caring is not adding layers. Build for the use the code has today:

- A new module must pass the deletion test: delete it in your head. If the complexity does not come back in its callers, it is a pass-through. Do not add it.
- The seams are the ones the spec agreed. A seam it did not agree is a change to the spec: ask. With no spec, add a seam only when two things vary across it.
- No option, parameter, or extension point that nothing uses yet.

## 3. Refactor first

Refactor the code the change lands in, as far as the change needs. Leave unrelated code alone.

- **Behaviour stays.** A refactor changes no behaviour, public API, schema, config name, or UI. A change to any of those is part of the feature: the spec covers it, or you ask.
- **ADRs win.** When the shape you want goes against an ADR, ask the person.
- **Pin it first.** No test covers the behaviour you will move? Write one at the agreed seam that pins what the code does today. Run it.
- **Small steps.** Each leaves the tests green.
- **No leftovers.** Move every caller to the new shape and delete the old one in the same change. No compatibility layer for code only we call. Delete dead code you pass. The exception: the ticket is one step of an expand-contract plan from `to-tickets`. Then the old shape stays until its contract ticket.

## 4. Build

Build the feature on the new shape with `tdd`, at the agreed seams: red, then green, one slice at a time. Without `tdd`, keep the same loop: a failing test through the interface, then the smallest code that passes it.

Tests go through the interface. When you have to test past it, the shape is wrong: go back to 2.

Run the typecheck and the test file you work in often. Run the full suite once at the end.

## 5. Review with fresh eyes

You wrote the code, so you do not judge it. Reviewers with a fresh context do, all at once:

- `code-review`: its Standards and Spec reviewers.
- The design reviewer, by [design-review.md](references/design-review.md): is the code easier to change than before? `code-review` does not ask that.

Give each one only the diff from the start commit, the ticket, and the paths to the spec, the code standards, the ADRs, and the glossary. Not your plan, your reasoning, or what you think went well: that is the bias they are there to avoid. No subagent tool: say that the review is not independent, and run both by their files yourself.

## 6. Fix

`tdd` leaves refactoring to the review. This is that refactor:

1. Fix every finding in the files the ticket changed, with the tests green and the behaviour the same.
2. A finding outside those files: name it in your summary, do not fix it.
3. A finding that goes against the spec or an ADR: the spec and the ADR win. Name it.
4. A finding you think is wrong: say why in your summary. Never drop one silently.
5. One review round. Run a second only when the fixes changed the shape, not for small edits.

## 7. Commit

1. Did the change make a real decision (a new seam, a module split, a rejected shape)? Write the ADR in the same change, by the repo's `AGENTS.md`. A new or renamed term: update `GLOSSARY.md`.
2. Run the full suite and the typecheck.
3. Commit to the current branch. The refactor first, as `refactor: <what>`, then the feature. A reviewer sees the same behaviour first, then the new behaviour.
4. Say in a few lines what you refactored and why, which findings you fixed, and which you did not and why.

## When the ticket is a refactor

The ticket names the destination. The behaviour stays, so the tests are the contract:

1. Pin the behaviour first, through the interface the callers use. Run it before you change anything.
2. Shape it by 2: a deeper module, the deletion test, no seams the spec did not agree.
3. Refactor by 3, in small green steps, until every caller uses the new shape and the old one is gone, or until this expand-contract step is done.
4. The pinning tests pass unchanged. A test you had to change pinned the inside, not the behaviour: say which.
5. Then 5 to 7.

## Companion skills

Call by exact name with the Skill tool when installed: `tdd`, `code-review`, `codebase-design`, `comment-root-cause`. If one is missing, say so once, name `/setup-nstack-skills`, and go on by these rules.
