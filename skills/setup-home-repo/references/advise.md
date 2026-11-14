# Advise

`/setup-home-repo advise` audits the home repo and says what to fix. It reads. It never writes, never runs a tool against a service, and never opens a secret file. In a local-only home repo, read "tracked file" as any file in the folder.

## Steps

1. **Read the home repo**: `AGENTS.md`, the pointer files, each harness's config, the skills folder, the router's map.
2. **Walk the registry** over the home repo, every pointed-at repo that is on disk, and the user folder. Use the Check column in [components.md](components.md).
3. **Run the checks below.** Each finding is one row.
4. **Print the table**, worst first, then the summary line.

## The checks

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

For a suspected secret, name the file and the key. Never print the value.

### Steering

| Finding | Severity |
| --- | --- |
| `AGENTS.md` over about 200 lines | medium |
| A procedure in `AGENTS.md` that a skill already holds | medium |
| Child repo with no `AGENTS.md`, or with a `CLAUDE.md`. The Fix is `/setup-agents-md <repo>`. | medium |
| Child repo without the line that points at the home repo | low |
| Claude Code in use and a `CLAUDE.md` or `.claude/CLAUDE.md` in the home repo or a folder above it. Claude Code reads that file and skips every `AGENTS.md` below it. | high |
| The `## Repos` heading missing | high |

### The router

| Finding | Severity |
| --- | --- |
| No router skill | high |
| Map line whose item is gone | high |
| Item with no map line | medium |
| Flow step that names a skill that does not exist | high |
| Map line that disagrees with the skill's own description | medium |

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
| One repo pointer in total. A home repo adds little. | low |
| Every pointed-at repo shares one remote host and one owner, and nothing mixes public with private. A monorepo may fit. | low |

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

- One row per finding. The Fix cell is one concrete action.
- Sort by severity, then by kind.
- With no findings, print the clean count and stop.
- A leaked secret needs more than removal. Say the token must be rotated, since git history keeps it.

## Advice beyond findings

After the table, add at most three lines of advice that no check covers. Only what you saw evidence for:

- A source the agent keeps needing with no access method: suggest one.
- A task the steering file explains in prose each time: suggest a skill.
- A script pasted into several skills: suggest a tool.
- A rule the agent must never break, written as text: suggest a hook.

No evidence, no advice. Leave the lines out.
