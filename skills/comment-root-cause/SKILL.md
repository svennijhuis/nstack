---
name: comment-root-cause
description: Use when you write a code comment, a TODO or HACK, or a lint or type suppression, or when the user asks to check the comments in a path. Asks why the comment is there and whether the code can be better, and fixes the root cause when the comment covers a shortcut or a problem.
---

When you write a comment, ask two questions:

1. **Why is this comment here?**
2. **Can the code be better, or is this the best it can be?**

Check only comments in lines you change, unless the person asks for a path. A comment on a line you edited, or directly above it, counts as changed. Leave other comments alone.

## Why is it there?

| Reason | Example | Do |
| --- | --- | --- |
| It explains what the code does | `// loop over the users and skip the inactive ones` | Often a shortcut in disguise. Say why the code needs it. A shortcut or a hidden failure: fix the root cause. The code is only hard to read: make it clear with a name, a type, or a smaller function, delete the comment, and keep the behaviour the same. If the comment only repeats code that is already clear, use the next row. If you only suspect the code is wrong, flag it and ask the person, and leave the comment until they answer. |
| It only restates code that is already clear | `// add the three together` | No root-cause steps. Delete it. Rename only if a name hides what the code does; `a, b, c` in a one-line sum do not. |
| It covers a shortcut, a workaround, or an unfixed cause | `// sometimes undefined`, `// retry because flaky`, `as any`, `@ts-ignore`, `TODO`, `eslint-disable` with no rule name | Fix the root cause. This includes a suppression with no reason on the same line, and an `eslint-disable` that names no rule. A reason on the same line does not move `as any`, `@ts-ignore`, `TODO`, or that `eslint-disable` to the keep row, and a reason that only restates the shortcut (`as any // we trust the caller`) is no reason. |
| A business rule or decision | `// orders over €500 need a manual check by finance` | Keep it. |
| A fact outside our code | `// the bank API returns 200 on failure: <link>` | Keep it, with its source: a link, or the file path if the source is code in the repo. A fact that also carries a marker (`no idea why`, `HACK`, `TODO`): keep the fact, drop the marker. |
| Docs or a marker a tool needs | API docs on an exported function, a license header, `// generated`, `@ts-expect-error` in a test of that error | Keep true docs and true tool markers. A suppression you keep needs a reason on the same line. A false marker does not belong in this row (it is a shortcut: a wrong claim left in the code): `// generated` on a hand-written file is wrong, so ask the person. If they say the file is hand-written, delete the marker. If nobody can confirm it, leave it and say it is unverified. |

Unsure if it is a business rule? Keep it. Otherwise, if the comment is not a shortcut and the code cannot be clearer, say why it stays.

## Fix the root cause

1. Reproduce the problem with a test or a command. Run it: reading the code or a library is not reproducing. For new code with no failing case yet, running sample inputs counts. Often that is hard: then write the smallest failing test you can, or run the code with the input that breaks it. If the case in the comment passes, try variants of it. Cannot reproduce it at all? Say so and ask the person for a failing case. Never guess a fix.
2. Ask why until you reach the cause in our code. If the chain ends in a library or service we do not own, or in callers we cannot see, stop there and go to 4.
3. Fix it there. Remove the shortcut and its comment. The tests pass, or with no test runner, the command that reproduced it now passes. If the fix needs a behaviour choice (for example what to return on bad input), or code outside ours depends on what changes (a published signature or API), go to 4. One obvious fix that only our code depends on: make it.
4. A behaviour choice, a change that code outside ours depends on, too big for this task, or outside our code: ask the person in one short question that names the choice and the options, and leave that code and its comment as they are until they answer. Carry on with the other comments. You may offer a guard at this call site (a check that fails or returns early when that outside case hits) as an option, but do not add it on your own. Never decide to keep a shortcut on your own.

## Check a path

`/comment-root-cause <path>` checks the comments already in a file, folder, or repo. List at most 20, each with its reason and what you will do (keep, fix, or ask), and wait for a yes. Say how many more comments are not yet listed.
