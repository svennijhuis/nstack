# Advise

`/setup-home-repo advise` audits the home repo. It never writes, runs a tool against a service, or opens a secret file. In a local-only home repo, "tracked file" means any file in the folder.

1. Read `AGENTS.md`, the pointer files, each harness's config, and the skills folder.
2. Walk the Check column of [components.md](components.md) over the home repo, every pointed-at repo on disk as checked out, and the user folder.
3. Run the checks below, one row per finding. Print them worst first, then by kind, then the summary line.

### Pointers

| Finding | Severity |
| --- | --- |
| Repo pointer whose path is missing and that names no remote | high |
| Repo on disk beside the others with no pointer | medium |
| Repo pointer with no commit in over a year | low |
| Two pointers to the same remote | medium |
| Source pointer whose access method is gone: the tool is off the path, the MCP server is not in the config | high |
| Source pointer that says `none yet` | medium |
| More than about 20 pointers in `AGENTS.md` | medium |

### Duplicates and drift

| Finding | Severity |
| --- | --- |
| Item in the home repo that also sits in a child repo, same content | medium |
| The same, with different content | high |
| Item in the home repo that also sits in the user folder | medium |
| Two skills with different names and near-identical descriptions | low |

### Harness parity

| Finding | Severity |
| --- | --- |
| Hook, MCP server, or rule present for one harness in use and missing for another | medium |
| Skills folder copied, not linked, and the copies differ | high |
| File for a harness nobody uses | low |
| User-only skill with the flag set for one harness and not another | medium |

### Hooks, MCP, settings

| Finding | Severity |
| --- | --- |
| Hook whose script is missing or not executable | high |
| Same hook registered twice | medium |
| MCP server whose command is not on the path | high |
| MCP server in both the project and the user config | medium |
| Something that looks like a literal token, key, or password in a tracked file | critical |
| Variable used in config and not listed under `## Environment` | medium |
| Permission rules that repeat or contradict | medium |
| Plugin enabled with no marketplace registered, or the reverse | medium |
| Personal preference in the shared settings file | low |

For a suspected secret, name the file and key, never the value.

### Steering

| Finding | Severity |
| --- | --- |
| `AGENTS.md` over about 200 lines | medium |
| A procedure in `AGENTS.md` that a skill already holds | medium |
| Child repo with no `AGENTS.md`, or a `CLAUDE.md` with its own text. Fix: `/setup-agents-md <repo>` when installed, otherwise the change by hand. | medium |
| Child repo with no `Home repo:` line | low |
| A `CLAUDE.md` or `.claude/CLAUDE.md` in the home repo with text of its own | high |
| A `.claude/CLAUDE.md` in the home repo whose only line is `@AGENTS.md` | high |
| Claude Code in use, `claude --version` older than 2.1.277 or no answer, and no root `CLAUDE.md` that imports `AGENTS.md` | high |
| Claude Code in use, a `CLAUDE.md` in the home repo or above, and a child repo below it with no `CLAUDE.md` that imports its `AGENTS.md` | high |
| The `## Repos` heading missing | high |

### Skills setup wrote

| Finding | Severity |
| --- | --- |
| A skill that says `Written by setup-home-repo`, such as an old router. Cleanup removes it and its `AGENTS.md` line. | medium |

### Worktrees, tools, wiki

| Finding | Severity |
| --- | --- |
| Worktree whose branch is merged | low |
| Worktree with no commit in over a month | low |
| Tool named in `AGENTS.md` that is missing or not executable | high |
| Wiki page nothing links to | low |
| Link to a page that is gone | medium |

### Fit

| Finding | Severity |
| --- | --- |
| One repo pointer in total | low |
| Every repo shares one host and owner, none public beside private: a monorepo may fit | low |

## Output

```text
Sev       Kind    Item                Finding                                   Fix
critical  mcp     github              literal token in .mcp.json                replace with ${GITHUB_TOKEN}, rotate the token
high      skill   review-pr           differs from storefront/.claude/skills    choose one, remove the other
high      repo    admin-dashboard     path missing, no remote                   add the remote or drop the pointer
medium    hook    block-force-push    in Claude Code, missing in Cursor         register in .cursor/hooks.json
low       repo    legacy-importer     no commit since 2024-11-02                drop the pointer or keep on purpose

5 findings: 1 critical, 2 high, 1 medium, 1 low. 37 items clean.
Fix them with /setup-home-repo cleanup.
```

The Fix cell is one concrete action. A leaked secret must be rotated: git history keeps it. With no findings, print the clean count and stop.

After the table, at most three lines of advice no check covers, each with evidence: an access method for a source the agent keeps needing, a skill for a task the steering file explains in prose, a tool for a script pasted into several skills, a hook for a rule written as text.
