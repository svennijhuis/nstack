# prep-refactor

Make the agent care about the code, not only the ticket, without a ticket that turns into a refactor nobody asked for. Type `/prep-refactor <ticket>`.

## Why

Agents are trained on tactical work: solve the problem in front of you. Told to care about the codebase, they are good at it. But a skill that starts on every ticket costs context and gets in the way, and a refactor that starts in the middle of a ticket eats the session.

So it is split in two:

- **The reflex, always on, in `AGENTS.md`.** `setup-agents-md` writes a Changes section: leave the code no worse, refactor only in files you already change, and when a refactor looks needed, stop and suggest `/prep-refactor`. A few lines, no subagent, every task.
- **This skill, only when you type it.** It never starts on its own.

## How a run works

1. A subagent checks the files the ticket lands in, against `AGENTS.md`, the code standards, `GLOSSARY.md`, and the ADRs. This session gets only a card of at most 15 lines.
2. Verdict: `fits`, `prep refactor`, or `too big`.
3. `prep refactor`: after a yes, one `refactor:` commit on a branch `refactor/<ticket>`, brought into the ticket branch, then the ticket on top. Tripwires stop it: a file outside the plan, tests red twice, a behaviour choice, a diff well past the plan. On a stop, the work stays on that branch as a `wip:` commit, and the ticket branch is untouched.
4. `too big`: a follow-up in `docs/follow-ups/<date>-<slug>.md`, routed as a ticket or a spec. You move it to your tracker or a design, then delete the file.

`/prep-refactor <ticket> no-refactor` checks only, and writes every finding as a follow-up.

To look for candidates without a ticket, use Matt Pocock's `improve-codebase-architecture`. `/setup-nstack-skills` installs it.

## With the other nstack skills

- `setup-agents-md` writes the reflex, and owns the ADRs and the glossary this skill reads.
- `tech-design` takes a follow-up routed as a spec, when the work is big enough for it.
- `align-code` is for a second way to do something across the whole codebase.

Uses `codebase-design` and `tech-design`.
