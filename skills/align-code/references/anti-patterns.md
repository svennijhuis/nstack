# Anti-patterns

Patterns that are bad wherever they appear, even when the code uses them everywhere. Cheap agents write these often, and the next agent copies them. Edit this file to make it yours.

An anti-pattern is always verdict `bad`. Found in every file of its area: danger `bad majority`, never `consistent`.

| Id | Anti-pattern | Looks like | Principle | Area |
| --- | --- | --- | --- | --- |
| A1 | Swallowed error | Empty catch. Catch, log, carry on. | P4 | Errors |
| A2 | Null for failure | `return null` when a call failed | P4 | Errors |
| A3 | Log and rethrow | The same error logged at every layer | P4 | Errors, Logging |
| A4 | Silent fallback | `\|\| {}`, `?? 0`, a default that hides a missing value | P4 | Nulls and optionals |
| A5 | Type escape | `any`, unchecked casts, `@ts-ignore`, `# type: ignore` | P2 | Types |
| A6 | Stringly typed | A status as a free string, booleans that can contradict | P2 | Types |
| A7 | Flag parameter | A boolean argument that switches what a function does | P1 | Internal interfaces |
| A8 | Forwarding layer | A function or class that only passes the call on | P1, P13 | Internal interfaces |
| A9 | One-implementation abstraction | An interface, factory, or base class with one user | P7, P13 | Internal interfaces |
| A10 | God file | One file or function that does several jobs | P1, P9 | Module boundaries |
| A11 | Reaching inside | Importing another module's internals | P1 | Module boundaries |
| A12 | Hidden dependency | Environment read, global, or singleton deep inside | P6 | Dependencies, Config |
| A13 | Mutable global state | Module-level state changed at runtime | P5 | Dependencies |
| A14 | Repeated validation | The same check deep inside, after the edge | P3 | Validation |
| A15 | Query in a loop | A database or network call per item | P5 | Data access |
| A16 | Copy-paste twin | Two near-identical blocks | P7 | Duplicate helpers |
| A17 | Impossible-case check | Guards for what no caller can send | P13 | Slop |
| A18 | Dead code | Unused exports, branches, parameters, files | P13 | Slop |
| A19 | Magic value | An unnamed number or string with a meaning | P8 | Naming |
| A20 | Unbounded retry | A retry or poll loop with no limit or timeout | P4 | Async |
| A21 | Mixed async | Callbacks, promises, and async in one flow | P1 | Async |
| A22 | Mock-everything test | A test that mocks every collaborator | P11 | Tests |
| A23 | Comment that explains code | See [comments.md](comments.md) | P10 | Comments |

## Use

- **Survey:** every area also searches for its anti-patterns. Each one found is a variant row with its id.
- **Grilling card:** an anti-pattern needs no vote on which variant wins. The question is how to remove it: the replacement, the exemplar, the outcome.
- **Review:** a ticket diff that adds an anti-pattern fails.
- **Check and advise:** an added anti-pattern is a finding.
- **Lint advice:** every anti-pattern a rule can catch gets a row.
