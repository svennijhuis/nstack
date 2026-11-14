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

### A shipped design in the home repo

A run on the home repo itself, and a run with `all`, handles each design in the home `docs/design/` that is `abandoned`, or `committed` and shipped by the person's word.

1. Ask which repos the design changed and which one owns the change, with the repos its text names as the recommended answer. For an `abandoned` design, ask which repo would have owned it: the one ADR goes there.
2. In each of those repos, write the ADRs by the cross-repo rule above, as that repo's own plan, on that repo's branch, after its own yes.
   When the run is on the home repo itself, that plan holds only those ADRs and the design's project terms, which go into the glossary of the repo that owns the change. It sorts nothing else, adds no section and no code standards file, and runs no command.
3. Only when every one of those ADRs is committed, offer to delete the design folder, as a row in the home repo's plan. If a repo said no or was skipped, keep the folder and report which repo is missing.
4. In a local-only home repo there is no git to keep the folder. Say so in the row, so the person knows the delete cannot be undone.

## Running in a home repo

**The repo list.** The child repos are the pointer lines under `## Repos`. Past about 20 repos, `setup-home-repo` writes area lines there instead, each naming a `repos/<area>.md` file. Then read every one of those files: their pointer lines are the repo list. An area is never a repo.

When the working directory is a home repo:

1. **With a repo name**, `/setup-agents-md <repo name>`: find its pointer in the repo list. If the path is missing, ask before you clone it from the remote in the pointer. Advise does not clone: it reports the missing path and stops. Run Create or Update on that repo.
2. **With `all`**: do step 1 for every repo in the repo list, one after the other. Each repo gets its own plan, its own yes, and its own branch. A no skips that repo only. Last, show a plan for the home repo that holds only its shipped designs, above.
3. **With nothing typed**: ask one question. "Which repo? The home repo itself, or one of: <names from the repo list>." With areas, show the names grouped by area. Recommend the child repo the person last named, or the home repo if none.
4. **On the home repo itself**: trim only the steering text above `## Repos` in `AGENTS.md`. Never change `## Repos`, `## Sources`, `## Tools`, or `## Environment`. They belong to `setup-home-repo`. For problems there, name `/setup-home-repo advise`. The home `AGENTS.md` follows `setup-home-repo`'s layout, so the skill's defaults do not apply to it: add no Commands, Parts, Decisions, or Docs section and no code standards file, and run no command check. Then do the shipped designs, below. A home repo that is not a git repo has no branch and no undo: write after the yes, and keep no copy.

## Running in a child repo

Work as in any repo. Do not copy text from the home repo's `AGENTS.md`. The agent reads both.

The line that points at the home repo belongs to `setup-home-repo`. It starts with `Home repo:`. Keep it, under the first sentence. When this skill was called from the home repo and the line is missing, do not write it: name `/setup-home-repo add <repo>`.

## Things in the wrong place

Advise reports these. Fixing one is a plan row, never a silent move.

- An ADR, glossary, or topic file in the home repo that is about one child repo: move it to that repo, on a branch there.
- A rule in a child repo's `AGENTS.md` that repeats the home repo's text: delete it from the child.
- A rule in the home repo's `AGENTS.md` that applies to only one child repo: move it to that repo.
