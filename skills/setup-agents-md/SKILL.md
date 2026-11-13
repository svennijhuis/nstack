---
name: setup-agents-md
description: Use when the user wants to create, update, trim, or audit a repo's AGENTS.md (or an old CLAUDE.md), or set up its commands, code standards, decisions (ADRs), and glossary.
---

A steering file loads on every request. Every line costs tokens and attention, and a line that restates the code becomes a second source of truth that nothing keeps honest. This skill writes the smallest `AGENTS.md` that still makes the agent better, moves the rest to files the agent reads only when a task needs them, and gives decisions and terms a home in the repo they belong to.

## Rules that outrank the rest

**Keep only what the code cannot say.** If the agent can learn it by reading the code, the config, or the tests, it does not go in a doc. Make the code clearer instead: a better name, a type, a test, or a short comment that says why.

**Read only until the plan is approved.** Explore, then show the plan table and the drafted files. Write nothing before a yes. Advise never writes.

**Decisions live in the repo they change.** ADRs, the glossary, and topic docs go in that repo, never in the home repo. The home repo holds only decisions about itself. See [home-repo.md](references/home-repo.md).

**Never invent a line.** Every command and every rule comes from the disk, the person, or a doc that is already there. Run or look up each command before you write it.

**Never push.** Commit on a new local branch. The person pushes.

**Ask on a conflict.** When two instructions disagree, show both and ask which one stays. Never pick one yourself.

## The words

The **steering file** is `AGENTS.md`. Every harness in nstack reads it, Claude Code included. A **part** is one thing in the repo that builds, runs, or deploys on its own: an app, a solution, a service, the infrastructure, a pipeline. The **root file** is the steering file at the repo root. A **topic file** is a doc the root file points at and the agent reads only when the task touches its topic. An **ADR** is one decision record in `docs/adr/`. The **glossary** is `GLOSSARY.md`. **Derivable** means the code already says it.

## What goes where

| Content | Where | Why |
| --- | --- | --- |
| What the project is, in one sentence | Root file | Anchors every task |
| The main parts and what each does, three to six lines, top-level folders at most | Root file | A thin map so the agent knows where to start |
| Package manager, when it is not npm and corepack does not pin it | Root file | The agent guesses wrong otherwise |
| How to start, build, and test, always, plus lint and typecheck | Root file | The agent needs them first |
| Each part and its commands: solutions, apps, infrastructure. Each pipeline and what it does. | Root file, or the part's own `AGENTS.md` | One repo can hold several of each |
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

The person-facing version of this table, with examples, is in [README.md](README.md).

## Invocation

The person types `/setup-agents-md`. Read the first word after it.

| Typed | Mode | Writes |
| --- | --- | --- |
| nothing | Detect, then Create or Update | After approval |
| `<repo name>` | From a home repo: run on that child repo | After approval, on a branch in that repo |
| `advise` | Audit, see [advise.md](references/advise.md) | Never |
| `help` | The card, see [help.md](references/help.md) | Never |

### Detect

1. Find where you are. If the working directory is a home repo (its `AGENTS.md` has a `## Repos` section), follow [home-repo.md](references/home-repo.md). It decides which repo the rest of the steps run on.
2. If the target repo has no steering file, run Create. If it has one, run Update.

## Create and Update

Same steps. Create starts with an empty inventory.

