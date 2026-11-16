---
name: align-code
description: Use when the user wants to align a codebase on one set of code standards and principles, find where the code does the same thing in different ways, decide which way wins, and plan or run the rewrite without breaking changes.
---

Agents copy the code they see, so a bad pattern spreads with every change. This skill charts one standard per area as a map at `docs/align/<yyyy-mm-dd>-<name>/`, closes one gap per session, then runs the rewrite with subagents. The code ends up worth copying, and the code is the docs. The why is in [README.md](README.md). You do not need to read it.

**Destination:** one decided standard and one exemplar per area, and a ticket for every change that gets the code there.

## Rules that outrank the rest

- **No breaking changes.** API, events, database schema, public exports, config names, CLI, and UI stay exactly as they are. See [contracts.md](references/contracts.md).
- **Behavior stays.** Build, test, lint, and contract checks pass after every ticket.
- **The majority does not win.** Count each variant, then judge it by [principles.md](references/principles.md).
- **No comments.** See [comments.md](references/comments.md).
- **An unknown is a gap.** Never an assumption, a default, or a guess.
- **Never invent a standard.** Options come from the code or a cited source. Only the person decides.
- **Read only until ready.** Before ready, write only the align folder. Code changes only in `apply`, on a local branch, after a yes. Never push.
- **One gap per session.** Surveys and research run beside it.

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

**Fog of war:** an in-scope question you cannot phrase yet is one line under Not yet specified. One you can phrase is a gap, even when blocked. Fog is `None.` at ready.

## Danger first

1. `bad spreading`: fails a principle and was added in the last 90 days.
2. `bad majority`: fails a principle and is the most common variant.
3. `bad`: fails a principle.
4. `inconsistent`: no variant is `bad`, the code just does it more than one way. A `weak` variant lands here.

Then by files touched. Open research and task gaps come before all of them: they unblock the rest.

## Gap types

Never answer the person's side of a HITL gap.

- **Research** (AFK). A fact. The survey of an area, by [survey.md](references/survey.md), or a principle that needs a source. A subagent with a fresh context does it.
- **Grilling** (HITL). Which variant becomes the standard. Show the card, ask one question, stop. Call `codebase-design`, `grilling`, and `domain-modeling`.
- **Prototype** (HITL). No module is good enough to be the exemplar. Rewrite one small module under `prototypes/`, never in the code. The person's reaction is the answer.
- **Task** (HITL or AFK). Work a decision waits on, such as writing a missing check. Drive it, or give the person a checklist. A question only the person can answer is grilling, not a task.

### The grilling card

```text
<area> (<id>): <question>
A. <variant>   <files> files, <n> in last 90 days   <good | weak | bad>: <principle id, one line>
B. <variant>   ...                                   recommended: <why, with the principle>
Exemplar: <module>
Contract: <none | the frozen surface, and the outcome you propose>
Changes: <files>   Left open: <what keeps spreading>
```

Answers: a variant, the person's own standard, `exception` with a reason, or research first. Every answer gets an outcome from [contracts.md](references/contracts.md): `apply`, `adapter`, `new-only`, or `exception`.

## Companion skills

Call by exact name: `grilling`, `domain-modeling`, `research`, `codebase-design`, `writing-for-agents`, `deslop`. `writing-for-agents` on every edit of `code-standards.md` or an ADR. `deslop` on every diff in apply. If one is missing, say so once, name `/setup-nstack-skills`, and go on by these rules.

## Invocation

| Typed | Mode |
| --- | --- |
| nothing, `help`, `<name> status`, `close <gap>`, `drop <gap>`, `abandoned` | See [help.md](references/help.md) |
| `new <name>` | Chart |
| `<name>` or `<name> grill [gap]` | Work |
| `<name> ready` | [ready-gate.md](references/ready-gate.md) |
| `<name> apply` | [rollout.md](references/rollout.md), lint advice at the end |
| `check`, `advise` | [advise.md](references/advise.md) |

Chart, work, ready, and apply sessions start and end by [resume.md](references/resume.md). `check` and `advise` do not.

### Chart

1. **Preflight.** Read the build, test, and lint commands from `AGENTS.md`. None: name `/setup-agents-md` and stop. Read `docs/agents/code-standards.md` and the ADRs when they exist: each line is a candidate, never a standard. Find the contract checks by [contracts.md](references/contracts.md).
2. **Destination.** Call `grilling` and `domain-modeling`. Agree the scope. Done when the person agrees with the destination.
3. **Sweep** every area in [survey.md](references/survey.md). Each ends as a survey gap, a fog line, or `n/a: <reason>` in its section.
4. **Create the folder** by [structure.md](references/structure.md). Status `draft`.
5. **Add the gaps.** One grilling gap: `Is comments.md our comments standard?`, recommended yes. A frozen surface with no check is a task gap. Fill `blocks` in a second pass. Status `discussion`.
6. **Start the surveys,** one subagent per area.
7. **Stop.** Log. Say the gap count by type and the first frontier gap.

A `new` for a name that exists stops. Tell them to resume.

### Work

1. **Catch up** by [resume.md](references/resume.md). Turn each finished survey into gaps: each Question a grilling gap with its danger, each Still unknown a gap. One `good` variant: the area is `consistent`, no gap.
2. **Claim** the gap the person named, or the first on the frontier.
3. **Resolve** it by type.
4. **Record** the answer and outcome on the row, status `decided`. No answer: `waiting-on-input`. Advice never closes a gap.
5. **Write** the standard into its area section of `align.md`. Add the gist to Decisions so far.
6. **Update the map.** Add the gaps it opens. Clear fog you can now phrase. A breaking change goes to Out of scope.
7. **Stop.**

Other sessions may edit the folder at the same time.

## When this is the wrong answer

Say so and stop.

- The code already does each thing one way.
- The person wants a contract made consistent. That breaks callers: `/tech-design`.
- No build or test command. Run `/setup-agents-md` first.
