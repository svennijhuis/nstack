# Git

How a prep refactor runs, and how it stops.

## Before

1. `git status`. Changes in the tree that are not yours: ask the person to commit them first. Never stash, reset, or commit someone else's work.
2. Note the ticket branch and the start commit: `git rev-parse HEAD`.
3. Make the refactor branch from it: `git switch -c refactor/<ticket-slug>`.

## Refactor

1. No test covers the behaviour you will move? Write a characterization test first: it pins what the code does today. Run it.
2. Refactor in the smallest steps that each leave the tests green. Run the tests after each step.
3. Move every caller to the new interface and delete the old one in the same change. No compatibility layer for code only we call.
4. One commit: `refactor: <what>, to make room for <ticket>`.
5. Back to the ticket branch and bring it in: `git switch <ticket branch> && git merge --ff-only refactor/<ticket-slug>`. Delete the refactor branch. Then build the ticket on top.

Never push. Never amend or rebase a commit you did not make in this session.

## Tripwires

Stop the moment one fires:

- It needs a file outside the plan on the card.
- The tests fail twice in a row on the same step.
- It needs a behaviour choice, a public contract change, or goes against an ADR.
- The diff has grown well past the plan on the card. Say how far.
- The person says stop.

Do not fix forward.

## Stop

1. Commit what is there on the refactor branch: `git commit -am "wip: <what>, stopped: <tripwire>"`. The ticket branch never had it.
2. `git switch <ticket branch>`. Check that it is at the start commit and the tests pass.
3. Write the follow-up by [follow-up.md](follow-up.md). Name the branch `refactor/<ticket-slug>` under Work so far.
4. Ask the person: build the ticket now, no worse, or stop here.
