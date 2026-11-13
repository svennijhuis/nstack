# Add or update one item

`/setup-home-repo add <thing>` puts one item into the home repo, or changes one that is there. It runs only inside a home repo. Outside one, say so and name setup.

## Steps

1. **Resolve the kind.** Match `<thing>` to a row in [components.md](components.md). A path or a git address is a `repo`. A web address is a `source`. A folder with a `SKILL.md` is a `skill`. If two kinds fit, ask which. If none fits, it is `other`: ask where it should live.
2. **Look for it.** If an item with that name and kind exists, this is an update. Show what is there.
3. **Explore what you need.** A repo: its remote, what it is, the path convention already used in `AGENTS.md`. A source: its location and the access method, checked by the same means as setup. An MCP server: its command or address, and the variables it needs.
4. **Ask only what is missing**, with a recommended answer.
5. **Show the diff.** Every file that changes, for every harness in use, plus the map line in the router. One item usually touches two to five files.
6. **Write** on a yes. Commit in the home repo. Do not push.
7. **Report** in one or two lines: what was added, where, and anything a harness had no place for.

## By kind

| Kind | What add does |
| --- | --- |
| `repo` | Adds the pointer line in the same format as the others. Past about 20 repos, offers the split into `repos/<area>.md` by [layout.md](layout.md). When the repo has no `AGENTS.md`, or one over about 60 lines, offers `/setup-agents-md <repo>` after the commit. |
| `source` | Adds the pointer line. If no access method exists, offers to add one first, such as an MCP server, and writes `none yet` if the person declines. |
| `skill` | Copies the folder whole into the skills folder. If it came from a child repo, offers to remove it there on a new local branch. |
| `rule` | Writes one file per harness in use, in each harness's format, with the same text. |
| `agent`, `command` | Writes it for each harness that has a place for it. Reports the ones that do not. |
| `hook` | Puts the script in one place. Registers it in each harness's config, with the event mapped by what it does. Makes the script executable. |
| `setting` | Changes the project settings file. A personal preference goes to the local file instead, and you say so. |
| `mcp` | Adds the entry per harness. Replaces every literal secret with a variable and adds the name under `## Environment`. |
| `registration` | Adds the marketplace and the plugin together. Never one without the other. |
| `tool` | Puts the file in `tools/`, makes it executable, and adds its usage line to `AGENTS.md`. |
| `wiki` | Adds the page under `wiki/` and links it from an index page or a related page. |

The paths per harness are in [harnesses.md](harnesses.md).

## Update

Same steps. Show the old and the new side by side. For a skill, replace the folder whole. Never patch a skill's body in place. If the name changes, change the map line and every place that names it: `AGENTS.md`, other skills' text, the router's flows.

## Remove

`add` does not remove. Removing is a cleanup row, so it gets the same checks.