1. **Inventory.** Read the steering files, `README*`, everything under `docs/`, `CONTEXT.md`, `GLOSSARY.md`, `DECISIONS.md`, `docs/adr/`, and any spec, PRD, plan, or memory file. Read the package manifest, the lockfile, the scripts, the linter config, and the CI config to learn the real commands. Never open `.env` or another secret file.
2. **Sort every section.** One row per section: file, section, kind, action. Kinds: `anchor`, `shape`, `command`, `rule`, `topic`, `procedure`, `decision`, `term`, `derivable`, `finished plan`, `lint rule`, `obvious`. Actions: keep, move, rewrite, delete, ask.
3. **Check what you keep.** Run or look up every command. Check every path still exists. A command that fails or a path that is gone is drift: fix it or delete it.
4. **Find conflicts.** Two lines that disagree, in one file or across files, become one `ask` row each.
5. **Pull out the why.** Before a spec, plan, or explanation is deleted, lift any decision or term in it into an ADR draft or a glossary line.
6. **Draft the files** from [templates.md](references/templates.md): the root file, the code standards file, the other topic files, the ADR drafts, and the glossary. Fold any `CLAUDE.md` into `AGENTS.md` by [the CLAUDE.md rule](#claudemd).
7. **Show the plan.** The table, the drafted files, the line count of the new root file, and the conflict questions, numbered, the recommended answer first. Wait for approval.
8. **Apply.** On a new local branch `agents-md/<yyyy-mm-dd>`. Move, write, delete. Never rewrite text the person wrote by hand without a row that says so. Commit.
9. **Report and stop.** One outcome per plan row, the root file's line count before and after, the drift found, and the branch to push. Offer the revert check in [revert-check.md](references/revert-check.md) if the repo has CI and none is installed.

In a monorepo, each package gets its own `AGENTS.md` with its purpose, its stack, and its own rules. The harness merges them with the root file, so neither repeats the other. The root says what the monorepo is, how packages are found, and the shared tooling.

Done when every plan row has an outcome, the root file and each part's `AGENTS.md` are under about 60 lines, and no kept line points at something that is gone.

## Commands, by default

The root file always says how to start, build, and test, even when the commands are the standard ones for the stack. These are the lines the agent needs first, and a wrong guess costs a failed run.

1. **Find every part.** Solutions and project files (`*.sln`, `*.slnx`, `*.csproj`), workspaces in the package manifest, `Makefile`, `docker-compose*`, `Dockerfile`, infrastructure (`*.tf`, `*.bicep`, Pulumi, Helm, Kubernetes manifests), and pipelines (`.github/workflows/`, `azure-pipelines*.yml`, `.gitlab-ci.yml`).
2. **Learn each part's commands** from its scripts, its manifest, and the pipeline that builds it. The pipeline is the best source: it is what really runs.
3. **Check them.** Run the start, build, and test commands that change nothing outside the repo. Never run a command that deploys, applies infrastructure, migrates a shared database, or publishes. Read those from the pipeline and write them down as they are.
4. **One part:** a `## Commands` section with Start, Build, Test, and Lint or Typecheck when they exist.
5. **Several parts:** a `## Parts` section, one short block per part: what it is, where its entry file is, and its commands. Past about four parts, or when a part needs its own rules, give it its own `AGENTS.md` in its folder and keep one line for it in the root. The harness loads a folder's `AGENTS.md` when the agent works there.
6. **Pipelines:** one line per pipeline: its file, what triggers it, and what it does. The agent learns what CI will check before it opens a pull request.
7. **Infrastructure:** say how to check a change without applying it, such as a plan or a what-if, and say that applying goes through the pipeline. Ask the person when the pipeline does not show it.

The template is in [templates.md](references/templates.md).

## Code standards, by default

Every repo gets `docs/agents/code-standards.md`, and the root file points at it in one line. It holds how code is written in this repo: conventions a reader cannot see from one file and no tool checks, such as how errors are returned, how modules are split, or which of two patterns to use.

1. **Fill it from what was found.** Code style rules from the old steering files, topic docs, and `CONTRIBUTING.md` move here.
2. **Send checkable rules to tools.** A rule a linter, formatter, or type checker can enforce becomes a plan row for that tool's config, not a line here.
3. **Ask when it is empty.** If nothing was found, ask one round: "Which conventions should every change follow?" Offer two or three candidates read from the code, marked as seen in the code, the recommended answer first. Write only what the person confirms.
4. **Skip it on a no.** If the person gives no conventions, leave the file out and say so in the report. An empty file is noise.
5. **Split past about 50 lines,** or when the repo has more than one language: one file per language under `docs/agents/`, such as `typescript.md` and `python.md`, each linked from the root file.

When the repo already has a standards file elsewhere, such as `docs/TYPESCRIPT.md` or `CONTRIBUTING.md`, point the root file at it and keep its name. Do not move a file other tools or people link to.

## CLAUDE.md

Claude Code reads `AGENTS.md` natively from version 2.1.277, but only when no `CLAUDE.md`, `.claude/CLAUDE.md`, or `CLAUDE.local.md` sits in the working folder or a folder above it. When one does, Claude reads that and ignores `AGENTS.md`.

So write only `AGENTS.md`.

- **A `CLAUDE.md` exists:** move each of its lines to `AGENTS.md` or a topic file as plan rows, then delete it. Do the same for `.claude/CLAUDE.md`.
- **A `CLAUDE.local.md` exists:** it is personal and untracked. Do not touch it. Tell the person it hides `AGENTS.md` from Claude, and that they can move its lines to their user `~/.claude/CLAUDE.md`, which does not.
- **A `CLAUDE.md` in a folder above the repo,** such as the home folder or the folder that holds the repos: report it. It hides every repo's `AGENTS.md` below it.
- **Old Claude Code, or a provider without native support:** when the person uses Claude Code before 2.1.277, or says it does not read `AGENTS.md` for them, keep a `CLAUDE.md` whose only line is `@AGENTS.md`. Ask before writing it.

## The decision rules

The root file always carries the decision rules from [templates.md](references/templates.md), so every agent that works in the repo records decisions and handles reverts. In short:

- A real decision gets an ADR in the same pull request as the code. A real decision is a new dependency, a change to the architecture, the data model, or a public contract, a trade-off, or a rejected alternative.
- An ADR body never changes. Only its status line does.
- A reversed decision gets a new ADR that supersedes the old one.
- A revert of code that came with an ADR gets a new ADR that says it was reverted and why, and the old ADR's status points at it. A git revert deletes the old ADR with the code, so restore it first.
- Before finishing, the agent asks: did this change contain a decision?

Text alone does not stop a person who reverts on the GitHub site. The CI check in [revert-check.md](references/revert-check.md) does.

## With the other nstack skills

**`setup-home-repo`.** This skill lives in the home repo's skills folder, so every repo can use it. Add it to the router's map with `/setup-home-repo add`. Setup step 7 trims each child repo's steering file to what is true only for that repo and adds the pointer line to the home repo. Run this skill on the child repo after that, with `/setup-agents-md <repo>`. It keeps the pointer line and never touches the home repo's `## Repos`, `## Sources`, `## Tools`, or `## Environment`.

**`tech-design`.** A design folder `docs/design/<yyyy-mm-dd>-<name>/` is a live doc while its status is `draft`, `discussion`, or `ready`, and while it is `committed` and the feature is not shipped. Leave it alone. When a committed design's feature has shipped, it is a finished plan: lift each line of its Decisions so far into an ADR, with the design folder and the pull request in `Change`, then offer to delete the folder as its own plan row. An `abandoned` design gets one ADR that says what was not built and why, then the same offer. Terms that `domain-modeling` wrote during the design stay in the glossary. When it wrote `CONTEXT.md` or `GLOSSARY.md`, keep that file and its name. Start `tech-design` in the repo the design is about. When it spans more than one repo, start it in the home repo. See [home-repo.md](references/home-repo.md). Either way, when it ships, each decision becomes an ADR in the repo it changes, never in the home repo.

While a design is open, the root file may carry one line: `Designs in progress: docs/design/. Read the one for your task.` Remove it when none is open.

## When this is the wrong answer

Say so before you build.

- The steering file is already short, true, and free of conflicts. Say so and stop.
- The person wants a style guide enforced. Point at the linter or a hook, not at `AGENTS.md`.
- The repo is a home repo and the person wants its pointers changed. That is `/setup-home-repo`.
