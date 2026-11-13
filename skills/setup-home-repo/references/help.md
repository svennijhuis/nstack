# Help and status

Neither changes a file.

## Help

On `/setup-home-repo help`, print this card and stop.

```text
/setup-home-repo                 no home repo here: build one. home repo here: show its status and ask what to do
/setup-home-repo update          rescan and propose what changed: new repos, new designs, drift
/setup-home-repo update <thing>  add or change one item: a repo, a source, a design, a skill, an MCP server,
                                 a hook, a rule, a setting, an agent, a command, a tool, a wiki page
/setup-home-repo advise          audit and say what to fix. changes nothing
/setup-home-repo cleanup         fix what advise found, the rows you pick
/setup-home-repo help            this card
```

`<thing>` is a path, an address, or a few words: `update ~/repos/acme/search`, `update the Confluence space OPS`, `update a hook that blocks force push`.

## Status

On `/setup-home-repo` inside a home repo, print the status, ask what to do, and wait. Count from disk. Do not run the full audit.

```text
Home repo: ~/repos/acme/home   Harnesses: Claude Code, Cursor
Repos 12 (2 not cloned)   Sources 4   Designs 3   Skills 9   Hooks 3   MCP servers 5   Rules 6   Tools 2   Wiki 31 pages
Last change 2026-11-03.

On disk with no pointer: repo search, design 2026-11-13-search.

What now?  1 update (recommended)  2 advise  3 cleanup  4 help
```

- Leave out a count that is zero.
- Name each repo and each design folder that sits on disk with no pointer, in one line. Leave the line out when there are none.
- Recommend `update`. Recommend `advise` instead when the last change is over a month old and nothing on disk lacks a pointer.
- Run the mode the person picks. Run nothing until they pick.

## Unclear call

When the word after `/setup-home-repo` matches no mode, or a sentence could mean two modes, do not pick one. Say in one line what you could not place. Inside a home repo, print the status and the same question. Outside one, ask whether to build a home repo here.

`add <thing>` is not unclear. Read it as `update <thing>`.
