# Finish

The summary the person reads, after the playbook's Reply line. A few lines each, in short declarative sentences. Give each claim its evidence, or label it inferred or guess. Never hand the person a check you could run yourself.

1. **The playbook** you picked, and **the call** you said before the code.
2. **The safety fact**: the one fact the change is safe because of (for a refactor: the pinning tests pass unchanged), how you proved it, or that you could not. Name the tests by name. Claim only tests that exist. Name the real run and its output.
3. **`/blast-radius`.** Suggest it when the change alters something code or systems outside the tests could rely on: a public signature or output, a set of allowed values, a stored value or schema, a wire format, a feature flag. Also when the ticket asked for it: the ticket chose the change, not its reach. Say in one line what could rely on it. Not for a change nothing outside can see: a new function nothing calls yet, a refactor with the same output.
4. **Findings**: fixed, not fixed and why, dropped and why.
5. **What you saw**: at most three places outside the ticket where a module should be deeper or tests are missing. `<file>: <what>. Strength: Strong | Worth exploring | Speculative.` No file, no ticket, no fix. None: say none.
6. **Decided, not asked**: each choice the person may overrule.
