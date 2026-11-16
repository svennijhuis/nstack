# Principles

Every verdict and every recommendation names one of these ids. Edit this file to make it yours. A rule the person states in a session outranks it, and goes on the gap row.

## Verdicts

- **good**: follows every principle that applies. Copy it.
- **weak**: breaks none, but makes the next change harder.
- **bad**: breaks one. Every copy costs.

## Principles

| Id | Rule | Bad | Source |
| --- | --- | --- | --- |
| P1 | Deep modules: small interface, much behind it. | Wrappers that forward. Callers that know the insides. | Ousterhout, *A Philosophy of Software Design*. `codebase-design`. |
| P2 | Illegal states cannot be built. | A status string and booleans that contradict. | Minsky: https://blog.janestreet.com/effective-ml-revisited/ |
| P3 | Parse at the edge, pass a proven type. | The same check repeated inside. | King: https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/ |
| P4 | Errors are explicit and handled once. | Swallowed catch. Null for failure. Logged at every layer. | Ousterhout, ch. 10. The language's error guide. |
| P5 | Logic in plain functions, side effects at the edges. | Rules mixed with database and HTTP calls. | Bernhardt: https://www.destroyallsoftware.com/talks/boundaries |
| P6 | Dependencies are passed in. | Globals, locators, environment reads deep inside. | Seemann, *Dependency Injection Principles, Practices, and Patterns*. |
| P7 | Duplication beats the wrong abstraction. | A shared helper with a flag per caller. | Metz: https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction |
| P8 | Names use the project's words. One word, one meaning. | `data`, `manager`, `utils`. Two words for one thing. | Evans, *Domain-Driven Design*. `domain-modeling`. |
| P9 | What changes together lives together. | One change across six folders. | Parnas, 1972. |
| P10 | No comments. See [comments.md](comments.md). | A comment that explains code. | pstack `no-comments`. |
| P11 | Tests check behavior through the public interface. | Tests that mock everything and break on refactor. | Beck, *TDD by Example*. Dodds: https://kentcdodds.com/blog/testing-implementation-details |
| P12 | A tool checks what a tool can check. | A style rule only in a doc. | Pocock: https://www.youtube.com/watch?v=Fj8DKMbdIzU |
| P13 | Less code. Nothing defensive no caller needs. | Impossible-case checks. Unused options. | `deslop`. |

## Use

- Known bad patterns are listed in [anti-patterns.md](anti-patterns.md). Each names its principle.
- Judge a variant by the principles its area touches. Name the id and one line.
- Two principles pull apart: say so on the card, recommend one. The person decides.
- No principle fits: research one with a source. Never judge without one.
- The language's or framework's official guide counts as a source.
