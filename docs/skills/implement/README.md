# implement

Make the agent care about the code while it builds a ticket, not only about the ticket. Say "implement this" or type `/implement`.

## Why

Agents are trained on tactical work: solve the problem in front of you. Left alone, they pile each ticket onto the code as it is, and the code gets worse with every ticket. Told to care about the codebase, they are good at it.

This skill tells them. It is how the agent implements, not a gate before it: no extra subagent, no card, no stop.

## How it works

1. **Read** `AGENTS.md`, the code standards, the glossary, the ADRs that cover the change, and the code it lands in.
2. **Shape**: what would this code look like if the requirement had been there from the start?
3. **Refactor** where the change needs it: same behaviour, a pinning test first, small green steps, old shape deleted, its own commit before the feature.
4. **Build** the feature on the new shape.
5. **Check the diff**: is the code easier to change than before? ADR for a real decision, glossary for a new term.

It asks the person only for a behaviour or public contract change, a conflict with an ADR, or two equal shapes.

## With the other nstack skills

- `setup-agents-md` writes the ADRs, the glossary, and the Changes section this skill builds on.
- `tech-design` makes the tickets for a big feature. This skill builds each one.
- `align-code` is for a second way to do something across the whole codebase.

Uses `codebase-design` and `comment-root-cause` when installed.
