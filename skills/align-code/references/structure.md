# Structure

## Folder

`docs/align/<yyyy-mm-dd>-<name>/`. Date of charting, from the system clock.

| Entry | Holds | Created |
| --- | --- | --- |
| `align.md` | Header, map, one section per area. This is the report. | chart |
| `gaps.md` | One row per gap | chart |
| `log.md` | Append only. One line per session, plus one line per area at chart. | chart |
| `survey/` | One file per area that is not n/a | first survey |

## Header

```markdown
# <name>

Status: draft
Scope: <parts or folders>
Created: <yyyy-mm-dd>
Updated: <yyyy-mm-dd>
Owner: <person>
```

## Area sections

After `## Map`, one `## <Area>` per area on the list in `align.md`, in order. Each holds exactly one of:

- `consistent: <the one way>. Exemplar: <module>.`
- `n/a: <reason>`
- `Waiting on <gap ids>.`
- A standard:

```markdown
Standard: <one sentence>. <source>.
Exemplar: <module, or none>
Rejected: <variant>: <why>.
Changes: <n> files:
- <path, one per line>
```

Name modules and symbols. No pasted code.

## gaps.md

Columns, in order: `id`, `question`, `area`, `type`, `danger`, `status`, `owner`, `answer or source`, `blocks`.

- `id`: `G-001` and up. Never reused.
- `type`: `research`, `grilling`.
- `danger`: a level from Danger first in [SKILL.md](../SKILL.md#danger-first). Empty for research.
- `status`: `open`, `research`, `waiting-on-input`, `decided`, `accepted-risk`.
- `blocks`: the ids that must close before this one.
- `owner`: who works it. A subagent: `survey`.

## log.md

`<yyyy-mm-dd> <mode> <id and question, or none>: <what changed>`

At chart, one extra line per area, in the same shape: `<yyyy-mm-dd> chart none: <area>: <why it is on the list, or why it is n/a>`.
