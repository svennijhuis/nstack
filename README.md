# nstack

The agent skills I use every day, cleaned up so anyone can use them. They work
in Claude Code, Codex, Cursor, and GitHub Copilot.

## Skills

| Skill | Say | What it does |
|---|---|---|
| `tech-design` | "tech design" | Charts a technical design as a shared map, finds every gap, and closes them one per session until a developer or an agent can build from it without guessing. |
| `setup-home-repo` | "set up a home repo" | Creates, updates, audits, and cleans up one repo that holds your shared skills, steering files, MCP servers, and hooks, with a router skill on top. Local only or git, and how it hands over to `setup-agents-md`: [README](skills/setup-home-repo/README.md). |
| `setup-agents-md` | "set up AGENTS.md" | Creates, trims, and audits a repo's `AGENTS.md`, keeps only what the code cannot say, and puts decisions (ADRs) and the glossary in the repo they belong to. What goes in the docs and what does not: [README](skills/setup-agents-md/README.md). |
| `setup-nstack-skills` | "set up nstack" | Installs the external skills nstack calls, at pinned commits, after you approve the plan. |

## How they work together

```text
1. setup-nstack-skills     once: install the external skills the others call
2. setup-home-repo         once: one home repo for skills, pointers, MCP, hooks, and a router
3. setup-agents-md <repo>  per repo, called by step 2 or by you: a lean AGENTS.md, code standards, ADRs, glossary
4. tech-design             per feature. One repo: start it there. Several repos: start it in the home repo
5. build                   agents follow AGENTS.md, write an ADR with each decision
6. setup-agents-md advise  now and then: report drift and shipped designs that are not ADRs yet
7. setup-agents-md         after a design ships: its decisions become ADRs
```

- **Each skill works alone.** A skill calls another by name only when it is
  installed. `setup-agents-md` needs no home repo, and `setup-home-repo` needs
  no `setup-agents-md`.
- **Where things live.** The skills and the pointers live in the home repo.
  Everything about a repo's code lives in that repo: its `AGENTS.md`, code
  standards, ADRs, and glossary. When a design ships, its decisions become
  ADRs in each repo they change.
- **Local only or git.** `setup-home-repo` asks whether the home repo is a git
  repo you share or a plain local folder. A local-only home repo is never
  committed. Everything else works the same.
- **Designs.** A design lives where you start `tech-design`. In a home repo it
  asks: here, or in one of the repos. Without a home repo it never asks.
- **Who owns what.** `setup-home-repo` owns the home repo and the one line in
  each child repo that points home. `setup-agents-md` owns the rest of each
  repo's `AGENTS.md` and folds an old `CLAUDE.md` into it. No skill writes a
  `CLAUDE.md`: every harness reads `AGENTS.md`, Claude Code from version
  2.1.277. `tech-design` owns `docs/design/` while a design is open.
- **Hand-offs.** After setup and after `add <repo>`, `setup-home-repo` calls
  `setup-agents-md` for the child repos you pick. Both commit on one local
  branch per repo, so you review and push one branch per repo.
  `setup-agents-md` advise reports a decision that sits in the home repo but
  belongs to a child repo, and a shipped design whose decisions are not ADRs
  yet.
- **Updating.** When a repo's structure has changed, type
  `/setup-agents-md <repo>` in the home repo, `/setup-agents-md` in the repo
  itself, or `/setup-agents-md all` for every child repo. It updates rather
  than starts over: it checks every line against the code, shows what to keep,
  move, or delete, and waits for your yes.

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
user-level steering file or in a repo's `AGENTS.md`, so you can update the
skills without losing them.

## License

None yet.
