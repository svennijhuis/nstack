# Comment kinds, by example

Each row is one new comment and what to do with it. The kinds are in [SKILL.md](../SKILL.md#the-three-kinds-of-comment).

## What

| Comment | Instead |
| --- | --- |
| `// loop over the users` | Delete it. The loop says it. |
| `# returns None when not found` | Name it `find_user`, or return `Optional[User]`. |
| `// step 2: validate` | Pull the step into `validate()`. |

## Outside why

Keep these, with a source.

| Comment | Why it stays |
| --- | --- |
| `// Bank API returns 200 on a failed transfer. See https://vendor.example/issues/412` | The cause is the vendor. The link says when it can go. |
| `# Dutch law: keep invoices 7 years (AWR art. 52)` | A law, not our code. |
| `// Safari < 17 ignores this header. Remove when support drops, ADR-0012` | The platform, with the decision that ends it. |

The same comment with no link is an excuse until it has one.

## Excuse

Run the loop in [SKILL.md](../SKILL.md#the-loop) for each.

| Comment or marker | The question to chase |
| --- | --- |
| `// user can be undefined here sometimes` | Who passes undefined, and why? |
| `// retry 3 times because it is flaky` | What makes it fail: order, time, a race, shared state? |
| `await sleep(500) // wait for the cache` | What signals the cache is ready? Wait on that. |
| `as any // types are off` | Which type is wrong? Fix that type. |
| `// @ts-ignore`, `// @ts-expect-error` | What does the checker see that you do not? |
| `// eslint-disable-next-line`, `# noqa`, `# type: ignore`, `//nolint`, `# rubocop:disable`, `#pragma warning disable`, `@SuppressWarnings` | What does the rule protect against here? |
| `catch (e) {} // ignore` | What fails, and who should handle it? |
| `// TODO: fix properly later`, `// HACK`, `// FIXME`, `// workaround` | Fix it now, or ask the person by step 6. |
| `if (x == null) return // just in case` | Can x be null? If not, delete the guard. If yes, make the type say so. |

## A test that was changed to pass

Not a comment, the same tell: a skipped test, a loosened assertion, a raised timeout, a test that now expects the wrong value. Treat it as an excuse.
