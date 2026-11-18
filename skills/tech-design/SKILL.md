---
name: tech-design
description: Use when the user wants to write, continue, review, or finish a technical design or design doc for a feature, API, integration, or data change.
---

A technical design developers can build is too big for one session, and most of what it needs is not known yet. This skill charts that design as a shared map at `docs/design/<yyyy-mm-dd>-<name>/`, finds every gap, claims one gap per session, and closes any other `open` or `waiting-on-input` gap whose outcome that answer states in full, until a developer or an agent can build from the design without guessing.

Name the destination first. The destination is that design. It fixes the scope of every gap.

## Three rules that outrank the rest

**An unknown that changes what gets built or its risk is a gap. Never write that unknown as an assumption.** When the design needs a fact or a decision and no source gives it, add a row to `gaps.md`. Do not fill it with a default, a guess, or wording that reads the same under two answers.

**Open a gap only when the answer changes what gets built or its risk.** Behaviour, contract, data, security, cost, or reversibility. This qualifies the rule above. The outside-system rule still opens one gap per empty contract field. Naming is not a gap: follow the convention named in `docs/align/` or `AGENTS.md` when there is one, otherwise the convention the code already uses. When the design needs a new term and neither source names it, ask the human once. Hold that meaning with the chart answers and write it to `glossary.md` in step 5, one line per term. A choice outside the list above is not a gap, and it is not an assumption: hold it the same way, then write it in the section that would have held the answer and add a Decisions row: decision, choice, why. The human overrides that line by replacing it in a later session. Do not use this to keep a vague requirement: ready-gate check 11 still fails it. Size sets depth, see [sizes.md](references/sizes.md). It never changes this bar.

**An outside system opens its gaps at once.** The moment a system, source, or vendor outside this codebase is named, add its row to Dependencies and one gap per empty field: owner, access, credentials, environments, contract, limits, change notice, proof. See [dependency-contract.md](references/dependency-contract.md). How to connect and how to authenticate are never left for the builder to find out.

## Plan, don't do

Each gap resolves a decision. The design is done when every gap is closed and a developer can build. Builders start after the design is done. `state.md` Notes may say this effort also does the work. Otherwise stop at the decision.

A length request limits a summary only, see [sizes.md](references/sizes.md). It never skips gaps, research, dependency rows, or the log, and never lowers the size.

## Refer by name

A gap's name is its question. Use the question when you talk to the human and in Decisions. The id rides along with the question in `gaps.md` and `log.md`. It never stands in for it, and it never appears in `design.md`.

## The map

Every design has the same folder, the same files, and the same 15 sections in the same order. See [structure.md](references/structure.md) for all of it. Size and types change depth, never structure. See [sizes.md](references/sizes.md).

`design.md` is the spec. It opens with the Summary, so the business reader gets the point first. Its header carries only the owner and approvers. `state.md` carries the status, size, types, dates, destination, and notes. `gaps.md` holds the gaps. Each closed gap is one row under Decisions. The answer stays on the row, and the result is written into the section its category names.

The status words are `draft`, `discussion`, `ready`, `committed`, and `abandoned`. `draft` is the new folder. `discussion` means gaps are still open. `ready` means the gate passed. `committed` means builders follow this design. `abandoned` means the work stopped.

**`design.md` stands alone.** A business reader with no repo access must be able to read it. It holds flows, decisions, and technical decisions. It has no gap ids, no links or paths to local files, no `input/` or `research/` references, and no process words such as gap, session, or chart. Name systems, components, and symbols in words. Do not paste code. Say each fact once, in the section that owns it, and refer to that section by name. Restate only where the reader could not follow without it. Gap ids, sources, and links live in `gaps.md`, `research/`, and `log.md`. Read dates from the system clock.

### The state file

Load `state.md` once per session. Open gaps stay in `gaps.md`. It holds the status, size, types, dates, the Destination, and the Notes, in the form in [structure.md](references/structure.md). None of it goes into `design.md`.

### Gaps

One row in `gaps.md` is one gap. The question fits one session and says when it is done. The type is `research`, `prototype`, `grilling`, or `task`. Read the type column.

**Claim** a gap by setting `owner` before any work. An open row with an empty owner is unclaimed. `blocks` lists the ids that must close first. The **frontier** is status `open`, unblocked, and unclaimed.

While a gap is studied, its status is `research`. No answer yet sets `waiting-on-input`, with who, when asked, and when due. The human's answer sets `decided`. Set `accepted-risk` only when the human accepts the risk you named. Advice alone never closes a gap.

## Gap types

**HITL** means the human speaks for themselves and you work with them. **AFK** means you drive the gap alone. A HITL gap closes only through that exchange. Never answer the human's side.

