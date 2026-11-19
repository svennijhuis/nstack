# implement

Make the agent care about the code while it builds a ticket, not only about the ticket. Say "implement this", or type `/implement <ticket>`.

## Why

Agents are trained on tactical work: solve the problem in front of you. Left alone, they pile each ticket onto the code as it is, and the code gets worse with every ticket. Told to care about the codebase, they are good at it.

This skill tells them. It is how the agent implements, not a gate before it.

## How it works

1. **Read** the ticket (from the tracker or from `to-tickets`' local files), its spec (`to-spec` or `tech-design`), `AGENTS.md`, the code standards, the glossary, the ADRs that cover the change, and the code it lands in.
2. **Shape**: what would this code look like if the requirement had been there from the start? The spec's decisions and seams outrank the agent's own taste.
3. **Refactor first** where the change needs it: same behaviour, a pinning test at the agreed seam, small green steps, the old shape deleted.
4. **Build** with `tdd` at the agreed seams. Typecheck and the test file often, the full suite at the end.
5. **Review with fresh eyes.** The agent that wrote the code does not judge it. `code-review`'s Standards and Spec reviewers, plus a design reviewer that asks: is the code easier to change than before? Each gets only the diff, the ticket, and the paths to the spec and the docs. Not the plan or the reasoning.
6. **Fix** the findings in the ticket's files, with the same behaviour. This is the refactor `tdd` leaves to the review. Findings outside the ticket, against the spec, or rejected are named, never dropped.
7. **Commit**: ADR for a real decision, glossary for a new term. The refactor commit first, then the feature.

Caring is not adding layers. A new module must pass the deletion test, a seam must be one the spec agreed, and nothing gets an option nobody uses yet.

It asks the person only for a behaviour or public contract change the spec does not cover, a conflict with an ADR or the spec, a seam the spec did not agree, or two equal shapes.

## Compared to Matt Pocock's `implement`

His skill is the loop: fetch the ticket, `tdd` at the agreed seams, typecheck and tests, `code-review`, commit. This skill keeps that loop and adds the strategic part. That matters because in his chain refactoring falls between two skills: `tdd` leaves it to the review, and `code-review` only reports smells. Here the agent refactors before the feature to make room, and after it applies what the reviewers find. A third reviewer checks the design, because `code-review` checks standards and the spec, not whether the code got easier to change.

Both are named `implement`. Install one of them.

## Where it sits

Matt Pocock's flow: `wayfinder`, then `to-spec`, then `to-tickets`, then this skill per ticket. The nstack flow: `tech-design`, then this skill per ticket.

## With the other nstack skills

- `setup-agents-md` writes the ADRs, the glossary, and the Changes section this skill builds on.
- `align-code` is for a second way to do something across the whole codebase.
- `comment-root-cause` fixes the cause behind a comment that covers a shortcut.

Uses `tdd`, `code-review`, `codebase-design`, and `comment-root-cause`. `/setup-nstack-skills` installs the external ones.
