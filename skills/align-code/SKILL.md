---
name: align-code
description: Use when the user wants to align a codebase on one set of code standards and principles, find where the code does the same thing in different ways, decide which way wins, and plan or run the rewrite without breaking changes.
---

Chart one standard per area in `docs/align/<yyyy-mm-dd>-<name>/`, close one gap per session, then rewrite the code with subagents.

**Destination:** one decided standard and one exemplar per area, and a ticket for every change that gets the code there.

## Rules that outrank the rest

- **No breaking changes.** API, events, database schema, public exports, config names, CLI, and UI stay exactly as they are. See [contracts.md](references/contracts.md).
- **Behavior stays.** Build, test, lint, and contract checks pass after every ticket.
- **The majority does not win.** Count each variant, then judge it by [Judging](#judging).
- **An anti-pattern is bad even when it is everywhere.** A `bad` variant is never `consistent`.
- **No comments.** See [comments.md](references/comments.md).
- **An unknown is a gap.** Never an assumption, a default, or a guess.
- **Never invent a standard.** Options come from the code or a cited source. Only the person decides.
- **Read only until ready.** Before ready, write only the align folder. Code changes only in `apply`, on a local branch, after a yes. Never push.
- **One gap per session.** Surveys and research run beside it.

## Invocation

| Typed | Mode | Main session loads | Subagents load |
| --- | --- | --- | --- |
| nothing, `help`, `<name> status`, `close <gap>`, `drop <gap>`, `abandoned` | [help.md](references/help.md) | help. Close also structure, contracts | none |
| `new <name>` | [Chart](#chart) | resume, structure, survey, contracts | Survey: its brief, contracts, `codebase-design`, comments |
| `<name>` or `<name> grill [gap]` | [Work](#work) | resume, help, structure, survey, contracts, the claimed gap's row and its one survey file | Survey and research: their brief |
| `<name> ready` | [ready-gate.md](references/ready-gate.md) | resume, help, ready-gate, structure, rollout, contracts, `to-tickets` | none |
| `<name> apply` | [rollout.md](references/rollout.md), lint advice at the end | resume, help, rollout, survey, contracts, comments | Ticket: its brief, contracts, comments, the exemplar. Review: `code-review`. Verify: survey brief |
| `check`, `advise` | [advise.md](references/advise.md) | advise, comments | Advise surveys: their brief |

Chart, work, ready, and apply sessions start and end by [resume.md](references/resume.md). `check` and `advise` do not.

Subagents return a short result and write only their own output file. Only the main session writes `gaps.md`, `align.md`, `log.md`, and `rollout.md`.

## The map

The folder, files, and sections are in [structure.md](references/structure.md). Statuses: `draft`, `discussion`, `ready`, `applying`, `aligned`, `abandoned`.

```markdown
## Map

### Destination
<one or two lines>

### Notes
Scope: <parts or folders>
Preferences: <the person's standing preferences>
Execution: apply runs the rollout after ready.

### Decisions so far
- <gap question> (<id>): <one-line gist>

### Not yet specified
<one line per question you cannot phrase yet, or None.>

### Out of scope
<one line per question past the destination, and why. Every breaking change lands here.>
```

A gap's name is its question. Use the question, never the bare id. **Claim** a gap by setting `owner` first. The **frontier** is `open`, unblocked, unclaimed, ordered danger first.

**Fog of war:** an in-scope question you cannot phrase yet is one line under Not yet specified. One you can phrase is a gap, even when blocked.

## Judging

Every verdict cites its source: a `codebase-design` term, a smell from the `code-review` baseline, [comments.md](references/comments.md), or a section of the language's or framework's official guide. No source: research one. Never judge without one.

- `good`: breaks nothing. Copy it.
- `weak`: breaks nothing, but makes the next change harder.
- `bad`: breaks a source. Every copy costs.

A rule the person states outranks every source, and goes on the gap row.

## Danger first

1. `bad spreading`: `bad`, and added in the last 90 days.
2. `bad majority`: `bad`, and the most common variant.
3. `bad`.
4. `inconsistent`: no variant is `bad`, but the code does it more than one way, or its one way is `weak`.

Then by files touched. Open research and task gaps come before all of them: they unblock the rest.

## Gap types

Never answer the person's side of a HITL gap.

- **Research** (AFK). A fact. The survey of an area, by [survey.md](references/survey.md), or a source a verdict needs. A subagent with a fresh context does it.
- **Grilling** (HITL). Which variant becomes the standard. Show the card, ask one question, stop. Call `codebase-design`, `grilling`, and `domain-modeling`.
- **Prototype** (HITL). No module is good enough to be the exemplar. Rewrite one small module under `prototypes/`, never in the code. The person's reaction is the answer.
- **Task** (HITL or AFK). Work a decision waits on, such as writing a missing check. Drive it, or give the person a checklist. A question only the person can answer is grilling, not a task.

### The grilling card

```text
<area> (<id>): <question>
A. <variant>   <files> files, <n> in last 90 days   <good | weak | bad>: <source, one line>
B. <variant>   ...
Recommended: <exactly one letter>: <why, with the source>. Or: none, research first.
Exemplar: <module>
Contract: <none | the frozen surface, and the outcome you propose>
Changes: <files>   Left open: <what keeps spreading>
```

Answers: a variant, the person's own standard, `exception` with a reason, or research first. Every answer gets an outcome from [contracts.md](references/contracts.md): `apply`, `adapter`, `new-only`, or `exception`.

## Companion skills

Call by exact name: `grilling`, `domain-modeling`, `research`, `codebase-design`, `to-tickets`, `code-review`, `writing-for-agents`, `deslop`. `to-tickets` at ready, for the slicing. `code-review` and `deslop` on every ticket diff in apply. `writing-for-agents` on every edit of `code-standards.md` or an ADR. If one is missing, say so once, name `/setup-nstack-skills`, and go on by these rules.

## Modes

### Chart

1. **Check what the run needs.** Read the build, test, and lint commands from `AGENTS.md`. None: name `/setup-agents-md` and stop. Read `docs/agents/code-standards.md` and the ADRs when they exist: each line is a candidate, never a standard. List the frozen surfaces in scope and the check for each, by [contracts.md](references/contracts.md).
2. **Destination.** Call `grilling` and `domain-modeling`. Agree the scope. Done when the person agrees with the destination.
3. **Sweep** every area in [survey.md](references/survey.md). Each ends as a survey gap, a fog line, or `n/a: <reason>` in its section.
4. **Create the folder** by [structure.md](references/structure.md). Status `draft`.
5. **Add the gaps.** One grilling gap: `Is comments.md our comments standard?`, with A. comments.md as written, B. comments.md with the person's edits. Recommended: A. Edits go on the row and outrank comments.md for this run. A frozen surface with no check is a task gap. Fill `blocks` in a second pass. Status `discussion`.
6. **Start the surveys** by [survey.md](references/survey.md#when).
7. **Stop.** Log. Say the gap count by type and the first frontier gap.

A `new` for a name that exists stops. Tell them to resume.

### Work

1. **Catch up** by [resume.md](references/resume.md). Turn each finished survey into gaps by [survey.md](references/survey.md#closing).
2. **Claim** the gap the person named, or the first on the frontier.
3. **Resolve** it by type.
4. **Record** the answer and outcome on the row, status `decided`. A prototype gap records its exemplar. The standard and outcome go on the grilling gap it unblocks. No answer: `waiting-on-input`. Advice never closes a gap.
5. **Write** a grilling gap's standard into its area section of `align.md`. Every gap: add the gist to Decisions so far.
6. **Update the map.** Add the gaps it opens. Clear fog you can now phrase. A breaking change goes to Out of scope.
7. **Stop.**

Other sessions may edit the folder at the same time.

## When this is the wrong answer

Say so and stop.

- The code already does each thing one way.
- The person wants a contract made consistent. That breaks callers: `/tech-design`.
- No build or test command. Run `/setup-agents-md` first.
