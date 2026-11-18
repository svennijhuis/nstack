---
name: verify-flow
description: Use when you plan or write code that creates, updates, or deletes stored state, changes a status, or runs a flow with shared state, retries, timeouts, ordering, or concurrency, or when the user asks to verify a flow. Models the resource, checks it against the code, and turns broken paths into tests. Run `before` on the design or plan, `after` on the code.
---

Model one resource at a time and check it. Call the pinned companion skills by name. Do not copy their text. If one is not installed, say so once, name `/setup-nstack-skills`, and stop that step until it is installed.

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

**Run `statechart` work in a scratch folder outside the repo.** Copy only the files named under Output into `docs/verify-flow/<resource>/`.

**One resource at a time.** Finish it before you start another.

## Triage

First step in both modes, before any companion skill. Triage is the main cost control: spend real effort here, because every later step costs more. Read the diff or the plan, and find other writers of the same resource (delegate this, see Delegation). Do not start a companion skill until the triage is logged.

Answer these in order. The first match decides.

Before the questions: an existing model with `status: aligned`, whose transitions the diff or the plan does not touch, is `skip`. Name the model in the reason.

1. Does the change write stored state, or read a resource that has writes? No: `skip`. This covers pure UI, static or pure lookup data, formatting, copy, and renames with no behavior change.
2. Does it add or change a state machine, a concurrency path, a retry or timeout, an ordering rule, or a multi-step flow? Yes: `full`.
3. Does a second writer, a background job, or a cache touch the same fields or status the change reads or writes? Yes: `full`. Name it in the reason. A second writer that sets only other fields, with a cache that does not hold these fields, does not count: go to 4. A writer with no caller does not count either, but name it in the reason.
4. Otherwise: `partial`. Check only the invariants the diff or the plan touches.
   - A new create endpoint checks idempotent retry, not the whole machine.
   - A single-field update checks lost update and authorization.
   - A read on a resource that has writes checks that no stale or leftover data is returned (cache after update or delete, a soft-deleted or half-written row visible, a read during an in-flight multi-step write).

Bias and limits:

- Never go below `partial` because a test already exists. A test that covers one path does not cover the interleavings.
- `full` on more than one resource: triage each resource alone and run them one at a time.

Write one line to `triage.md`: `triage: <skip|partial|full> | <resource> | <reason, with the deciding question number>`. In `after`, if the new line differs from the line already in `triage.md`, add why to the new line. On `skip`, that line is the whole record.

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

Call a companion by its exact name with the Skill tool: `create-formal-verification-skill`, `maintain-formal-verification-skill`, `statechart`. The mode sections say which one to call. If a companion is not installed, stop that step, as the opening rule says. Each companion sets `disable-model-invocation: true`, so the Skill tool can refuse an installed one and tell you to ask the person. Do not work around that refusal by reading the file and following it. Stop that step, ask the person to run `/<name>` themselves, say what you need from it, and continue from its output. Do not copy a companion's text into this skill.

## Invocation

The person types `/verify-flow <before|after> <resource>`. `<resource>` is the entity, in kebab-case. You can also start it yourself when the description matches: `before` once a design or plan for such a change is agreed, `after` once the code is written and before you hand it over. Pick the resource yourself then. If the mode or the resource is missing when the person types it, say that form and stop. When you start it yourself, the triage runs first, so a change that needs nothing ends at `skip` after one line.

## Output

Write only under `docs/verify-flow/<resource>/`. Do not write into `docs/design/`. Files:

- `triage.md`: the triage line, then `status: intent`, `status: aligned`, or `status: drifted`.
- `SPEC.tla`, `SPEC.cfg`, and `view.ts`: the model, copied out of the scratch folder.
- `chart.mmd`: only when `statechart` writes one. If it writes none, say that in `omitted.md` on `before`, and in `report.md` on `after`.
- `invariants.md`: the invariants this triage includes, each as a requirement.
- `omitted.md`: what the model leaves out.
- `planned-tests.md`: the shortest broken paths (`before`).
- `report.md`: the `after` report.

Pass `statechart` `--out` a new empty folder in the scratch folder, because the command exits with an error when the folder is not empty. Copy `chart.mmd` only. Leave `tlc.out` and statechart's own `report.md` there. They are not this skill's `report.md`.

### Before

Triage first. On `skip`, stop. When `SPEC.tla` is already in the folder and the triage is `partial`, edit `SPEC.tla` and `invariants.md` so they include only the invariants the diff or the plan touches, then call `statechart` on that spec. Do not write a new spec from scratch. When the file is missing, or the triage is `full`, call `statechart` and write a TLA+ spec in a scratch folder outside the repo. Do not call `create-formal-verification-skill` or `maintain-formal-verification-skill`. Include every default invariant the triage keeps. Copy the model files and `chart.mmd` (when `statechart` writes it) into the folder, plus `invariants.md`, `planned-tests.md`, and `omitted.md`. Write `status: intent` in `triage.md` only when no code for this resource exists yet. If code already exists, do not change the status in `before`.

### After

After does not require a `before` run. Triage first. On `skip`, stop. If `SPEC.tla` exists, start from it.

If a project-local verify skill names this resource, call `maintain-formal-verification-skill` and do not call create. A skill for a different resource does not count. If none does, call `create-formal-verification-skill` once. Name this resource and one invariant this triage keeps. Do not call create again in this run, and do not call maintain in this run. Write the other invariants to `invariants.md` as not checked yet.

If the check is TLA+, rerun `statechart` in a scratch folder, scoped to the triage, and copy the same files as `before`. If it is not TLA+, do not call `statechart`.

At the start of a non-skip `after`, if the status is missing, or is `aligned` and the diff or the plan touches the model's transitions, set `status: drifted` before you compare. List each difference between the model and the code, and decide for each one whether the code or the model is wrong. A code bug is a finding. A model gap is fixed in the model. When the model and the code agree, set `status: aligned`.

Replay each broken path against the code. If a path does not reproduce, the model is wrong: fix the model or the verify skill and rerun before any test. Stop if you cannot show the model is right. If a path does reproduce, add a regression test beside the resource's existing tests. Write the test file and do not commit it unless the person asks. This outranks maintain's rule against adding a repro to product code. If the repo has no test runner, put the steps in `report.md` and do not claim a test exists.

Write `report.md`: the triage line, the model status before and after, the outcome (`in sync`, `updated`, `bug`, or `blocked`), the differences found, each broken path, and what is still left out. If a PR is open, use that text as the PR body.
