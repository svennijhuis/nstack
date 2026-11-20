---
name: setup-home-repo
description: Use when the user wants to create, update, audit, or clean up a home repo that holds shared skills, steering files, MCP servers, and hooks for many repos.
---

A home repo is one repo that holds everything the agent needs in every session, plus a pointer to every other repo and source. The agent starts there. This skill builds it from what the person already has, keeps it current, audits it, and cleans it up.

## Rules that outrank the rest

- **Explore before you ask.** Read the disk, git remotes, and config first. Ask only what that left open, each question with a recommended answer.
- **Read only until the plan is approved.** Setup and cleanup write nothing before a yes. Advise never writes.
- **Secrets stay out.** Never read `.env` or another secret file. Never write a token, key, or password into a tracked file: config names an environment variable.
- **Never push.** Commit in the home repo, unless it is local only. In any other repo, edit only on a new local branch.
- **Work from what was found.** Never invent a component. One that fits no kind goes in the `other` row, and you ask.
- **Move a skill whole.** Copy the folder as it is. Never edit its body.
- **Write no skill of your own.** No router, updater, or helper skill. Adding and updating go through this skill.

## The words

A **home repo** is the repo the agent starts in; **local only** when its folder is not a git repo. A **child repo** is one it points at. A **component** is one thing the agent uses: a skill, hook, MCP server, rule, or pointer. A **kind** is its row in [components.md](references/components.md). A **source** is a place outside git: a wiki, issue tracker, pipeline, or chat. A **harness** is Claude Code, Cursor, Copilot, or Codex.

Every mode walks the registry in [components.md](references/components.md) and gives each item one bucket:

| Bucket | Meaning | Action |
| --- | --- | --- |
| `shared` | Useful in more than one repo | Move to the home repo |
| `duplicate` | Same item in several places | Keep one in the home repo, remove the copies |
| `repo-specific` | Only makes sense in its repo | Leave it |
| `installed` | From a plugin or marketplace | Leave it, record the registration |

Steering and pointers live in `AGENTS.md`, which all four harnesses read. Everything else goes where each harness in use looks, by [harnesses.md](references/harnesses.md). Where a harness has no place for a kind, say so. The layout is in [layout.md](references/layout.md). Create only folders with content.

## Invocation

| Typed after `/setup-home-repo` | Mode | Writes |
| --- | --- | --- |
| nothing | In a home repo: status from [help.md](references/help.md). Otherwise: Setup. | Setup only, after approval |
| `add <thing>`, `update <thing>` | One item, by [add.md](references/add.md) | After the diff is shown |
| `update` | Explore again, propose only what changed, by Update in [setup.md](references/setup.md) | After approval |
| `advise` | Audit, by [advise.md](references/advise.md) | Never |
| `cleanup` | Fix what advise found, by [cleanup.md](references/cleanup.md) | After approval |
| `help` | The card in [help.md](references/help.md) | Never |

The working directory is a home repo when its `AGENTS.md` has a `## Repos` section from this skill, or the person says so. Setup never runs twice on one home repo: `update` is the way back in. Any other first word: print the help card and stop.

## Setup

Follow [setup.md](references/setup.md): explore the repos, the components, then the sources and harnesses; ask what is left; show the plan and wait; apply; hand each picked child repo to `setup-agents-md`, which owns its steering file; report. Done when every plan row has an outcome. The last report line names `/setup-home-repo update`.

## When a home repo is the wrong answer

Say so before you build, and let the person choose.

- Everything could live in one monorepo, and nothing stops it.
- There is one repo.
- There are thousands of repos: a plugin marketplace fits better.
