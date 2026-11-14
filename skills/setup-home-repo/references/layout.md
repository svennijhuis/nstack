# The home repo layout

Create only what has content. An empty folder is noise.

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
  .gitignore           local settings files, worktrees, secret files, child repo clones   (git only)
  .backup/             dated copies of overwritten files   (local only)
```

The exact files per harness are in [harnesses.md](harnesses.md).

## `AGENTS.md`

Keep it short. It is loaded every session. A skill holds a procedure. `AGENTS.md` holds where things are.

```markdown
# <team or person> home repo

Start every session here. Reach other repos and sources through the pointers below.
Not sure which skill, repo, or source fits? Type the router: <router slash>.

## How to work across repos

- A repo that is missing at its path: clone it from the remote in its pointer.
- One clone per repo. For a second task in the same repo at the same time, add a git worktree inside that clone.
- Read a repo's own steering file before you change it.
- Open one pull request per repo. Name the others in each description.
- Record decisions, terms, and topic docs in the repo they are about, never here.

## Repos

- <name> (<what it is>): <local path>. Clone from <remote> if missing.

## Sources

- <name> (<kind>): <location>. Reach via <how>.

## Tools

- <name>: <what it does>. Run `<command>`.

## Environment

- <VARIABLE_NAME>: <what it is for>
```

Leave out a section that has no lines. The `## Repos` heading is how this skill knows a home repo. Keep it.

## The repo pointer

```text
<name> (<what it is>): <local path>. Clone from <remote> if missing.
```

- `<what it is>` is a few words the agent can match a task against: "storefront, Next.js", "payments API, .NET".
- `<local path>` is the same for everyone on the team. Use a path under the home folder, such as `~/repos/acme/storefront`. Ask once what the convention is.
- A repo with no remote drops the second sentence.
- Add a hint after it only when it changes what the agent does: "Run `git pull` first.", "Never push to main here."

Good: `storefront (web shop, Next.js): ~/repos/acme/storefront. Clone from git@github.com:acme/storefront.git if missing.`

Bad: `storefront: the storefront repo`. No path, no remote, and the description repeats the name.

## The source pointer

```text
<name> (<kind>): <location>. Reach via <how>.
```

- `<kind>` is free text: wiki, issue tracker, pipeline, chat, docs, dashboard.
- `<location>` is the address a person would open: a URL, an organisation and project, a channel.
- `<how>` is the thing the agent calls. One of: an MCP server by its name in the config, a command line tool, or a plain URL to fetch.

```text
engineering wiki (wiki): dev.azure.com/acme/platform, wiki "Platform". Reach via the `az` tool: `az devops wiki page show`.
tickets (issue tracker): github.com/acme/storefront/issues. Reach via `gh issue`.
runbooks (docs): Confluence space OPS. Reach via the MCP server `atlassian`.
```

Nothing from a source is copied into the home repo. The pointer says where it is and how to reach it. If no access method exists yet, write `Reach via: none yet` and report it. Do not invent one.

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

Each area file holds pointer lines in the same format. Ask the person for the areas. Do not guess them from repo names alone.

## Clones inside the home repo

When the clones sit inside the home folder, they stay where they are. In a git home repo, `.gitignore` lists each clone folder. The pointers use their paths.

## Local only

A local-only home repo is a plain folder. It has no git, no `.gitignore`, and no commit. The person shares its files by hand, or not at all. Every mode works the same there, with one difference: a copy is the undo. Before a mode overwrites or removes a file, it shows the diff and copies the old file to `.backup/<name>-<yyyy-mm-dd>`.

To share it later, the person types `/setup-home-repo add git`, see [add.md](add.md).

## Worktrees

One clone per repo. A parallel task gets a worktree inside that clone, under `.worktrees/<task>`. Put `.worktrees/` in that repo's local exclude file, not in its tracked `.gitignore`. Cleanup removes worktrees whose branch is merged.

## What stays out

- Secrets, tokens, and `.env` files.
- A person's own settings. They stay in the user folder or in a local settings file that git ignores.
- Copies of content that lives in a source.
- Anything bucketed `repo-specific`.
