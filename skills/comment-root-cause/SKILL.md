---
name: comment-root-cause
description: Use when you write or find a code comment, a TODO or HACK, or a lint or type suppression, and when a hook points at a new comment. Checks why the comment is there, and fixes the root cause when the comment covers a shortcut or a workaround.
---

A comment often covers a problem: a shortcut, a workaround, a cause that was never found. When you write or find a comment, check why it is there.

## Why is it there?

| Reason | Example | Do |
| --- | --- | --- |
| It says what the code does | `// loop over the users` | Make the code say it with a name or a type. Drop the comment. |
| A business rule or decision | `// orders over €500 need a manual check by finance` | Keep it. |
| A fact outside our code | `// the bank API returns 200 on failure: <link>` | Keep it, with its source. |
| It covers a shortcut, a workaround, or an unfixed cause | `// sometimes undefined`, `// retry because flaky`, `as any`, `@ts-ignore`, `TODO` | Fix the root cause. |

Unsure if it is a business rule? Keep it.

## Fix the root cause

1. Reproduce the problem with a test or a command.
2. Ask why until you reach the cause in our code.
3. Fix it there. Remove the shortcut and its comment. The tests pass.
4. Too big for this task, or outside our code: ask the person. Never keep a shortcut on your own.

## Existing comments

`/comment-root-cause <path>` checks the comments already in a file, folder, or repo. List each with its reason and what you will do, and wait for a yes.

## When you finish

Name each shortcut that is still in the code, and why.
