# Help and status

Neither changes a file.

## Help

On `/setup-home-repo help`, print this card and stop.

```text
/setup-home-repo                 no home repo here: build one. home repo here: show its status
/setup-home-repo add <thing>     add or update one item: a repo, a source, a skill, an MCP server,
                                 a hook, a rule, a setting, an agent, a command, a tool, a wiki page
/setup-home-repo add git         turn a local-only home repo into a git repo
/setup-home-repo advise          audit and say what to fix. changes nothing
/setup-home-repo cleanup         fix what advise found, the rows you pick
/setup-home-repo help            this card
```

`<thing>` is a path, an address, or a few words: `add ~/repos/acme/search`, `add the Confluence space OPS`, `add a hook that blocks force push`.

Then one line: the router answers "what do I use for this?" once a home repo exists.

## Status

On `/setup-home-repo` inside a home repo, print the status and stop. Count from disk. Do not run the full audit.

```text
Home repo: ~/repos/acme/home   Harnesses: Claude Code, Cursor   Router: /ask-home
Repos 12 (2 not cloned)   Sources 4   Skills 9   Hooks 3   MCP servers 5   Rules 6   Tools 2   Wiki 31 pages
Last change 2026-11-03.

Next: /setup-home-repo advise
```

- Leave out a count that is zero. Add `Local only` to the first line when the folder is not a git repo.
- Name `advise` as the next step when the last change is over a month old or a repo is not cloned. Otherwise name `add`.
- If a repo sits beside the others with no pointer, say so in one line and offer to run setup again. On a yes, do setup from step 1. It proposes only what changed.
