# Git

How a prep refactor runs, and how it stops.

## Before

1. `git status`. The working tree holds changes that are not yours: ask the person to commit or stash them. Never stash, reset, or commit someone else's work on your own.
2. Note the start commit: `git rev-parse HEAD`. Put it in the card's plan line.
3. Stay on the branch the ticket is on. No branch yet and you are on the default branch: make one, by the repo's `AGENTS.md`.

## Refactor

1. No test covers the behaviour you will move? Write a characterization test first: it pins what the code does today. Run it.
2. Refactor in the smallest steps that each leave the tests green. Run the tests after each step.
3. Move every caller to the new interface and delete the old one in the same change. No compatibility layer for code only we call.
4. Test at the interface, not the inside. Delete tests that only pinned the old inside.
5. One commit: `refactor: <what>, to make room for <ticket>`. Then the ticket in its own commit on top.

Never push. Never amend or rebase a commit you did not make in this session.

## Tripwires

Stop the refactor the moment one fires:

- It needs a file outside the plan on the card.
- The tests fail twice in a row on the same step.
- It needs a behaviour choice, a public contract change, or goes against an ADR.
- The diff is past twice the size the card planned.
- The person says stop.

Do not fix forward. Go to [Stop](#stop).

## Stop

1. Keep the work, never discard it:
   - Changes not committed: `git stash push -u -m "care-for-the-code: <ticket>: <what>"`.
   - Refactor commits from this session, not pushed: show them, and ask before `git reset --keep <start commit>`. The commits stay reachable by their hash. Write the hash in the follow-up.
2. Check that the tree is back at the start commit and the tests pass.
3. Write the follow-up by [follow-up.md](follow-up.md), with the stash name or the commit hash, and the tripwire that fired.
4. Ask the person: build the ticket now, no worse, or stop here.
