# Help, list, status, batch, close, drop, committed, abandoned

These modes let the human see where a design stands and steer it. Help, list, and status change no file.

## Help

On `/tech-design help`, print this card and stop.

```text
/tech-design                        list every design with its state
/tech-design new <name> [types]     chart a new design. types: web api data integration
/tech-design <name>                 resume: show the board, then work one gap
/tech-design <name> grill [gap]     work one gap by question and answer
/tech-design <name> batch           every frontier grilling gap at once
/tech-design <name> status          the board and what you need to do. changes nothing
/tech-design <name> close <gap>     you give the answer, the gap closes
/tech-design <name> drop <gap>      move a gap out of scope, with a reason
/tech-design <name> ready           strict gate. refuses while anything is open
/tech-design <name> ready anyway    ready with open gaps you accept one by one
/tech-design <name> committed       builders follow this design now. only from ready
/tech-design <name> tickets         write tickets. only from committed, only if you ask
/tech-design <name> abandoned       the work stopped, with a reason
/tech-design help                   this card
```

`<name>` matches the folder name with or without its date. `<gap>` is an id or a few words of the question.

## List

On `/tech-design` with no argument, read `state.md` and `gaps.md` of every folder under `docs/design/`. Print one row per design, newest `Updated` first, and stop. When the working directory's `AGENTS.md` has a `## Repos` section, read the same folder in each repo it points at that is on disk, and add a Repo column. When the lines under `## Repos` name `repos/<area>.md` files, the repos are the pointer lines in those files. To work on one of those, the human runs the skill from that repo.

```text
Design              Size    Types        Status      Created     Updated     Open  Waiting
2026-03-02-billing  medium  api, data    discussion  2026-03-02  2026-03-09  4     2 (1 overdue)
```

With no designs, say so and show the `new` line from the card.

## Status

On `/tech-design <name> status`, print the board, then the to-do list, and stop. Change nothing.

### The board

```text
<name>   Status: discussion   Size: medium   Types: api, data
Created 2026-03-02   Updated 2026-03-09   Owner: <person>

Gaps: 14 total. 8 decided, 1 accepted-risk, 3 open, 2 waiting.
Fog:  2 lines under Open questions.
Sections filled: 9 of 15.
```

### What you need to do

Group the open work by who must act. Leave out a group that is empty. Name each gap by its question.

```text
Needs your answer (3)
  G-007  Which roles may refund an order?
Waiting on others (2)
  G-004  How does the billing service authenticate callers?   Sam, asked 2026-03-03, due 2026-03-06, OVERDUE
         sheet: questions/sam.md
The agent can do alone (1)
  G-011  What are the vendor rate limits?   research
Blocked (1)
  G-012  How are refunds retried?   waits on G-004
Next: /tech-design <name> grill G-007
```

End with one line saying how far ready is: the count of gaps and sections still to close.

## Batch

Follow Batch in the skill. Plain `/tech-design <name>` still claims one gap per session.

## Close

On `/tech-design <name> close <gap>`, the human closes a gap directly.

1. Find the row. If the words match more than one, list them and ask which.
2. If the human gave no answer with the command, ask for it once.
3. Write the answer on the row. Set `decided`. Clear the waiting fields.
4. Write the result into the `design.md` section its category names, and add the gist to Decisions.
5. Add any gap the answer opens.
6. Close every other gap in `open` or `waiting-on-input` whose outcome this answer states in full: set it `decided`, set `answer or source` to `<gist> (from <id>)`, clear `owner`, `waiting on`, `asked`, and `due`, move its question sheet from Open to Answered when it has one, add that gist to Decisions, and write the result into the section its category names. Do not infer a further answer.
7. Log one line. Stop.

Only the human's own answer closes a gap this way. Do not fill it in for them.

## Drop

On `/tech-design <name> drop <gap>`:

1. Ask for the reason if none was given.
2. Remove the row from `gaps.md`. Add one line under Goals and non-goals, as a non-goal: the question and the reason.
3. Clear its id from every `blocks` cell. Log one line. Stop.

Drop a gap only when it sits past the destination. A gap that is in scope but unanswered is not dropped. It is closed, or accepted as a risk at ready.

## Committed and abandoned

Only the human's own command sets these two. Never set one yourself.

On `/tech-design <name> committed`:

1. If the status is not `ready`, say what it is and stop.
2. Ask for each approver's verdict and date. Fill Sign-off.
3. Set `Status: committed` and `Updated`. Log one line. Stop.

On `/tech-design <name> abandoned`, from any status:

1. Ask for the reason if none was given.
2. Set `Status: abandoned` and `Updated`. Log the reason. Change no gap. Stop.
