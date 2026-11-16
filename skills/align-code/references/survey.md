# Survey

The survey finds every place where the code does the same thing in more than one way, counts each way, sees which ways are spreading, and judges each against [principles.md](principles.md). It never decides. It reads the code and writes one file per area.

## The areas

Run every area at chart against the scope. Each ends in exactly one of: a research gap that surveys it, one line under Not yet specified, or one `log.md` line `sweep <area>: n/a: <reason>`.

| # | Area | Ask |
| --- | --- | --- |
| 1 | Naming | Do files, types, functions, and variables follow one naming scheme? Does one word mean one thing? |
| 2 | Files and folders | Is code grouped one way: by feature, by layer, or mixed? Where does a new file go? |
| 3 | Module boundaries | Do modules reach into each other's insides? Is there one way to expose a module? |
| 4 | Internal interfaces | Are modules deep, with a small interface, or shallow wrappers? One way to pass options? |
| 5 | Errors | How does a failing call report it: throw, a result type, null, an error code? Where is it caught and logged? |
| 6 | Nulls and optionals | How is a missing value shown and checked? |
| 7 | Types | How strict? Any untyped escape hatches? Domain types or raw strings and numbers? |
| 8 | Async and concurrency | One async style? How are timeouts, retries, and cancellation done? |
| 9 | Validation | Where is input checked, and with what? Parsed once at the edge or checked again inside? |
| 10 | Data access | How does code reach the database or a store: one layer, or queries anywhere? |
| 11 | Dependencies and setup | How does a module get what it needs: injected, imported, global? |
| 12 | Config | How is config read: one place, or environment reads scattered through the code? |
| 13 | Logging | One logger, one shape, one place that logs an error? |
| 14 | Comments | Which comments say a why the code cannot, and which explain code, mark sections, or hold dead code? Which hide a surprise or a suppression? See [comments.md](comments.md). |
| 15 | Duplicate helpers | The same helper written more than once? |
| 16 | Slop | Code an agent left behind: defensive checks nothing needs, unused code, wrappers that only forward. Use `deslop` to find it. |
| 17 | UI components | One way to structure a component, hold state, fetch data, and style? |
| 18 | Tests | One structure, naming, and way to mock and set up? Survey it, but its tickets run last. |

Add an area the stack needs that this list misses. Write it in `log.md` with the reason.

## When subagents start

1. **End of chart.** One subagent per area that became a research gap, all at once.
2. **Start of a work session.** One for each survey gap added since the last session and still `open`.
3. **During a session.** When a gap opens a survey, start it before you stop.

Subagents never block the session.

## Model

Survey subagents read a lot and judge a little. Use a mid model, such as `sonnet` in Claude Code. Use the main model for an area that needs heavy judgment, such as module boundaries in a large repo.

## The brief

Give each subagent this, and nothing from the conversation:

```markdown
Area: <area name and its Ask line, word for word>
Gap: <id>, in docs/align/<folder>/gaps.md
Scope: <the Scope line from align.md>
Principles: <full path to this skill's references/principles.md>, and docs/agents/code-standards.md if it exists
Contracts: <full path to this skill's references/contracts.md>. Mark every variant that sits on a frozen surface.
Write: docs/align/<folder>/survey/<area>.md
Do not: change any code, decide the standard, call a live system, edit align.md
```

Write the paths from the working directory. The subagent claims the gap by setting `owner` and status `research`.

## How to count

- Find each variant by reading the code. Search helps you find candidates. It is not a count by itself: read enough hits to be sure each one is that variant.
- Count files, not lines.
- For spread, look at what the last 90 days of git history added: `git log --since=90.days --diff-filter=AM -p` over the scope, and count new uses of each variant. In a shallow clone, say how far back the history goes.
- Name one example per variant by module and symbol.

## The survey file

`survey/<area>.md`, always in this shape:

```markdown
# <area>

Gap: <id>
Date: <yyyy-mm-dd>
History read: <from date> to <to date>

## Answer

<consistent | inconsistent>. <one or two lines>

## Variants

| Variant | Files | Added in last 90 days | Example | Verdict | Principle | Frozen surface |
| --- | --- | --- | --- | --- | --- | --- |
| <short name> | <n> | <n> | <module, symbol> | good, weak, or bad | <id and one line> | <none or which> |

## Exemplar

<the module that shows the best variant most cleanly, and why. Or: none good enough, propose a prototype.>

## Danger

<bad spreading | bad majority | bad | inconsistent | none>

## Questions

- <each difference as a question the person can answer. One line each.>

## Still unknown

- <what reading the code did not answer>
```

## Closing a survey gap

- The subagent writes the Answer on the row, links the file, and sets `decided`. A survey is the only gap an agent may close alone.
- The next work session turns each line under Questions into a grilling gap with its danger. Each line under Still unknown becomes a gap too.
- An area with one variant that is `good` needs no grilling. Its section reads `consistent`.
