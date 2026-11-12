---
name: setup-home-repo
description: When the user types /setup-home-repo to create, update, check, or clean up a home repo.
---

A team with many repos copies its skills, steering files, MCP servers, and hooks into each one, or hides them in the user folder where they go stale. A home repo ends that. It is one repo that holds everything the agent needs in every session, plus a pointer to every other repo and source. The agent always starts in the home repo and reaches out from there.

This skill builds that repo from what the person already has, keeps it current, audits it, and cleans it up. It ends on a router skill inside the home repo, so one slash answers "what do I use for this?".

## Rules that outrank the rest

**Explore before you ask.** Read the disk, the git remotes, and the config first. Ask only what exploring did not answer. Every question carries a recommended answer.

**Read only until the plan is approved.** Setup and cleanup write nothing before the person approves the plan table. Advise never writes.

**Secrets stay out.** Never read `.env` or any other secret file. Never write a token, key, or password into a tracked file. Config names an environment variable instead.

**Never push.** Commit in the home repo. In any other repo, edit only on a new local branch. The person pushes.

**Work from what was found.** Never invent a component the person does not have. Never drop one because it fits no kind. It goes in the `other` row and you ask.

**Move a skill whole.** Copy the folder as it is. Never edit the body of a skill you move.

## The words

A **home repo** is the repo the agent starts in. A **child repo** is any other repo it points at. A **component** is one thing the agent uses: a skill, a hook, an MCP server, a rule, a pointer. A **kind** is its row in the registry. A **source** is a place outside git the agent reads or writes: a wiki, an issue tracker, a pipeline, a chat. A **harness** is the agent client: Claude Code, Cursor, Copilot, or Codex. The **map** is the list of one line per item that the router answers from.

## The registry

Every mode walks one table, [components.md](references/components.md). Each row is a kind: what counts, where to look, where it lives in the home repo, and what advise checks. A new kind is a new row. No mode changes.

Each found item gets one **bucket**:

| Bucket | Meaning | Action |
| --- | --- | --- |
| `shared` | Useful in more than one repo | Move to the home repo |
| `duplicate` | Same item in several places | Keep one in the home repo, remove the copies |
| `repo-specific` | Only makes sense in its repo | Leave it there |
| `installed` | Comes from a plugin or marketplace | Leave it, record the registration |

## The harnesses

Steering, repo pointers, and source pointers live in `AGENTS.md`, which all four harnesses read. Everything else goes where each harness in use looks for it. The paths per kind and per harness are in [harnesses.md](references/harnesses.md). Write files only for a harness the person uses. Where a harness has no place for a kind, say so. Do not fake one.

## The home repo

The layout, the two pointer formats, and the rule for many repos are in [layout.md](references/layout.md). Create only the folders that have content.

## Invocation

The person types `/setup-home-repo`. Read the first word after it.

| Typed | Mode | Writes |
| --- | --- | --- |
| nothing | Detect, then Setup or Status | Setup only, after approval |
| `add <thing>` | Add or update one item, see [add.md](references/add.md) | After the diff is shown |
| `advise` | Audit, see [advise.md](references/advise.md) | Never |
| `cleanup` | Fix what advise found, see [cleanup.md](references/cleanup.md) | After approval |
| `help` | The card, see [help.md](references/help.md) | Never |

### Detect

The working directory is a home repo when its `AGENTS.md` has a `## Repos` section written by this skill, or the person says it is. If it is one, print the status from [help.md](references/help.md) and stop. If it is not, run Setup.

A second Setup on an existing home repo never starts over. It explores again and proposes only the rows that changed.

### Setup

Follow [setup.md](references/setup.md) step by step.

1. **Explore the repos.** Find the git repos, their remotes, and how recently each changed.
2. **Explore the components.** Walk the registry over the chosen repos and the user folder. Give each item a bucket.
3. **Explore the sources and the harnesses.** Read remotes, MCP config, and the command line tools on the path.
4. **Ask what is left**, in numbered rounds, the recommended answer first.
5. **Show the plan.** One table of every item with where it is and where it goes, the drafted `AGENTS.md`, and the drafted map. Wait for approval.
6. **Apply.** Create the home repo, move the shared items, merge the config per harness, remove the moved copies in each child repo on a new local branch, commit in the home repo.
7. **Write the router** by [router.md](references/router.md).
8. **Report and stop.** One outcome per plan row, the branches created, what was skipped and why. The last line names the router slash as the place to start.

Setup is done when every plan row has an outcome and the router lists every item that was kept.

### After setup

`add`, `advise`, and `cleanup` keep the home repo true. Each one that changes an item changes its map line in the same diff, so the router never lags.

## When a home repo is the wrong answer

Say so before you build, and let the person choose.

- Everything could live in one monorepo, and nothing stops it. A monorepo is simpler.
- There is one repo. A home repo adds nothing.
- There are thousands of repos. A plugin marketplace fits better than pointers.
