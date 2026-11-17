# align-code

Make every part of the code do the same thing the same way, so the code is worth copying. Say "align the code" or type `/align-code`.

## Why

Agents copy the code near the change. A bad pattern copied once is two, then four. This skill finds every place the code does one thing in more than one way, lets you pick the way, reports what does not match, and rewrites it one standard at a time. It aligns code to standards and principles. Nothing more.

## How a run works

It follows wayfinder: a map, a list of gaps, one decision per session.

1. `/align-code new <name>`: agree the scope, discover the areas from the code (every seed area is covered or marked n/a), write the list into `align.md` so you can add or drop, and start one survey subagent per area on that list.
2. `/align-code <name>`: one session, one gap. Each survey counts every variant and judges it against a cited source. You choose the standard.
3. `/align-code <name> report`: the report gate checks every area. On pass, the report lists each standard, its exemplar, and the files that do not match.
4. `/align-code <name> apply`: rewrites one standard per session on a local branch `align/<name>`. You approve the file list first. If the repo has a linter, the rule goes into its config first, the linter fixes what it can, and the rest is fixed by hand. Build and test must pass, and lint too when the repo has one. Never pushes.

The majority does not win. Every variant is judged, even a variant used everywhere, and questions come in order of danger: bad and common first, then bad, then only inconsistent.

## Output

`docs/align/<yyyy-mm-dd>-<name>/`: `align.md` (the report), `gaps.md`, `log.md`, `survey/`. Code changes only in `apply`, on a local branch.

## With the other nstack skills

Uses `grilling`, `domain-modeling`, `research`, `codebase-design`, `code-review`, `comment-root-cause`, and `writing-for-agents`. `/setup-nstack-skills` installs them.
