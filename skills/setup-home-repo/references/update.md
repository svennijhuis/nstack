# Update

`/setup-home-repo update` keeps the home repo current. With no thing it rescans and proposes what changed. With a thing it adds or changes that one item. It runs only inside a home repo. Outside one, say so and name setup.

`add <thing>` is read as `update <thing>`.

## Rescan: `update`

Use this after a new repo was cloned, a design was written, or an item changed in a child repo.

1. **Explore again.** Do steps 1 to 3 of [setup.md](setup.md): the repos, the components, the sources and the harnesses.
2. **Scan the home repo itself.** The `docs/design/` folders, `wiki/`, `tools/`, the skills folder, and each harness's config. Anything on disk that `AGENTS.md` does not name is a row. Anything `AGENTS.md` names that is gone from disk is a row.
3. **Compare** with what the home repo holds. Give each difference one row:

   | Change | Row |
   | --- | --- |
   | Repo on disk with no pointer | Add the pointer |
   | Pointer whose repo is gone and that names no remote | Ask: drop the pointer, or add the remote |
   | Design folder with no pointer | Add the pointer under `## Designs` |
   | Design whose status changed | Change the status in its pointer |
   | New item in a child repo | Bucket it by [components.md](components.md) |
   | Item that differs from the home repo's copy | Drift. Show both and ask which wins |
   | New source or access method | Add or change the pointer |

4. **Ask only what is missing**, the recommended answer first.
5. **Show the plan.** The table holds only the rows that changed. Rows that are already true are counted, not listed. Show the `AGENTS.md` diff below it. Wait for approval.

   ```text
   Item               Kind    Change                          To
   search             repo    on disk, no pointer             AGENTS.md Repos
   2026-11-13-search  design  on disk, no pointer             AGENTS.md Designs
   review-pr          skill   differs from storefront's copy  ask which wins

   3 changes. 41 items already true.
   ```

6. **Apply** on a yes, in the order of step 6 in [setup.md](setup.md). Commit in the home repo. Do not push.
7. **Report** one outcome per row.

When nothing changed, say so in one line with the clean count and stop.

Never rewrite `AGENTS.md` whole. Change the lines that differ, and keep what the person wrote by hand.

## One item: `update <thing>`

`<thing>` is a path, an address, or a few words.

1. **Resolve the kind.** Match `<thing>` to a row in [components.md](components.md). A path or a git address is a `repo`. A web address is a `source`. A folder with a `SKILL.md` is a `skill`. A folder under `docs/design/` is a `design`. If two kinds fit, ask which. If none fits, it is `other`: ask where it should live.
2. **Look for it.** If an item with that name and kind exists, this is a change to it. Show what is there.
3. **Explore what you need.** A repo: its remote, what it is, the path convention already used in `AGENTS.md`. A source: its location and the access method, checked by the same means as setup. An MCP server: its command or address, and the variables it needs.
4. **Ask only what is missing**, with a recommended answer.
5. **Show the diff.** Every file that changes, for every harness in use. One item usually touches one to four files.
6. **Write** on a yes. Commit in the home repo. Do not push.
7. **Report** in one or two lines: what was added or changed, where, and anything a harness had no place for.

### By kind

| Kind | What update does |
| --- | --- |
| `repo` | Adds the pointer line in the same format as the others. Past about 20 repos, offers the split into `repos/<area>.md` by [layout.md](layout.md). |
| `source` | Adds the pointer line. If no access method exists, offers to add one first, such as an MCP server, and writes `none yet` if the person declines. |
| `design` | Adds the pointer line under `## Designs`, by [layout.md](layout.md). The design folder itself is not changed. |
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

### Changing an item that exists

Same steps. Show the old and the new side by side. For a skill, replace the folder whole. Never patch a skill's body in place. If the name changes, change every place that names it: `AGENTS.md` and other skills' text.

## Remove

`update` does not remove a file. Removing is a cleanup row, so it gets the same checks. A rescan may drop a pointer line whose repo or design is gone, after the person says yes to that row.
