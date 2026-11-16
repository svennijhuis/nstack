# Structure

Every run has the same folder, the same files, and the same sections in the same order.

## Folder

`docs/align/<yyyy-mm-dd>-<name>/`. The date is the day of charting. Read it from the system clock.

| Entry | Holds | Created |
| --- | --- | --- |
| `align.md` | The header, the map, then one section per area | chart |
| `gaps.md` | One row per gap | chart |
| `log.md` | One dated line per session, append only | chart |
| `survey/` | One file per surveyed area | chart |
| `research/` | One file per research gap that is not a survey | chart |
| `prototypes/` | One rough rewrite per prototype gap. Never imported by the code. | chart |
| `rollout.md` | The tickets and their board | ready |

Create the three folders empty at chart, each with a `.gitkeep`.

## Header

The first lines of `align.md`, under the title, in this order:

```markdown
# <name>

Status: draft
Scope: <the parts or folders this run covers>
Created: <yyyy-mm-dd>
Updated: <yyyy-mm-dd>
Owner: <person driving the run>
Branch: <the apply branch, filled at apply>
```

Set `Updated` on every session that changes a file.

## Sections

After `## Map`, one `## <Area>` section per area in [survey.md](survey.md), in that order, with the area's name as the heading. A section holds one of:

- `consistent: <the one way the code does it>. Exemplar: <module>.`
- `n/a: <reason>`
- `Waiting on <gap ids>.`
- The decided standard:

```markdown
## Errors

Standard: <one plain sentence>. <Why, with the principle id.>
Exemplar: <module or feature, by name>
Outcome: <apply | new-only | adapter | exception>
Rejected: <variant>: <why>. <variant>: <why>.
Checked by: <the lint rule, type, or test that enforces it, or none>
Changes: <count> files. <Frozen surfaces left as they are, if any.>
```

Name modules and symbols. Do not paste code. The answer and the discussion stay on the gap row and in `survey/`.

## gaps.md

One table. Columns, in this order: `id`, `question`, `area`, `type`, `danger`, `status`, `owner`, `outcome`, `answer or source`, `blocks`.

- `id` is `G-001` and up. Ids are never reused.
- `area` is one of the areas in [survey.md](survey.md).
- `type` is `research`, `prototype`, `grilling`, or `task`.
- `danger` is `bad spreading`, `bad majority`, `bad`, `inconsistent`, or empty for research and task gaps.
- `status` is `open`, `research`, `waiting-on-input`, `decided`, or `accepted-risk`.
- `outcome` is `apply`, `new-only`, `adapter`, or `exception`, set when a grilling gap closes.

## log.md

One line per session: `<yyyy-mm-dd> <mode> <gap or ticket id and its question or title, or none>: <what changed>`.
