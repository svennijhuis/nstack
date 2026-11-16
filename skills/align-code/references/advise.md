# Check and advise

Alignment is only worth something while it holds. Agents keep copying, so one bad copy that gets merged becomes the pattern the next agent copies. `check` stops a bad copy before it is merged. `advise` finds the ones that got through. Both only read. They never write, never run a project command that changes anything, and never open a secret file.

## Where the standards are

Read them, in this order:

1. ADRs in `docs/adr/` titled `Code standard: <area>`.
2. The area sections of any align folder under `docs/align/`.
3. `docs/agents/code-standards.md`, when it exists.
4. The frozen and exception markers in the code.

The lint rules need no reading: the linter runs them. When none of the four holds a standard, say so, name `/align-code new <name>`, and stop.

## Check

`/align-code check` reads the current branch's diff against the default branch. Use it before a pull request, or as the last step of a builder's ticket.

1. List the files the branch added or changed.
2. For each standard, look at the added lines in those files. A line that uses a rejected variant is a finding.
3. Code that copies the shape of a symbol with a frozen or exception marker is a finding. Code that touches the marked symbol itself is not.
4. A new file in an area with an exemplar that does not follow the exemplar is a finding.
5. An added comment that explains code, marks a section, or holds dead code is a finding, by [comments.md](comments.md). An added suppression on a rule that catches bugs is a finding.
6. Print the table, then the summary line.

```text
File                       Line  Area    Finding                                     Fix
src/orders/refund.ts       14    Errors  returns null on failure (rejected, P4)      return a Result, as in billing
src/api/v2/users.ts        3     API     copies the frozen v1 user shape             follow ADR 2026-11-20-code-standard-api

2 findings. Fix them before you open the pull request.
```

With no findings, say the branch follows the standards and stop.

## Advise

`/align-code advise` audits the whole scope of the last `aligned` run, or the whole repo when there is none.

1. Run each area in [survey.md](survey.md) that has a standard, read-only, with survey subagents. Write nothing: they return their tables to the main session.
2. Each variant that is not the standard and carries no marker is drift. Find where it came from: `git log --diff-filter=A -S<the variant's key text>` over the files that hold it. When the first copy came from an older copy, name that file: it is the source the agents copy from.
3. Print the table, worst first, then the summary line.

```text
Sev     Area    Files  Finding                                       Copied from               Fix
high    Errors  6      null on failure is back, 5 in the last 30 d   src/legacy/payments.ts    /align-code new errors-drift, and mark payments.ts
medium  Naming  3      "Manager" suffix again                         src/users/userManager.ts  add a lint rule for the suffix
low     Tests   2      mock-everything style in two new tests          none                      fix in the next change to those files

3 findings: 1 high, 1 medium, 1 low.
```

Severity: `high` for drift that fails a principle and grew in the last 30 days. `medium` for drift that fails a principle. `low` for drift that only breaks consistency.

The Fix cell is one concrete action. After the table, at most three lines of advice no row covers, only with evidence, such as a standard that a lint rule could now enforce.
