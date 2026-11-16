---
name: comment-root-cause
description: Use before you write a code comment, a TODO or HACK, a lint or type suppression, or a workaround (a guard, retry, sleep, cast, empty catch, skipped or loosened test), with or without a comment. Also use when a hook blocks a comment, a test is flaky, a value is "sometimes" wrong, the user asks for the root cause, or the user wants comments cleaned up.
---

Fix the root cause. Never comment it, never work around it. An agent that cannot find a cause patches the symptom, and often writes a comment that makes the patch sound reasonable. The comment is the tell. The workaround is the bug.

## Rules that outrank the rest

**A workaround is an excuse, with or without a comment.** A guard, retry, sleep, cast, suppression, empty catch, or skipped, loosened, or slowed test that hides behavior of code we own: run [the loop](#the-loop).

**An excuse moved is still an excuse.** In a name, a log line, a docstring, an error message, a commit message, or a PR description, it counts the same as in a comment.

**Only the person decides to keep a workaround.** Out of scope, too big, out of reach: say so and let them choose. Never decide it with a comment.

**Never remove an excuse without its cause.** Deleting the comment and keeping the workaround hides the bug. Both go when the cause is fixed.

**A source or label must be true, not pass the hook.** The optional hook refuses a comment with no source or business label. One you added only to get past it is a lie.

## Four kinds of comment

Sort every new comment, marker, and workaround. Examples: [comment-classes.md](references/comment-classes.md).

| Kind | Test | Do |
| --- | --- | --- |
| **What** | Says what the code does. | Delete. Make the code say it: a name, a type, a smaller function. |
| **Business why** | Explains a business rule or a decision the code cannot show: why 14 days, why this order, why these customers skip a step. | Keep. Start it with `Business rule:` or `Decision:`. |
| **Outside why** | Names a cause outside code we own: a vendor bug, a law, a protocol, a measured limit. | Keep, with a source that shows it. No source, no comment. |
| **Excuse** | Explains away code we own, or is a workaround. | Run the loop. Workaround and comment both go. |

A business why says what the business wants. An excuse says why the code misbehaves. Unsure between those two: keep it as a business why, the next reader needs it. Unsure between outside why and excuse: could someone in this repo change what the comment blames? Then it is an excuse.

## The loop

1. **Symptom.** One line: what goes wrong without the workaround.
2. **Reproduce.** A failing test, or the exact command. Cannot reproduce: add no workaround, tell the person what you tried, and stop.
3. **Why, until the source.** Each answer is something you saw in code, a log, or a run, never a guess. Stop at the first cause in code we own.
4. **Fix it there.** Remove the workaround and its comment. The step 2 test passes, the suite passes, no test was skipped or loosened.
5. **Out of reach.** The cause is in a vendor, another repo, or the platform, and a source shows it. Keep the smallest workaround at the boundary, with an outside-why comment and that source. No source shows it: it is not out of reach, go to step 6.
6. **Ask.** Bigger than the task, or step 5 has no source: stop. Give the person the cause, where the fix goes, and the choice: fix it now, keep it with a ticket they give you, or accept the risk by name.

Done when the cause is fixed or the person chose.

## Excuses and their answers

| You think | Answer |
| --- | --- |
| "It's defensive." | Find who passes the bad value. Fix the caller, or make the type say it can be missing. |
| "It's flaky." | Flaky has a cause: order, time, shared state, a race. A retry hides it. |
| "The types are wrong." | Fix the type. A cast turns the check off. |
| "The linter is too strict." | Change the code, or change the rule for the repo with a reason. Never for one line. |
| "Out of scope." | The person's call, by step 6. |
| "I'll leave a TODO." | Fix it, or step 6. |
| "It works now." | Name why. Working by accident is not working. |

## Clean up existing comments

`/comment-root-cause <path>`, or "clean up the comments in <path>". No path: the current change only.

1. **List** every comment, marker, and workaround under the path. Skip docs, generated files, and licence headers.
2. **Plan.** One line each: file and line, kind, action. Write nothing before a yes.
3. **What comments:** delete, after moving any meaning into a name or type. **Business why:** keep, and add its label.
4. **Outside why with no source:** find the source, or ask.
5. **Excuses:** the loop, one per change. Step 6 for one does not stop the rest.
6. **Report** what was deleted, fixed, kept with its source, and waits on the person.

## When you finish

List each comment and workaround you added or kept: file and line, kind, source, and for a workaround, the person's choice. Added none: say nothing. The optional hook checks this list.
