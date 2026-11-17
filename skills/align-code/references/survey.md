# Survey

Find every thing the code does more than one way. Judge every variant, even when it is the only one: an anti-pattern used everywhere is still `bad`. Count each. Never decide. Never change code.

## Discover

Build the list from the code in scope: the stack, its frameworks, the folders, and every place the code does one thing in more than one way. The seed list below is a checklist, not the run's list. Every seed area is on the Areas list as `- <Area>: <Ask>` with the Ask copied from the table, or `- <Area>: n/a: <reason>`. A new area's Ask is one line. The survey brief copies that Ask word for word.

Rule: anything the code in scope does in two or more ways that no area on the list covers must become an area. The main session adds it to `align.md` with a one-line reason in `log.md`. A survey subagent only lists it under New areas in its own file. Never add an area for anything else.

Write the list into `align.md` before any survey starts, with `n/a` areas marked on it. The person may add or drop areas. A dropped seed area stays on the list as `n/a: dropped by the person`. A dropped area that is not a seed is removed, its section included. Surveys skip `n/a`. After surveys have started, record a list change in `align.md` and in `log.md`. An added area gets a survey gap, and that gap starts before the session stops. Close a dropped area's open survey gap as `accepted-risk`, owner the person, answer `drift in this area stays because the area was dropped`.

Each area, seed or new, gets one line in `log.md`: why it is on the list, or why it is `n/a`.

Each area on the list ends as a survey gap, a fog line, or `n/a: <reason>` in its section of `align.md`.

## Seed list

| # | Area | Ask |
| --- | --- | --- |
| 1 | Naming | One naming scheme? One word, one meaning? |
| 2 | Files and folders | Grouped one way? Where does a new file go? |
| 3 | Module boundaries | Do modules reach into each other? One way to expose a module? |
| 4 | Internal interfaces | Deep modules or forwarding wrappers? One way to pass options? |
| 5 | Errors | Throw, result, null, or code? Caught and logged where? |
| 6 | Nulls and optionals | How is a missing value shown and checked? |
| 7 | Types | How strict? Escape hatches? Domain types or raw values? |
| 8 | Async | One style? Timeouts, retries, cancellation? |
| 9 | Validation | Where, and with what? Once at the edge? |
| 10 | Auth checks | Where is the caller checked, and with what? Same pattern on every path? |
| 11 | Data access | One layer, or queries anywhere? One way to fetch and cache data? |
| 12 | Dependencies | Injected, imported, or global? |
| 13 | Config | Read in one place? |
| 14 | Logging | One logger, one shape, logged once? |
| 15 | Comments | Every comment against [comments.md](comments.md). |
| 16 | Duplicate helpers | The same helper twice? |
| 17 | UI components | One way to structure, hold state, and style? |
| 18 | Tests | One structure, naming, mocking, setup? |

## When

- End of chart: one subagent per survey gap, all at once.
- Start of a session: one per survey or research gap still `open`. A gap in `research` with its file: read the file. Without its file: ask the person once whether the session that started it is still open. Yes: leave it and read its file next session. No: its subagent died with that session, so start it again.
- During a session: a new survey gap starts before you stop.

Surveys never block the session. Model: `mid` (`sonnet` in Claude Code).

## Brief

Give this, and nothing from the conversation:

```markdown
Area: <name and Ask, word for word>
Gap: <id>, in docs/align/<folder>/gaps.md
Scope: <Scope from align.md>
Judge: by the Judging section of <full path to SKILL.md>, with `codebase-design`, the `code-review` smell baseline, and <full path to references/comments.md>. Plus docs/agents/code-standards.md if it exists.
Write: docs/align/<folder>/survey/<area>.md. Create its folder if it is missing.
New areas: one line per behavior done in two or more ways that no area in align.md covers, formatted `- <area>: <the two or more ways>, <files>`. If there are none, write `none`. Do not edit align.md or log.md.
Return: <gap id> <area>: <consistent | inconsistent>, danger <danger>, <n> questions, <n> new areas, <path>
Do not: change code, decide, call a live system, edit any file but the one in Write
```

Before it starts, the main session sets the gap's `owner` to `survey` and status `research`. The table stays in the file.

## Counting

- Read each hit before you count it. A search result is a candidate, not a count.
- Count files, not lines. Time does not matter: count all code in scope.
- One example per variant, by module and symbol.
- No source for a verdict: write `unjudged` as the Verdict and `none` as the Source, and add a Still unknown line naming the source it needs. Any `unjudged` variant makes the Danger `unjudged`. Never guess a verdict.

## The file

```markdown
# <area>

Gap: <id>
Date: <yyyy-mm-dd>

## Answer
<consistent: only one variant, and it is `good` | inconsistent: anything else>. <one line>

## Variants
| Variant | Files | Example | Verdict | Source |
| --- | --- | --- | --- | --- |

## Exemplar
<module, and why. Or: none.>

## Danger
<a level from Danger first in SKILL.md, none, or unjudged>

## Questions
- <one line per standard to decide. Never one per file or per line.>

## Still unknown
- <what the code did not answer>

## New areas
none
```

## Closing

- On catch-up, the main session writes the Answer on the row, links the file, and sets `decided`. The only gap closed without the person.
- New areas: if the section is only `none`, add nothing. For any other line, if that area is already on the list in `align.md`, skip it. Otherwise add it once as `- <Area>: <one-line Ask>`, log the reason, add a survey gap, and start that survey.
- Each Question becomes a grilling gap. Each Still unknown becomes a gap. A missing source is a research gap that blocks the area's grilling gaps.
- Only one variant, `good`: the area is `consistent`. No gap.
- Only one variant, `weak` or `bad`: one grilling gap, what replaces it. Danger by Danger first in SKILL.md: `bad` is `bad majority`, `weak` is `inconsistent`.
