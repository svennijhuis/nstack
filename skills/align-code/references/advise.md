# Check and advise

`check` stops a bad copy before merge. `advise` finds the ones that got through. Both only read. Never write, never run a command that changes anything, never open a secret file.

## The standards

Read, in order:

1. ADRs in `docs/adr/` titled `Code standard: <area>`.
2. Area sections of folders under `docs/align/` with status `aligned` or `applying`. No other status. Two runs set the same area: `aligned` wins over `applying`, then the newest `Created`.
3. `docs/agents/code-standards.md`.
4. Frozen and exception markers in the code.

None found: name `/align-code new <name>` and stop.

## Check

`/align-code check`: `git diff <default>...HEAD`. The default branch is `origin/HEAD`, else `main`, else `master`. Skip a standards source that does not exist.

A finding is an added line that:

- uses a rejected variant
- copies the shape of a marked symbol
- adds a comment not on the keep list of [comments.md](comments.md). Not sure? Flag it, and say why.
- adds a suppression on a rule that catches bugs
- adds a `bad` variant: a `code-review` smell or a `codebase-design` break

```text
File    Line  Area    Finding                        Fix
<path>  <n>   <area>  <what, and the rule it breaks>  <one concrete action>

<n> findings. Fix them before the pull request.
```

None: say the branch follows the standards.

## Advise

`/align-code advise`: the scope of the last `aligned` run, or the whole repo.

1. Run the survey of every area with a standard, read only. Subagents write nothing and return only the drift rows, each with its verdict, `Files`, and `Last 90 days`.
2. Every variant that is not the standard and has no marker is drift. So is every new `bad` variant.
3. Find the source: `git log --diff-filter=A -S<key text>` over its files. The oldest copy is where the agents copy from.

```text
Sev                  Area    Files  Finding                           Copied from  Fix
<high | medium | low>  <area>  <n>    <what, and <n> in the last 90 days>  <path>       <one concrete action>

<n> findings: <n> high, <n> medium, <n> low.
```

- `high`: `bad spreading`: `bad`, and the survey's `Last 90 days` is above 0.
- `medium`: `bad`.
- `low`: only inconsistent.

One concrete action per Fix. At most three lines of advice after the table, only with evidence.
