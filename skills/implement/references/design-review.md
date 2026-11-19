# Design review

The third reviewer, beside the Standards and Spec reviewers of `code-review`. It asks one question: is the code easier to change after this diff than before it?

It runs in a subagent with a fresh context. It did not write the code and does not know why it was written this way. It reads, writes nothing, and changes no code.

## Input

- The diff from the start commit.
- The ticket.
- The paths to the spec, `docs/agents/code-standards.md`, `docs/adr/`, and `GLOSSARY.md`, where they exist.

Nothing else. Not the plan, not the reasoning, not a summary of the work.

## Read

The diff, then the files it touches and their direct callers. The ADRs whose titles match those files. The glossary terms the diff uses. Stop at direct callers.

## Ask

A yes is a finding.

| Question | Source |
| --- | --- |
| Does a module the diff adds fail the deletion test? Delete it in your head: if the complexity does not come back in its callers, it is a pass-through. | `codebase-design`: depth |
| Does the diff add an `if`, a flag, or a boolean to code that already branches on a mode? | `codebase-design`: depth |
| Does the diff add a second way to do something the code already does? | the existing way, by file and line |
| Must a caller now know what a module should hide (call order, internal state)? | `codebase-design`: interface |
| Is there copied code that should have one home? | both places, by file and line |
| Does the diff add a seam, a layer, an option, or a parameter that nothing uses, or a seam the spec did not agree? | the spec, or `codebase-design`: seam |
| Do the tests reach past the interface into the inside? | `codebase-design`: interface |
| Did the old shape stay behind after a refactor: a wrapper, a compatibility layer, dead code? Not a finding when the ticket is an expand step of an expand-contract plan. | the ticket |
| Does the diff add or edit a comment, `TODO`, `HACK`, or suppression (`as any`, `@ts-ignore`, `eslint-disable`, `# type: ignore`) that covers a shortcut instead of fixing its cause? | `comment-root-cause` |
| Does the diff change behaviour that no test covers? | the tests |
| Does a name differ from `GLOSSARY.md`? | the glossary |
| Does the diff go against an ADR? | the ADR |

## Output

At most 10 findings, the worst first:

```text
<file:line>: <finding>. Source: <source>. Fix: <one line>.
```

No praise, no summary, no code. No finding: say `none`. A finding outside the files the diff touches: mark it `outside`.
