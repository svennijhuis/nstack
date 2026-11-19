# nstack

The agent skills I use every day, cleaned up so anyone can use them. They work
in Claude Code, Codex, Cursor, and GitHub Copilot.

## Skills

| Skill | Say | What it does |
|---|---|---|
| `tech-design` | "tech design" | Charts a technical design as a shared map, finds every gap, and closes them one per session until a developer or an agent can build from it without guessing. |
| `setup-home-repo` | "set up a home repo" | Creates, updates, audits, and cleans up one repo that holds your shared skills, steering files, MCP servers, and hooks. Local only or git, and how it hands over to `setup-agents-md`: [README](docs/skills/setup-home-repo/README.md). |
| `setup-agents-md` | "set up AGENTS.md" | Creates, trims, and audits a repo's `AGENTS.md`, keeps only what the code cannot say, and puts decisions (ADRs) and the glossary in the repo they belong to. What goes in the docs and what does not: [README](docs/skills/setup-agents-md/README.md). |
| `align-code` | "align the code" | Finds every place the code does one thing in more than one way, lets you pick the way, reports what does not match, and rewrites it one standard at a time on a local branch: [README](docs/skills/align-code/README.md). |
| `setup-nstack-skills` | "set up nstack" | Installs the external skills nstack calls, at pinned commits, after you approve the plan. |
| `implement` | "implement this" | Builds a ticket so the codebase gets better, not worse: deeper modules, better tests, no comment that covers a shortcut, the glossary's words. Says its refactor call before the code, refactors first where the change needs it, builds with `tdd`, gets an independent review, proves it works, and names deepening candidates it saw. Works after `tech-design` or after Matt Pocock's `to-spec` and `to-tickets`: [README](docs/skills/implement/README.md). |
| `comment-root-cause` | "check the comments" | Asks why a comment is there and whether the code can be better. A comment that covers a shortcut means: fix the root cause. A business rule, a decision, or API docs stay. The agent starts it when it writes a comment: [SKILL.md](skills/comment-root-cause/SKILL.md). |

## How they work together

```mermaid
flowchart TD
    A[setup-nstack-skills<br/>once: install the external skills] --> B{More than one repo?}
    B -->|Yes| C[setup-home-repo<br/>once: skills, pointers, MCP, hooks]
    B -->|No| D
    C -->|calls, per child repo| D[setup-agents-md<br/>lean AGENTS.md, code standards, ADRs, glossary]
    D -->|code written many ways| I[align-code<br/>one or more standards per area, report]
    I --> E
    D --> E[tech-design<br/>per feature. One repo: start it there.<br/>Several repos: start it in the home repo]
    E --> F[implement<br/>per ticket: refactor where the change needs it,<br/>follow AGENTS.md, one ADR per decision]
    F <-->|a new comment| R[comment-root-cause<br/>fix the cause, not the symptom]
    F -->|now and then| G[setup-agents-md advise<br/>reports drift and shipped designs]
    F -->|now and then| A2[improve-codebase-architecture<br/>candidates for deeper modules,<br/>each one a ticket for implement]
    G -->|once a feature has shipped| H[setup-agents-md<br/>shipped decisions become ADRs,<br/>the design folder is offered for deletion]
    H --> E
```

A design from start to shipped:

1. `/tech-design new <name>` charts the design and lists its gaps.
2. `/tech-design <name>` closes one gap per session.
3. `/tech-design <name> ready` runs the gate and writes the tickets.
4. `/tech-design <name> committed` records the sign-off. Builders start.
5. After the feature ships, `/setup-agents-md` in the repo that holds the
   design asks if it shipped, turns its decisions into ADRs, and offers to
   delete the folder.

- **Each skill works alone.** A skill calls another only when it is installed.
- **Who owns what.** `setup-home-repo` owns the home repo and the one line in
  each child repo that points home. `setup-agents-md` owns the rest of a repo's
  `AGENTS.md`, its ADRs, and its glossary. `tech-design` owns `docs/design/`.
  `align-code` owns `docs/align/`.
- **One branch per repo.** The two setup skills put every change to a repo on
  one local branch, after you approve the plan. You review and push it.
  `tech-design` writes only its design folder and commits nothing. You commit
  it.
- **`AGENTS.md` by default.** Claude Code reads it from version 2.1.277. A
  `CLAUDE.md` is written only when you ask for one, use an older Claude Code,
  or another `CLAUDE.md` hides `AGENTS.md`. Then it is one line: `@AGENTS.md`.

The details are in the READMEs of
[setup-home-repo](docs/skills/setup-home-repo/README.md) and
[setup-agents-md](docs/skills/setup-agents-md/README.md).

