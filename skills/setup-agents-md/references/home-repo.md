# Home repo or child repo

This skill works without a home repo. Skip this file then. A home repo, from `setup-home-repo`, is the repo the agent starts in. A child repo is any repo it points at under `## Repos`. This skill works in both, but they hold different things.

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

A design lives in the folder `tech-design` was started in.

| The design touches | Start `tech-design` in | The design lives in |
| --- | --- | --- |
| One repo | That repo | That repo's `docs/design/` |
| More than one repo | The home repo. `tech-design` asks there, and the person may pick a repo instead. | The home repo's `docs/design/`, while it is open |

A design is a plan, not a decision record. A cross-repo plan has no single repo to live in, so it stays in the home repo while it is open. Its decisions do not stay there. When the feature ships, the skill's `tech-design` steps turn them into ADRs by the cross-repo rule above.

So the home repo may hold open designs. It never holds a shipped design or an ADR about a child repo.

## Running in a home repo

When the working directory is a home repo:

1. **With a repo name**, `/setup-agents-md <repo name>`: find its pointer under `## Repos`. If the path is missing, ask before you clone it from the remote in the pointer. Advise does not clone: it reports the missing path and stops. Run Create or Update on that repo.
2. **With `all`**: do step 1 for every repo under `## Repos`, one after the other. Each repo gets its own plan, its own yes, and its own branch. A no skips that repo only.
3. **With nothing typed**: ask one question. "Which repo? The home repo itself, or one of: <names from `## Repos`>." Recommend the child repo the person last named, or the home repo if none.
4. **On the home repo itself**: trim only the steering text above `## Repos` in `AGENTS.md`. Never change `## Repos`, `## Sources`, `## Tools`, or `## Environment`. They belong to `setup-home-repo`. For problems there, name `/setup-home-repo advise`. A home repo that is not a git repo has no branch: after the yes, copy the old file to `.backup/AGENTS.md-<yyyy-mm-dd>`, then write.

## Running in a child repo

Work as in any repo. Do not copy text from the home repo's `AGENTS.md`. The agent reads both.

The line that points at the home repo belongs to `setup-home-repo`. Keep it, under the first sentence. When this skill was called from the home repo and the line is missing, do not write it: name `/setup-home-repo add <repo>`.

## Things in the wrong place

Advise reports these. Fixing one is a plan row, never a silent move.

- An ADR, glossary, or topic file in the home repo that is about one child repo: move it to that repo, on a branch there.
- A rule in a child repo's `AGENTS.md` that repeats the home repo's text: delete it from the child.
- A rule in the home repo's `AGENTS.md` that applies to only one child repo: move it to that repo.
