# Report gate

Proves every area has a standard and the report can be trusted. Changes no code. Closes no gap.

## Run

1. Walk every check. Print `pass` or `fail` with file, line, and what is wrong. Run all of them, even after a fail.
2. Nothing to check is a fail.
3. Any fail: status unchanged. A missing fact or decision becomes a gap. Say what to run next.

## Checks

### Map

1. `align.md`, `gaps.md`, and `log.md` exist. Every file a gap row links to exists.
2. Every header field has a value.
3. Every area on the Areas list in `align.md` has its section. None is blank. Every seed area in [survey.md](survey.md) is on that list, with its Ask or `n/a: <reason>`.
4. No gap is `open`, `research`, or `waiting-on-input`.
5. Every `accepted-risk` gap has an owner and names the risk.
6. Not yet specified is `None.`
7. No survey is older than the last code commit in scope. Older: run it again.

### Standards

8. Every section is `consistent`, `n/a` with a reason, or a standard with every field.
9. Every exemplar exists in the code. `none` only for a rule of absence, such as comments.
10. Every standard cites a source.
11. No standard changes behavior, a public API, schema, config name, or UI.
12. No two standards contradict. Compare every pair. Print each pair that conflicts.
13. Every file under `Changes` is in exactly one standard.
14. No `TBD`, `TODO`, `???`, or unfilled `<...>`.

## Pass

1. Status `aligned`. `Updated` today.
2. Log. Print the report.

There is no `report anyway`. A gap the person will not decide is closed as `accepted-risk`, with them as owner.
