# Structure

## Folder

`docs/align/<yyyy-mm-dd>-<name>/`. Date of charting, from the system clock.

| Entry | Holds | Created |
| --- | --- | --- |
| `align.md` | Header, map, one section per area | chart |
| `gaps.md` | One row per gap | chart |
| `log.md` | One line per session, append only | chart |
| `survey/` | One file per area | chart |
| `research/` | One file per other research gap | chart |
| `prototypes/` | One rewrite per prototype gap. Never imported. | chart |
| `rollout.md` | The board and the tickets | ready |
| `lint.md` | The lint advice | finish |

Folders start with a `.gitkeep`. Delete it when the first file lands.

## Header

```markdown
# <name>

Status: draft
Scope: <parts or folders>
Created: <yyyy-mm-dd>
Updated: <yyyy-mm-dd>
Owner: <person>
Branch: <filled at apply>
```

`Updated` changes on every session that writes.

## Area sections

After `## Map`, one `## <Area>` per area in [survey.md](survey.md), in order. Each holds exactly one of:

- `consistent: <the one way>. Exemplar: <module>.`
- `n/a: <reason>`
- `Waiting on <gap ids>.`
- A standard:

```markdown
Standard: <one sentence>. <principle id>.
Exemplar: <module, or none: a rule of absence, such as comments>
Outcome: <apply | adapter | new-only | exception>
Rejected: <variant>: <why>.
Checked by: <lint rule, type, or test, or none>
Changes: <n> files.
```

Name modules and symbols. No pasted code. The discussion stays on the gap row and in `survey/`.

## gaps.md

Columns, in order: `id`, `question`, `area`, `type`, `danger`, `status`, `owner`, `outcome`, `answer or source`, `blocks`.

- `id`: `G-001` and up. Never reused.
- `type`: `research`, `prototype`, `grilling`, `task`.
- `danger`: `bad spreading`, `bad majority`, `bad`, `inconsistent`. Empty for research and task.
- `status`: `open`, `research`, `waiting-on-input`, `decided`, `accepted-risk`.
- `blocks`: the ids that must close before this one. Empty when none.
- `outcome`: `apply`, `adapter`, `new-only`, `exception`. Grilling only.

## log.md

`<yyyy-mm-dd> <mode> <id and question or title, or none>: <what changed>`

One line per session. Several modes in one session: one line each.
