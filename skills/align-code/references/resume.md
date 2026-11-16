# Stop and resume

An alignment takes many sessions. Each one must be safe to stop, and each new one must start cold from the files alone.

## Waiting on a person

When a gap cannot close because someone else has the answer, such as the owner of a public API:

1. Set status `waiting-on-input`. Write who, when asked, and when due in the answer cell.
2. Give the person one question they can paste to that someone: the area, the question, the recommended answer, and the form of the answer needed. Do not send it yourself.
3. Go on. A waiting gap blocks only the rows that list it under `blocks`.

When the answer comes back, write it on the row with who said it and when, and close the gap as in the skill.

## End of every session

Before you stop, in any mode, write state to disk. Nothing may live only in the chat.

1. The gap row or ticket holds its new status and, when closed, its answer or commit.
2. `log.md` has one new dated line.
3. `Updated` in the header is today.
4. The last thing you say is three lines: what changed, what waits on whom, and the next frontier gap or ticket by its question or title.

Outside apply, do not commit, switch branch, or push. The person commits the align folder.

## Start of every work session

1. Read the header, the map, `gaps.md`, and the last five `log.md` lines. Do not read `survey/` or `research/` yet.
2. Turn every survey finished since the last session into gaps, as the skill's Work step 1 says.
3. Print the board from [help.md](help.md).
4. Flag every waiting gap past its due date and ask once: chase, extend, or accept the risk.
5. Start survey and research subagents for new open research gaps, see [survey.md](survey.md).
6. Then choose one gap.

## More than one run

Each run is its own dated folder. Sessions never mix them. Two open runs whose scopes overlap would rewrite the same files: refuse `new` for a scope that overlaps a run not yet `aligned` or `abandoned`, and name it.
