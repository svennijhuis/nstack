# Comments

No comments. The code says what it does.

## Keep only

- **Business or decision why.** One line.
- **Outside constraint.** A vendor, platform, or protocol we cannot change. One line, with a link.
- **Public API doc comment.** An internal export is not public.
- **License header.**
- **Tool directive** with its reason on the same line.

Not sure it fits? It goes in the report as a change.

## Report

Everything else. Explanations, banners, commented-out code, `TODO`, `FIXME`, and any why longer than one line.

## Fix the code, not the comment

- A comment that explains a surprise in our code: rename, extract, type, or test.
- A suppression on a rule that catches bugs: fix the code.
- `IMPORTANT`, `do not remove`: encode it as a test, type, or lint rule. If it is false, drop it.
