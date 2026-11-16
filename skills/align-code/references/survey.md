# Survey

Find every thing the code does more than one way, and every anti-pattern in [anti-patterns.md](anti-patterns.md), even when the code does it one way. Count each, see if it spreads, judge it. Never decide. Never change code.

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
| 16 | Slop | Unneeded checks, unused code, forwarding wrappers. Use `deslop`. |
| 17 | UI components | One way to structure, hold state, fetch, style? |
| 18 | Tests | One structure, naming, mocking, setup? |

A missing area the stack needs: add it, with the reason in `log.md`.

## When

- End of chart: one subagent per survey gap, all at once.
- Start of a session: one per survey gap still `open`.
- During a session: a new survey gap starts before you stop.

Surveys never block the session. Model: `mid` (`sonnet` in Claude Code). `main` for an area that needs heavy judgment.

## Brief

Give this, and nothing from the conversation:

```markdown
Area: <name and Ask, word for word>
Gap: <id>, in docs/align/<folder>/gaps.md
Scope: <Scope from align.md>
Principles: <full path to references/principles.md> and <full path to references/anti-patterns.md>, plus docs/agents/code-standards.md if it exists
Contracts: <full path to references/contracts.md>. Mark every variant on a frozen surface.
Write: docs/align/<folder>/survey/<area>.md
Do not: change code, decide, call a live system, edit align.md
```

The subagent claims the gap: `owner`, status `research`. It returns one line: `<gap id> <area>: <consistent | inconsistent>, danger <danger>, <n> questions, <path>`. The table stays in the file.

## Counting

- Read each hit before you count it. A search result is a candidate, not a count.
- Count files, not lines. `Files` and `Last 90 days` are both file counts.
- Spread: new uses in `git log --since=90.days --diff-filter=AM -p` over the scope. Shallow clone: say how far back.
- One example per variant, by module and symbol.

## The file

```markdown
# <area>

Gap: <id>
Date: <yyyy-mm-dd>
History: <from> to <to>

## Answer
<consistent | inconsistent>. <one line>

## Variants
| Variant | Anti-pattern | Files | Last 90 days | Example | Verdict | Principle | Frozen |
| --- | --- | --- | --- | --- | --- | --- |

## Exemplar
<module, and why. Or: none, propose a prototype.>

## Danger
<bad spreading | bad majority | bad | inconsistent | none>

## Questions
- <one line per standard to decide. Never one per file or per line.>

## Still unknown
- <what the code did not answer>
```

## Closing

- The subagent writes the Answer on the row, links the file, sets `decided`. The only gap an agent closes alone.
- Each Question becomes a grilling gap. Each Still unknown becomes a gap.
- One `good` variant and no anti-pattern: the area is `consistent`. No gap.
- An anti-pattern in every file of the area: danger `bad majority`, one grilling gap: how to remove it.
