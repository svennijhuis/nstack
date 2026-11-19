# Small change

An existing text or value changes, nothing new is added, and no shape signal. New output, a new field, or a new case is a feature. **Small, not careless.** The ticket is done when the change is in, tested, and nothing around it got worse.

1. Read.
2. Say the call: "Fits as it is: <why>." A shape signal fires: this is a feature, switch playbooks. A comment, `TODO`, or suppression on or right above a line you change goes through `comment-root-cause` now, before the change: a shortcut it covers is fixed first, in its own `refactor:` commit.
3. Build test-first: a test that pins the new text or value goes red, then green.
4. Review with fresh eyes, with one reviewer: the design reviewer, also asked for the Standards and Spec questions of `code-review`.
5. Fix.
6. Finish.

**Reply:** what changed, the test that pins it.
