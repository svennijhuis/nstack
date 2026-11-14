# Setup

Setup builds a home repo from what the person already has. Steps 1 to 5 only read. Step 6 is the first write, and it waits for approval.

Use subagents for the wide searches in steps 1 to 3 when the harness has them. Each one returns a table, not file contents.

## 1. Explore the repos

Ask one thing first if you do not know it: which folders hold the person's repos. Recommend the parent of the working directory.

If the working directory is not a git repo and holds child repos, it is the home folder and holds the repos. The home repo is that folder itself. Skip the question above and the location in round one question 2. Its clones stay where they are.

Find every git repo under those folders. Skip dependency and build folders. For each, record:

| Field | From |
| --- | --- |
| Name | The folder name |
| Path | Absolute, then shortened to start at the home folder |
| Remote | `git remote get-url origin`. None is allowed. |
| Host | github.com, dev.azure.com, gitlab.com, or other, read from the remote |
| Last commit | `git log -1 --format=%cs` |
| What it is | The first lines of its readme or steering file, as a few words |

Done when every repo found is a row.

## 2. Explore the components

Walk [components.md](components.md) over every repo from step 1 and over the user folder of each harness. Record each item and give it a bucket by the rules in that file.

Done when every item found is a row with a kind and a bucket, and nothing agent-related is left unlisted. What fits no kind is `other`.

## 3. Explore the sources and the harnesses

Find sources without asking:

- **Remotes.** A github.com remote means GitHub issues, pull requests, and maybe a wiki. A dev.azure.com remote means Azure DevOps boards, pipelines, and maybe a wiki. The same holds for GitLab and others.
- **MCP config.** Each server already configured is a way to reach something. Name what it reaches.
- **Tools on the path.** Check which of `gh`, `az`, `glab`, `jira`, `linear`, `kubectl`, `aws`, `gcloud` exist with `command -v`. Do not run them against a service.
- **Steering files.** Links and names already written there: a wiki address, a board, a channel.

Find the harnesses by the signs in [harnesses.md](harnesses.md).

When Claude Code is one of them, run `claude --version`. It only reads. Note the version, or that there was no answer. Question 5 uses it.

Done when each source has a name, a kind, a location, and an access method or `none yet`.

## 4. Ask what is left

Ask in numbered rounds. One round is a short list of questions, each with a recommended answer the person can accept with one word. Skip a question exploring already answered. Most setups need two rounds.

Round one, the shape:

1. Which repos go in? Recommend all with a commit in the last year. List the rest as left out.
2. Where does the home repo live, and what is it called? Skip the location when step 1 found the home folder. Recommend a new private repo beside the others, named `home`.
3. Is it for one person or a team? This decides what stays in the user folder.
4. Is the home repo a git repo, or local only? Skip this when the folder already is a git repo. Recommend git, also for one person: the commit is the undo, and nothing is pushed. A team needs git. When the person picks local only, say once that it has no undo: a changed or removed file is gone.
5. Which harnesses? Recommend the ones detected. When Claude Code is one and its version is older than 2.1.277 or was not found, ask too: write a one-line `CLAUDE.md`? Recommend yes. Without it that Claude Code reads no `AGENTS.md`. Name the other cases in the question: Bedrock or telemetry off on a version from 2.1.277 to 2.1.280, or project instructions set to `CLAUDE.md` only on any version.
6. What is the local path convention for repos? Recommend the one most repos already follow.

Round two, the gaps:

7. Sources that exploring missed. Ask openly once: wikis, issue trackers, pipelines, chat, dashboards, anything else the agent should reach. For each, the location and how to reach it.
8. Each drift pair: which copy wins. Each skill with 1 or 2 mentions, see [components.md](components.md): `shared` or `repo-specific`.
9. Each `other` item: keep, and as what, or leave.
10. Past about 20 repos: the areas to group them in, and whether the areas follow teams. Recommend team areas when the person names teams.
11. Which child repos get `setup-agents-md` after setup? Recommend all that go in. Leave this out when that skill is not installed.

If a monorepo would do, or there is only one repo, say so now and ask whether to go on.

Done when no row in the plan would hold a question mark.

## 5. Show the plan

