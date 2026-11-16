# Principles

The yardstick for every variant. A count says what the code does most. A principle says whether that is worth copying. Every verdict in a survey and every recommendation on a grilling card names one of these ids.

Edit this file. Add your own, change one, or delete one. A rule the person states in a session outranks any principle here, and goes on the gap row.

## Verdicts

- **good**: follows the principles that apply. Worth copying.
- **weak**: breaks none, but makes the next change harder than it needs to be.
- **bad**: breaks a principle. Every copy adds a bug risk or a cost.

## The principles

| Id | Principle | Bad looks like | Source |
| --- | --- | --- | --- |
| P1 | Deep modules: a small interface hides a lot of work. | A wrapper that only forwards. A module whose callers must know its insides. | John Ousterhout, *A Philosophy of Software Design*. Also `codebase-design`. |
| P2 | Make illegal states unrepresentable. | A status string and three booleans that can contradict each other. | Yaron Minsky, "Effective ML": https://blog.janestreet.com/effective-ml-revisited/ |
| P3 | Parse, don't validate: check input once at the edge, then pass a type that proves it. | The same check repeated deep inside. Raw strings passed around after a check. | Alexis King: https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/ |
| P4 | Errors are explicit and handled once. A caller can see that a call can fail. One place logs it. | A swallowed catch. Null for an error. The same error logged at every layer. | Ousterhout, chapter 10, on exceptions. The language's own error guide. |
| P5 | Functional core, imperative shell: logic in plain functions, side effects at the edges. | Business rules mixed with database calls and HTTP. | Gary Bernhardt, "Boundaries": https://www.destroyallsoftware.com/talks/boundaries |
| P6 | Dependencies are explicit. A module gets what it needs passed in, not reached for. | A global, a service locator, or an environment read deep inside. | Mark Seemann, *Dependency Injection Principles, Practices, and Patterns*. |
| P7 | Duplication is cheaper than the wrong abstraction. | A shared helper with flags for each caller. Also: the same helper written five times. Judge which one. | Sandi Metz: https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction |
| P8 | Names say what a thing is, in the project's words. One word, one meaning. | `data`, `handle`, `manager`, `utils`. Two words for one thing. | Eric Evans, *Domain-Driven Design*, ubiquitous language. Also `domain-modeling`. |
| P9 | Code is grouped by what changes together. | One change that touches six folders. | David Parnas, "On the Criteria To Be Used in Decomposing Systems into Modules", 1972. |
| P10 | No comments that explain code. A comment says only a decision or business why, or an outside constraint. A surprise in our own code is fixed in the code. | A comment that restates the next line. Banners. Commented-out code. A paragraph that excuses a workaround. | pstack `no-comments`: https://github.com/cursor/plugins/tree/ec569379616a4826b98f0f0a205dd3411b573611/pstack/skills/no-comments. Details in [comments.md](comments.md). |
| P11 | Tests check behavior through the public interface. | Tests that mock every collaborator and break on each refactor. | Kent Beck, *Test Driven Development: By Example*. Kent C. Dodds: https://kentcdodds.com/blog/testing-implementation-details |
| P12 | Let a tool check what a tool can check. | A style rule that lives only in a doc or a review comment. | Matt Pocock, "Delete (most of) your docs": https://www.youtube.com/watch?v=Fj8DKMbdIzU |
| P13 | Less code is better code. Nothing defensive that no caller needs. | Checks for cases that cannot happen. Unused options. Agent slop. | `deslop`. |

## How to use them

- A variant is judged by the principles its area touches. Name the id and one line on how it breaks or follows it.
- When two principles pull apart, such as P7 against duplication, say so on the card and recommend one. The person decides.
- When no principle here fits, research one: a gap of type `research` that cites a source. Never judge without one.
- The stack's own guide counts as a source: the language's official style guide, the framework's documented patterns. Cite it.