## With Matt Pocock's skills

nstack works next to [Matt Pocock's skills](https://github.com/mattpocock/skills).
A flow that uses both:

```mermaid
flowchart TD
    S[once: setup-agents-md + setup-matt-pocock-skills] --> P{Per feature}
    P -->|developers and business sign a design| TD[tech-design]
    P -->|only technical decisions| W[wayfinder]
    TD -->|its tickets.md| IM
    TD -.->|only to put them in your tracker| SP
    W --> SP[to-spec]
    SP --> TT[to-tickets]
    TT --> IM[implement, per ticket]
    IM --> V[verify-flow before and after,<br/>when the ticket writes stored state]
    IM --> CR[code-review + the design reviewer,<br/>fresh context]
    IM --> PR[pr: you run it, for the pull request body]
```

### `tech-design` or `wayfinder`

Pick one per feature, not both. Both chart a map and close one question per
session.

| Use | When | You get |
| --- | --- | --- |
| `tech-design` | Others must read and sign the plan: developers and business, a reviewer, an approver. An outside system or vendor is involved (access, contracts, limits). Requirements and acceptance criteria must be written down. The feature spans several repos. | A design document in `docs/design/`: 14 fixed sections, requirements, diagrams, failure modes, dependencies, sign-off. The ready gate checks it and writes `tickets.md`. |
| `wayfinder` | The work is too big for one session, but the open points are technical decisions for the team itself. Nobody outside needs a document. You want the decisions as tickets in your tracker. | A map issue in your tracker with one ticket per decision. The decisions are the result, not a document. Then `to-spec` and `to-tickets`. |
| neither | The change is clear and fits a few tickets. | Straight to `to-spec`, or to `implement` for a single ticket. |

In doubt: `wayfinder`. It is lighter, and a design can still start from its
decisions when someone asks for a document.

After `tech-design` you can skip `to-spec` and `to-tickets`: the ready gate
already wrote the tickets. Use them only to put the spec and the tickets in
your tracker.

### Rules for the combined flow

- `implement` runs `verify-flow` and `code-review` itself. Do not run them
  again after it: that reviews the same diff twice. It stops at the commit:
  you open the pull request, with `pr` or by hand.
- Install nstack's `implement`, not Matt Pocock's. Both have that name, and
  this one holds his loop.
- Claude Code ships its own `code-review` skill. Matt Pocock's has the same
  name. `implement` and `align-code` mean his two-axis review. When the other
  one loads, `implement` says so and runs the two reviews as subagents itself.
- Now and then, run `improve-codebase-architecture`. It finds where the code
  needs deeper modules. Each candidate you pick becomes a ticket, and
  `implement` builds it as a refactor ticket.
- `setup-agents-md` leaves the files `setup-matt-pocock-skills` owns alone:
  the `## Agent skills` block and `docs/agents/issue-tracker.md`, `domain.md`,
  and `triage-labels.md`.

Some skills call skills that live in other repos. Run `setup-nstack-skills` to
install them. The list is in
[external-skills.md](skills/setup-nstack-skills/external-skills.md):

- `tech-design` uses `grilling`, `domain-modeling`, `research`,
  `codebase-design`, `writing-for-agents`, `deslop`, `technical-writing`, and
  `unslop`.
- `align-code` uses `grilling`, `domain-modeling`, `research`,
  `codebase-design`, `code-review`, `comment-root-cause`, and
  `writing-for-agents`.
- `implement` uses `tdd`, `code-review`, `codebase-design`,
  `comment-root-cause`, `diagnosing-bugs`, and `verify-flow` when it is
  installed, and suggests `blast-radius`.

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

With a home repo, `setup-home-repo` moves the skills from the user folder into
it, after you approve the plan.

## Requirements

- Network access for `setup-nstack-skills`, to fetch external skills at their
  pinned commit.
- A git repo to work in, or a local-only home repo. `tech-design` writes to
  `docs/design/<yyyy-mm-dd>-<name>/` relative to the folder the agent runs in.
  Start the agent in the repo that should hold the design. With a home repo,
  start in the child repo the design is about. When the design spans several
  repos, start in the home repo. Either way its decisions end up as ADRs in
  the repos they change. See [setup-agents-md](docs/skills/setup-agents-md/README.md).

## Make them yours

These are starting points. Edit them. Put personal settings in your
user-level instructions file or in a repo's `AGENTS.md`, so you can update the
skills without losing them.

## License

MIT. See [LICENSE](LICENSE). Each skill's `NOTICE.md` names where its ideas
come from.
