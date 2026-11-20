# Templates

Leave out a section with no lines, and a line whose file will not exist. Never fill a line with a guess.

## Root `AGENTS.md`

Under about 60 lines, each true for every task.

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
- Lint and typecheck: `<command>`. When the repo has linting rules, add: rules in `<config file>`, fix with `<fix command>`. No linting rules: no mention of linting.

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

## Changes

- Leave the code you touch no worse. Follow the shape it already has. Do not add a second way to do something the code already does.
- When the change needs a refactor to fit, do it first, with the same behaviour. When you commit, the refactor is its own commit before the change.
- Build for the use the code has today. No layer, seam, or option that nothing uses yet.

## Decisions

- When a change makes a real decision, add an ADR in `docs/adr/` in the same change. A real decision is a new dependency, a change to the architecture, the data model, or a public contract, a trade-off, or a rejected alternative. Use the format of the newest ADR there.
- Before you add an ADR, look at the ADRs this branch added compared to the default branch. They are not merged yet. If one is about the same decision, update it. Add a new file only for a different decision.
- Leave an ADR's body as it was merged. To reverse a decision, add a new ADR that supersedes it and change only the old one's status line.
- When you revert or undo a change, look in `docs/adr/` for an ADR from that change. If there is one, add an ADR that records the revert and why. A git revert deletes the old ADR too: restore it, and set its status to `Reverted by <new ADR>`.
- Before you finish, ask: did this change contain a decision? If yes, and no ADR was written, write it.
```

For a repo with several parts, replace Shape and Commands with Parts. Keep Pipelines.

```markdown
## Parts

### <Part name> (<stack>)

<What it is, in one line.> Entry: `<solution or project file>`.

- Install: `<command>`
- Start: `<command>`
- Build: `<command>`
- Test: `<command>`
- Integration test: `<command>`. Needs <what must run first>.
- Lint: `<command>`. Rules in `<config file>`. Fix: `<fix command>`.

### Infrastructure (<tool>)

<What it provisions.> In `<folder>`.

- Check a change: `<plan or what-if command>`
- Apply: runs through the `<pipeline>` pipeline, not from a local machine.
```

Leave out a command the part does not have, and the Package manager line unless the stack has several and nothing pins one. Shape is three to six lines, naming a top-level folder at most. Write rules as plain, calm sentences: no ALL CAPS, no "IMPORTANT". Keep Docs, Changes, and Decisions as they are, except the paths.

## Code standards

Each line was confirmed by the person or came from an existing doc. No rule a tool enforces.

```markdown
# Code standards

Read this before you write or change code. The linter and the type checker cover formatting and types. These are the conventions they do not check.

## <Area, such as Errors>

- <Convention, in one plain sentence.> <Why, when it is not obvious.>
- Follow the pattern in <module or feature, by name>.

## <Area, such as Modules>

- <Convention.>
```

Likely areas: errors, modules and boundaries, naming, data access, async work, logging, comments, dependencies. Leave out an area with no confirmed line.

## Topic file

`docs/agents/<topic>.md`, or the repo's own docs folder. One topic per file.

```markdown
# <Topic>

Read this when <situation>.

- <Rule.>
- <Rule.> Follow the pattern in <the module or feature, by name>.
```

Name the part of the code that shows the pattern. Paste no code and list no file paths.

## ADR

One file per decision: `docs/adr/<yyyy-mm-dd>-<short-slug>.md`. A repo that numbers its ADRs or keeps one `DECISIONS.md` keeps its way.

```markdown
# <Decision as a short statement>

Status: Accepted
Date: <yyyy-mm-dd>
Change: <the work item, such as a PBI, when known>, <pull request or commit that made it. "this pull request" until it has a number>

## Decision

<What was decided, in one to three sentences.>

## Why

<The reason. The constraint, the cost, the evidence.>

## Rejected

- <Alternative>: <why not>.
```

Status words: `Accepted`, `Superseded by <file>`, `Reverted by <file>`. After merge only the status line changes. Fill `Change` once the pull request has its number. Leave out an unknown work item. Never guess one.

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

At the repo root. Only terms with a project meaning.

```markdown
# Glossary

- **<Term>**: <what it means here>. Not <the meaning people might assume>.
```

A `CONTEXT.md` that holds the terms keeps its name. With `GLOSSARY-MAP.md`, point the Terms line at the map.
