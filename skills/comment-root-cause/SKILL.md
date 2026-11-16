---
name: comment-root-cause
description: Use before you write a code comment, a lint or type suppression, a TODO or HACK, or a guard, retry, sleep, cast, or catch that works around behavior instead of fixing it. Also use when a hook flags a new comment, when a test is flaky or a value is "sometimes" wrong, when the user asks to fix a bug at its root cause, and when the user wants to remove or clean up the comments in a file, folder, or repo.
---

Fix the root cause, don't comment it. An agent that cannot find the cause of a problem patches the symptom and writes a comment that makes the patch sound reasonable. The comment is the tell. So a comment that excuses a workaround becomes a fixed cause, and a comment that says what the code does becomes clearer code. One exception: a fact outside code we own, with its source.

## Rules that outrank the rest

**A comment never fixes anything.** When you want to explain why the code works around something, stop and look at that something first.

**Fix the cause where it lives.** The fix goes in the first place the cause sits in code we own, not in the place the symptom showed up.

**Never ship a workaround silently.** When the cause cannot be fixed in this task, say so to the person and let them choose. Do not decide it for them with a comment.

**Never delete an excuse without its cause.** An excuse comment that is already in the code points at a cause that is still there. Removing the comment and keeping the workaround hides the bug. Fix the cause, then the workaround and the comment go together.

**A blocked comment is a question, not an obstacle.** The optional hook refuses a new comment with no source. Sort it by the table below. Never add a link, an issue, or a ticket only to get past the hook. A source must say why the comment is true.

## The three kinds of comment

Sort each new comment, suppression, or marker before you keep it. Examples per language are in [comment-classes.md](references/comment-classes.md).

| Kind | Test | What to do |
| --- | --- | --- |
| **What** | It says what the code does. | Delete it. Make the code say it: a name, a type, a smaller function. |
| **Outside why** | It names a cause outside code we own: a vendor bug, a law, a protocol, a measured limit. | Keep it, with its source: a link, an issue, an ADR, a ticket. No source, no comment. |
| **Excuse** | It explains away behavior of code we own: "needed because X is sometimes null", "retry because it is flaky", "cast because the type is wrong", `@ts-ignore`, `eslint-disable`, `TODO`, `HACK`, an empty `catch`. | Stop. Run the loop below. The workaround and its comment both go. |

When unsure between outside why and excuse, ask: could someone in this repo change the thing the comment blames? If yes, it is an excuse.

## The loop

1. **Name the symptom.** One line: what goes wrong without the workaround.
2. **Reproduce it.** A failing test, or the exact command that shows it. No reproduction, no fix: you are still guessing.
3. **Ask why until you reach the source.** Each answer must be something you saw in the code, a log, or a run, never a guess. Stop at the first cause that sits in code we own.
4. **Fix it there.** Remove the workaround and its comment. The test from step 2 now passes, and the rest of the suite still does.
5. **The source is out of reach.** It sits in a vendor, another repo, or the platform. Keep the smallest workaround at the boundary, write an outside-why comment with the source, and tell the person.
6. **The fix is bigger than the task.** Stop and ask the person. Give the cause you found, where the real fix goes, and the options: fix it now, open a ticket and keep the workaround with the ticket in its comment, or accept the risk by name.

The loop is done when the cause is fixed, or the person chose in step 6.

## Excuses and their answers

| You think | Do this |
| --- | --- |
| "It's just defensive." | Find who passes the bad value. Fix the caller, or make the type say it can be missing. |
| "The test is flaky." | Flaky has a cause: order, time, shared state, a race. Find it. A retry hides it. |
| "The types are wrong." | Fix the type, or the code that makes it wrong. A cast or ignore just turns off the check. |
| "The linter is too strict here." | Read the rule. Change the code it flags, or change the rule for the repo with a reason. Never turn it off for one line to get green. |
| "It's out of scope." | Then it goes to the person, by step 6. Out of scope is their call, not yours. |
| "I'll leave a TODO." | A TODO is a ticket nobody opens. Fix it, or open the ticket and link it. |
| "It works now." | Working by accident is not working. Name why it works. |

## Clean up existing comments

The person types `/comment-root-cause <path>`, or asks to remove the comments from a file, a folder, or the repo. With no path, check only the current change.

1. **Find them.** List every comment and marker under the path. Skip docs, generated files, licence headers, and docstrings that a tool reads, such as an API doc generator.
2. **Sort them.** Give each one its kind from the table above.
3. **Show the plan.** One line per comment: file and line, kind, and what you will do. Delete for a what. Keep for an outside why that has its source. Find the source, or ask, for an outside why without one. Run the loop for an excuse. End with the count per kind. Write nothing before the person says yes.
4. **Delete the what comments.** Where a comment carried meaning, move it into a name, a type, or a smaller function first.
5. **Fix the excuses, one at a time.** Run the loop for each. One excuse is one change the person can review. When one needs step 6 of the loop, ask, and go on with the next.
6. **Report.** What you deleted, what you fixed, what you kept with its source, and what waits on the person.

## When you finish

In your final message, list each comment you added and kept: the file and line, its kind, and its source. Name each workaround still in the code and why the person agreed to it. If you added no comment, say nothing about it.
