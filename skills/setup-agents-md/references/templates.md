# Templates

Fill these in. Leave out a section that has no lines. Never fill a line with a guess.

## Root `AGENTS.md`

Aim for under 60 lines. Each line must apply to every task in the repo.

```markdown
# <project name>

<One sentence: what this project is and who it is for.>

## Shape

- <Main part, by name>: <what it does>. In `<top-level folder>`.
- <Main part>: <what it does>.

## Commands

- Install: `<command>`
- Test: `<command>`. Run it before you finish a change.
- Typecheck: `<command>`
- Lint: `<command>`

## Rules

- <A rule for every task that no tool enforces.>

## Read when relevant

- Testing: `docs/agents/testing.md`. Read before you write or change a test.
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

Shape is the thin navigation layer: three to six lines, the main parts of the project and what each does. Name a top-level folder at most. No deeper paths and no folder trees, because those move. The agent finds the rest itself.

Leave out the package manager line when it is npm, or when the repo pins it with corepack (`packageManager` in `package.json`). Leave out a command that is the standard one for the stack. Write the rules in plain, calm sentences. No ALL CAPS, no "IMPORTANT", no "always" or "never" where a plain sentence works. Keep the Docs and Decisions sections as they are, except for the paths.

In a child repo of a home repo, keep the one line `setup-home-repo` wrote that points at the home repo. Put it under the first sentence.

## `CLAUDE.md`

Claude Code reads `CLAUDE.md`, not `AGENTS.md`. Write one line:

```markdown
@AGENTS.md
```

When a `CLAUDE.md` with its own text exists, move each line to `AGENTS.md` or to a topic file in the plan, then replace the file with the import. A symlink also works, except on Windows without developer mode.

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
Change: <pull request or commit that made it>

## Decision

<What was decided, in one to three sentences.>

## Why

<The reason. The constraint, the cost, the evidence.>

## Rejected

- <Alternative>: <why not>.
```

Status words: `Accepted`, `Superseded by <file>`, `Reverted by <file>`. Only the status line changes after the ADR is merged.

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
