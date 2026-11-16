# Check and advise

`check` stops a bad copy before merge. `advise` finds the ones that got through. Both only read. Never write, never run a command that changes anything, never open a secret file.

## The standards

Read, in order:

1. ADRs in `docs/adr/` titled `Code standard: <area>`.
2. Area sections of any folder under `docs/align/`.
3. `docs/agents/code-standards.md`.
4. Frozen and exception markers in the code.

None found: name `/align-code new <name>` and stop.

## Check

`/align-code check`: `git diff <default>...HEAD`. The default branch is `origin/HEAD`, else `main`, else `master`. Skip a standards source that does not exist.

A finding is an added line that:

- uses a rejected variant
- copies the shape of a marked symbol
- adds a comment not on the keep list of [comments.md](comments.md). Not sure? Flag it, and say why.
- adds a suppression on a rule that catches bugs
- adds a variant that breaks a principle in [principles.md](principles.md)

```text
File                  Line  Area      Finding                                 Fix
src/orders/refund.ts  14    Errors    returns null on failure (rejected, P4)  return { ok, error }, as billing
src/api/v2/users.ts   3     API       copies the frozen v1 user shape         follow the API ADR
src/cart/total.ts     22    Comments  explains the loop                       delete it

3 findings. Fix them before the pull request.
```

None: say the branch follows the standards.

## Advise

`/align-code advise`: the scope of the last `aligned` run, or the whole repo.

1. Run the survey of every area with a standard, read only. Subagents write nothing and return only the drift rows.
2. Every variant that is not the standard and has no marker is drift. So is every new `bad` variant.
3. Find the source: `git log --diff-filter=A -S<key text>` over its files. The oldest copy is where the agents copy from.

```text
Sev     Area    Files  Finding                                  Copied from               Fix
high    Errors  6      null on failure, 5 in the last 30 days   src/legacy/payments.ts    new run on errors, mark payments.ts
medium  Naming  3      "Manager" suffix again                   src/users/userManager.ts  add a lint rule

2 findings: 1 high, 1 medium.
```

- `high`: fails a principle and grew in the last 30 days.
- `medium`: fails a principle.
- `low`: only inconsistent.

One concrete action per Fix. At most three lines of advice after the table, only with evidence.
