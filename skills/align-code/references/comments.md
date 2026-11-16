# Comments

No comments. The code says what it does.

## Keep only

- **Business or decision why.** One line. A decision with rejected options gets an ADR, and the line names it.
- **Outside constraint.** A vendor, platform, or protocol we cannot change. One line, with a link.
- **Public API doc comment.**
- **License header.**
- **Marker** from [contracts.md](contracts.md).
- **Tool directive** with its reason on the same line.

Not sure it fits? Delete it.

## Delete

Everything else. Explanations, banners, commented-out code, `TODO`, `FIXME`, and any why longer than one line.

## Fix, never comment

- A comment that explains a surprise in our code: delete it, fix the code. Rename, extract, type, or test. One `mid` ticket.
- A suppression on a rule that catches bugs: delete it, fix the code. One `mid` ticket.
- `IMPORTANT`, `do not remove`: encode it as a test, type, or lint rule, then delete it. If it is false, delete it.

## In the rollout

Deletes run in the comments wave, model `cheap`. No ticket adds a comment that explains code. Review, `check`, and `advise` flag every one.
