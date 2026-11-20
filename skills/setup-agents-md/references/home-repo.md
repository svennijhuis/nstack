# Home repo or child repo

Skip this file when there is no home repo. A home repo, from `setup-home-repo`, is where the agent starts. A child repo is one it points at under `## Repos`.

| Thing | Home repo | Child repo |
| --- | --- | --- |
| This skill | In the skills folder | No copy |
| `AGENTS.md` | How to work across repos, and pointers | What is true only for that repo |
| ADRs, glossary, topic files | Only about the home repo itself | Everything about that repo |

A decision that spans repos: the full ADR goes in the repo that owns the change, and each other repo it touches gets a short ADR with the decision in one sentence and a link.

## Designs

| The design touches | Start `tech-design` in | It lives in |
| --- | --- | --- |
| One repo | That repo | That repo's `docs/design/` |
| Several repos | The home repo, or a repo the person picks | The home `docs/design/`, while open |

The home repo may hold open designs. It never holds a shipped design or an ADR about a child repo.

**A shipped design in the home repo.** A run on the home repo itself, or with `all`, handles each home design that is `abandoned`, or `committed` and shipped by the person's word:

1. Ask which repos it changed and which owns the change, the repos its text names recommended. For `abandoned`, ask which repo would have owned it.
2. In each, write the ADRs by the cross-repo rule, as that repo's own plan, branch, and yes. On a run on the home repo itself, that plan holds only those ADRs and the design's terms for the owning repo's glossary. It sorts nothing else and runs no command.
3. Only when all those ADRs are committed, offer to delete the folder as a home repo plan row. A repo that said no or was skipped keeps the folder: report it.
4. A local-only home repo has no git: say in the row that the delete cannot be undone.

## Running in a home repo

**The repo list** is the pointer lines under `## Repos`. Past about 20 repos those are area lines naming `repos/<area>.md` files: read each, their pointer lines are the list. An area is never a repo.

1. **`<repo name>`:** find its pointer. Its path is missing: ask before you clone from the pointer's remote. Advise reports it and stops. Then Create or Update that repo.
2. **`all`:** step 1 for every repo, each with its own plan, yes, and branch. A no skips only that repo. Last, a home repo plan that holds only its shipped designs.
3. **Nothing typed:** ask "Which repo? The home repo itself, or one of: <names>", grouped by area when there are areas. Recommend the repo last named, or the home repo.
4. **The home repo itself:** trim only the text above `## Repos`. Never change `## Repos`, `## Sources`, `## Tools`, or `## Environment`: name `/setup-home-repo advise` for those. Add no Commands, Parts, Decisions, Changes, or Docs section and no code standards file, and run no command check.

## Running in a child repo

Work as in any repo. Copy nothing from the home `AGENTS.md`. Keep the line that starts `Home repo:` under the first sentence. It belongs to `setup-home-repo`: when it is missing, name `/setup-home-repo add <repo>` and do not write it.

## Things in the wrong place

Advise reports these. Each fix is a plan row.

- An ADR, glossary, or topic file in the home repo about one child repo: move it there, on a branch.
- A child `AGENTS.md` rule that repeats the home repo: delete it from the child.
- A home `AGENTS.md` rule for one child repo: move it to that repo.
