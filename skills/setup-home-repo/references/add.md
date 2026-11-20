# Add or update one item

`/setup-home-repo add <thing>` or `update <thing>` adds or changes one item. Only inside a home repo; outside one, name setup.

1. **Resolve the kind** by [components.md](components.md). A path or git address is a `repo`, a web address a `source`, a folder with `SKILL.md` a `skill`. Two fit: ask. None: `other`, ask where it lives.
2. **Look for it.** Same name and kind exists: this is an update. Show it.
3. **Explore what you need**: a repo's remote, what it is, and the path convention; a source's location and access method, checked as in setup; an MCP server's command and variables.
4. **Ask only what is missing**, recommended answer first.
5. **Show the diff** of every file, for every harness in use.
6. **Write** on a yes. Commit in the home repo unless local only.
7. **Report** in one or two lines, including any harness with no place for it.

## By kind

| Kind | What add does |
| --- | --- |
| `repo` | Adds the pointer, and the `Home repo:` line in the child by apply step 7 in [setup.md](setup.md). A clone inside a git home folder goes into `.gitignore` first. Offers `/setup-agents-md <repo>` when installed. Past about 20 repos, offers the `repos/<area>.md` split. |
| `source` | Adds the pointer. No access method: offers one first, else writes `none yet`. |
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

Show old and new side by side. A skill is replaced whole, never patched. A rename changes every place that names it: `AGENTS.md`, pointer files, other skills.

## From local only to git

`/setup-home-repo add git` turns a local-only home repo into git:

1. `git init`.
2. The full `.gitignore` by apply step 5 in [setup.md](setup.md).
3. Show the files the first commit holds: no clone, local settings file, or secret, by the advise secret check.
4. Commit on a yes.

## Remove

`add` never removes. Removing is a cleanup row.
