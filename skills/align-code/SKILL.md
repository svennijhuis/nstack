---
name: align-code
description: Use when the user wants to align a codebase on one set of code standards and principles, find where the code does the same thing in different ways, decide which way wins, and plan or run the rewrite without breaking changes.
---

Agents copy the code they see. When cheap and medium agents wrote the code, it holds three ways to return an error, two folder layouts, and mixed names, and every new change copies whichever one sits closest. A bad pattern spreads faster than a good one. This skill charts the way to one standard per area as a shared map at `docs/align/<yyyy-mm-dd>-<name>/`, closes one gap per session until every standard is decided and every rewrite is a ticket, then runs those tickets with subagents. The code ends up worth copying, and the code becomes the docs.

Name the destination first. The destination is the alignment plan: one decided standard and one exemplar per area, and a ticket for every change that gets the code there. It fixes the scope of every gap.

## Rules that outrank the rest

**No breaking changes.** What a caller outside the code can see stays exactly as it is: API routes, request and response shapes, status codes, error bodies, events and messages, the database schema, public exports, config and environment names, CLI flags, and the UI: how it looks, how it behaves, its text and its URLs. Only the code behind those contracts changes. See [contracts.md](references/contracts.md).

**The majority does not win by default.** The most common pattern is often the bad one that got copied. Judge each variant against [principles.md](references/principles.md) and cite the principle. Count it, then judge it.

**An unknown is a gap. Never write it as an assumption.** When a standard needs a fact or a decision and no source gives it, add a row to `gaps.md`.

**No comments.** The code says what it does. Only a one-line business or decision why, or an outside constraint, may stay. See [comments.md](references/comments.md).

**Never invent a standard.** The options come from variants found in the code or from a cited source. Only the person's answer makes one a standard.

**Behavior stays.** Build, test, lint, and every contract check pass after each ticket, the same as before it. A ticket that changes behavior is rejected.

**Read only until ready.** Chart and work sessions write only the align folder. Code changes only in `apply`, on a local branch, after a yes. Never push.

## Plan, then apply

Each gap resolves a decision. The map is done when every area has a standard and every change is a ticket. `apply` is part of this effort, so the map's Notes always say: `Execution: apply runs the rollout after ready.` Before ready, stop at the decision. The pull to just fix the code is the sign that a gap is ready to close, not to skip.

## Refer by name

A gap's name is its question. Use the question when you talk to the person and in Decisions so far. The id rides along. It never stands in for it.

## The map

Every run has the same folder and the same files. See [structure.md](references/structure.md). `align.md` holds the header, the map, and one section per area. `gaps.md` holds the gaps. `rollout.md` holds the tickets, written at ready.

The status words are `draft`, `discussion`, `ready`, `applying`, `aligned`, and `abandoned`.

### The map body

```markdown
## Map

### Destination

<one or two lines. The standards this run decides and the rollout that reaches them.>

### Notes

Scope: <the parts or folders this run covers>
Skills: <only the skills this run needs>
Preferences: <the person's standing preferences>
Execution: apply runs the rollout after ready.

### Decisions so far

- <gap question> (<id>): <one-line gist>

### Not yet specified

<one line per in-scope question you cannot phrase yet, or None.>

### Out of scope

<one line per question past the destination, and why. Every change that would break a contract lands here.>
```

### Gaps

