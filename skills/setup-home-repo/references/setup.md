# Setup

Steps 1 to 5 only read. Step 6 is the first write, after a yes. Use subagents for the wide searches in steps 1 to 3 when the harness has them; each returns a table, not file contents.

## 1. Explore the repos

Unless you know it, ask which folders hold the repos, the parent of the working directory recommended. A working directory that is not a git repo and holds child repos is the home folder: it becomes the home repo, its clones stay where they are, and you skip this question and the location in question 2.

Find every git repo there, skipping dependency and build folders. Record per repo:

| Field | From |
| --- | --- |
| Name | The folder name |
| Path | Absolute, shown from the home folder |
| Remote | `git remote get-url origin`. None is allowed. |
| Host | github.com, dev.azure.com, gitlab.com, or other |
| Last commit | `git log -1 --format=%cs` |
| What it is | A few words from its readme or steering file |

Done when every repo found is a row.

## 2. Explore the components

Walk [components.md](components.md) over every repo and each harness's user folder. Done when every agent-related item is a row with a kind and a bucket. What fits no kind is `other`.

## 3. Explore the sources and the harnesses

- **Remotes.** github.com means GitHub issues, pull requests, maybe a wiki. dev.azure.com means boards, pipelines, maybe a wiki. The same for GitLab and others.
- **MCP config.** Name what each configured server reaches.
- **Tools.** `command -v` for `gh`, `az`, `glab`, `jira`, `linear`, `kubectl`, `aws`, `gcloud`. Never run them against a service.
- **Steering files.** Wiki addresses, boards, and channels already named there.

Find the harnesses by [harnesses.md](harnesses.md). With Claude Code, run `claude --version` and note the answer for question 5.

Done when each source has a name, a kind, a location, and an access method or `none yet`.

## 4. Ask what is left

Numbered rounds, each question with a one-word recommended answer. Skip what exploring answered.

Round one, the shape:

1. Which repos go in? Recommend all with a commit in the last year, and list the rest.
2. Where does the home repo live, and its name? Recommend a new private repo beside the others, named `home`.
3. One person or a team? This decides what stays in the user folder.
4. Git or local only? Skip when the folder is already a git repo. Recommend git, also for one person: the commit is the undo. A team needs git. On local only, say once there is no undo.
5. Which harnesses? Recommend the detected ones. With Claude Code below 2.1.277 or no version, also ask to write a one-line `CLAUDE.md`, recommended yes, and name the other cases: Bedrock or telemetry off on 2.1.277 to 2.1.280, or project instructions set to `CLAUDE.md` only.
6. The local path convention for repos? Recommend the one most repos follow.

Round two, the gaps:

7. Sources exploring missed: wikis, trackers, pipelines, chat, dashboards. For each, the location and how to reach it.
8. Each drift pair: which copy wins. Each `shared` item in one repo only: `shared` or `repo-specific`.
9. Each `other` item: keep, as what, or leave.
10. Past about 20 repos: the areas, and whether they follow teams. Recommend team areas when the person names teams.
11. Which child repos get `setup-agents-md`? Recommend all that go in. Skip when it is not installed.

A monorepo would do, or there is one repo: say so now and ask whether to go on. Done when no plan row would hold a question mark.

## 5. Show the plan

**The plan table**, one row per item, with the final path of every repo and item:

```text
Item              Kind    From                               To                        Bucket
review-pr         skill   storefront/.claude/skills (+2)     .claude/skills/review-pr  duplicate
block-force-push  hook    payments/.claude/settings.json     .claude/settings.json     shared
github            mcp     ~/.claude.json                     .mcp.json                 shared
migrate-db        skill   payments/.claude/skills            stays                     repo-specific
engineering wiki  source  dev.azure.com/acme/platform        AGENTS.md Sources         shared
```

Group long tables by bucket, counts first. Show `repo-specific` and `installed` rows too.

**The drafted `AGENTS.md`**, by [layout.md](layout.md). Then, per child repo: what it loses, the branch it will sit on, and its steering state (none, `CLAUDE.md`, or `AGENTS.md`).

The person may change any row. Apply nothing until they approve.

## 6. Apply

In this order, so a stop halfway breaks nothing.

1. **Create the home repo.** `git init`, or only the folder when local only. An existing git repo is used as is.
2. **Write `AGENTS.md`.** A `CLAUDE.md` only by the steering row in [harnesses.md](harnesses.md). A home `CLAUDE.md` or `.claude/CLAUDE.md` with its own text: move its lines into `AGENTS.md` as plan rows, then delete it. A kept `CLAUDE.md` is the one-line file at the root.
3. **Copy the `shared` and `duplicate` items in**, also from user folders. For a duplicate, the winning copy once.
4. **Merge the config** per harness, in its format: hooks, settings, MCP servers, registrations. Replace each literal secret with a variable listed under `## Environment`, and tell the person which to set, without the values.
5. **Write `.gitignore`**: local settings files, `.worktrees/`, secret files, child repo clones. Not when local only.
6. **Commit** once in the home repo, the plan summary as message. Not when local only.
7. **Clean each child repo** on a new branch `home-repo/move-agent-config`, adding `-2`, `-3` when taken: remove the moved copies, keep `repo-specific` items, and add the `Home repo:` line by [layout.md](layout.md). With no steering file, that line is the whole `AGENTS.md`. Change nothing else there. Commit, stay on the branch. Skip and report a repo with uncommitted changes to tracked files outside `docs/design/`; an open design there stays uncommitted.
8. **The user folder last.** Name each removal and get its own yes. On a no, say that an item in both places registers twice.

On a failure, stop and report what was done and what was not. Roll nothing back.

## 7. Hand over the child repos

For each repo picked in question 11, call `setup-agents-md <repo>`. It shows its own plan, waits for its own yes, and commits on the step 6 branch. When it is not installed, say so once.

## 8. Report and stop

```text
Home repo: ~/repos/acme/home   Harnesses: Claude Code, Cursor
Moved 14, kept in place 6, left installed 3, skipped 1.

Skipped
  payments   uncommitted changes, not touched

Branches to review and push
  storefront   home-repo/move-agent-config
  admin        home-repo/move-agent-config

Steering files left as they are
  admin      has a CLAUDE.md. Run /setup-agents-md admin

Set these variables: GITHUB_TOKEN, AZURE_DEVOPS_PAT
No place in Copilot for: user-only skills

Start every session in ~/repos/acme/home. Keep it current with /setup-home-repo update.
```

## Update

`/setup-home-repo update` runs only inside a home repo; outside one, name setup.

1. Do steps 1 to 3 again and compare.
2. Plan only what changed: a repo with no pointer, a pointer whose repo moved or is gone, a new item, an item that drifted from its home copy, a new source or harness. Count the rows that are still true.
3. Ask only about those rows. A new repo gets question 11. Never ask question 4 again.
4. Show the plan by step 5, apply by step 6, hand over by step 7, report by step 8.

Change only the `AGENTS.md` lines that differ, and keep what the person wrote. An item exploring did not find again is a row to ask about, never a silent removal. Nothing changed: say so in one line.
