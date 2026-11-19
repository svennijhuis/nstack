---
name: implement
description: Use when you implement a ticket, issue, feature, or fix in code. Builds it so the codebase gets better over time, not worse. Reads the code the change lands in, shapes it as if the requirement had been there from the start, refactors where the change needs it, and leaves the code easier to change next time.
---

The ticket is the tactical goal. The codebase is the strategic one. A ticket is not done when it works but leaves the code harder to change. Make the change easy, then make the easy change.

## 1. Read

Read what exists, skip what does not:

- `AGENTS.md` and `docs/agents/code-standards.md`.
- `GLOSSARY.md` (or `CONTEXT.md`): the terms the ticket uses.
- The ADRs in `docs/adr/`: titles first, then the ones that cover the code you will change.
- The code the change lands in, its direct callers, and its tests. Stop at direct callers.
- `git log --oneline -20 -- <files>`: a file with many recent fixes is where the shape hurts most.

## 2. Shape

Ask: if this requirement had been there from the start, what would this code look like? Build toward that shape, not on top of the current one.

The change needs a refactor first when, without one, you would:

- add an `if`, a flag, or a boolean to code that already branches on a mode
- add a second way to do something the code already does
- copy code to reach what you need
- make a caller know what a module should hide (call order, internal state)
- put logic where no test can reach it
- work around a name, a type, or a module that no longer fits

Pick the shape that hides the most from its callers, by `codebase-design`. Two good shapes and no clear winner: ask the person in one question with both options.

Caring is not adding layers. Build for the use the code has today:

- A new module must pass the deletion test: delete it in your head. If the complexity does not come back in its callers, it is a pass-through. Do not add it.
- One adapter is a hypothetical seam. Add a seam only when two things vary across it, or a test needs it.
- No option, parameter, or extension point that nothing uses yet.

## 3. Refactor

Refactor the code the change lands in, as far as the change needs. Leave unrelated code alone.

- **Behaviour stays.** A refactor changes no behaviour, public API, schema, config name, or UI. A change to any of those is part of the feature: ask the person before you make it.
- **ADRs win.** When the shape you want goes against an ADR, ask the person.
- **Pin it first.** No test covers the behaviour you will move? Write one that pins what the code does today.
- **Small steps.** Each leaves the tests green. Run them after each step.
- **No leftovers.** Move every caller to the new shape and delete the old one in the same change. No compatibility layer for code only we call. Delete dead code you pass.
- **Its own commit.** When you commit, the refactor goes first, as `refactor: <what>`, then the feature on top. A reviewer sees the same behaviour first, then the new behaviour.

## 4. Build

Build the feature on the new shape.

The interface is the test surface. Test the behaviour you add or change through it, not through the inside. When you have to test past the interface, the shape is wrong: go back to 2. Behaviour you touched that had no test gets one. Delete tests that only pinned an inside that no longer exists.

## 5. Before you finish

Read your own diff and ask:

- Is the code easier to change than before? If not, where did it get worse, and why?
- Did you add a layer, a seam, or an option nothing uses yet? Remove it.
- Did a comment cover a shortcut? Fix the cause, by `comment-root-cause`.
- Did the change make a real decision (a new seam, a module split, a rejected shape)? Write the ADR in the same change, by the repo's `AGENTS.md`.
- A new or renamed term? Update `GLOSSARY.md`.

Then say in one or two lines what you refactored and why, so the reviewer knows where to look.

## When the ticket is a refactor

The ticket names the destination. The behaviour stays, so the tests are the contract:

1. Pin the behaviour first, through the interface the callers use. Run it before you change anything.
2. Shape it by 2: a deeper module, the deletion test, no speculative seams.
3. Refactor by 3, in small green steps, until every caller uses the new shape and the old one is gone.
4. The pinning tests pass unchanged. A test you had to change pinned the inside, not the behaviour: say which.

## Companion skills

Call by exact name when installed: `codebase-design`, `comment-root-cause`. If one is missing, go on by these rules.
