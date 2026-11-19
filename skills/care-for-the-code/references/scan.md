# Scan

`/care-for-the-code scan [path]` looks for refactor candidates without a ticket. It writes nothing and changes no code.

1. **Scope**: the path, or the 20 files with the most commits in `git log --since=3.months --name-only`.
2. **Walk**: a subagent with a fresh context reads by [check.md](check.md#1-read) and asks the questions in [check.md](check.md#3-ask) for the scope. It returns only the list below.
3. **List** at most 10 candidates, strongest first:

```text
<n>. <module>: <finding>. Source: <source>.
   Before: <shape now, one line>. After: <shape after, one line>.
   Strength: Strong | Worth exploring | Speculative.  Route: ticket | spec.
```

4. **Ask** which one to take. Do not propose interfaces before the person picks one.
5. **Route** the pick by [follow-up.md](follow-up.md). A ticket: write it. A spec: write the brief. Shaping it is the next session's work, with `grilling` and `codebase-design`, or in `/tech-design`.

One candidate per session. A candidate the person rejects for a reason that will hold: offer an ADR.
