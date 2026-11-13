# Advise

`/setup-agents-md advise` audits the steering file and the docs around it, and says what to fix. It reads. It never writes and never opens a secret file. In a home repo it asks which repo first, as in [home-repo.md](home-repo.md).

## Steps

1. Do Create and Update steps 1 to 4 from the skill, without drafting anything.
2. Run the checks below. Each finding is one row.
3. Print the table, worst first, then the summary line.

## The checks

### Root file

| Finding | Severity |
| --- | --- |
| No `AGENTS.md` | high |
| A `CLAUDE.md` or `.claude/CLAUDE.md` with its own text beside `AGENTS.md`. Claude Code reads it and ignores `AGENTS.md`. | high |
| A `CLAUDE.md` in a folder above the repo | high |
| A `CLAUDE.local.md` in the repo. It hides `AGENTS.md` from Claude for that person. | medium |
| No start, build, or test command | high |
| A part with no commands, or a pipeline with no line | medium |
| A deploy or apply command with no word on how it runs | medium |
| Two instructions that contradict | high |
| A command that fails or does not exist | high |
| A path that does not exist | high |
| Root file over about 60 lines | low |
| Root file over about 100 lines | medium |
| A folder tree or a list of file paths | medium |
| Rules for one area only, in the root file | medium |
| A procedure with steps that could be a skill | medium |
| A style rule a linter or formatter could check | low |
| Obvious advice, vague rules, or ALL-CAPS commands | low |
| No Decisions section | medium |
| No code standards file, and no line pointing at one | low |
| A code standard that a linter or the type checker could enforce | low |

### Docs

| Finding | Severity |
| --- | --- |
| A doc that explains how the code works | medium |
| A spec, PRD, or plan for a feature that has shipped | medium |
| A `tech-design` folder whose status is `committed` or `abandoned` and whose feature has shipped or stopped | medium |
| A doc that explains something a type, a test, or a lint rule could enforce. The Fix names which one. | low |
| A topic file nothing points at | low |
| A pasted code snippet that differs from the code now | medium |
| Auto-generated steering text left as written | low |

### Decisions

| Finding | Severity |
| --- | --- |
| A commit that reverts a commit which added or changed an ADR, with no ADR marking the revert | high |
| An ADR whose status says `Superseded by` or `Reverted by` a file that does not exist | high |
| An ADR whose `Change` names a commit or pull request that cannot be found | low |
| An ADR body edited after merge, seen in `git log -p` | medium |
| A merged change that adds a dependency with no ADR in the same change, last 30 days | low |
| Decision text in a spec, plan, or comment with no ADR | low |

To find reverts, read `git log --grep="This reverts commit"` and, for each reverted commit, check whether it touched `docs/adr/` or `DECISIONS.md`. In a shallow clone, say the check covers only the history on disk.

### Home repo

Only when the target is in a home repo setup.

| Finding | Severity |
| --- | --- |
| An ADR, glossary, or topic file in the home repo about one child repo | medium |
| A child repo `AGENTS.md` that repeats the home repo's text | low |
| A rule in the home repo `AGENTS.md` for only one child repo | medium |
| A child repo `AGENTS.md` without the line that points at the home repo | low |
| A `tech-design` folder in the home repo about one child repo. It belongs in that repo. | low |
| A shipped or abandoned `tech-design` folder in the home repo whose decisions are not ADRs in the child repos | medium |

## Output

```text
Sev     Kind      Item                       Finding                                         Fix
high    decision  docs/adr/2026-10-02-redis  commit 4f2a1c9 reverted it, no revert ADR       add a revert ADR, set status to Reverted by
high    root      AGENTS.md:14               test command does not exist                     use the one the pipeline runs, or delete the line
medium  root      AGENTS.md:20-48            folder tree                                     delete it
medium  docs      docs/specs/checkout.md     feature shipped in #212                         move the why to an ADR, delete the spec
low     root      AGENTS.md                  84 lines                                        move testing rules to docs/agents/testing.md

5 findings: 2 high, 2 medium, 1 low.
Fix them with /setup-agents-md.
```

- The Fix cell is one concrete action.
- With no findings, say the steering file is clean and stop.
- After the table, at most three lines of advice no check covers, only with evidence. Example: decisions appear in pull request descriptions but never as ADRs, so suggest a line in the pull request template.
