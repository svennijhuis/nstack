---
name: verify-flow
description: Use when a change writes stored state, or a flow has shared state, retries, timeouts, ordering, or concurrency, to model the resource and check it against the code.
---

Model one resource at a time and check it. Call the pinned companion skills by name. Do not copy their text. If one is not installed, say so once, name `/setup-nstack-skills`, and do that step by the rules in this skill.

## When to run

Run on any endpoint that changes stored state (create, update, delete, or a status change), and on a flow with shared state, retries, timeouts, ordering, or concurrency. Model the resource, not the endpoint: the entity's states, with the write endpoints as transitions. Read-only endpoints and pure UI skip with a one-line reason.

Default invariants to check:

- no lost update on concurrent writes (version, ETag, or equivalent)
- idempotent retry of the same request
- no illegal status transition
- a partial failure leaves no half-written state
- authorization checked on every transition

## Rules that outrank the rest

**Never weaken an invariant to pass.**

**Label states in the reader's language.**

**Run `statechart` work in a scratch folder outside the repo.** Copy only the required outputs into the output folder.

**One resource at a time.** Finish it before you start another.

## Companion skills

Call each by its exact name with the Skill tool: `create-formal-verification-skill`, `maintain-formal-verification-skill`, `statechart`.

## Invocation

The person types `/verify-flow`. The next word is the mode: `before` or `after`. If there is no mode, say the two modes and stop.

Write into the design or plan folder when one exists. Otherwise write into `docs/verify-flow/<resource>/`.

### Before

On a resource or flow that meets When to run, call `create-formal-verification-skill`, then `statechart`. Write into the folder: the model, a mermaid chart, the invariants as requirements, the shortest paths to broken invariants as planned test cases, and an explicit list of what the model leaves out. Skip with a one-line reason when nothing meets When to run.

### After

After works alone. Reuse the model from `before` when it exists. If it does not, build it from the real code with `create-formal-verification-skill`, then continue.

Call `maintain-formal-verification-skill` so the model matches the real code, then rerun `statechart`. Replay each broken path against the code. A path that does not reproduce means the model is wrong until proven otherwise. Each path that reproduces becomes a regression test. Write a short report for the PR body. Skip with a one-line reason when nothing meets When to run.
