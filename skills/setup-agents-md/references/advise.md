# Advise

`/setup-agents-md advise` audits the steering file and the docs around it. It never writes, runs a project command, clones, or opens a secret file. In a home repo it asks which repo first, by [home-repo.md](home-repo.md). With `all` it audits every repo in the repo list and prints one table, repo first.

1. Do Create and Update steps 1 to 4, drafting nothing. Files `setup-matt-pocock-skills` owns are never a finding.
2. Run the checks below, one row per finding.
3. Print the table worst first, then the summary line.

## Root file

| Finding | Severity |
| --- | --- |
| No `AGENTS.md` | high |
| A `CLAUDE.md` or `.claude/CLAUDE.md` with text of its own | high |
| A `CLAUDE.md` above the repo, or a `CLAUDE.local.md` in it, and no repo `CLAUDE.md` that imports `AGENTS.md` | high |
| A `.claude/CLAUDE.md` whose only line is `@AGENTS.md` | high |
| Claude Code in use, `claude --version` below 2.1.277 or no answer, and no `CLAUDE.md` that imports `AGENTS.md` | high |
| An `AGENTS.md` in a part's folder | medium |
| A start, build, or test command a script, manifest, or pipeline defines, with no line | high |
| A part with no commands, a pipeline with no line, or a line for one that is gone | medium |
| A deploy or apply command with no word on how it runs | medium |
| Two instructions that contradict | high |
| A command nothing defines and not marked `Not in the code.` | high |
| A path that does not exist, other than the Decisions section's `docs/adr/` | high |
| Over about 60 lines, not counting Parts | low, medium past about 100 |
| A folder tree or a list of file paths | medium |
| Rules for one area only, outside that part's block | medium |
| A procedure with steps that could be a skill | medium |
| A style rule a linter or formatter could check | low |
| Obvious advice, vague rules, or ALL-CAPS commands | low |
| No Decisions section | medium |
| No Changes section | low |
| A `Designs in progress` line and no open design | low |

## Docs

| Finding | Severity |
| --- | --- |
| A doc that explains how the code works | medium |
| A spec, PRD, or plan for a shipped feature | medium |
| A `tech-design` folder `abandoned`, or `committed` and shipped by the person's word | medium |
| A doc or standards line a type, test, or lint rule could enforce. The Fix names which. | low |
| A topic file nothing points at | low |
| A pasted snippet that differs from the code now | medium |
| Auto-generated steering text left as written | low |

## Decisions

| Finding | Severity |
| --- | --- |
| A commit that reverts one that added or changed an ADR, with no revert ADR | high |
| An ADR `Superseded by` or `Reverted by` a file that does not exist | high |
| A merged ADR whose `Change` cannot be found or still says `this pull request` | low |
| An ADR body edited after merge, by `git log -p` | medium |
| A merged change in the last 30 days that adds a dependency with no ADR | low |
| Decision text in a spec, plan, or comment with no ADR | low |

Find reverts with `git log --grep="This reverts commit"`, then check whether each reverted commit touched `docs/adr/` or `DECISIONS.md`. In a shallow clone, say the check covers only the history on disk. With no git, skip the history checks and say so.

## Home repo

Only in a home repo setup. On the home repo's own `AGENTS.md`, count only the lines above `## Repos`, and skip the checks for commands, parts and pipelines, and the Decisions section.

| Finding | Severity |
| --- | --- |
| An ADR, glossary, or topic file in the home repo about one child repo | medium |
| A child repo `AGENTS.md` that repeats the home repo's text | low |
| A rule in the home `AGENTS.md` for one child repo only | medium |
| A `tech-design` folder in the home repo about one child repo | low |
| An abandoned or shipped design in the home repo whose decisions are not ADRs in the child repos | medium |

## Output

```text
Sev     Kind      Item                       Finding                                         Fix
high    decision  docs/adr/2026-10-02-redis  commit 4f2a1c9 reverted it, no revert ADR       add a revert ADR, set status to Reverted by
high    root      AGENTS.md:14               no script defines the test command              use the one the pipeline runs, or delete the line
medium  root      AGENTS.md:20-48            folder tree                                     delete it
low     root      AGENTS.md                  84 lines                                        move testing rules to docs/agents/testing.md

4 findings: 2 high, 1 medium, 1 low.
Fix them with /setup-agents-md.
```

The Fix cell is one concrete action. With no findings, say the steering file is clean and stop. After the table, at most three lines of advice no check covers, each with its evidence.
