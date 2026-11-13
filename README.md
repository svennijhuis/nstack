# nstack

The agent skills I use every day, cleaned up so anyone can use them. They work
in Claude Code, Codex, Cursor, and GitHub Copilot.

## Skills

| Skill | Say | What it does |
|---|---|---|
| `tech-design` | "tech design" | Charts a technical design as a shared map, finds every gap, and closes them one per session until a developer or an agent can build from it without guessing. |
| `setup-home-repo` | "set up a home repo" | Creates, updates, audits, and cleans up one repo that holds your shared skills, steering files, MCP servers, and hooks, with a router skill on top. |
| `setup-agents-md` | "set up AGENTS.md" | Creates, trims, and audits a repo's `AGENTS.md`, keeps only what the code cannot say, and puts decisions (ADRs) and the glossary in the repo they belong to. What goes in the docs and what does not: [README](skills/setup-agents-md/README.md). |
| `setup-nstack-skills` | "set up nstack" | Installs the external skills nstack calls, at pinned commits, after you approve the plan. |

## How they work together

```text
1. setup-nstack-skills     once: install the external skills the others call
2. setup-home-repo         once: one home repo for skills, pointers, MCP, hooks, and a router.
                           It asks whether to run step 3 on every child repo.
3. setup-agents-md <repo>  per repo: a lean AGENTS.md, code standards, ADRs, glossary
4. tech-design             per feature. One repo: start it there. Several repos: start it in the home repo
5. build                   agents follow AGENTS.md, write an ADR with each decision
6. setup-agents-md advise  now and then: find drift, turn shipped designs into ADRs
```

- **Where things live.** The skills and the pointers live in the home repo. Everything about a repo's code lives in that repo: its `AGENTS.md`, code standards, ADRs, glossary, and designs. One exception: an open design that spans several repos lives in the home repo. When it ships, its decisions become ADRs in each repo they change. Start in the home repo and type `/setup-agents-md <repo>`, or start in the repo itself.
- **Who owns what.** `setup-home-repo` owns the home repo's `## Repos`, `## Sources`, `## Tools`, and `## Environment`, and trims each child repo's `AGENTS.md` to what is true for that repo. `setup-agents-md` then keeps that file lean and never touches the home repo's pointers. `tech-design` owns `docs/design/` while a design is open.
- **Hand-offs.** `setup-home-repo` advise reports a decision that sits in the home repo but belongs to a child repo. `setup-agents-md` advise reports a shipped design whose decisions are not ADRs yet. Each tells you which skill fixes it.
- **Updating.** Run `/setup-agents-md` again in a repo that already has an `AGENTS.md`. It updates rather than starts over: it checks every line against the code, shows what to keep, move, or delete, and waits for your yes.

Some skills call skills that live in other repos. Run `setup-nstack-skills` to
install them. The list is in
[external-skills.md](skills/setup-nstack-skills/external-skills.md):

- `tech-design` uses `technical-writing` and `unslop`.

## Install

```bash
git clone https://github.com/svennijhuis/nstack
cp -R nstack/skills/* ~/.claude/skills/    # Claude Code
cp -R nstack/skills/* ~/.codex/skills/     # Codex
cp -R nstack/skills/* ~/.cursor/skills/    # Cursor
cp -R nstack/skills/* ~/.copilot/skills/   # GitHub Copilot
```

Create the target folder first if it does not exist (`mkdir -p ~/.cursor/skills`).

Then say "set up nstack" to pull in the external skills.

## Requirements

- Network access for `setup-nstack-skills`, to fetch external skills at their
  pinned commit.
- A git repo to work in. `tech-design` writes to
  `docs/design/<yyyy-mm-dd>-<name>/` relative to the folder the agent runs in.
  Start the agent in the repo that should hold the design. With a home repo,
  start in the child repo the design is about. When the design spans several
  repos, start in the home repo. Either way its decisions end up as ADRs in
  the repos they change. See [setup-agents-md](skills/setup-agents-md/README.md).

## Make them yours

These are starting points. Edit them. Put personal settings in your
user-level steering file (`~/.claude/CLAUDE.md` for Claude Code) or in a repo's
`AGENTS.md`, so you can update the skills without losing them.

## License

None yet.
