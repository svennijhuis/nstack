---
name: prep-refactor
description: Use only when the person types /prep-refactor. Before a ticket is built, checks whether the code it lands in needs a small refactor first. Does that refactor on its own branch with tripwires, or turns anything bigger into a follow-up ticket or a spec instead of doing it now.
disable-model-invocation: true
---

Make the change easy, then make the easy change. Only when the first part is small. Anything bigger is a follow-up, for another session.

The reflex lives in the repo's `AGENTS.md`, under Changes: leave the code no worse, refactor only in files you already change, stop and suggest `/prep-refactor` when a refactor looks needed. This skill is the deliberate version of that.

## Invocation

| Typed | Does |
| --- | --- |
| `/prep-refactor <ticket>` | [Check](#check), card, then the verdict |
| `/prep-refactor <ticket> no-refactor` | Check and card only. Every finding becomes a follow-up. No code outside the ticket |

`<ticket>` is the ticket text, a link, or a few words. Missing: ask for it, and stop.

## Rules

- **Small or not now.** A prep refactor touches only files the ticket already changes, and their tests. It is one commit. Anything more is `too big`.
- **In doubt, no refactor.** A follow-up costs little. A refactor that grows costs the session.
- **Behaviour stays.** A refactor never changes behaviour, a public API, a schema, a config name, or a UI.
- **ADRs win.** Never refactor against an ADR in `docs/adr/`. When the code fights one, ask the person.
- **A finding names its evidence**: the file and line, and what it costs this ticket. A design term alone is not evidence.
- **Stop, do not fix forward.** When a [tripwire](references/git.md#tripwires) fires, stop, keep the work, and write the follow-up. Never push.

## Check

A subagent with a fresh context runs [check.md](references/check.md) and returns only the card. This session does not read the landing zone for the check.

```text
prep-refactor: <ticket>
Landing zone: <files>
Findings:
- <finding>: <file:line>. Costs this ticket: <how>.
Verdict: fits | prep refactor | too big
Plan: <the refactor in one line, then the ticket>. Or: <the follow-up: ticket or spec>.
```

`fits` with no findings is one line: `prep-refactor: fits, <why in a few words>.`

## Verdict

- **`fits`**: build the ticket.
- **`prep refactor`**: wait for a yes. Then [git.md](references/git.md). Then the ticket, on top.
- **`too big`**: write the follow-up by [follow-up.md](references/follow-up.md). Then ask one question:
  - A. Build the ticket now, no worse. Recommended.
  - B. Stop. The follow-up comes first.

## Sessions

One refactor per session. When the refactor and the ticket are not both small, commit the refactor, write the [handoff](references/follow-up.md#handoff), and stop. The next session builds the ticket on a clean context.

## When the ticket is a refactor

The ticket names the destination: a deeper module, same behaviour. The size rule applies to the ticket's scope. Sketch two interfaces and pick the one that hides the most from its callers, by `codebase-design`. More than one good shape, or a public contract changes: a spec, by [follow-up.md](references/follow-up.md). Otherwise [git.md](references/git.md), with its tripwires.

## What to keep

- The person rejects a finding for a reason that will hold: offer an ADR, so the next agent does not raise it again. Use the format of the newest ADR in `docs/adr/`.
- A refactor makes a real decision: the ADR goes in the same change, by the repo's `AGENTS.md`.
- A new or renamed term: update `GLOSSARY.md` in the same change.

## Companion skills

Call by exact name: `codebase-design`, `tech-design`. If one is missing, say so once, name `/setup-nstack-skills`, and go on by these rules.

To look for candidates without a ticket: `/improve-codebase-architecture`.
