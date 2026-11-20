# Where each kind lives, per harness

Paths from the home repo root, read from each harness's docs in November 2026. When one does not work, use the harness's current docs and tell the person this file is behind.

## Detect the harnesses in use

In use when its folder is in a chosen repo or the user folder, or the person says so. Write files only for harnesses confirmed in round one.

| Harness | Signs on disk |
| --- | --- |
| Claude Code | `.claude/`, `CLAUDE.md`, `.mcp.json`, `~/.claude/` |
| Cursor | `.cursor/`, `~/.cursor/` |
| Copilot | `.github/copilot-instructions.md`, `.github/instructions/`, `.github/skills/`, `.github/hooks/`, `~/.copilot/` |
| Codex | `.codex/`, `.agents/`, `~/.codex/` |

## Shared by all four

| Kind | Path | Note |
| --- | --- | --- |
| `steering`, `repo`, `source` | `AGENTS.md` | Claude Code reads it from 2.1.277, unless a `CLAUDE.md`, `.claude/CLAUDE.md`, or `CLAUDE.local.md` here or above hides it. No `CLAUDE.md` by default. On request, or when the setup step 3 version check fails, write a root `CLAUDE.md` whose only line is `@AGENTS.md`, never in `.claude/`. With clones inside the home folder, each child repo then needs the same file. |
| `tool` | `tools/` | Plain files. One line per tool in `AGENTS.md`. |
| `wiki` | `wiki/` | Plain markdown. One line in `AGENTS.md` says what is in it. |

## Skills

One real folder.

| Harnesses in use | Real folder | Extra |
| --- | --- | --- |
| Claude Code, with or without Cursor and Copilot | `.claude/skills/` | None. Cursor and Copilot read this folder too. |
| Any set without Claude Code | `.agents/skills/` | None. Cursor, Copilot, and Codex all read it. |
| Claude Code and Codex together | `.claude/skills/` | `.agents/skills` as a link to `.claude/skills`. Where links do not work, such as Windows without developer mode, copy the folder and let advise watch for drift. |

A skill only the person may start needs a flag per harness:

| Harness | How |
| --- | --- |
| Claude Code, Cursor | `disable-model-invocation: true` in the `SKILL.md` frontmatter |
| Codex | `agents/openai.yaml` in the skill folder, with `policy.allow_implicit_invocation: false` |
| Copilot | No setting found. Say so in the report. |

## The other kinds

| Kind | Claude Code | Cursor | Copilot | Codex |
| --- | --- | --- | --- | --- |
| `rule` | `.claude/rules/*.md` | `.cursor/rules/*.mdc` with `description`, `globs`, `alwaysApply` | `.github/instructions/*.instructions.md`, and `.github/copilot-instructions.md` for repo-wide text | None. Put the text in `AGENTS.md`, or a nested `AGENTS.md` in the folder it covers. |
| `agent` | `.claude/agents/*.md` | `.cursor/agents/*.md` | `.github/agents/*.md` | `[agents.<name>]` in `.codex/config.toml`, each with a `config_file` |
| `command` | `.claude/commands/*.md`. Prefer a skill. | `.cursor/commands/*.md`. Prefer a skill. | `.github/prompts/*.prompt.md` | None. Use a skill. |
| `hook` | `hooks` in `.claude/settings.json`, scripts in `.claude/hooks/` | `.cursor/hooks.json` with `"version": 1`, scripts in `.cursor/hooks/` | `.github/hooks/*.json` with `"version": 1`, fields `bash` and `powershell` | `[hooks]` in `.codex/config.toml`, with `features.hooks = true` |
| `setting` | `.claude/settings.json`. Personal overrides in `.claude/settings.local.json`, not tracked. | Mostly in the app, not in a file. Report it. | `.github/copilot/settings.json` for the command line client | `.codex/config.toml` |
| `mcp` | `.mcp.json`, key `mcpServers` | `.cursor/mcp.json`, key `mcpServers` | `.vscode/mcp.json`, key `servers`, for the editor. The cloud agent takes its servers from the repository settings on GitHub, not from a file. | `[mcp_servers.<id>]` in `.codex/config.toml` |
| `registration` | `enabledPlugins` and `extraKnownMarketplaces` in `.claude/settings.json` | In the app. Report it. | In the client. Report it. | In the client. Report it. |

Map a hook's event by what it does (before a tool, after an edit, at session start). No matching event: leave that harness out and report it. Codex loads a project `.codex/config.toml` only when trusted: say so when you write one.

## One item, several harnesses

An MCP server or hook keeps one script, and each harness config points at it in its own format: the top-level keys differ. Advise checks **parity** across the harnesses in use.

## Secrets in config

Never write the value. Name the variable.

| Harness | Form |
| --- | --- |
| Claude Code | `${NAME}` in `.mcp.json` |
| Cursor | `${env:NAME}` in `.cursor/mcp.json` |
| Copilot in the editor | `${input:name}` with an `inputs` entry, or `${env:NAME}` |
| Codex | `bearer_token_env_var = "NAME"`, or an `env` table that reads from the shell |

List each variable under `## Environment`: name and purpose.
