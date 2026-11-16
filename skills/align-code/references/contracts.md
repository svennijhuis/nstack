# Contracts

Change how the code is written. Never what a caller sees.

## Frozen

| Surface | Stays exactly as it is |
| --- | --- |
| API | Routes, methods, request and response shapes, field names, status codes, error bodies, headers |
| Events | Names, payloads, ordering, delivery |
| Database | Schema, names, stored formats. No migration. |
| Public exports | Every name and type a caller outside this repo imports: a published package, another repo, another service |
| Config | Environment names, keys, defaults |
| CLI | Commands, flags, parsed output, exit codes |
| UI | Look, behavior, text, routes, analytics |
| Files | Paths, names, formats others read |
| Timing | Order of side effects, idempotency, sync or async |

Not sure it is frozen? It is. Ask as a grilling gap.

**Inside the repo nothing is frozen.** An export only this repo imports is internal. The ticket changes it and every caller in the same commit. Never keep an old shape as a wrapper for an internal caller: the next agent copies the wrapper.

## Outcomes

| Outcome | When | Apply does |
| --- | --- | --- |
| `apply` | The change stays behind the contract | Rewrite to the standard |
| `adapter` | The inside can change, the outside cannot | Rewrite the inside, keep a thin edge layer |
| `new-only` | The standard would change a frozen surface | Leave it, add the frozen marker. New code follows the standard. |
| `exception` | The person keeps a second way on purpose | Leave it, add the exception marker |

Making a contract consistent is out of scope. Point at `/tech-design`.

## Markers

One per symbol, in the language's comment syntax:

```text
Frozen contract: do not copy this shape. New code follows <ADR file>.
Exception: <reason>. Do not copy. See <ADR file>.
```

## Checks

Every frozen surface in scope has a check that shows no difference before and after each ticket. A missing check is a task gap, and its ticket runs first, on the unchanged code.

**Every file a ticket changes must be run by a check.** A file no test runs, or a frozen response no test asserts, gets a characterization test in wave 0: it records what the code does today, on the unchanged code. Tests may be added. Never changed. Checks may live outside the scope.

| Surface | Check |
| --- | --- |
| API | Snapshot of the generated schema, diffed. None generated: response snapshot tests. |
| Events | Payload snapshot tests |
| Database | No migration in the diff. Schema dump diff when the stack can. |
| Public exports | Declaration or API report diff |
| Config, CLI | Diff of keys and environment names read, and of the help output |
| UI | Playwright screenshot diff of every touched screen, plus the UI tests |
| Timing | The existing tests. None: the ticket may not touch it. |

Build, test, and lint always run. Red before the first ticket: log it. A ticket may not make it worse.

## A ticket never

- changes a frozen surface
- adds or changes a migration
- adds a dependency
- changes a test's expected value
- deletes a test
