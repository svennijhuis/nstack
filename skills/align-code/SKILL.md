---
name: align-code
description: Use when the user wants to align a codebase on one set of code standards and principles, find where the code does the same thing in different ways, and decide which way wins.
---

Chart one standard per area in `docs/align/<yyyy-mm-dd>-<name>/`, close one gap per session, end with a report, then rewrite the code one standard at a time. Align the code to the standards. Nothing more.

**Destination:** one decided standard and one exemplar per area, a report of the files that do not match, and the code rewritten to match.

## Rules

- **Read only until aligned.** Before `aligned`, write only the align folder. Code changes only in `apply`, on a local branch, after a yes. Never push.
- **The majority does not win.** Count each variant, then judge it by [Judging](#judging). An anti-pattern is bad even when it is everywhere.
- **No breaking changes.** A standard never changes behavior, a public API, schema, config name, or UI. Such a change goes to Out of scope.
- **Comments follow `comment-root-cause`.** See [comments.md](references/comments.md).
- **An unknown is a gap.** Never an assumption or a guess.
- **Never invent a standard.** Options come from the code or a cited source. Only the person decides.
- **One gap per session.** Surveys run beside it.

## Invocation

| Typed | Mode |
| --- | --- |
| nothing | List the runs under `docs/align/`, newest first, with the `new` line |
| `new <name>` | [Chart](#chart) |
| `<name>` | [Work](#work) |
| `<name> report` | [Report](#report), by [report-gate.md](references/report-gate.md) |
| `<name> apply [area]` | [apply.md](references/apply.md) |

`<name>` matches the folder with or without its date. Layout of the folder: [structure.md](references/structure.md).

## The map

Statuses: `draft`, `discussion`, `aligned`, `abandoned`. `aligned` only through the [report gate](references/report-gate.md).

```markdown
## Map

### Destination
<one or two lines>

### Notes
Scope: <parts or folders>
Preferences: <the person's standing preferences>

### Areas
- <Area>: <Ask>
- <Area>: n/a: <reason>

### Decisions so far
- <gap question> (<id>): <one-line gist>

### Not yet specified
<one line per question you cannot phrase yet, or None.>

### Out of scope
<one line per question past the destination, and why. Every breaking change lands here.>
```

A gap's name is its question. **Claim** a gap by setting `owner` first. The **frontier** is `open`, unblocked, unclaimed, ordered danger first.

**Fog of war:** an in-scope question you cannot phrase yet is one line under Not yet specified. One you can phrase is a gap, even when blocked.

## Judging

Every verdict cites a source: a `codebase-design` term, a smell from the `code-review` baseline, [comments.md](references/comments.md), or a section of the language's or framework's official guide. No source: call `research`, or ask the person. Never judge without one.

- `good`: breaks nothing. Copy it.
- `weak`: breaks nothing, but makes the next change harder.
- `bad`: breaks a source. Every copy costs.

A rule the person states outranks every source, and goes on the gap row.

## Danger first

1. `bad majority`: `bad`, and the most common variant.
2. `bad`.
3. `inconsistent`: no variant is `bad`, but the code does it more than one way, or its one way is `weak`.

Research gaps come before all of them: they unblock the rest.

## Gap types

- **Research** (AFK). The survey of one area, by [survey.md](references/survey.md). A subagent with a fresh context does it.
- **Grilling** (HITL). Which variant becomes the standard. Show the card, ask one question, stop. Call `grilling`, `domain-modeling`, and `codebase-design`. Never answer the person's side.

### The grilling card

```text
<area> (<id>): <question>
A. <variant>   <files> files   <good | weak | bad>: <source, one line>
B. <variant>   ...
Recommended: <exactly one letter>: <why, with the source>. Or: none, research first.
Exemplar: <module>
Changes: <files>
```

Answers: a variant, the person's own standard, `exception` with a reason, or research first.

## Companion skills

Call by exact name: `grilling`, `domain-modeling`, `research`, `codebase-design`, `code-review`, `comment-root-cause`, `writing-for-agents`. `research` for a source a verdict needs. `writing-for-agents` on every edit of `align.md`. If one is missing, say so once, name `/setup-nstack-skills`, and go on by these rules.

## Modes

### Chart

1. **Scope.** Call `grilling` and `domain-modeling`. Agree the destination and the scope. Read `AGENTS.md` and `docs/agents/code-standards.md` when they exist: each line is a candidate, never a standard.
2. **Discover** the areas by [survey.md](references/survey.md#discover).
3. **Create the folder** by [structure.md](references/structure.md), with the Areas list in `align.md`. Status `draft`. Show the list and wait: surveys start only after the person approves it.
4. **Add the gaps.** One grilling gap: `Is comments.md our comments standard?`. A. as written, B. with the person's edits. Recommended: A. One research gap per approved area that is not `n/a`. Status `discussion`.
5. **Start the surveys**, one subagent per survey gap, all at once, by [survey.md](references/survey.md#when).
6. **Stop.** Log. Say the gap count and the first frontier gap.

A `new` for a name that exists stops. Tell them to resume.

### Work

1. **Catch up.** Read the header, the map, `gaps.md`, and the last five `log.md` lines. Turn each finished survey into gaps by [survey.md](references/survey.md#closing). Start any survey still `open`.
2. **Claim** the gap the person named, or the first on the frontier.
3. **Resolve** it by type.
4. **Record** the answer on the row, status `decided`. No answer: `waiting-on-input`. Advice never closes a gap.
5. **Write** a grilling gap's standard into its area section of `align.md`. Add the gist to Decisions so far.
6. **Update the map.** Add the gaps it opens. Clear fog you can now phrase.
7. **End.** Append one line to `log.md`, set `Updated`, and say three lines: what changed, what waits on whom, what is next.

Other sessions may edit the folder at the same time.

### Report

Run the [report gate](references/report-gate.md). On pass, print the report: for each area, the standard, the exemplar, and the files that do not match. Write no code. Rewriting is `apply`.

## When this is the wrong answer

Say so and stop.

- The code already does each thing one way.
- The person wants a public contract made consistent. That breaks callers: `/tech-design`.
