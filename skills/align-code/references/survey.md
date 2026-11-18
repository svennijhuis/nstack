# Survey

Find every thing the code does more than one way. Judge every variant, even when it is the only one: an anti-pattern used everywhere is still `bad`. Count each. Never decide. Never change code.

## Discover

Build the Areas list from the code in scope: the stack, its frameworks, the folders, and every place the code does one thing in more than one way. The seed list below is a checklist, not the run's list. Every seed area is on the list as `- <Area>: <Ask>` (Ask copied from the table) or `- <Area>: n/a: <reason>`. A new area's Ask is one line.

New areas: only behavior that no area on the list could cover, even loosely. Query building is Data access, not a new area. Only the main session adds an area. A survey subagent lists candidates under New areas in its own file.

Chart step 3 writes the list into `align.md` and shows it. The person's reply may add or drop areas; the main session applies that to the list before chart step 4. Surveys skip `n/a`. After surveys start, record a list change in `align.md` and `log.md`. An area added then that is not `n/a`, including one from a survey's New areas, gets one survey gap if it has none: type `research`, status `open`, started before the session stops.

An area's section is derived from its gaps; rewrite it whenever one of them changes. An `n/a` area: `n/a: <reason>`. Dropping an area closes each of its gaps that is `open`, `research`, or `waiting-on-input` as `accepted-risk`, owner the person, answer `drift in <area> stays because the area was dropped`. A dropped seed stays on the list as `- <Area>: n/a: dropped by the person`. A dropped new area is removed with its section. Any other area: a gap not `decided` or `accepted-risk` gives `Waiting on <those ids>.`, and no gap yet (only while the list waits for approval) gives `Waiting on survey.` After chart step 4 every area has a gap, so use its id. When all its gaps are closed: one Standard block per decided grilling gap, or `consistent: <the one way>. Exemplar: <module>.` when the survey said consistent. Add `Accepted risk: <ids>` for any `accepted-risk` gap. When every grilling gap is `accepted-risk`, the section is only `Accepted risk: <ids>`.

Log one line per area added or dropped after the first list: `<yyyy-mm-dd> chart none: <area>: <why>`. The first list needs no per-area line.

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
Judge: by the Judging section of <full path to SKILL.md>, with `codebase-design`, the `code-review` smell baseline, and <full path to references/comments.md>. Plus docs/agents/code-standards.md if it exists. A missing source is `unjudged` by Counting, not a call to `research`.
Write: docs/align/<folder>/survey/<area>.md. Create its folder if it is missing.
New areas: one line per behavior done in two or more ways that no area in align.md covers, formatted `- <area>: <the two or more ways>, <files>`. If there are none, write `none`. Do not edit align.md or log.md.
Return: <gap id> <area>: <consistent | inconsistent>, danger <danger>, <n> questions, <n> new areas, <path>
Do not: change code, decide, call a live system, edit any file but the one in Write
```

Before it starts, the main session sets the gap's `owner` to `survey` and status `research`. The table stays in the file.

## Counting

- Read each hit before you count it. A search result is a candidate, not a count.
- Count files, not lines. A file that holds two variants counts once in each. "Most common" means most files. On a tie for most common, a tied `bad` variant counts as the most common only when it has 2 or more files. Two tied `bad` variants beside a more common good one: `bad`. Time does not matter: count all code in scope.
- A variant is one whole way of doing what the area asks. For Errors, throw, result, null, and code are the variants. A part of that way, such as where it is caught or how it is wrapped, is not a variant: it is a Question only when the code does that part more than one way. Identical copies of a helper are one variant, `weak` when it is in more than one file. A different body is a different variant. One example per variant, by module and symbol.
- No source for a verdict: do not call `research` and do not ask the person. Closing adds that research gap. Write `unjudged` as the Verdict and `none` as the Source, and add a Still unknown line naming the source it needs. The judged variants set the Danger. It is `unjudged` only when no variant is judged. A judging skill that is not installed is not a source, but an official language or framework guide still is. Never guess a verdict.

## The file

```markdown
# <area>

Gap: <id>
Date: <yyyy-mm-dd>

## Answer
<consistent: only one variant, and it is not `weak` or `bad` | inconsistent: anything else>. <one line>

## Variants
| Variant | Files | Example | Verdict | Source |
| --- | --- | --- | --- | --- |

## Exemplar
<module, and why. Or: none.>

## Danger
<a level from Danger first in SKILL.md, none, or unjudged>

## Questions
- <one line per standard to decide, at most 5, the most dangerous first. Never one per file or per line. Put any further lines below a line that says `later`.>

## Still unknown
- <what the code did not answer>

## New areas
none
```

## Closing

- On catch-up, the main session writes the Answer on the row, links the file, and sets `decided`. The only gap closed without the person.
- New areas: skip `none` and any area the list already covers. Match by behavior, not by name: `Translations` and `Localization` are one area. Add the rest by the Discover rule, with its survey gap.
- Each Question above `later` becomes a grilling gap. Leave the lines under `later` unopened. With more than 5 Questions and no `later` line, open the first 5 and treat the rest as under `later`. When those gaps are `decided` or `accepted-risk`, open the next 5 and delete them from under `later`. Every Question stays a gap, even one whose answer might change behavior, a public API, schema, config name, or UI. It moves to Out of scope only after the person says so, with one line there.
- Still unknown: one research gap for the area, naming every unknown and missing source. It blocks that area's grilling gaps. Do not edit another area's survey file. A bug or a fact for another area goes in this gap's text.
- A grilling gap takes the survey's Danger. When that is `unjudged` or `none`, write `inconsistent`. Grilling gaps from one survey tie in the order of its Questions. Leave every research gap's danger empty.
- Only one variant, `good` or `unjudged`: the Answer is `consistent`. No grilling gap. An `unjudged` variant keeps its research gap, and the section stays `Waiting on <that id>.` until it closes. If that source says `weak` or `bad`, change the Answer to `inconsistent` and add the grilling gap below.
- Only one variant, `weak` or `bad`: one grilling gap, what replaces it. Danger by Danger first in SKILL.md: `bad` is `bad majority`, `weak` is `inconsistent`.
