# setup-home-repo

One place for everything your agent needs in every session: skills, pointers to your repos and sources, MCP servers, and hooks, with a router skill on top. You start every session there and reach the other repos from it. Say "set up a home repo" or type `/setup-home-repo`.

This file is for people. The agent reads [SKILL.md](SKILL.md).

## What it does

1. Reads your repos, your agent config, and your tools. It asks only what it could not find.
2. Shows a plan: every item, where it is now, and where it goes.
3. Waits for your yes. Then it builds the home repo and writes the router.
4. In each child repo it removes what moved and adds one line that points home, on a new local branch. It never pushes.

## Local only or git

Setup asks once which one you want. It skips the question when the folder already is a git repo.

| | Local only | Git |
| --- | --- | --- |
| For | One person | A team |
| Git, commits, `.gitignore` | No | Yes |
| The undo | A dated copy in `.backup/` | A commit |
| Sharing | You share files yourself, or not at all | Through the repo |

Everything else works the same. To switch later, type `/setup-home-repo add git`.

## One branch per repo

The home repo never changes a child repo's main branch. Each child repo gets one local branch, `home-repo/move-agent-config`. You review it and push it through your normal review.

## With setup-agents-md

Each skill works without the other.

- `setup-home-repo` owns the home repo and the one line in each child repo that points home.
- `setup-agents-md` owns the rest of each child repo's `AGENTS.md`, its ADRs, and its glossary.
- After setup and after `add <repo>`, this skill asks which child repos get `setup-agents-md` and calls it for those. Each repo shows its own plan and waits for its own yes. Both skills commit on the same branch.
- Without `setup-agents-md`, the child repos' steering files stay as they are, and the report names them.
- `AGENTS.md` is the default. Every harness reads it, Claude Code from version 2.1.277. A `CLAUDE.md` is written only when you ask for one or use an older Claude Code, and then it is one line: `@AGENTS.md`.

## Designs

A design from `tech-design` lives where you start it. Started in the home repo, it asks: here, or in one of the repos. A design that spans repos fits best in the home repo. When it ships, its decisions become ADRs in the repos they change.

## Commands

```text
/setup-home-repo                 no home repo here: build one. home repo here: show its status
/setup-home-repo add <thing>     add or update one item: a repo, a source, a skill, an MCP server,
                                 a hook, a rule, a setting, an agent, a command, a tool, a wiki page
/setup-home-repo add git         turn a local-only home repo into a git repo
/setup-home-repo advise          audit and say what to fix. changes nothing
/setup-home-repo cleanup         fix what advise found, the rows you pick
/setup-home-repo help            this card
```

Nothing is written before you approve the plan. Nothing is pushed.

## When not to use it

- You have one repo. A home repo adds nothing.
- Everything could live in one monorepo. That is simpler.
- You have thousands of repos. A plugin marketplace fits better.
