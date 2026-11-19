---
name: care-for-the-code
description: Use when you start a ticket, issue, or task that changes code, before you write it, and when the ticket is itself a refactor. Also when the user asks to scan a path for refactor candidates. Checks whether the code the change lands in will hold it for the long term. Leaves the code no worse, refactors first only when it is small, and turns anything bigger into a ticket or a spec instead of doing it now.
---

The ticket is the tactical goal. The codebase is the strategic one. A ticket is not done when it works but leaves the code harder to change.

Caring is not refactoring. The floor is: **leave the code no worse.** A refactor is the exception, and only when it is small. Anything bigger becomes a ticket or a spec, for another session.

## Modes

| Mode | When | Does |
| --- | --- | --- |
| `care` | The default | Check, card, a prep refactor only after a yes |
| `no-refactor` | The person says "no refactor", the ticket says so, or a hotfix | Check, build no worse, every finding becomes a follow-up. No code outside the ticket |
| `off` | The person says skip | Nothing |

A default may be set in `AGENTS.md` under Rules: `care-for-the-code: no-refactor`. The person's word in this session outranks it.

## Rules

- **No worse, always.** In every mode: follow the shape the code already has, add no second way to do a thing, no new shortcut, no new term the glossary does not have.
- **Small or not now.** A prep refactor touches only files the ticket already changes, and their tests. It is one commit and smaller than the ticket. Anything more is `too big`.
- **In doubt, no refactor.** A follow-up ticket costs little. A refactor that grows costs the session.
- **Behaviour stays.** A refactor never changes behaviour, a public API, a schema, a config name, or a UI.
- **ADRs win.** Never refactor against an ADR. When the code fights one, ask the person.
- **Every finding cites a source**: a `codebase-design` term, an ADR, a glossary term, or a line in `docs/agents/code-standards.md`. No source: no finding.
- **Stop, do not fix forward.** When a [tripwire](references/git.md#tripwires) fires, stop the refactor, keep the work, and route it. Never push.

## Flow

1. **Size the check.** One file, no new module, no new term: check it yourself in a few lines. Otherwise a subagent with a fresh context runs the check by [check.md](references/check.md) and returns only the card. Never load the whole landing zone into this session for the check.
2. **Show the card.**
3. **Act on the verdict:**
   - `fits`: build.
   - `prep refactor`: wait for a yes, then [git.md](references/git.md). Then build.
   - `too big`: route it by [follow-up.md](references/follow-up.md). Then build the ticket no worse, unless the person picks another option.
4. **Before you finish:** did the ticket leave the code worse anywhere? Say where, or fix it.

### The card

```text
care-for-the-code (<mode>): <ticket>
Landing zone: <modules>
Findings:
- <finding>: <files>. Source: <source>.
Verdict: fits | prep refactor | too big
Plan: <the refactor in one line, then the ticket>. Or: <route: ticket | spec, and the options>.
```

`fits` with no findings is one line: `care-for-the-code: fits, <why in a few words>.`

`too big` asks one question:

- A. Build the ticket now, no worse, and write the follow-up as a [ticket or a spec](references/follow-up.md). Recommended.
- B. Stop this ticket. The follow-up comes first.
- C. Build it now with the bigger refactor anyway. Only when the person types it.

## Sessions

- **One refactor per session.** A prep refactor and the ticket share a session only when both are small. Otherwise commit the refactor, write the [handoff](references/follow-up.md#handoff), and stop. The next session builds the ticket on a clean context.
- **State lives in git and on disk**, never only in chat: the refactor commit, the stash, the follow-up file.

## When the ticket is a refactor

The ticket names the destination: a deeper module, same behaviour. The size rule then applies to the ticket's scope, not zero. Sketch two interfaces and pick the one that hides the most from its callers, by `codebase-design`. More than one good shape, or a public contract changes: it is a spec, by [follow-up.md](references/follow-up.md). Otherwise refactor by [git.md](references/git.md), with its tripwires.

## What to keep

- The person rejects a finding for a reason that will hold: offer an ADR, so the next agent does not raise it again. Use the format of the newest ADR in `docs/adr/`.
- A refactor makes a real decision: write the ADR in the same change, by the repo's `AGENTS.md`.
- A new or renamed term: update `GLOSSARY.md` in the same change.

## Scan

`/care-for-the-code scan [path]`: candidates without a ticket. See [scan.md](references/scan.md).

## Companion skills

Call by exact name: `codebase-design`, `grilling`, `domain-modeling`, `align-code`, `tech-design`, `comment-root-cause`. If one is missing, say so once, name `/setup-nstack-skills`, and go on by these rules.
