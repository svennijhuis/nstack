---
name: setup-agents-md
description: Use when the user wants to create, update, trim, or audit a repo's AGENTS.md, or set up its commands, code standards, decisions (ADRs), and glossary.
---

Write the smallest `AGENTS.md` that makes the agent better. Move the rest to files the agent reads only when a task needs them, and give decisions and terms a home in the repo they belong to.

## Rules that outrank the rest

- **Keep only what the code cannot say.** What the code, config, or tests show goes in no doc: make the code clearer instead. The exception is the commands and pipelines, by [Commands](#commands).
- **Read only until the plan is approved.** Before a yes, write nothing, run no project command, and clone nothing. Advise never does any of these.
- **Decisions live in the repo they change.** ADRs, the glossary, and topic docs never go in the home repo, unless they are about the home repo itself. See [home-repo.md](references/home-repo.md).
- **Never invent a line.** A command comes from a script, the manifest, or the pipeline, or else from the person. A rule comes from the person or an existing doc. The only fixed text is the Docs, Changes, and Decisions sections in [templates.md](references/templates.md).
- **Never push.** Commit on a local branch, one per repo.
- **Ask on a conflict.** Two instructions that disagree: show both and ask which stays.
- **Never open `.env` or another secret file.**

## The words

The **root file** is `AGENTS.md` at the repo root. A **part** builds, runs, or deploys on its own: an app, a package, a solution, a service, the infrastructure. Projects one build command builds together are one part. A folder with its own `.git` is another repo, never a part. A test-only project gets its commands in the root file, under the part it tests or as its own block when it tests several. A service only tests need is no part: name it on that test line. A **topic file** is a doc the root file points at, read only when the task touches its topic. An **ADR** is one decision record in `docs/adr/`. The **glossary** is `GLOSSARY.md`.

## What goes where

| Content | Where |
| --- | --- |
| What the project is, in one sentence | Root file |
| The main parts and what each does | Root file |
| The package manager, only when the stack has several and no lockfile or manifest field pins it | Root file |
| Install, start, build, test, lint, typecheck, per part. Each pipeline and what it does. | Root file |
| Rules for every task that no tool enforces | Root file |
| One line per topic file, ADRs, and glossary | Root file |
| How code is written here, beyond the linter | `docs/agents/code-standards.md` |
| Rules for one area: testing, API design, a framework | `docs/agents/<topic>.md` |
| A procedure with steps | A skill. Until there is one, a topic file. Never deleted. |
| Why something was chosen, and what was rejected | `docs/adr/` |
| Terms with a project meaning | `GLOSSARY.md` |
| How the code works, folder trees, deep paths | Delete |
| Finished specs, PRDs, plans | Delete, after the why is lifted out |
| Style rules a linter or formatter can check | The tool's config, or a hook |
| Advice the agent already follows | Delete |

## Invocation

| Typed after `/setup-agents-md` | Mode | Writes |
| --- | --- | --- |
| nothing | Detect, then Create or Update | After approval |
| `<repo name>` | From a home repo: that child repo | After approval, on a branch there |
| `all` | From a home repo: every child repo, one plan and one yes each | After each approval |
| `advise`, `advise <repo>`, `advise all` | Audit by [advise.md](references/advise.md) | Never |
| `help` | The card in [help.md](references/help.md) | Never |

**Detect.** The working directory is a home repo when its `AGENTS.md` has a `## Repos` section from `setup-home-repo`, or the person says so. Then follow [home-repo.md](references/home-repo.md) to pick the target repo. A target with no `AGENTS.md` and no `CLAUDE.md` gets Create. Otherwise Update. Create has no steering file to sort, only the docs around it.

## Create and Update

1. **Inventory.** Read `AGENTS.md`, any `CLAUDE.md`, `README*`, `docs/`, `CONTEXT.md`, `GLOSSARY.md`, `DECISIONS.md`, `docs/adr/`, and any spec, plan, or memory file. Read the manifest, lockfile, scripts, linter config, and CI config for the real commands.
2. **Sort.** One row per section: file, section, kind (`anchor`, `shape`, `command`, `rule`, `topic`, `procedure`, `decision`, `term`, `derivable`, `finished plan`, `lint rule`, `obvious`), action (keep, move, rewrite, delete, ask).
3. **Check what you keep.** A command nothing defines and not marked `Not in the code.`, or a path that is gone, is drift: fix or delete it. In Update, find the parts and pipelines again by [Commands](#commands) step 1. A part or pipeline with no line, or a line for one that is gone, is drift.
4. **Conflicts.** Each pair of lines that disagree is one `ask` row.
5. **Pull out the why.** Before a spec, plan, or explanation is deleted, lift its decisions and terms into ADR drafts and glossary lines.
6. **Draft** from [templates.md](references/templates.md): the root file, code standards, topic files, ADRs, glossary.
7. **Show the plan.** The table, the drafted files, the new root file's line count, the commands step 8 will run, and every open question numbered, the recommended answer first. Wait for a yes.
8. **Apply.**
   - Uncommitted changes to tracked files outside `docs/design/`: stop and report. An open design under `docs/design/` is `tech-design`'s: leave it uncommitted.
   - No git: say in the plan that there is no undo, write after the yes, keep no copy.
   - Otherwise work on a new branch `agents-md/<yyyy-mm-dd>`, adding `-2`, `-3` when taken. When the current branch starts with `home-repo/` and is not pushed, commit there instead.
   - Run the commands by [Commands](#commands) step 3. Move, write, delete. Rewrite hand-written text only where a row says so.
   - Commit only the files the plan names. Report and leave uncommitted anything a build changed.
9. **Report and stop.** One outcome per row, the root file's line count before and after, the drift found, the branch to push.

Done when every row has an outcome, the root file is under about 60 lines not counting Parts (in a home repo, the lines above `## Repos`), and no kept line points at something gone.

## CLAUDE.md

`AGENTS.md` holds all the text. Claude Code reads it from version 2.1.277, unless a `CLAUDE.md`, `.claude/CLAUDE.md`, or `CLAUDE.local.md` in the working folder or above hides it. The only allowed `CLAUDE.md` sits at the root beside `AGENTS.md`, and its one line is `@AGENTS.md`. In `.claude/` that import resolves to nothing.

- **Write none by default.** Offer the one-line file, recommended yes, when the person asks, a hiding file is there, or the version check fails.
- **Version check.** When Claude Code is in use, run `claude --version` in the inventory. Ask about the one-line file on a version below 2.1.277 or no answer; on 2.1.277 to 2.1.280 with Bedrock or telemetry off; on any version with project instructions set to `CLAUDE.md` only.
- **A one-line `CLAUDE.md`,** also with a `## Agent skills` block from `setup-matt-pocock-skills`: leave it.
- **`CLAUDE.md` or `.claude/CLAUDE.md` with its own text:** sort its lines into `AGENTS.md` or a topic file, then ask: delete it (recommended) or keep a one-line root `CLAUDE.md`. `.claude/CLAUDE.md` is deleted either way, also when its only line is `@AGENTS.md`.
- **`CLAUDE.local.md`:** do not touch it. Say it hides `AGENTS.md` for that person, and offer the one-line file.
- **`CLAUDE.md` above the repo:** report it, change nothing outside the repo, offer the one-line file.

## Commands

Every root file but a home repo's says how to install, start, build, and test, even when the commands are standard. A start, build, or test command nothing defines is asked once per part, the stack's standard command recommended. On a yes, write it ending with `Not in the code.` On a no, leave it out.

1. **Find every part** from solution and project files, workspaces, build scripts, container files, infrastructure as code, and pipelines.
2. **Learn its commands** from its scripts, manifest, and pipeline, never from a doc. The pipeline is what really runs.
3. **Check them after approval.** Install first when defined, then build, test, lint. A defined command that fails here is still written, with the first line of its error in the report. Only an undefined, unconfirmed command is left out. When install cannot run, skip the check and say so. Never run a start, deploy, infrastructure apply, shared-database migration, or publish command: write those as the scripts or pipeline have them.
4. **One part:** `## Commands` with Start, Build, Test, and Lint or Typecheck. With linting rules, the lint line names the config, how to run it, and how to fix with it. With none, no lint line. Several of one kind get one line each, named for what it runs and what must run first.
5. **Several parts:** `## Parts`, one block per part: what it is, its entry file, its commands. All in the root file. Write no `AGENTS.md` in a part's folder. One already there is sorted and its kept lines move up, as plan rows.
6. **Pipelines:** one line each: file, trigger, what it does.
7. **Infrastructure:** how to check a change without applying it, and that applying goes through the pipeline. Ask when the pipeline does not show it.

## Code standards

Every plan proposes `docs/agents/code-standards.md` and one root line pointing at it: conventions no tool checks and one file does not show, such as how errors return or which of two patterns to use.

1. Move code-style rules from old steering files, topic docs, and `CONTRIBUTING.md` here.
2. A rule a linter, formatter, or type checker can enforce becomes a plan row for that tool's config.
3. Nothing found: ask one round, "Which conventions should every change follow?", with two or three candidates seen in the code, recommended first. Write only what the person confirms.
4. No conventions: no file, no pointer line, and say so in the report.
5. Past about 50 lines, or with more than one language: one file per language under `docs/agents/`.

An existing standards file elsewhere keeps its name and place: point at it.

## Decisions and Changes

Every root file but a home repo's carries the Changes and Decisions sections from [templates.md](references/templates.md). Change only the paths in Decisions and nothing in Changes. A `docs/adr/` that does not exist yet is not drift: the first ADR creates it.

## With the other skills

Each is optional. This skill works alone.

- **`setup-home-repo`** owns the home repo and the `Home repo:` line in each child repo. It calls `/setup-agents-md <repo>` after setup and `add`. What this skill may change in a home repo: [home-repo.md](references/home-repo.md).
- **`setup-matt-pocock-skills`** owns the `## Agent skills` block (in `AGENTS.md` or `CLAUDE.md`), `docs/agents/issue-tracker.md`, `domain.md`, and `triage-labels.md`. Never trim, move, delete, or report them. Its glossary layout counts as the glossary: `GLOSSARY.md`, or `GLOSSARY-MAP.md` with one `GLOSSARY.md` per context. Follow its renames.
- **`tech-design`.** A design in `docs/design/<yyyy-mm-dd>-<name>/` is live while `draft`, `discussion`, `ready`, or `committed` and not shipped. Leave it alone. Ask the person once per `committed` design whether it shipped. Never infer it.
  - **Shipped:** lift each real decision in its Decisions so far into an ADR, `Change` naming the folder and the pull request. List the lines not lifted. Lift its project terms into the glossary. Then offer to delete the folder as its own row, saying when it holds uncommitted files git does not keep.
  - **`abandoned`:** one ADR on what was not built and why, then the same offer.
  - A `CONTEXT.md` or `GLOSSARY.md` that `domain-modeling` wrote keeps its name.
  - While a design is open the root file may say `Designs in progress: docs/design/. Read the one for your task.` Remove it when none is open.

## When this is the wrong answer

Say so before you build.

- The steering file is already short, true, and free of conflicts: say so and stop.
- The person wants style enforced: point at the linter or a hook.
- They want a home repo's pointers changed: that is `/setup-home-repo`.