**Research** (AFK). A fact, not a preference. A subagent with a fresh context finds it and writes `research/<gap-id>-<topic>.md`. The triggers, the brief, and the file shape are in [research.md](references/research.md).

**Prototype** (HITL). Use when the question is how it should look or behave. Make a rough artifact and link it from the row. The human's reaction is the answer.

**Grilling** (HITL). The default. Give advice first: 2 to 3 options, the recommended one, why with a source, and the risk if it is left open. Call `codebase-design` for the options, then `grilling` and `domain-modeling`. Ask this gap's question, and stop. On `<name> batch`, give this advice for every frontier grilling gap in one turn instead. The human's answer closes the gap.

**Task** (HITL or AFK). Work that must finish before a decision can be made, such as requesting access. Drive it when you can. Otherwise give the human a checklist. Make no live call to a dependency. Proof is a spec or a written answer in `input/`. A chat line is not proof.

## Fog of war

Open questions is also the **fog of war**: in-scope questions still too vague to be gaps. A question you can phrase now is a gap, even when it is blocked. A question you cannot phrase stays one line in the fog. Resolving a gap lets you phrase the next ones. Write each as a gap and delete its line. One line may become several gaps, or none.

Fog is legal while the design is in `discussion`. It must be `None.` at ready.

## Out of scope

Work past the destination is out of scope. Drop the row and add one line under Goals and non-goals, as a non-goal, with the question and why. It never comes back into this design. Start a new design if the destination changes.

## Companion skills

Call each by its exact name with the Skill tool: `grilling`, `domain-modeling`, `research`, `codebase-design`, `writing-for-agents`, `deslop`. On each edit of `design.md`, call `writing-for-agents`. When a code snippet changes, call `deslop`. If one is not installed, say so once, name `/setup-nstack-skills`, and do that step by the rules in this skill.

## Invocation

The person types `/tech-design`. Read the first word after it.

| Typed | Mode |
| --- | --- |
| nothing | List, see [help.md](references/help.md) |
| `help` | Help, see [help.md](references/help.md) |
| `new <name> [types]` | Chart |
| `<name>` or `<name> grill [gap]` | Work |
| `<name> batch` | Batch |
| `<name> status`, `close <gap>`, `drop <gap>` | See [help.md](references/help.md) |
| `<name> ready` or `<name> ready anyway` | Ready |
| `<name> committed`, `<name> abandoned` | Set that status, see [help.md](references/help.md) |
| `<name> tickets` | Only from `committed`, when the human asks: write `tickets.md`, see [the ready gate](references/ready-gate.md) |

Claim one gap per session, then stop. Also close any other `open` or `waiting-on-input` gap whose outcome that answer states in full. `<name> batch` is the exception: it claims and closes every answered frontier grilling gap in that turn. Research gaps run beside it. Chart and ready close no gap. Every session ends by writing state to disk, see [resume.md](references/resume.md).

### Chart the map

1. **Name the destination and scope.** Before any grilling or sweep, ask the human in one turn: what is in, what is deliberately out and why, what is already decided, and the hard constraints (time, stack, systems). If a deliberately-out item has no why, ask for that why once. Hold the answers until `design.md` exists. If the session must stop before step 5, print the held answers in the closing message so the human can paste them into the next `new`. Then call `grilling` and `domain-modeling`. Done when the destination is one or two lines the human agrees with and the four answers are recorded.
2. **Pick the size.** Propose `small`, `medium`, or `big` with reasons from [sizes.md](references/sizes.md). Record the types the person named. Done when the human confirms the size.
3. **Map the frontier.** Grill again, breadth-first. List the decisions you can phrase. If you find no fog and one session can finish the design, stop and ask how to proceed.
4. **Sweep.** Run all 18 categories in [gap-sweep.md](references/gap-sweep.md). Done when every category is a gap, a fog line, or `n/a` with a reason in `log.md`.
5. **Create the folder** by [structure.md](references/structure.md), in the working directory: every entry, `state.md` at `draft`, `design.md` with all 15 headings, Summary first. Only when the working directory's `AGENTS.md` has a `## Repos` section, ask first: "Here, or in one of: <those repos>?" The repos are the pointer lines under `## Repos`. When those lines name `repos/<area>.md` files instead, read the files: an area is not a repo. Recommend here when the design changes more than one of those repos, and the one repo it changes otherwise. For another repo, create the folder there and tell the human to run later sessions from that repo. For the rest of this session, every `docs/design/` path in this skill and its references is under that repo's root, not the working directory. Use the full path in each step and in every subagent brief. Fill the map and what is already known. Write what is in into Summary and Context and scope, and into Goals and non-goals when it is a goal. Write the Destination into `state.md`. Write each deliberately-out item under Goals and non-goals as a non-goal `<thing>: <why>`. Write each constraint in `state.md` Notes as `Constraints: <time, stack, systems>`. Write each prior decision under Decisions as a Decisions row: decision, choice, why. Do not open a gap for those lines. Write each held term into `glossary.md`, one line per term with its one meaning. Write each held gapless choice into the section that would have held the answer, and under Decisions as `- <choice>: <gist>`. Every other section holds `n/a: <reason>` or `Pending: <the open question in words>`, with no gap id. Write the held sweep endings from step 4 into `log.md` now. Add a Dependencies row for each outside system.
6. **Add the gaps.** Each row starts `open`, with a category, a type, and a real id. Then merge: two gaps that ask for the same decision become one row. Keep the lower id. Leave its question unchanged. Add the line `merged <dropped id> into <kept id>` to `log.md`. Repoint any `blocks` cell that named the dropped id to the kept id. If that was the category's only gap, log `sweep <category>: n/a: same decision as <kept id>`. Then fill `blocks` with ids that still exist. When gap A's answer would settle gap B, set B's `blocks` to A's id, so A is asked first. A gap whose answer sits with a named person starts `waiting-on-input`, with its question sheet. Set status `discussion`.
7. **Start the research subagents**, one per research gap, by [research.md](references/research.md).
8. **Stop.** Log one line. Tell the human the size, the gap count by type, who is being waited on, and the first frontier gap. If the human asked for something short, offer a summary by [sizes.md](references/sizes.md). Never replace the map with it.

