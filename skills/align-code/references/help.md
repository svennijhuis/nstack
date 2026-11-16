# Help, list, status, close, drop, abandoned

These modes let the person see where a run stands and steer it. Help, list, and status change no file.

## Help

On `/align-code help`, print this card and stop.

```text
/align-code                      list every run with its state
/align-code new <name>           chart a run: scope, sweep, start the surveys
/align-code <name>               resume: show the board, then work one gap
/align-code <name> grill [gap]   work one gap by question and answer
/align-code <name> status        the board and what you need to do. changes nothing
/align-code <name> close <gap>   you give the answer, the gap closes
/align-code <name> drop <gap>    move a gap out of scope, with a reason
/align-code <name> ready         strict gate, then writes the rollout tickets
/align-code <name> apply         run the tickets with subagents, on a local branch
/align-code <name> abandoned     the run stopped, with a reason
/align-code check                check this branch's diff against the standards
/align-code advise               find drift since the last run. changes nothing
/align-code help                 this card
```

`<name>` matches the folder name with or without its date. `<gap>` is an id or a few words of the question.

## List

On `/align-code` with no argument, read the header and `gaps.md` of every folder under `docs/align/`. Print one row per run, newest `Updated` first, and stop.

```text
Run                  Scope         Status      Created     Updated     Open  Tickets
2026-11-16-backend   api, worker   applying    2026-11-16  2026-11-24  0     31 done, 2 blocked, 9 todo
```

With no runs, say so and show the `new` line from the card.

## Status

On `/align-code <name> status`, print the board, then the to-do list, and stop.

### The board

```text
<name>   Status: discussion   Scope: api, worker
Created 2026-11-16   Updated 2026-11-19   Owner: <person>

Areas: 18. 9 decided, 4 consistent, 2 n/a, 3 waiting on a survey.
Gaps:  22. 12 decided, 6 open (2 bad spreading, 1 bad majority), 1 waiting, 3 research.
Fog:   1 line under Not yet specified.
```

During apply, add the ticket board from [rollout.md](rollout.md).

### What you need to do

Group the open work by who must act. Leave out an empty group. Name each gap by its question, danger first.

```text
Needs your answer (3)
  G-009  How should a failing call report its error?          bad spreading
  G-014  Where is input validated?                            bad majority
Waiting on others (1)
  G-011  May the v1 user response gain a field?               Sam, due 2026-11-21
The agent can do alone (3)
  G-002  Survey: data access                                  research
Next: /align-code <name> grill G-009
```

End with one line saying how far ready is.

## Close

On `/align-code <name> close <gap>`, the person closes a gap directly.

1. Find the row. If the words match more than one, list them and ask which.
2. If no answer came with the command, ask for it once. Ask for the outcome too when it is a grilling gap.
3. Write the answer and outcome on the row. Set `decided`.
4. Write the result into its area section of `align.md` and add the gist to Decisions so far.
5. Add any gap the answer opens. Log one line. Stop.

Only the person's own answer closes a gap this way.

## Drop

On `/align-code <name> drop <gap>`:

1. Ask for the reason if none was given.
2. Remove the row. Add one line under Out of scope: the question and the reason.
3. Clear its id from every `blocks` cell. Log one line. Stop.

Drop a gap only when it sits past the destination. A difference the person wants to keep is not dropped: close it with outcome `exception`.

## Abandoned

Only the person's own command sets it. On `/align-code <name> abandoned`, from any status:

1. Ask for the reason if none was given.
2. Set `Status: abandoned` and `Updated`. Log the reason. Change no gap and no ticket. Stop.

Commits already on the apply branch stay. Tell the person the branch name, so they can keep or delete it.
