# Comments

Agents copy comments too. A comment that explains what the code does is a second source of truth: the code changes, the comment does not, and the next agent trusts the comment. So the default standard for the comments area is: no comments, except a why the code cannot say.

This is the recommended answer on the comments gap. The person confirms it, or edits it, like any other standard.

## What stays

A comment stays only when it is one of these, and says it in one or two lines:

- **A decision or business why.** Why the code does this and not the obvious thing: a business rule, a trade-off, a choice someone made. `Refunds after 30 days go to manual review: finance rule, see ADR 2026-03-02-refund-window.` When the why is a real decision with rejected options, it also gets an ADR, and the comment points at it.
- **An outside constraint.** Behavior forced by a vendor, a platform, a protocol, or a library we cannot change. Name it, and link the issue or doc when there is one.
- **A public API doc comment** that defines the contract for callers outside the code.
- **A legal or license header.**
- **A marker** from [contracts.md](contracts.md): frozen contract or exception.
- **A tool directive**, such as a formatter ignore, or a lint suppression whose rule is style-only or wrong here. Name the reason on the same line.

When you are not sure a comment fits a keep, it goes.

## What goes

Everything else:

- A comment that says what the next lines do.
- Section banners and dividers.
- Commented-out code. Git keeps it.
- `TODO` and `FIXME` with no ticket. A real one becomes an issue in the tracker, and the comment goes.
- A long justification. A why that needs a paragraph is a decision: write the ADR, keep one line that points at it.

## When a comment hid a surprise

A comment that explains surprising behavior in our own code is a sign the code is wrong, not that it needs a comment. Delete the comment and fix the cause: a better name, an extracted function, a type that makes the wrong use impossible, or a test that pins the behavior. Each one becomes a ticket of its own, model `mid`, in the same wave as the comments.

## Suppressions and warnings

- A lint or type suppression (`eslint-disable`, `@ts-ignore`, `# type: ignore`, `#pragma warning disable`, and the like) on a rule that catches real bugs is not kept. Remove it and fix the code it hid, as its own ticket.
- `IMPORTANT`, `do not remove`, `do not change`: read the code around it. When the claim is a real constraint, encode it as a test, a type, or a lint rule, then delete the comment. When the claim is not true, delete the comment. When it is true and nothing can encode it, keep one line that says why.

## In the rollout

- **Survey.** The comments area counts each kind above, lists the files, and marks every surprise and every suppression on a correctness rule.
- **Wave.** One comments wave, after the rest and before the tests. Deleting comments is `cheap`. Each surprise or suppression fix is its own `mid` ticket.
- **Every ticket.** No ticket adds a comment that explains code. The review in [rollout.md](rollout.md) rejects a diff that does.
- **Check and advise.** A new comment that explains code is a finding, see [advise.md](advise.md).
