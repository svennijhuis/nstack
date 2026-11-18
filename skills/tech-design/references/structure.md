# Structure

Every design has the same folder, the same files, and the same sections in the same order. Size and types change how deep a section goes. They never change the structure.

## Folder

`docs/design/<yyyy-mm-dd>-<name>/`. The date is the day of charting. Read it from the system clock.

| Entry | Holds | Created |
| --- | --- | --- |
| `design.md` | The design, readable alone by the business and the lead developer | chart |
| `state.md` | Status, size, types, dates, destination, and notes. Working state, not for the business | chart |
| `gaps.md` | One row per gap | chart |
| `glossary.md` | One meaning per term | chart |
| `log.md` | One dated line per session, append only | chart |
| `research/` | One file per research gap | chart |
| `questions/` | One question sheet per person | chart |
| `input/` | Answers and specs received from people | chart |
| `tickets.md` | The tickets, optional | `tickets`, after committed |

Create the three folders empty at chart, each with a `.gitkeep`.

## Header

`design.md` opens with the title, then the owner and approvers. Nothing else: no status, size, skills, or dates of work.

```markdown
# <name>

Owner: <person driving the design>
Approvers: <people who sign off>
```

`state.md` holds the working state:

```markdown
# <name>: state

Status: draft
Size: <small | medium | big>
Types: <web, api, data, integration, or none>
Created: <yyyy-mm-dd>
Updated: <yyyy-mm-dd>

## Destination

<one or two lines. The technical design this effort ends on. Read this before you pick a gap.>

## Notes

Domain: <one line>
Skills: <only the skills this design needs>
Preferences: <preferences for this design>
Constraints: <time, stack, systems>
```

Set `Updated` on every session that changes a file. At ready with accepted open gaps, add `Open at ready: <n>` under `Updated`.

## Sections

`design.md` holds these sections, in this order, with these exact headings. A section that does not apply keeps its heading and one line: `n/a: <reason>`. Never drop a heading. Never leave a section blank.

| # | Heading | Holds | Done when |
| --- | --- | --- | --- |
| 1 | `## Summary` | A one-sentence TL;DR, then who gains what, how it is measured, and what the approvers are asked to decide | A reader with no code knowledge can repeat it |
| 2 | `## Context and scope` | What exists today, what forces the change, what is inside the boundary | Names the code areas and systems in words, with no links or paths |
| 3 | `## Goals and non-goals` | Goals as outcomes. Non-goals: what a reader might expect but will not get, and what is deliberately out, each with the reason | Each goal can be checked. Each non-goal has a reason |
| 4 | `## Decisions` | Table: decision, choice, why. Business and technical decisions, one row each | Every closed decision is a row |
| 5 | `## Actors` | Table: actor, human or system, permission level, what it does here | Every actor in a diagram is in the table |
| 6 | `## Requirements` | One table row per requirement, see below | Every row follows the form |
| 7 | `## Design` | `### Overview`, `### Context`, `### Boundaries and contracts`, `### Data model`, `### Flows`, `### State` | Every required diagram is present with its text twin |
| 8 | `## Failure modes` | Table: step or dependency, failure, how it is detected, what the user sees, mitigation | Every dependency and every flow step with an outside call has a row |
| 9 | `## Dependencies` | The contract table from [dependency-contract.md](dependency-contract.md) | No empty cell |
| 10 | `## Alternatives` | Table: option, why it lost. Includes "do nothing" | At least "do nothing" and one other |
| 11 | `## Cross-cutting` | `### Security`, `### Privacy`, `### Observability`, `### Rollout and rollback`, `### Testing` | Each has content or `n/a: <reason>` |
| 12 | `## Assumptions and risks` | Table: statement, owner, consequence if wrong, how it is checked | Every row has an owner |
| 13 | `## Acceptance criteria` | One table row per criterion, see below | Every requirement is cited at least once |
| 14 | `## Open questions` | Table: question, why open, possible answers, risk if open, follow-up action, owner, due. Or `None.` At ready anyway, one row per accepted open question | Reads `None.` at ready |
| 15 | `## Sign-off` | Table: approver, date, verdict | Filled at `committed` |

`design.md` stands alone for a business reader: no gap ids, no links or paths to local files, no references to `input/` or `research/`. Name systems and symbols in words. Do not paste code. Prefer tables for anything with the same fields on every item. Keep answers on the gap row and research in `research/`. `design.md` holds the result, not the discussion.

## Requirement form

One table. One row per requirement.

```markdown
| ID | When | The system MUST | Number source |
| --- | --- | --- | --- |
| R-001 | WHEN <trigger> | <response> | decided |
| R-002 | WHILE <state> | <response> | |
| R-003 | IF <unwanted condition> | <response> | |
| R-004 | Always | <response> | |
```

One requirement states one behaviour. Write MUST in capitals. Do not write "should". A requirement with a number fills `Number source`: `measured`, `decided`, or `guessed`. A `guessed` number is a gap until a person decides it or research measures it.

Do not use these words without a number in the same row: fast, scalable, robust, secure, intuitive, user-friendly, efficient, appropriate, as needed, etc.

## Acceptance criterion form

```markdown
| ID | Covers | Given | When | Then | Test |
| --- | --- | --- | --- | --- | --- |
| AC-001 | R-001, R-003 | <state> | <action> | <observable result> | unit / integration / manual |
```

A criterion can fail. "Handles errors well" is not a criterion. "Returns 400 naming the missing field" is.

## Decisions and open questions form

```markdown
| Decision | Choice | Why |
| --- | --- | --- |
| <what was decided> | <the choice> | <the reason in one line> |

| Question | Why open | Possible answers | Risk if open | Follow-up | Owner | Due |
| --- | --- | --- | --- | --- | --- | --- |
| <the question in words> | <why not decided> | <option A, option B> | <what goes wrong> | <action that settles it> | <person> | <yyyy-mm-dd> |
```

## gaps.md

One table. Columns, in this order: `id`, `question`, `category`, `type`, `status`, `owner`, `waiting on`, `asked`, `due`, `answer or source`, `blocks`.

- `id` is `G-001` and up. Ids are never reused.
- `category` is one of the categories in [gap-sweep.md](gap-sweep.md).
- `type` is `research`, `prototype`, `grilling`, or `task`.
- `status` is `open`, `research`, `waiting-on-input`, `decided`, or `accepted-risk`.
- `waiting on`, `asked`, and `due` are filled only while the status is `waiting-on-input`.

## log.md

One line per session: `<yyyy-mm-dd> <mode> <gap id and question, or none>: <what changed>`.
