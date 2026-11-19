# care-for-the-code

Make the agent care about the codebase, not only the ticket, without a ticket that turns into a refactor nobody asked for. It starts on its own when the agent picks up a ticket. Type `/care-for-the-code scan` to look for candidates.

## Why

Agents are trained on tactical work: solve the problem in front of you. Left alone, they pile each ticket onto the code as it is. Told to care, they are good at the strategic part too. But a refactor that starts in the middle of a ticket eats the session's context and the person's review time.

So caring has a floor and a ceiling:

- **Floor, always:** leave the code no worse.
- **Ceiling, this session:** one small prep refactor, in files the ticket already changes, after a yes.
- **Everything bigger** goes back into the flow: a ticket, or a spec for `tech-design`.

## How a ticket runs

1. A subagent checks the code the ticket lands in against `AGENTS.md`, the code standards, `GLOSSARY.md`, and the ADRs. This session gets only a card of at most 15 lines.
2. Verdict: `fits`, `prep refactor`, or `too big`.
3. `prep refactor`: clean tree, start commit noted, one `refactor:` commit, then the ticket on top. Tripwires stop it: a file outside the plan, tests red twice, a behaviour choice, a diff twice the plan. On a stop, the work goes in a stash or stays reachable by its hash, and becomes a follow-up.
4. `too big`: a follow-up ticket, or a brief for `/tech-design new`. For a ticket from a design, it lands under `## Follow-ups` in that design's `tickets.md`.

## Modes

- `care`: the default.
- `no-refactor`: check and build no worse. Every finding becomes a follow-up. Also for hotfixes.
- `off`: skip.

Set a default in a repo's `AGENTS.md` under Rules: `care-for-the-code: no-refactor`.

## With the other nstack skills

- `tech-design` makes the tickets. This skill runs on each one, and sends what is too big back as a ticket or a spec.
- `align-code` is for a second way to do something across the codebase. This skill flags it on one ticket.
- `setup-agents-md` owns the ADRs and the glossary this skill reads and adds to.

Uses `codebase-design`, `grilling`, `domain-modeling`, `align-code`, `tech-design`, and `comment-root-cause`. `/setup-nstack-skills` installs the external ones.
