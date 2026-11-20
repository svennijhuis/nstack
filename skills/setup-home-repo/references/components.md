# The component registry

Setup finds items by "What counts" and "Where to look", apply and add place them by "Home", advise uses "Check". Paths per harness: [harnesses.md](harnesses.md). A new kind is a row here and in the harness table, nothing else.

## The kinds

| Kind | What counts | Where to look | Home | Check |
| --- | --- | --- | --- | --- |
| `steering` | The file the harness loads every session: `AGENTS.md`, `CLAUDE.md`, Copilot instructions | Root of each repo, the user folder | `AGENTS.md` at the root | Too long. Restates a skill. Two files that disagree. |
| `repo` | A git repo the agent may need to read or change | The folders the person names | A pointer line under `## Repos` | Path gone and no remote. Repo on disk with no pointer. No commit in a long time. |
| `source` | A place outside git: wiki, issue tracker, pipeline, chat, docs site, dashboard | Git remotes, MCP config, tools on the path, links in steering files | A pointer line under `## Sources` | The access method is gone. Two pointers to the same place. |
| `skill` | A folder with a `SKILL.md` | Skill folders of each harness, in each repo and the user folder | The skills folder | Same name in two places. Copies that differ. Missing from a harness in use. |
| `rule` | A scoped instruction file: Cursor rule, Copilot instruction file, Claude rule | Rule folders of each harness | The rules folder of each harness in use | Applies to paths that do not exist. Says what `AGENTS.md` already says. |
| `agent` | A subagent or custom agent definition | Agent folders of each harness | The agents folder | Same name in two places. Names a tool or model that is not available. |
| `command` | A slash command or prompt file | Command and prompt folders of each harness | The commands folder | Same name as a skill. Same name in two places. |
| `hook` | A hook entry and the script it runs | Settings and hook files of each harness | The hook config, scripts beside it | Script missing or not executable. Same hook registered twice. |
| `setting` | Permissions, environment, model, and other harness settings | Settings files, project and user | The project settings file | Rules that repeat or conflict. A personal preference in the shared file. |
| `mcp` | One MCP server entry | MCP config of each harness, project and user | The project MCP config | Same server in two scopes. Command not on the path. A literal secret. |
| `registration` | An enabled plugin or a known marketplace | Settings files | The project settings file | Plugin enabled with no marketplace. Marketplace with no plugin. |
| `tool` | A script or command line tool the agent runs | `tools/`, `scripts/`, `bin/` in each repo, paths named in steering files | `tools/`, one line each in `AGENTS.md` | Named in steering but missing. Not executable. No usage line. |
| `wiki` | Markdown the agent reads for knowledge, kept in git | `wiki/`, `docs/`, `notes/` in each repo | `wiki/` | Page nothing links to. Link to a page that is gone. |
| `other` | Anything agent-related that fits no row above | Everywhere | Ask the person | Listed here with no decision yet. |

## Rules for the walk

- Skip dependency and build folders: `node_modules`, `vendor`, `obj`, `dist`, `target`, `.venv`, and a `bin` that git ignores.
- Note but never open `.env`, key files, and what a `.gitignore` marks as a secret store.
- Read each harness's user folder too.
- Record per item: kind, name, path, harness, repo, and a content hash.
- In a child repo, the steering file (`AGENTS.md`, `CLAUDE.md`, `copilot-instructions.md`), `docs/adr/`, `docs/agents/`, `docs/design/`, `GLOSSARY.md`, `CONTEXT.md`, and `DECISIONS.md` are `repo-specific`, skip the bucket rules, and are never `wiki`. Apply adds only the `Home repo:` line; the rest belongs to `setup-agents-md`.
- Same name and kind: a `duplicate` when the hashes match, `drift` when not. On drift, show both and ask which wins. Never merge them.

## Choosing the bucket

Take the first rule that fits.

1. It comes from a plugin or a marketplace → `installed`.
2. It is in two or more places → `duplicate`.
3. A `tool` or `wiki` item in one repo only → `repo-specific`.
4. In one repo, and its body names that repo, a path in it, or its service 3 or more times → `repo-specific`.
5. Otherwise → `shared`. In one repo only, round two asks.

The person can change any bucket in the plan.

## Personal or team

A team home repo holds what everyone needs. Personal taste (editor style, model choice, shortcuts) stays in the user folder: bucket it `repo-specific` with the user folder as its repo, and say why.
