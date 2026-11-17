# nstack

Agent skills as Markdown: no code, no build. Each skill is `skills/<name>/SKILL.md` plus `references/`. Its README for people is `docs/skills/<name>/README.md`.

## Rules

- Change a skill's behavior in its `SKILL.md` or `references/`. Keep the README in `docs/skills/` and the table in the root `README.md` true to it.
- Skills call each other by exact name and work alone when the others are missing.
- Never push. Commit on a local branch.
