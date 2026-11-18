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

## Triage

First step in both modes, before any companion skill: decide `skip`, `partial`, or `full`, and log the one-line reason. Do not spend tokens on work the triage rules out.

- `skip` when nothing changes stored state.
- `partial`: check only the invariants the diff touches, and reuse an existing model when present. A new create endpoint, for example, checks idempotent retry, not the whole machine.
- `full` only for a new or changed state machine, concurrency, or a multi-step flow.

## Companion skills

Call each by its exact name with the Skill tool: `create-formal-verification-skill`, `maintain-formal-verification-skill`, `statechart`.

## Invocation

The person types `/verify-flow`. The next word is the mode: `before` or `after`. If there is no mode, say the two modes and stop.

Write into the design or plan folder when one exists. Otherwise write into `docs/verify-flow/<resource>/`.

### Before

Triage first. On `skip`, stop. Otherwise call `create-formal-verification-skill`, then `statechart`, scoped to the triage. Write into the folder: the model, a mermaid chart, the invariants as requirements, the shortest paths to broken invariants as planned test cases, and an explicit list of what the model leaves out.

### After

After works alone. Triage first. On `skip`, stop. Reuse the model from `before` when it exists. If it does not, build it from the real code with `create-formal-verification-skill`, then continue.

Call `maintain-formal-verification-skill` so the model matches the real code, then rerun `statechart`, scoped to the triage. Replay each broken path against the code. A path that does not reproduce means the model is wrong until proven otherwise. Each path that reproduces becomes a regression test. Write a short report for the PR body.
