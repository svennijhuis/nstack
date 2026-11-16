# Comments and workarounds, by example

The kinds are in [SKILL.md](../SKILL.md#three-kinds-of-comment).

## What: delete

| Comment | Instead |
| --- | --- |
| `// loop over the users` | Nothing. The loop says it. |
| `# returns None when not found` | Name it `find_user`, or return `Optional[User]`. |
| `// step 2: validate` | Pull the step into `validate()`. |

## Outside why: keep, with the source that proves it

| Comment | Why it stays |
| --- | --- |
| `// Bank API returns 200 on a failed transfer: https://vendor.example/issues/412` | The vendor. The link says when it can go. |
| `# Keep invoices 7 years: https://wetten.overheid.nl/BWBR0002320` | A law. |
| `// Safari < 17 ignores this header, ADR-0012` | The platform, with the decision that ends it. |

Without its source, each of these is an excuse.

## Excuse: run the loop

| Comment, marker, or workaround | The question to chase |
| --- | --- |
| `// user can be undefined here sometimes`, `if (!x) return` | Who passes undefined, and why? |
| `retry(3, f)`, `// flaky` | What makes it fail: order, time, a race, shared state? |
| `await sleep(500)` | What signals ready? Wait on that. |
| `as any`, `as unknown as T`, `@ts-ignore` | Which type is wrong? Fix that type. |
| `eslint-disable`, `noqa`, `type: ignore`, `nolint`, `rubocop:disable`, `#pragma warning disable`, `@SuppressWarnings` | What does the rule protect against here? |
| `catch {}`, `.catch(() => {})`, `except: pass` | What fails, and who should handle it? |
| `TODO`, `FIXME`, `HACK`, `XXX` | Fix it now, or ask the person. |
| `it.skip`, `xit`, `@pytest.mark.skip`, `@Disabled`, `t.Skip()` | Why does it fail? |
| A loosened assertion, a raised timeout, a test that now expects the wrong value | What changed the behavior? |
| `"""Retries because the API is slow."""`, `log("ignoring bad state")`, a commit message that explains a workaround | The same excuse, moved. Chase it the same way. |
