---
name: comment-root-cause
description: Use when you write a code comment, a TODO or HACK, or a lint or type suppression, or when the user asks to check the comments in a path. Asks why the comment is there and whether the code can be better, and fixes the root cause when the comment covers a shortcut or a problem.
---

When you write a comment, ask two questions:

1. **Why is this comment here?**
2. **Can the code be better, or is this the best it can be?**

Check only comments in lines you change, unless the person asks for a path. Leave other comments alone.

## Why is it there?

| Reason | Example | Do |
| --- | --- | --- |
| It explains what the code does | `// loop over the users and skip the inactive ones` | Make the code clear: a name, a type, a smaller function. Then the comment goes. |
| It covers a shortcut, a workaround, or an unfixed cause | `// sometimes undefined`, `// retry because flaky`, `as any`, `@ts-ignore`, `TODO` | Fix the root cause. |
| A business rule or decision | `// orders over €500 need a manual check by finance` | Keep it. |
| A fact outside our code | `// the bank API returns 200 on failure: <link>` | Keep it, with its source. |
| Docs or a marker a tool needs | API docs, a license header, `// generated`, `@ts-expect-error` in a test of that error | Keep it. A suppression keeps a reason on the same line. |

Unsure if it is a business rule? Keep it. Cannot make the code better? Say why.

## Fix the root cause

1. Reproduce the problem with a test or a command.
2. Ask why until you reach the cause in our code.
3. Fix it there. Remove the shortcut and its comment. The tests pass.
4. Too big for this task, or outside our code: ask the person. Never keep a shortcut on your own.

## Check a path

`/comment-root-cause <path>` checks the comments already in a file, folder, or repo. List at most 20, each with its reason and what you will do, and wait for a yes. Say how many are left.

## When you finish

Name each shortcut that is still in the code, and why.
