# Survey

Find every thing the code does more than one way. Judge every variant, even when it is the only one: an anti-pattern used everywhere is still `bad`. Count each, see if it spreads. Never decide. Never change code.

## Areas

Each area ends as a survey gap, a fog line, or `n/a: <reason>` in its section of `align.md`.

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
| 10 | Data access | One layer, or queries anywhere? |
| 11 | Dependencies | Injected, imported, or global? |
| 12 | Config | Read in one place? |
| 13 | Logging | One logger, one shape, logged once? |
| 14 | Comments | Every comment against [comments.md](comments.md). |
| 15 | Duplicate helpers | The same helper twice? |
| 16 | UI components | One way to structure, hold state, fetch, style? |
| 17 | Tests | One structure, naming, mocking, setup? |

A missing area the stack needs: add it, with the reason in `log.md`.

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
Do not: change code, decide, call a live system, edit any file but the one in Write
```

Before it starts, the main session sets the gap's `owner` to `survey` and status `research`. The subagent returns one line: `<gap id> <area>: <consistent | inconsistent>, danger <danger>, <n> questions, <path>`. The table stays in the file.

## Counting

- Read each hit before you count it. A search result is a candidate, not a count.
- Count files, not lines. `Files` and `Last 90 days` are both file counts.
- Spread: new uses in `git log --since=90.days --diff-filter=AM -p` over the scope. Shallow clone: say how far back.
- One example per variant, by module and symbol.
- No source for a verdict: write `unjudged` as the Verdict and `none` as the Source, and add a Still unknown line naming the source it needs. Any `unjudged` variant makes the Danger `unjudged`. Never guess a verdict.

## The file

```markdown
# <area>

Gap: <id>
Date: <yyyy-mm-dd>
History: <from> to <to>

## Answer
<consistent: only one variant, and it is `good` | inconsistent: anything else>. <one line>

## Variants
| Variant | Files | Last 90 days | Example | Verdict | Source |
| --- | --- | --- | --- | --- | --- |

## Exemplar
<module, and why. Or: none.>

## Danger
<a level from Danger first in SKILL.md, none, or unjudged>

## Questions
- <one line per standard to decide. Never one per file or per line.>

## Still unknown
- <what the code did not answer>
```

## Closing

- On catch-up, the main session writes the Answer on the row, links the file, and sets `decided`. The only gap closed without the person.
- Each Question becomes a grilling gap. Each Still unknown becomes a gap. A missing source is a research gap that blocks the area's grilling gaps.
- Only one variant, `good`: the area is `consistent`. No gap.
- Only one variant, `weak` or `bad`: one grilling gap, what replaces it. Danger by Danger first in SKILL.md: `bad` and spreading is `bad spreading`, `bad` otherwise is `bad majority`, `weak` is `inconsistent`.
