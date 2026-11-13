# Home repo or child repo

A home repo, from `setup-home-repo`, is the repo the agent starts in. A child repo is any repo it points at under `## Repos`. This skill works in both, but they hold different things.

## Where each thing lives

| Thing | Home repo | Child repo |
| --- | --- | --- |
| This skill | Yes, in the skills folder, so every repo can use it | No copy |
| `AGENTS.md` | Yes: how to work across repos, pointers | Yes: what is true only for that repo |
| ADRs | Only decisions about the home repo itself: which harnesses, which skills, how repos are laid out | Every decision about that repo's code |
| Glossary | Only terms about the home repo itself | Every term of that repo's domain |
| Topic files | Only for working across repos | Every topic of that repo |

A decision belongs next to the code it changes. A reader of that repo finds it, a revert of that code can be checked against it, and it stays true when the home repo changes.

A decision that spans repos: write the full ADR in the repo that owns the change. In each other repo it touches, write a short ADR with the decision in one sentence and a link to the full one.

## Designs from `tech-design`

| The design touches | Start `tech-design` in | The design lives in |
| --- | --- | --- |
| One repo | That repo | That repo's `docs/design/` |
| More than one repo | The home repo | The home repo's `docs/design/`, while it is open |

A design is a plan, not a decision record. A cross-repo plan has no single repo to live in, so it stays in the home repo while it is open. Its decisions do not stay there. When the feature ships, each line of Decisions so far becomes an ADR in the repo it changes, by the cross-repo rule above. Then the design folder is offered for deletion.

So the home repo may hold open designs that span repos. It never holds a shipped design, and never holds an ADR about a child repo.

## Running in a home repo

When the working directory is a home repo:

1. **With a repo name**, `/setup-agents-md <repo name>`: find its pointer under `## Repos`. If the path is missing, clone it from the remote in the pointer. Run Create or Update on that repo. Work on a new local branch there. If it has uncommitted changes, stop and report it.
2. **With nothing typed**: ask one question. "Which repo? The home repo itself, or one of: <names from `## Repos`>." Recommend the child repo the person last named, or the home repo if none.
3. **On the home repo itself**: trim only the steering text at the top of `AGENTS.md`. Never change `## Repos`, `## Sources`, `## Tools`, or `## Environment`. They belong to `setup-home-repo`. For problems there, name `/setup-home-repo advise`.

Offer to add this line under `## How to work across repos` in the home `AGENTS.md`, if it is not there:

```markdown
- Record decisions, terms, and topic docs in the repo they are about, never here. Run `/setup-agents-md <repo>` to set that repo up.
```

## Running in a child repo

Work as in any repo. Keep the line that points at the home repo. Do not copy text from the home repo's `AGENTS.md`. The agent reads both.

## Things in the wrong place

Advise reports these. Fixing one is a plan row, never a silent move.

- An ADR, glossary, or topic file in the home repo that is about one child repo: move it to that repo, on a branch there.
- A rule in a child repo's `AGENTS.md` that repeats the home repo's text: delete it from the child.
- A rule in the home repo's `AGENTS.md` that applies to only one child repo: move it to that repo.
