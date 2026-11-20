# The home repo layout

Create only what has content.

```text
<home>/
  AGENTS.md            steering, Repos, Sources, Tools, Environment
  CLAUDE.md            one line: @AGENTS.md   (only when asked for, see harnesses.md)
  .claude/             skills, rules, agents, hooks, settings   (Claude Code)
  .cursor/             rules, hooks, mcp.json                   (Cursor)
  .github/             instructions, hooks, agents, prompts     (Copilot)
  .codex/              config.toml                              (Codex)
  .agents/skills/      skills, or a link to them
  .mcp.json            MCP servers                              (Claude Code)
  repos/<area>.md      pointer files, only past about 20 repos
  wiki/                knowledge in markdown, only if there is any
  tools/               scripts the agent runs, only if there are any
  docs/adr/            decisions about the home repo itself   (from setup-agents-md, left alone)
  docs/design/         open designs that span repos           (from tech-design, left alone)
  .gitignore           local settings files, worktrees, secret files, child repo clones   (git only)
```

## `AGENTS.md`

Short: it loads every session. It says where things are; a skill holds a procedure.

```markdown
# Home repo

Start every session here. Reach other repos and sources through the pointers below.

## How to work across repos

- A repo that is missing at its path: clone it from the remote in its pointer.
- One clone per repo. For a second task in the same repo at the same time, add a git worktree inside that clone.
- Read a repo's own steering file before you change it.
- Open one pull request per repo. Name the others in each description.
- Record decisions, terms, and topic docs in the repo they are about. Only decisions about this home repo itself go here.

## Repos

- <name> (<what it is>): <local path>. Clone from <remote> if missing.

## Sources

- <name> (<kind>): <location>. Reach via <how>.

## Tools

- <name>: <what it does>. Run `<command>`.

## Environment

- <VARIABLE_NAME>: <what it is for>
```

Leave out a section with no lines, but always keep `## Repos`: it marks the home repo.

## The repo pointer

```text
<name> (<what it is>): <local path>. Clone from <remote> if missing.
```

- `<what it is>`: a few words to match a task against, such as "payments API, .NET".
- `<local path>`: the same for the whole team, under the home folder, by the convention asked once.
- No remote: drop the second sentence.
- A hint after it only when it changes what the agent does: "Run `git pull` first."

Good: `storefront (web shop, Next.js): ~/repos/acme/storefront. Clone from git@github.com:acme/storefront.git if missing.`

Bad: `storefront: the storefront repo`. No path, no remote, the name repeated.

## The source pointer

```text
<name> (<kind>): <location>. Reach via <how>.
```

- `<kind>`: free text, such as wiki, issue tracker, pipeline, chat.
- `<location>`: what a person would open: a URL, an organisation and project, a channel.
- `<how>`: an MCP server by its config name, a command line tool, or a URL to fetch.

```text
engineering wiki (wiki): dev.azure.com/acme/platform, wiki "Platform". Reach via the `az` tool: `az devops wiki page show`.
tickets (issue tracker): github.com/acme/storefront/issues. Reach via `gh issue`.
runbooks (docs): Confluence space OPS. Reach via the MCP server `atlassian`.
```

Copy nothing from a source. With no access method yet, write `Reach via: none yet` and report it.

## The line that points home

In each child repo's steering file, under its first sentence, or first when there is none:

```text
Home repo: <local path>. Shared skills and pointers to the other repos and sources live there.
```

Every mode finds it by `Home repo:`.

## Many repos

| Repos | Shape |
| --- | --- |
| Up to about 20 | Every pointer in `AGENTS.md` |
| More | One file per area under `repos/`. `AGENTS.md` lists the areas, one line each, with what belongs there. |
| Thousands | Stop. Tell the person a plugin marketplace fits better. |

Past about 20, `## Repos` becomes:

```markdown
## Repos

- Frontend: `repos/frontend.md`. Web and mobile apps.
- Backend: `repos/backend.md`. Services and APIs.
- Internal: `repos/internal.md`. Tooling and infrastructure.
```

Each area file holds pointer lines. Ask for the areas; never guess them from repo names.

## Clones inside the home repo

Clones inside the home folder stay put. In a git home repo, `.gitignore` lists each one.

## Local only

A plain folder: no git, no `.gitignore`, no commit. Every mode works the same, without undo: it still shows the diff and waits for a yes, but keeps no copy. `/setup-home-repo add git` turns it into git, by [add.md](add.md).

## Worktrees

A parallel task gets a worktree in the clone under `.worktrees/<task>`, listed in that repo's local exclude file, not its `.gitignore`. Cleanup removes merged ones.

## What stays out

- Secrets, tokens, and `.env` files.
- A person's own settings: user folder, or a local settings file git ignores.
- Copies of content that lives in a source.
- Anything bucketed `repo-specific`.
