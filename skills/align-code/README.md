# align-code

Make every part of the code do the same thing the same way, so the code is worth copying. Say "align the code" or type `/align-code`.

## Why

Agents copy the code near the change. A bad pattern copied once is two, then four. This skill finds every place the code does one thing in more than one way, lets you pick the way, and reports what does not match. It aligns standards and principles. It never changes code.

## How a run works

It follows wayfinder: a map, a list of gaps, one decision per session.

1. `/align-code new <name>`: agree the scope, sweep 17 areas (naming, errors, async, data access, comments, tests, and more), and start one survey subagent per area.
2. `/align-code <name>`: one session, one gap. Each survey counts every variant and judges it against a cited source. You choose the standard.
3. `/align-code <name> report`: the report gate checks every area. On pass, the report lists each standard, its exemplar, and the files that do not match.

The majority does not win. Every variant is judged, even a variant used everywhere, and questions come in order of danger: bad and spreading first, then bad and common, then bad, then only inconsistent.

## Output

`docs/align/<yyyy-mm-dd>-<name>/`: `align.md` (the report), `gaps.md`, `log.md`, `survey/`. Nothing else is written. You or an agent rewrite the code as normal work.

## With the other nstack skills

Uses `grilling`, `domain-modeling`, `research`, `codebase-design`, `code-review`, and `writing-for-agents`. `/setup-nstack-skills` installs them.
