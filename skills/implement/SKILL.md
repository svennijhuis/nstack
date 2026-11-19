---
name: implement
description: Use when you implement a ticket, issue, spec, feature, or bug fix in code. Builds it so the codebase gets better over time, not worse. Reads the ticket and its spec, shapes the code the change lands in as if the requirement had been there from the start, refactors where the change needs it, builds with tdd at the agreed seams, proves it works, and ends with an independent review and a commit.
---

The ticket is the tactical goal. The codebase is the strategic one. A ticket is not done when it works but leaves the code harder to change. Make the change easy, then make the easy change.

The person cares about the long term, so you do too. Every ticket leaves the code it touches:

- **deeper**: modules that hide more behind a smaller interface, by `codebase-design`
- **better tested**: behaviour you touch has a test through its interface
- **cleaner**: no comment that covers a shortcut, by `comment-root-cause`
- **in the domain's words**: names from `GLOSSARY.md`, choices that follow the ADRs

Be the colleague who says "we need to refactor this first", out loud and before the code, not the one who piles the ticket on top.

## 1. Read

- **The ticket.** A ticket reference: fetch it from the issue tracker, by `docs/agents/issue-tracker.md` when it exists, or from `.scratch/<feature>/issues/` when `to-tickets` wrote local files. Say its title before you start. A reference that matches more than one ticket: ask which.
- **Its spec.** Only the spec the ticket names or links, or its parent issue: from `to-spec`, or a `docs/design/` folder from `tech-design`. Its decisions are made: in a `to-spec` spec, Implementation Decisions, Testing Decisions, and the seams; in a `tech-design` design, Decisions so far, Design (Boundaries and contracts, Data model), and Cross-cutting, Testing. They outrank your own shape choices. A spec the ticket does not name is not its spec, even when it is about the same code: its decisions do not bind this ticket. No spec: say so, and go on without one.
- **The repo.** `AGENTS.md`, `docs/agents/code-standards.md`, the terms in `GLOSSARY.md` (or `CONTEXT.md`, or the context's glossary that `GLOSSARY-MAP.md` points at) the ticket uses, and the ADRs in `docs/adr/` that cover the code you will change. Titles first, then the ones that match. Skip what does not exist.
- **The code.** Where the change lands, its direct callers, and its tests. Stop at direct callers. `git log --oneline -20 -- <files>`: a file with many recent fixes is where the shape hurts most.
- **The start commit.** `git rev-parse HEAD`. The review reads the diff from here.

**A bug ticket** goes through `diagnosing-bugs` first: a command that goes red on the bug, then the cause, then a regression test at the right seam. Then shape the fix by 2 and go on from 3. Without `diagnosing-bugs`, keep that order: no fix before a red reproduction. A bug that exists because the code does one thing in two places is fixed by moving it to one place: one function both callers use, where its meaning belongs. Copying the working idiom into the broken place still leaves two places. Pin the caller that works first, so the move cannot break it.

## 2. Shape

Ask: if this requirement had been there from the start, what would this code look like? Build toward that shape, not on top of the current one.

The change needs a refactor first when, without one, you would:

- add an `if`, a flag, or a boolean to code that already branches on a mode
- add a second way to do something the code already does
- copy code to reach what you need
- make a caller know what a module should hide (call order, internal state)
- put logic where no agreed seam can test it
- work around a name, a type, or a module that no longer fits

Put code where its meaning belongs: the module whose name, glossary term, or ADR covers it. A helper does not go in a module only because its callers already import that module.

Pick the shape that hides the most from its callers, by `codebase-design`. The spec already decided the modules and interfaces: follow it. The code fights the spec, or two shapes are equal and the spec does not choose: ask the person in one question with the options.

Caring is not adding layers. Build for the use the code has today:

- A new module must pass the deletion test: delete it in your head. If the complexity does not come back in its callers, it is a pass-through. Do not add it.
- A seam is a place where behaviour can be swapped or tested from outside: an interface that tests or adapters use. A new module, function, or private helper is not a seam. Testing through the public function of a new module is fine.
- When the ticket's spec names its seams, a new seam it did not name is a change to the spec: ask. When it names none, or there is no spec, add a seam only when two things vary across it.
- No option, parameter, or extension point that nothing uses yet.

**Say the call.** Before you write code, say it in one or two lines: "Refactor first: <what>, because <the signal above>." or "Fits as it is: <why>." Then go on. Do not wait for an answer unless 'Decide, or ask' says so.

**Stored state.** When the ticket writes stored state (create, update, delete, a status change) and `verify-flow` is installed, run `verify-flow before <resource>` now, on the shape. Its invariants and planned tests join the ticket's tests.

## 3. Refactor first

Refactor the code the change lands in, as far as the change needs. Leave unrelated code alone.

- **Behaviour stays.** A refactor changes no behaviour, public API, schema, config name, or UI. A change to any of those is part of the feature: the spec covers it, or you ask.
- **ADRs win.** When the shape you want goes against an ADR, ask the person.
- **Pin it first.** No test covers the behaviour you will move? Write one at the agreed seam that pins what the code does today. Run it.
- **Small steps.** Each leaves the tests green.
- **Commit it now.** When the refactor is green, commit it as `refactor: <what>`, before you build. Then the feature goes on top.
- **No leftovers.** Move every caller to the new shape and delete the old one in the same change. No compatibility layer for code only we call. Delete dead code you pass. The exception: the ticket is one step of an expand-contract plan from `to-tickets`. Then the old shape stays until its contract ticket.

## 4. Build

Build the feature on the new shape with `tdd`, at the agreed seams: red, then green, one slice at a time. When the spec names no seams, `tdd` asks the person to confirm them: propose the public functions the ticket changes, and wait. Without `tdd`, keep the same loop: a failing test through the interface, then the smallest code that passes it.

Tests go through the interface. When you have to test past it, the shape is wrong: go back to 2. Behaviour you touched that had no test gets one.

Every comment, `TODO`, `HACK`, or lint or type suppression you write or edit goes through `comment-root-cause`: why is it there, and can the code be better? One that covers a shortcut means fix the cause, not keep the comment. Without `comment-root-cause`, ask those two questions yourself.

Run the typecheck and the test file you work in often. Run the full suite once at the end.

With `verify-flow before` run in 2: run `verify-flow after <resource>` once the feature is green, before the review.

## 5. Review with fresh eyes

You wrote the code, so you do not judge it. Reviewers with a fresh context do, all at once:

- `code-review`: its Standards and Spec reviewers.
- The design reviewer, by [design-review.md](references/design-review.md): is the code easier to change than before? `code-review` does not ask that.

Give each one only the diff from the start commit, the ticket, and the paths to the spec, the code standards, the ADRs, and the glossary. Not your plan, your reasoning, or what you think went well: that is the bias they are there to avoid. No subagent tool: say that the review is not independent, and run both by their files yourself.

## 6. Fix

`tdd` leaves refactoring to the review. This is that refactor:

1. **A finding that claims a bug** counts only when it is proven: write a test that fails on it, or run the command that shows it. It does not fail: drop it and name it. It fails: the test stays as a regression test, then fix it.
2. Fix every other finding in the files the ticket changed, with the tests green and the behaviour the same. A fix to the feature's own code goes in the feature commit. A fix to code the feature did not add goes in its own `refactor:` commit.
3. A finding outside those files: name it in your summary, do not fix it.
4. A finding that goes against the spec or an ADR: the spec and the ADR win. Name it.
5. A finding you think is wrong: say why in your summary. Never drop one silently.
6. One review round. Run a second only when the fixes changed the shape, not for small edits.

## 7. Commit

1. Did the change make a real decision (a new seam, a module split, a rejected shape)? Write the ADR in the same change, by the repo's `AGENTS.md`. A new or renamed term: update `GLOSSARY.md`.
2. Run the full suite and the typecheck.
3. **Prove it works.** Green tests are not the proof. Run the real thing the ticket changed (the command, the endpoint, the page, the function from a script) and read the actual output. A file date, a log line you wrote, or "it compiles" is no proof. When the check fails, suspect the check first, then the code.
4. **Name the safety fact**: the one fact the change is safe because of (for a refactor: the pinning tests pass unchanged), and how you proved it, or that you could not. Name the tests by name. Claim only tests that exist.
5. **Suggest `/blast-radius`** before merge only when the change alters, without the ticket asking for it, a public signature or contract, a stored format or schema, a wire format, or a feature flag. A change the ticket asks for is never a reason, even when systems outside the repo might see it: the person chose it. Then say nothing about it.
6. Commit the feature to the current branch, on top of the refactor commit. A reviewer sees the same behaviour first, then the new behaviour.
7. Say in a few lines what you refactored and why, the safety fact, which findings you fixed, and which you did not and why.
8. **Name what you saw.** At most three places outside the ticket where a module should be deeper or tests are missing, one line each: `<file>: <what>. Strength: Strong | Worth exploring | Speculative.` No file, no ticket, no fix: the person picks one for a ticket or for `improve-codebase-architecture`. Saw none: say none.

## Decide, or ask

Ask the person only for: a behaviour or public contract change the ticket and its spec do not cover, a shape that goes against an ADR or the spec, a new seam the spec did not agree, the seams `tdd` asks to confirm, or two shapes that are equal for the long term.

Everything else, decide and name it in your summary, so the person can overrule it:

- A test the ticket changes on purpose, because the behaviour it pinned is what the ticket changes.
- A detail the ticket leaves open: take the one that matches the code around it.
- Whether a choice is an ADR: decide by the repo's `AGENTS.md`.

## When the ticket is a refactor

The ticket names the destination. The behaviour stays, so the tests are the contract:

1. Pin the behaviour first, through the interface the callers use. Run it before you change anything.
2. Shape it by 2: a deeper module, the deletion test, no seams the spec did not agree.
3. Refactor by 3, in small green steps, until every caller uses the new shape and the old one is gone, or until this expand-contract step is done.
4. The pinning tests pass unchanged. A test you had to change pinned the inside, not the behaviour: say which.
5. Then 5 to 7.

## Companion skills

Call by exact name with the Skill tool when installed: `tdd`, `code-review`, `codebase-design`, `comment-root-cause`, `diagnosing-bugs`, `verify-flow`. If one is missing, say so once, name `/setup-nstack-skills`, and go on by these rules.

`code-review` means Matt Pocock's two-axis review (Standards and Spec). Claude Code ships its own skill with that name. When the one that loads is not the two-axis review, say so once, and run the Standards and Spec reviews as fresh subagents yourself: Standards against the code standards and the smells in `code-review`'s baseline, Spec against the ticket and its spec.

`blast-radius` runs only when the person types it: suggest it, never call it. Do not open a pull request or write its body: the person does that, with `pr` or by hand.
