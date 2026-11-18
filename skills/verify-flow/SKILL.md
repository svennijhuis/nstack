---
name: verify-flow
description: Use when a change writes stored state, or a flow has shared state, retries, timeouts, ordering, or concurrency, to model the resource and check it against the code.
---

Model one resource at a time and check it. Call the pinned companion skills by name. Do not copy their text. If one is not installed, say so once, name `/setup-nstack-skills`, and do that step by the rules in this skill.

## When to run

Run on any endpoint that changes stored state (create, update, delete, or a status change), and on a flow with shared state, retries, timeouts, ordering, or concurrency. Model the resource, not the endpoint: the entity's states, with the write endpoints as transitions. A read (GET) on a resource that has writes is included. Pure UI is not.

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

First step in both modes, before any companion skill. Triage is the main cost control: spend real effort here, because every later step costs more. Read the diff or the plan, and find other writers of the same resource (delegate this, see Delegation). Do not start a companion skill until the triage is logged.

Answer these in order. The first match decides.

1. Does the change write stored state, or read a resource that has writes? No: `skip`. This covers pure UI, static or pure lookup data, formatting, copy, and renames with no behavior change.
2. Does it add or change a state machine, a concurrency path, a retry or timeout, an ordering rule, or a multi-step flow? Yes: `full`.
3. Does a second writer, a background job, or a cache touch the same fields or status the change reads or writes? Yes: `full`. Name it in the reason. A second writer that sets only other fields, with a cache that does not hold these fields, does not count: go to 4. A writer with no caller does not count either, but name it in the reason.
4. Otherwise: `partial`. Check only the invariants the diff touches.
   - A new create endpoint checks idempotent retry, not the whole machine.
   - A single-field update checks lost update and authorization.
   - A read on a resource that has writes checks that no stale or leftover data is returned (cache after update or delete, a soft-deleted or half-written row visible, a read during an in-flight multi-step write).

Bias and limits:

- Choose the lower level when two fit, and write what new fact would raise it.
- Never go below `partial` because a test already exists. A test that covers one path does not cover the interleavings.
- `full` on more than one resource: triage each resource alone and run them one at a time.
- An existing model with status `aligned` and a diff that does not touch its transitions is `skip`, with the model named in the reason.

Log one line: `triage: <skip|partial|full> | <resource> | <reason, with the deciding question number>`. In `after`, if the triage differs from the one logged in `before`, say why in the report.

## Delegation

Use a cheap subagent (the smallest model tier available) for mechanical work only. The main agent keeps every judgment.

Delegate:

- **Triage facts.** Give the subagent the diff and the resource name. It returns a short list: every file that writes the resource, every job, cron, queue consumer, or cache that touches it, whether anything calls it, the fields each writer sets (a writer that applies an arbitrary patch counts as setting every field), and which of the triage questions 1 to 3 the facts bear on. It does not return a level.
- **Replay.** One subagent per broken path. It runs the steps against the code or a test and returns the exact steps run, the output, and `reproduces` or `does not reproduce`.
- **Model against code.** It returns each place the model and the code differ, with file and line. It does not say which one is wrong.

Keep with the main agent: the triage level, the invariants, the model, and the decision whether the code or the model is wrong.

Rules:

- A subagent result without its evidence (files, steps, output) does not count. Ask again or do the step yourself.
- Check every `does not reproduce` yourself before you change the model: rerun the steps. A cheap subagent may have run them wrong.
- If a subagent finds a writer, job, or cache the diff did not mention, that fact can only raise the triage level, never lower it.
- Run subagents for different paths in parallel. If no subagent tool exists, do the same steps yourself.

## Companion skills

Call each by its exact name with the Skill tool: `create-formal-verification-skill`, `maintain-formal-verification-skill`, `statechart`.

## Invocation

The person types `/verify-flow`. The next word is the mode: `before` or `after`. If there is no mode, say the two modes and stop.

Write into the design or plan folder when one exists. Otherwise write into `docs/verify-flow/<resource>/`.

### Before

Triage first. On `skip`, stop. Otherwise call `create-formal-verification-skill`, then `statechart`, scoped to the triage. Write into the folder: the model, a mermaid chart, the invariants as requirements, the shortest paths to broken invariants as planned test cases, and an explicit list of what the model leaves out. Put `status: intent` at the top of the model. The model describes what the code should do, so no code exists yet to match it.

### After

After works alone. Triage first. On `skip`, stop. Reuse the model from `before` when it exists. If it does not, build it from the real code with `create-formal-verification-skill`, then continue.

Read the `status` of the `before` model: `intent` or `drifted` means it may differ from the code. List each difference between the model and the code, and decide for each one whether the code or the model is wrong. A code bug becomes a finding. A model gap is fixed in the model. Then call `maintain-formal-verification-skill` so the model matches the real code, set `status: aligned`, and rerun `statechart`, scoped to the triage. Replay each broken path against the code. A path that does not reproduce means the model is wrong until proven otherwise. Each path that reproduces becomes a regression test. If the code changes later and the model is not rerun, set `status: drifted`. Write a short report for the PR body: the triage line, the model status before and after, the differences found, and the regression tests added.
