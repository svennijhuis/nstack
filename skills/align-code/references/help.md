# Help, list, status, close, drop, abandoned

Help, list, and status change no file.

## Help

```text
/align-code                      list every run
/align-code new <name>           chart: scope, sweep, start the surveys
/align-code <name>               resume: board, then one gap
/align-code <name> grill [gap]   work one gap
/align-code <name> status        board and to-do. changes nothing
/align-code <name> close <gap>   you answer, the gap closes
/align-code <name> drop <gap>    out of scope, with a reason
/align-code <name> ready         strict gate, then the tickets
/align-code <name> apply         run the tickets, local branch
/align-code <name> abandoned     stop the run, with a reason
/align-code check                this branch against the standards
/align-code advise               drift since the last run
/align-code help                 this card
```

`<name>` matches the folder with or without its date. `<gap>` is an id or words from its question.

## List

One row per folder under `docs/align/`, newest first:

```text
Run                 Scope        Status    Created     Updated     Open  Tickets
2026-11-16-backend  api, worker  applying  2026-11-16  2026-11-24  0     31 done, 2 blocked, 9 todo
```

None: say so and show the `new` line.

## Status

```text
<name>   Status: discussion   Scope: api, worker   Updated 2026-11-19

Areas: 18. 9 decided, 4 consistent, 2 n/a, 3 surveying.
Gaps:  22. 12 decided, 6 open (2 bad spreading, 1 bad majority), 1 waiting, 3 research.
Fog:   1 line.

Needs your answer
  G-009  How should a failing call report its error?   bad spreading
Waiting on others
  G-011  May the v1 user response gain a field?        Sam, due 2026-11-21
Agent alone
  G-002  Survey: data access                            research
Next: /align-code <name> grill G-009
```

During apply, add the board from [rollout.md](rollout.md). Leave out an empty group. End with what is left before ready.

## Close

1. Find the row. Several match: list them and ask.
2. No answer given: ask once. Grilling: ask the outcome too.
3. Write answer and outcome. `decided`.
4. Write the standard into `align.md`. Add the gist to Decisions so far.
5. Add the gaps it opens. Log. Stop.

Only the person's own answer closes a gap this way.

## Drop

1. No reason given: ask.
2. Remove the row. One line under Out of scope.
3. Clear its id from every `blocks`. Log. Stop.

Only for a gap past the destination. A difference the person keeps is closed as `exception`, not dropped.

## Abandoned

Only on the person's command.

1. No reason given: ask.
2. Status `abandoned`. Log the reason. Change no gap or ticket. Stop.
3. Name the apply branch, if any, to keep or delete.
