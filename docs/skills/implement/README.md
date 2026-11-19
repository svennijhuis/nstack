# implement

Make the agent care about the code while it builds a ticket, not only about the ticket. Say "implement this", or type `/implement <ticket>`.

## Why

Agents are trained on tactical work: solve the problem in front of you. Left alone, they pile each ticket onto the code as it is, and the code gets worse with every ticket. Told to care about the codebase, they are good at it.

This skill tells them. It is how the agent implements, not a gate before it. Every ticket leaves the code it touches deeper, better tested, free of comments that cover shortcuts (by `comment-root-cause`), and in the words of the glossary and the ADRs. Before it writes code, the agent says its call out loud: refactor first, and why, or fits as it is. At the end it names up to three places outside the ticket where a module should be deeper or tests are missing, scored like `improve-codebase-architecture`, so you can pick one.

## Playbooks

Like pstack's `poteto-mode`, the agent picks one playbook for the kind of ticket, copies its steps into a todo list, and reads only that playbook. The shared steps (read, shape, refactor first, build, review, fix, finish) sit once in `SKILL.md`. Each playbook has its own Reply: what its summary must show.

| Playbook | For | Its own proof |
| --- | --- | --- |
| `bug-fix` | something is broken | red reproduction first, the cause and the commit that caused it |
| `perf` | too slow, against a number | baseline and result with the same command |
| `migration-step` | one step of an expand-contract plan | old callers still work; contract only when no caller is left |
| `refactor` | structure only | the pin passes unchanged, old-against-new run, easier to read or revert |
| `small-change` | a text, a value, one line | a test that pins it, one reviewer |
| `feature` | new or changed behaviour | the call, what was refactored for it, red then green |

A ticket that writes stored state also runs `verify-flow`, on top of any playbook.

## How it works

1. **Read** the ticket (from the tracker or from `to-tickets`' local files), its spec (`to-spec` or `tech-design`), `AGENTS.md`, the code standards, the glossary, the ADRs that cover the change, and the code it lands in.
2. **Shape**: what would this code look like if the requirement had been there from the start? The spec's decisions and seams outrank the agent's own taste.
3. **Refactor first** where the change needs it: same behaviour, a pinning test at the agreed seam, small green steps, the old shape deleted.
4. **Build** with `tdd` at the agreed seams. Typecheck and the test file often, the full suite at the end.
5. **Review with fresh eyes.** The agent that wrote the code does not judge it. `code-review`'s Standards and Spec reviewers, plus a design reviewer that asks: is the code easier to change than before? Each gets only the diff, the ticket, and the paths to the spec and the docs. Not the plan or the reasoning.
6. **Fix** the findings in the ticket's files, with the same behaviour. This is the refactor `tdd` leaves to the review. Findings outside the ticket, against the spec, or rejected are named, never dropped.
7. **Commit**: ADR for a real decision, glossary for a new term. Prove it works by running the real thing, not only the tests, and name the one fact the change is safe because of. The refactor commit first, then the feature. The pull request is yours: `implement` stops at the commit.

A bug ticket starts with `diagnosing-bugs`: a red reproduction before any fix. A ticket that writes stored state runs `verify-flow` before and after, when it is installed. A finding that claims a bug counts only with a failing test, as in pstack's `interrogate`. A risky change gets a suggestion to run pstack's `blast-radius` before merge.

Caring is not adding layers. A new module must pass the deletion test, a seam must be one the spec agreed, and nothing gets an option nobody uses yet.

It asks the person only for a behaviour or public contract change the spec does not cover, a conflict with an ADR or the spec, a seam the spec did not agree, or two equal shapes.

## Compared to Matt Pocock's `implement`

His skill is the loop: fetch the ticket, `tdd` at the agreed seams, typecheck and tests, `code-review`, commit. This skill keeps that loop and adds the strategic part. That matters because in his chain refactoring falls between two skills: `tdd` leaves it to the review, and `code-review` only reports smells. Here the agent refactors before the feature to make room, and after it applies what the reviewers find. A third reviewer checks the design, because `code-review` checks standards and the spec, not whether the code got easier to change.

Both are named `implement`. Install one of them.

## Tests

`evals/implement/` holds the scenarios this skill was tested on, a script that builds their repos, and what passing looks like. Run them after you change the skill.

## Where it sits

Matt Pocock's flow: `wayfinder`, then `to-spec`, then `to-tickets`, then this skill per ticket. The nstack flow: `tech-design`, then this skill per ticket.

## With the other nstack skills

- `setup-agents-md` writes the ADRs, the glossary, and the Changes section this skill builds on.
- `align-code` is for a second way to do something across the whole codebase.
- `comment-root-cause` fixes the cause behind a comment that covers a shortcut.

Uses `tdd`, `code-review`, `codebase-design`, `comment-root-cause`, `diagnosing-bugs`, and `verify-flow`, and suggests `blast-radius`. `/setup-nstack-skills` installs the external ones.
