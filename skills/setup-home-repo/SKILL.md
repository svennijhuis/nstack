---
name: setup-home-repo
description: Use when the user wants to create, update, audit, or clean up a home repo that holds shared skills, steering files, MCP servers, and hooks for many repos.
---

A team with many repos copies its skills, steering files, MCP servers, and hooks into each one, or hides them in the user folder where they go stale. A home repo ends that. It is one repo that holds everything the agent needs in every session, plus a pointer to every other repo and source. The agent always starts in the home repo and reaches out from there.

This skill builds that repo from what the person already has, keeps it current, audits it, and cleans it up. One command does all of it: `/setup-home-repo`. It never writes a second skill to do part of its job.

## Rules that outrank the rest

**Explore before you ask.** Read the disk, the git remotes, and the config first. Ask only what exploring did not answer. Every question carries a recommended answer.

**Read only until the plan is approved.** Setup and cleanup write nothing before the person approves the plan table. Advise never writes.

**Secrets stay out.** Never read `.env` or any other secret file. Never write a token, key, or password into a file in the home repo or a tracked file. Config names an environment variable instead.

**Never push.** Commit in the home repo, unless it is local only. In any other repo, edit only on a new local branch, one per repo. The person pushes.

**Work from what was found.** Never invent a component the person does not have. Never drop one because it fits no kind. It goes in the `other` row and you ask.

**Move a skill whole.** Copy the folder as it is. Never edit the body of a skill you move.

**Write no skill of your own.** The home repo holds only skills the person already has. Never generate a router, an updater, or any other helper skill. Adding and updating go through this skill.

## The words

A **home repo** is the repo the agent starts in. It is **local only** when its folder is not a git repo: one person uses it, and nothing is committed there. See [layout.md](references/layout.md). A **child repo** is any other repo it points at. A **component** is one thing the agent uses: a skill, a hook, an MCP server, a rule, a pointer. A **kind** is its row in the registry. A **source** is a place outside git the agent reads or writes: a wiki, an issue tracker, a pipeline, a chat. A **harness** is the agent client: Claude Code, Cursor, Copilot, or Codex.

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
| `add <thing>`, `update <thing>` | Add or update one item, see [add.md](references/add.md). The two words do the same. | After the diff is shown |
| `update` | Read everything again and propose only what changed, see Update in [setup.md](references/setup.md) | After approval |
| `advise` | Audit, see [advise.md](references/advise.md) | Never |
| `cleanup` | Fix what advise found, see [cleanup.md](references/cleanup.md) | After approval |
| `help` | The card, see [help.md](references/help.md) | Never |

### Detect

The working directory is a home repo when its `AGENTS.md` has a `## Repos` section written by this skill, or the person says it is. If it is one, print the status from [help.md](references/help.md) and stop. If it is not, run Setup.

Setup never runs twice on one home repo. `update` is the way back in: it explores again and proposes only the rows that changed.

Any other first word is not a mode. Print the help card and stop.

### Setup

Follow [setup.md](references/setup.md) step by step.

1. **Explore the repos.** Find the git repos, their remotes, and how recently each changed.
2. **Explore the components.** Walk the registry over the chosen repos and the user folder. Give each item a bucket.
3. **Explore the sources and the harnesses.** Read remotes, MCP config, and the command line tools on the path.
4. **Ask what is left**, in numbered rounds, the recommended answer first.
5. **Show the plan.** One table of every item with where it is and where it goes, and the drafted `AGENTS.md`. Wait for approval.
6. **Apply.** Create the home repo, move the shared items, merge the config per harness, commit in the home repo, and on a new local branch in each child repo remove the moved copies and add the line that points home.
7. **Hand over the child repos.** Call `setup-agents-md` for each repo the person picked. It owns what a child repo's steering file says.
8. **Report and stop.** One outcome per plan row, the branches created, what was skipped and why. The last line names `/setup-home-repo update` as the way to keep it current.

Setup is done when every plan row has an outcome.

### After setup

`add`, `update`, `advise`, and `cleanup` keep the home repo true. `add` changes one item the person names. `update` finds what changed on its own.

## When a home repo is the wrong answer

Say so before you build, and let the person choose.

- Everything could live in one monorepo, and nothing stops it. A monorepo is simpler.
- There is one repo. A home repo adds nothing.
- There are thousands of repos. A plugin marketplace fits better than pointers.