A second `new` for a name that already exists stops. Tell them to resume. Check again at step 5 in the repo the human picked, before you create the folder.

### Work through the map

1. **Load and catch up** by [resume.md](references/resume.md): read `state.md` and `design.md`, take in new files under `input/`, print the board, flag overdue gaps, start new research. When no design of that name is here and the working directory's `AGENTS.md` has a `## Repos` section, look in the repos it points at. If it is in one, name that repo, tell the human to run the skill from there, and stop. If the status is `ready`, `committed`, or `abandoned`, say so and stop.
2. **Choose the gap and claim it.** Use the one the person named. Otherwise take the first frontier gap. Set `owner` before any work.
3. **Resolve it by type.** Read a related row or research file when you need it. On a grilling gap, advice comes before the one question.
4. **Record the resolution.** Write the answer on the row and set `decided`, or `accepted-risk` when the human accepts the risk you named. With no answer, set `waiting-on-input` and write the question sheet. Advice alone never closes a gap.
5. **Write it into the design.** Put the result in the section its category names. Draw any diagram the answer now triggers, by [diagrams.md](references/diagrams.md). Add the gist to Decisions. A new term goes to `glossary.md`, and a gapless choice goes in its section and under Decisions as `- <choice>: <gist>`, by the materiality rule.
6. **Update the map.** Add the gaps this answer opens, then fill `blocks`. Apply the rules at the top. Delete fog you can now phrase. Raise the size if a larger one now holds. Close every other gap in `open` or `waiting-on-input` whose outcome this answer states in full: set it `decided`, set `answer or source` to `<gist> (from <id>)`, clear `owner`, `waiting on`, `asked`, and `due`, move its question sheet from Open to Answered when it has one, add that gist to Decisions, and write the result into the section its category names. Do not infer a further answer. Update rows it invalidates.
7. **Stop.** Write state. The session is done when that one gap is claimed and either closed or `waiting-on-input`. On batch, it is done when every accepted gap is closed and every skipped gap is `open` or closed by the cascade.

Other sessions may edit this folder at the same time.

### Batch

Follow this on `<name> batch`, after load and catch up. Only grilling gaps are batched.

1. If there is no frontier grilling gap, say so and stop.
2. Set `owner` on each one, then number them in frontier order and print the id. For each, give the Grilling advice: 2 to 3 options, the recommended one, why with a source, and the risk if it is left open.
3. The human answers in one turn. `ok` accepts every remaining recommendation, and the answer recorded is that recommended option, as the human's own answer because they said `ok`. `<n>: <answer>` overrides that number. `skip <n>` clears `owner` and leaves the gap `open`. A number not named is accepted. `ok` is not acceptance of the risk of leaving a gap open.
4. Record those answers first. Then run Work steps 5 and 6 in number order. Do not replace an answer recorded in this turn. A skipped gap stays `open` unless that cascade states its outcome in full.
5. Write state by Work step 7. The session is done when every accepted gap is closed and every skipped gap is `open` or closed by that cascade. Then stop.

### Ready

Follow [the ready gate](references/ready-gate.md). Walk every check and print pass or fail for each. Any fail stops ready and leaves the status unchanged. When all pass, set `ready`. Write no tickets. `ready anyway` exists only when the human types it. Each open gap is then accepted by name, one at a time, by the human.
