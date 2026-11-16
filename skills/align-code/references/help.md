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
Run       Scope    Status    Created  Updated  Open  Tickets
<folder>  <scope>  <status>  <date>   <date>   <n>   <n> done, <n> blocked, <n> todo, or -
```

None: say so and show the `new` line.

## Status

```text
<name>   Status: <status>   Scope: <scope>   Updated <date>

Areas: <n>. <n> decided, <n> consistent, <n> n/a, <n> surveying.
Gaps:  <n>. <n> decided, <n> open (<n> per danger), <n> waiting, <n> research.
Fog:   <n> lines.

Needs your answer
  <id>  <question>  <danger>
Waiting on others
  <id>  <question>  <who>, due <date>
Agent alone
  <id>  <question>  <status>
Next: /align-code <name> grill <id>
```

During apply, add the board from [rollout.md](rollout.md). Leave out an empty group. End with what is left before ready.

## Close

1. Find the row. Several match: list them and ask.
2. No answer given: ask once. Grilling: ask the outcome too.
3. Run Work steps 4 to 6 in [SKILL.md](../SKILL.md#work).
4. Log. Stop.

Only the person's own answer closes a gap this way.

## Drop

1. No reason given: ask.
2. Remove the row. One line under Out of scope.
3. Clear its id from every `blocks`. Log. Stop.

Only for a gap past the destination. A difference the person keeps is closed as `exception`, not dropped.

## Abandoned

Only on the person's command.

1. No reason given: ask.
2. Status `abandoned`. Log the reason. Change no gap or ticket.
3. Name the apply branch, if any, to keep or delete. Stop.
