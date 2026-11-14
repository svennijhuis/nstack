# Templates

Fill these in. Leave out a section that has no lines, and a line whose file does not exist after this run. Never fill a line with a guess.

## Root `AGENTS.md`

Aim for under 60 lines. Each line must apply to every task in the repo.

```markdown
# <project name>

<One sentence: what this project is and who it is for.>

## Shape

- <Main part, by name>: <what it does>. In `<top-level folder>`.
- <Main part>: <what it does>.

## Commands

- Package manager: <the one this repo uses>
- Install: `<command>`
- Start: `<command>`
- Build: `<command>`
- Test: `<command>`. Run it before you finish a change.
- Lint and typecheck: `<command>`

## Pipelines

- `<pipeline file>`: on <trigger>, <what it checks or deploys>.

## Rules

- <A rule for every task that no tool enforces.>

## Read when relevant

- Code standards: `docs/agents/code-standards.md`. Read before you write or change code.
- <Topic>: `docs/agents/<topic>.md`. Read when <situation>.
- Terms: `GLOSSARY.md`. Read when a word in the task has a project meaning.
- Decisions: `docs/adr/`. Read before you change something an ADR covers.

## Docs

- Do not write docs that restate the code. Improve a name, a type, or a test, or add a short comment that says why.
- When a change makes a doc wrong, fix or delete it in the same change.
- Delete a spec or plan once its feature ships. Keep its decisions as ADRs.

## Decisions

- When a change makes a real decision, add an ADR in `docs/adr/` in the same change. A real decision is a new dependency, a change to the architecture, the data model, or a public contract, a trade-off, or a rejected alternative. Use the format of the newest ADR there.
- Leave an ADR's body as it was merged. To reverse a decision, add a new ADR that supersedes it and change only the old one's status line.
- When you revert or undo a change, look in `docs/adr/` for an ADR from that change. If there is one, add an ADR that records the revert and why. A git revert deletes the old ADR too: restore it, and set its status to `Reverted by <new ADR>`.
- Before you finish, ask: did this change contain a decision? If yes, and no ADR was written, write it.
```

For a repo with several parts, replace Shape and Commands with Parts. Keep Pipelines.

```markdown
## Parts

### <Part name> (<stack>)

<What it is, in one line.> Entry: `<solution or project file>`.

- Start: `<command>`
- Build: `<command>`
- Test: `<command>`

### Infrastructure (<tool>)

<What it provisions.> In `<folder>`.

- Check a change: `<plan or what-if command>`
- Apply: runs through the `<pipeline>` pipeline, not from a local machine.
```

When a part has its own `AGENTS.md`, the root keeps one line for it: `- <Part>: <what it is>. See <folder>/AGENTS.md.`

Leave out a command the part does not have.

Shape is the thin navigation layer: three to six lines. Name a top-level folder at most. No deeper paths and no folder trees, because those move. The agent finds the rest itself.

Write the rules in plain, calm sentences. No ALL CAPS, no "IMPORTANT", no "always" or "never" where a plain sentence works. Keep the Docs and Decisions sections as they are, except for the paths.

## Code standards

`docs/agents/code-standards.md`. Each line is a convention the person confirmed or that came from an existing doc. No rule a linter or the type checker already enforces.

```markdown
# Code standards

Read this before you write or change code. The linter and the type checker cover formatting and types. These are the conventions they do not check.

## <Area, such as Errors>

- <Convention, in one plain sentence.> <Why, when it is not obvious.>
- Follow the pattern in <module or feature, by name>.

## <Area, such as Modules>

- <Convention.>
```

Areas that often hold a real convention: errors, modules and boundaries, naming, data access, async work, logging, comments, dependencies. Leave out an area with no confirmed line.

## Topic file

`docs/agents/<topic>.md`, or the docs folder the repo already uses. One topic per file. A topic file may point at a deeper file.

```markdown
# <Topic>

Read this when <situation>.

- <Rule.>
- <Rule.> Follow the pattern in <the module or feature, by name>.
```

Describe the pattern and name the part of the code that shows it. Do not paste code or list file paths. Both go stale, and the agent finds the files itself.

## ADR

One file per decision: `docs/adr/<yyyy-mm-dd>-<short-slug>.md`. One file each, so two agents working at once do not conflict on a shared file. When the repo already numbers its ADRs, or keeps one `DECISIONS.md`, follow what is there.

```markdown
# <Decision as a short statement>

Status: Accepted
Date: <yyyy-mm-dd>
Change: <pull request or commit that made it. "this pull request" until it has a number>

## Decision

<What was decided, in one to three sentences.>

## Why

<The reason. The constraint, the cost, the evidence.>

## Rejected

- <Alternative>: <why not>.
```

Status words: `Accepted`, `Superseded by <file>`, `Reverted by <file>`. After the ADR is merged only the status line changes. The `Change` line is filled in once, when the pull request has its number.

A revert ADR:

```markdown
# Revert: <old decision>

Status: Accepted
Date: <yyyy-mm-dd>
Change: <revert pull request or commit>
Reverts: <old ADR file>

## Why

<What went wrong, or what changed.>
```

## `GLOSSARY.md`

At the repo root. Only terms whose meaning is special to this project.

```markdown
# Glossary

- **<Term>**: <what it means here>. Not <the meaning people might assume>.
```

When the repo has a `CONTEXT.md` that holds the terms, keep that name. Do not rename a file other tools or skills read.
