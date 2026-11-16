# Contracts

Alignment changes how the code is written. It never changes what a caller outside the code can see. This file says what is frozen, how each frozen surface is checked, and what happens to a standard that would break one.

## Frozen surfaces

| Surface | What stays exactly as it is |
| --- | --- |
| HTTP and RPC API | Routes, methods, request and response shapes, field names and casing, status codes, error bodies, headers |
| Events and messages | Topic or queue names, payload shapes, ordering and delivery promises |
| Database | Schema, table and column names, stored formats. No migration. |
| Public exports | Every exported name and its type in a package others import |
| Config | Environment variable names, config keys, defaults |
| CLI | Command names, flags, output that scripts read, exit codes |
| UI | How each screen looks, what it does, its text, its URLs and routes, what it sends to analytics |
| Files and storage | Paths, file names, and formats other systems read |
| Timing a caller relies on | Order of side effects, idempotency, what is sync and what is async |

When you are not sure a surface is frozen, it is. Ask the person, as a grilling gap.

## Outcomes for a standard

Every decided grilling gap gets one outcome:

| Outcome | When | What apply does |
| --- | --- | --- |
| `apply` | The change stays behind the contracts | Rewrites the code to the standard |
| `adapter` | The inside can follow the standard while a thin layer at the edge keeps the outside shape | Rewrites the inside, adds or keeps the edge layer, contract checks prove the outside is the same |
| `new-only` | Following the standard would change a frozen surface | Leaves the old code. Adds the frozen marker. New code follows the standard. |
| `exception` | The person keeps a second way on purpose | Leaves it. Adds the exception marker. The reason goes in the ADR. |

Making the contract itself consistent, such as renaming API fields, is out of scope. It needs a versioned API or a migration. Add one line under Out of scope and point at `/tech-design`.

## Markers

The code is the docs, so the warning lives where the agent reads it: one comment on the frozen or excepted symbol, never a paragraph.

```text
Frozen contract: do not copy this shape. New code follows <ADR file>.
Exception: <reason in a few words>. Do not copy. See <ADR file>.
```

Use the language's comment syntax. One marker per symbol or file, not per line.

## Contract checks

Every frozen surface the scope touches needs a check that runs before and after each ticket and shows no difference. At chart, find which checks exist. Each surface with no check becomes a task gap, and its check becomes a ticket that runs before every other ticket, against the unchanged code, to record the baseline.

| Surface | Check |
| --- | --- |
| HTTP and RPC API | A snapshot of the generated OpenAPI, GraphQL, or proto schema, diffed. Where nothing generates one, contract or snapshot tests on the responses. |
| Events and messages | Snapshot tests of each payload a producer emits |
| Database | No new or changed migration file in the diff. A schema dump, diffed, when the stack can produce one. |
| Public exports | A diff of the generated declaration or API report, such as `.d.ts` files or an API extractor report |
| Config and CLI | A diff of every config key and environment name read, and of the CLI help output |
| UI | Playwright screenshot diffs of the screens a ticket touches, plus the existing UI tests. Text and routes come with the screenshots. |
| Timing | The existing tests. When none covers it, the ticket may not touch it. |

The existing build, test, and lint commands always run too. A check that was already red before the first ticket is recorded in `log.md` and does not block, but a ticket may not make it worse.

## What a ticket may never do

- Change anything in the frozen surfaces table.
- Add or change a migration.
- Add a dependency. A standard that needs one is its own gap, and its ADR names it.
- Change a test's expected value to make it pass.
- Delete a test. A test may move or be rewritten only in the tests area, and must check the same behavior.
