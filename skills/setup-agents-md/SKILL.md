---
name: setup-agents-md
description: Use when the user wants to create, update, trim, or audit a repo's AGENTS.md, or set up its commands, code standards, decisions (ADRs), and glossary.
---

A steering file loads on every request. Every line costs tokens and attention, and a line that restates the code becomes a second source of truth that nothing keeps honest. This skill writes the smallest `AGENTS.md` that still makes the agent better, moves the rest to files the agent reads only when a task needs them, and gives decisions and terms a home in the repo they belong to.

## Rules that outrank the rest

**Keep only what the code cannot say.** If the agent can learn it by reading the code, the config, or the tests, it does not go in a doc. Make the code clearer instead: a better name, a type, a test, or a short comment that says why. One exception: the commands and the pipelines, by [Commands](#commands-by-default). The agent needs them before it has read anything.

**Read only until the plan is approved.** Explore, then show the plan table and the drafted files. Before a yes, write nothing, run no project command, and clone nothing. Advise never does any of the three.

**Decisions live in the repo they change.** ADRs, the glossary, and topic docs go in that repo, never in the home repo. The home repo holds only decisions about itself. See [home-repo.md](references/home-repo.md).

**Never invent a line.** Every command and every rule comes from the disk, the person, or a doc that is already there. The only fixed text is the Docs and Decisions sections in [templates.md](references/templates.md).

**Never push.** Commit on a local branch, one per repo. The person pushes.

**Ask on a conflict.** When two instructions disagree, show both and ask which one stays. Never pick one yourself.

## The words

The **steering file** is `AGENTS.md`. Every harness in nstack reads it. A **part** is one thing in the repo that builds, runs, or deploys on its own: an app, a package, a solution, a service, the infrastructure. The **root file** is the steering file at the repo root. A **topic file** is a doc the root file points at and the agent reads only when the task touches its topic. An **ADR** is one decision record in `docs/adr/`. The **glossary** is `GLOSSARY.md`. **Derivable** means the code already says it.

## What goes where

| Content | Where | Why |
| --- | --- | --- |
| What the project is, in one sentence | Root file | Anchors every task |
| The main parts and what each does | Root file | A thin map so the agent knows where to start |
| The package manager or build tool, when the stack has more than one to choose from and the repo does not pin it | Root file | The agent guesses wrong otherwise |
| How to start, build, and test, plus lint and typecheck | Root file | The agent needs them first |
| Each part and its commands. Each pipeline and what it does. | Root file, or the part's own `AGENTS.md` | One repo can hold several of each |
| Rules for every task that no tool enforces | Root file | They apply everywhere |
| One line per topic file, ADRs, and glossary | Root file | Progressive disclosure |
| Code standards: how code is written here, beyond what the linter checks | `docs/agents/code-standards.md`, a default topic file | Loaded when the agent writes code, not on every request |
| Rules for one area: testing, API design, a framework | Topic file under `docs/agents/` | Loaded only when needed |
| A procedure with steps | A skill | Loaded only when triggered |
| Why something was chosen, and what was rejected | `docs/adr/` | The code shows what, never why |
| Terms with a meaning special to this project | `GLOSSARY.md` | The code uses the words, it does not define them |
| How the code works, folder trees, deep file paths | Nowhere. Delete it. | Goes stale, misleads the agent |
| Finished specs, PRDs, plans | Nowhere. Delete it. Git keeps it. | Describes a past intent, not the code |
| Style rules a linter or formatter can check | The linter config, or a hook | Tools are faster, cheaper, and always right |
| Advice the agent already follows: "write clean code" | Nowhere | Spends the budget for nothing |

[README.md](README.md) explains this table to people. You do not need to read it.

## Invocation

The person types `/setup-agents-md`. Read the first word after it.

| Typed | Mode | Writes |
| --- | --- | --- |
| nothing | Detect, then Create or Update | After approval |
| `<repo name>` | From a home repo: run on that child repo | After approval, on a branch in that repo |
| `all` | From a home repo: run on every child repo, one plan and one yes each | After each approval, on a branch in each repo |
| `advise`, `advise <repo name>`, `advise all` | Audit, see [advise.md](references/advise.md) | Never |
| `help` | The card, see [help.md](references/help.md) | Never |

### Detect

1. Find where you are. The working directory is a home repo when its `AGENTS.md` has a `## Repos` section written by `setup-home-repo`, or the person says it is. If it is one, follow [home-repo.md](references/home-repo.md). It decides which repo the rest of the steps run on.
2. If the target repo has no `AGENTS.md` and no `CLAUDE.md`, run Create. If it has either, run Update.

## Create and Update

Same steps. In Create there is no steering file to sort, only the docs around it.

1. **Inventory.** Read `AGENTS.md`, any `CLAUDE.md`, `README*`, everything under `docs/`, `CONTEXT.md`, `GLOSSARY.md`, `DECISIONS.md`, `docs/adr/`, and any spec, PRD, plan, or memory file. Read the package manifest, the lockfile, the scripts, the linter config, and the CI config to learn the real commands. Never open `.env` or another secret file.
2. **Sort every section.** One row per section: file, section, kind, action. Kinds: `anchor`, `shape`, `command`, `rule`, `topic`, `procedure`, `decision`, `term`, `derivable`, `finished plan`, `lint rule`, `obvious`. Actions: keep, move, rewrite, delete, ask.
3. **Check what you keep.** Look up every command in the scripts, the manifest, or the pipeline. Check every path still exists. A command nothing defines or a path that is gone is drift: fix it or delete it. In Update, find the parts and the pipelines again by [Commands](#commands-by-default) step 1 and compare them with the root file. A part or pipeline with no line, and a line for one that is gone, are drift too.
4. **Find conflicts.** Two lines that disagree, in one file or across files, become one `ask` row each.
5. **Pull out the why.** Before a spec, plan, or explanation is deleted, lift any decision or term in it into an ADR draft or a glossary line.
6. **Draft the files** from [templates.md](references/templates.md): the root file, the code standards file, the other topic files, the ADR drafts, and the glossary.
7. **Show the plan.** The table, the drafted files, the line count of the new root file, the commands step 8 will run, and the conflict questions, numbered, the recommended answer first. Wait for approval.
8. **Apply.** If the repo has uncommitted changes, stop and report it. Work on a new local branch `agents-md/<yyyy-mm-dd>`, with `-2` added when that name is taken. When the repo's current branch starts with `home-repo/` and is not pushed, `setup-home-repo` just made it: commit there instead, so the repo has one branch to review. Run the build and test commands by [Commands](#commands-by-default) step 3. One that fails is not written: report it with its error. Move, write, delete. Never rewrite text the person wrote by hand without a row that says so. Commit.
9. **Report and stop.** One outcome per plan row, the root file's line count before and after, the drift found, and the branch to push.

Done when every plan row has an outcome, the root file and each part's `AGENTS.md` are under about 60 lines, and no kept line points at something that is gone. In a home repo's own `AGENTS.md`, count only the lines above `## Repos`.

## CLAUDE.md

`AGENTS.md` is the default and holds all the text. Claude Code reads it itself from version 2.1.277, but only when no `CLAUDE.md`, `.claude/CLAUDE.md`, or `CLAUDE.local.md` sits in the working folder or a folder above it. One that does hides `AGENTS.md` from Claude Code, unless a `CLAUDE.md` in the repo imports it.

So a `CLAUDE.md` is allowed in one shape: its only line is `@AGENTS.md`.

- **Do not write one by default.** Offer the one-line file only when the person asks for a `CLAUDE.md`, uses Claude Code older than 2.1.277, or has one of the hiding files below. Write it on a yes.
- **A one-line `CLAUDE.md` exists.** Leave it.
- **`CLAUDE.md` or `.claude/CLAUDE.md` with text of its own.** Sort its lines like any other section and move the kept ones into `AGENTS.md` or a topic file. Then ask: delete the file, which is the recommended answer, or keep it as the one line. Each is a plan row.
- **`CLAUDE.local.md` in the repo.** It is personal and untracked. Do not touch it. Tell the person it hides `AGENTS.md` from Claude Code for them, and offer the one-line file.
- **`CLAUDE.md` in a folder above the repo.** Report it and change nothing outside the repo. Offer the one-line file.

## Commands, by default

The root file always says how to start, build, and test, even when the commands are the standard ones for the stack. A wrong guess costs a failed run.

1. **Find every part.** Solution and project files, workspaces in a package manifest, build scripts, container files, infrastructure as code, and pipeline definitions. Look for whatever the stack uses.
2. **Learn each part's commands** from its scripts, its manifest, and the pipeline that builds it. The pipeline is the best source: it is what really runs.
3. **Check them, after approval.** Run the build and test commands. Never run a start command: it may not exit. Never run a command that deploys, applies infrastructure, migrates a shared database, or publishes. Write those down as the scripts or the pipeline have them.
4. **One part:** a `## Commands` section with Start, Build, Test, and Lint or Typecheck when they exist.
5. **Several parts:** a `## Parts` section, one short block per part: what it is, where its entry file is, and its commands. Past about four parts, or when a part needs its own rules, the part gets its own `AGENTS.md` in its folder with what it is, its stack, its commands, and its rules. The root keeps one line for it, and neither file repeats the other. The harness loads a folder's `AGENTS.md` when the agent works there.
6. **Pipelines:** one line per pipeline: its file, what triggers it, and what it does. The agent learns what CI will check before it opens a pull request.
7. **Infrastructure:** say how to check a change without applying it, such as a plan or a what-if, and say that applying goes through the pipeline. Ask the person when the pipeline does not show it.

## Code standards, by default

Every plan proposes `docs/agents/code-standards.md`, with one line in the root file that points at it. It holds how code is written in this repo: conventions a reader cannot see from one file and no tool checks, such as how errors are returned, how modules are split, or which of two patterns to use.

1. **Fill it from what was found.** Code style rules from the old steering files, topic docs, and `CONTRIBUTING.md` move here.
2. **Send checkable rules to tools.** A rule a linter, formatter, or type checker can enforce becomes a plan row for that tool's config, not a line here.
3. **Ask when it is empty.** If nothing was found, ask one round: "Which conventions should every change follow?" Offer two or three candidates read from the code, marked as seen in the code, the recommended answer first. Write only what the person confirms.
4. **Skip it on a no.** If the person gives no conventions, leave out the file and the line that points at it, and say so in the report. An empty file is noise.
5. **Split past about 50 lines,** or when the repo has more than one language: one file per language under `docs/agents/`, named after the language, each linked from the root file.

When the repo already has a standards file elsewhere, such as a language file under `docs/` or `CONTRIBUTING.md`, point the root file at it and keep its name. Do not move a file other tools or people link to.

## The decision rules

The root file always carries the Decisions section from [templates.md](references/templates.md), so every agent that works in the repo records its decisions and handles reverts. Change only its paths.

## With the other nstack skills

Each one is optional. This skill works alone in any repo.

**`setup-home-repo`.** It owns the home repo and the one line in each child repo that points home. This skill owns everything else a child repo's steering file says. `setup-home-repo` calls `/setup-agents-md <repo>` after its setup and after `add <repo>`. What this skill may change in a home repo is in [home-repo.md](references/home-repo.md).

**`tech-design`.** A design folder `docs/design/<yyyy-mm-dd>-<name>/` is a live doc while its status is `draft`, `discussion`, or `ready`, and while it is `committed` and the feature has not shipped. Leave it alone. `tech-design` has no status for shipped, so ask the person, one question per `committed` design. Never infer it.

- **Shipped.** The design is a finished plan. Lift each line of its Decisions so far into an ADR, with the design folder and the pull request in `Change`. Lift each term in its `glossary.md` that has a project meaning into the repo's glossary. Then offer to delete the folder, as its own plan row.
- **`abandoned`.** One ADR that says what was not built and why, then the same offer.
- **Terms.** When `domain-modeling` wrote `CONTEXT.md` or `GLOSSARY.md` during the design, keep that file and its name.
- **Where.** Which repo a design starts in, and where its ADRs go, is in [home-repo.md](references/home-repo.md).

While a design is open, the root file may carry one line: `Designs in progress: docs/design/. Read the one for your task.` Remove it when none is open.

## When this is the wrong answer

Say so before you build.

- The steering file is already short, true, and free of conflicts. Say so and stop.
- The person wants a style guide enforced. Point at the linter or a hook, not at `AGENTS.md`.
- The repo is a home repo and the person wants its pointers changed. That is `/setup-home-repo`.