Show two things and wait.

**The plan table.** One row per item.

```text
Item              Kind    From                               To                        Bucket
review-pr         skill   storefront/.claude/skills (+2)     .claude/skills/review-pr  duplicate
block-force-push  hook    payments/.claude/settings.json     .claude/settings.json     shared
github            mcp     ~/.claude.json                     .mcp.json                 shared
migrate-db        skill   payments/.claude/skills            stays                     repo-specific
engineering wiki  source  dev.azure.com/acme/platform        AGENTS.md Sources         shared
```

Settle the layout and show the final path of every repo and item in the table, so nothing moves after the commit. Group long tables by bucket and show the counts first. Show the `repo-specific` and `installed` rows too, so the person sees nothing was missed.

**The drafted `AGENTS.md`**, by [layout.md](layout.md).

Then list, per child repo, what it will lose, the branch name that change will sit on, and its steering state: none, `CLAUDE.md`, or `AGENTS.md`.

The person may change any row. Apply nothing until they approve.

## 6. Apply

In this order, so a stop halfway leaves nothing broken.

1. **Create the home repo.** `git init` at the chosen path, or only the folder when it is local only. If the folder already is a git repo, use it.
2. **Write `AGENTS.md`.** Write a `CLAUDE.md` only by the steering row in [harnesses.md](harnesses.md). If the home folder already has a `CLAUDE.md` or a `.claude/CLAUDE.md` with text of its own, move its lines into `AGENTS.md` as plan rows. Then delete it. When the person keeps a `CLAUDE.md`, the one-line file goes at the root, never in `.claude/`.
3. **Copy the `shared` and `duplicate` items in**, also when the only copy is in a user folder. A skill folder moves whole. For a duplicate, copy the winning one once.
4. **Merge the config.** Hooks, settings, MCP servers, and registrations from every source into one file per harness, in that harness's format. Replace each literal secret with a variable and list the variable under `## Environment`. Tell the person which values to set. Do not print the values.
5. **Write `.gitignore`**: local settings files, `.worktrees/`, secret files, child repo clones. Skip this when local only.
6. **Commit in the home repo.** One commit, the plan summary as its message. Skip this when local only.
7. **Clean each child repo.** On a new local branch named `home-repo/move-agent-config`, with `-2` added when that name is taken, remove the copies that moved. Leave `repo-specific` items. Add the line that points home, by [layout.md](layout.md), to the repo's steering file. If the repo has no steering file, that line is its whole `AGENTS.md`. Change nothing else in that file. Commit, and leave the repo on that branch. Do not push. Do not touch a repo with uncommitted changes to tracked files, other than under `docs/design/`; report it instead. An open design there is `tech-design`'s work in progress: leave it uncommitted.
8. **Leave the user folder for last and ask again.** Removing an item there changes every session the person runs. Name each one and get a yes. On a no, say that an item now in both the home repo and the user folder registers twice.

If a step fails, stop. Report what was done and what was not. Do not roll back what the person can see and fix.

## 7. Hand over the child repos

What a child repo's steering file says belongs to `setup-agents-md`. For each repo picked in question 11, call `setup-agents-md <repo>`. It shows its own plan for that repo, waits for its own yes, and commits on the branch step 6 made, so each repo has one branch to review.

When that skill is not installed, say so once. The steering files stay as they are.

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

Done when every plan row has an outcome.

## Update

`/setup-home-repo update` keeps a home repo current. It runs only inside a home repo. Outside one, say so and name setup.

1. Do steps 1 to 3 again and compare with what is there.
2. Build the plan table with only what changed: a new repo with no pointer, a pointer whose repo is gone or moved, a new item in a child repo or the user folder, an item that drifted from its copy in the home repo, a new source, a new harness. Rows that are already true are counted, not listed.
3. Ask only about those rows. A new repo gets question 11 too. Never ask question 4 again.
4. Show the plan and wait, by step 5.
5. Apply in the order of step 6, then hand over by step 7 and report by step 8.

Never rewrite `AGENTS.md` whole. Change the lines that differ, and keep what the person wrote by hand. Never remove an item only because exploring did not find it again. Show it as a row and ask.

When nothing changed, say so in one line and stop.