One row in `gaps.md` is one gap. The question fits one session and says when it is done. **Claim** a gap by setting `owner` before any work. The **frontier** is status `open`, unblocked, and unclaimed, in the order of [Danger first](#danger-first).

## Gap types

**HITL** means the person speaks for themselves and you work with them. **AFK** means you drive the gap alone. Never answer the person's side of a HITL gap.

**Research** (AFK). A fact, not a preference. The survey of one area is research: a subagent with a fresh context reads the code and writes `survey/<area>.md` by [survey.md](references/survey.md). A principle or practice that needs an outside source is research too.

**Grilling** (HITL). The default. Which variant becomes the standard. Give advice first, by [the grilling card](#the-grilling-card). Call `codebase-design` for the options, then `grilling` and `domain-modeling`. Ask this gap's question, and stop.

**Prototype** (HITL). Use when no module in the code is good enough to be the exemplar, or the person wants to see the standard before choosing it. Rewrite one small module the way the standard says, as a file under `prototypes/`, never in the code. The person's reaction is the answer.

**Task** (HITL or AFK). Work that must finish before a decision can be made, such as finding out which contract checks exist, or asking who owns a public API. Drive it when you can. Otherwise give the person a checklist.

### The grilling card

Show this, then ask one question:

```text
<area> (<id>): <question>
A. <variant>   <count> files, <added in the last 90 days>   <verdict>: <principle id and why>
B. <variant>   ...                                              recommended: <why, with the principle>
C. <variant>   ...
Exemplar: <the module that shows the recommended variant best>
Contract: <none | which frozen surface it touches, and the outcome you propose>
Changes: <files to rewrite>   Risk if left open: <what keeps spreading>
```

The person may pick a variant, give a standard of their own, keep more than one with a reason (`exception`), or ask for research first. Write down the outcome: `apply`, `new-only`, `adapter`, or `exception`, by [contracts.md](references/contracts.md).

## Danger first

Order the frontier by danger, then by files touched:

1. `bad spreading`: fails a principle and was added in the last 90 days. Every day open adds copies.
2. `bad majority`: fails a principle and is the most common variant. The next agent copies it first.
3. `bad`: fails a principle.
4. `inconsistent`: every variant passes, the code just does it more than one way.

## Fog of war

Not yet specified is the **fog of war**: in-scope questions still too vague to be gaps, such as an area not yet surveyed, or a standard that depends on another one. A question you can phrase now is a gap, even when it is blocked. Resolving a gap lets you phrase the next ones. Fog must be `None.` at ready.

## Companion skills

Call each by its exact name with the Skill tool: `grilling`, `domain-modeling`, `research`, `codebase-design`, `writing-for-agents`, `deslop`. Call `writing-for-agents` on each edit of `code-standards.md` or an ADR. Call `deslop` on every diff in apply. If one is not installed, say so once, name `/setup-nstack-skills`, and do that step by the rules in this skill.

## Invocation

The person types `/align-code`. Read the first word after it.

| Typed | Mode |
| --- | --- |
| nothing | List, see [help.md](references/help.md) |
| `help` | Help, see [help.md](references/help.md) |
| `new <name>` | Chart |
| `<name>` or `<name> grill [gap]` | Work |
| `<name> status`, `close <gap>`, `drop <gap>`, `abandoned` | See [help.md](references/help.md) |
| `<name> ready` | Ready, see [ready-gate.md](references/ready-gate.md) |
| `<name> apply` | Apply, see [rollout.md](references/rollout.md) |
| `check` | Check the current branch's diff, see [advise.md](references/advise.md) |
| `advise` | Audit drift, see [advise.md](references/advise.md) |

Resolve one gap per session, then stop. Research gaps run beside it. Every session ends by writing state to disk, see [resume.md](references/resume.md).

### Chart the map

1. **Preflight.** Read `AGENTS.md` for the build, test, and lint commands. When it has none, tell the person to run `/setup-agents-md` first and stop. Read `docs/agents/code-standards.md` and the ADRs when they exist: each standards line is a candidate standard, never a decided one. Find which contract checks the repo already has, by [contracts.md](references/contracts.md).
2. **Name the destination.** Call `grilling` and `domain-modeling`. Agree on the scope: the whole repo, or named parts. Done when the destination is one or two lines the person agrees with.
3. **Sweep.** Run every area in [survey.md](references/survey.md) against the scope. Each area ends as a research gap (survey it), a fog line, or `n/a` with a reason in `log.md`.
4. **Create the folder** by [structure.md](references/structure.md), with the header at `draft`, the map, and one section per area.
5. **Add the gaps.** Each row starts `open`. Fill `blocks` in a second pass, with real ids. A frozen surface with no check is a task gap. Set status `discussion`.
6. **Start the survey subagents**, one per area, by [survey.md](references/survey.md).
7. **Stop.** Log one line. Tell the person the gap count by type and the first frontier gap.

A second `new` for a name that exists stops. Tell them to resume.

### Work through the map

1. **Load and catch up** by [resume.md](references/resume.md). Turn each finished survey into grilling gaps: one per difference, labelled by [Danger first](#danger-first). An area with one variant that passes the principles is `consistent`: one line in its section, no gap.
2. **Choose the gap and claim it.** Use the one the person named. Otherwise take the first frontier gap.
3. **Resolve it by type.** On a grilling gap, the card comes before the one question.
4. **Record the resolution.** Write the answer and the outcome on the row and set `decided`. With no answer, set `waiting-on-input`. Advice alone never closes a gap.
5. **Write it into `align.md`.** In the area's section: the standard in one plain sentence, the exemplar, the outcome, and the files that must change. Add the gist to Decisions so far.
6. **Update the map.** Add the gaps this answer opens, then fill `blocks`. Delete fog you can now phrase. A change that would break a contract goes to Out of scope, with the outcome it gets instead.
7. **Stop.** Write state.

Other sessions may edit this folder at the same time.

### Ready

Follow [the ready gate](references/ready-gate.md). Print pass or fail for each check. Any fail stops ready. When all pass, set `ready` and write `rollout.md`.

### Apply

Follow [rollout.md](references/rollout.md). Show the rollout and wait for a yes. Subagents work one ticket each. The main session reviews every diff before it commits. At the end, verify, trim `code-standards.md`, write the ADRs, and set `aligned`.

## When this is the wrong answer

Say so before you chart.

- The code is small enough to read in one session and already follows one way. Say so and stop.
- The person wants a contract made consistent. That is a breaking change: a versioned API or a migration, which is `/tech-design`.
- The repo has no build or test command. Run `/setup-agents-md` first. Without them, no ticket can prove it kept behavior.
