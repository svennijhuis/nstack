# Comments

The comments standard is the `comment-root-cause` skill. Call it by name. Never restate its rules here.

## In a survey

- Judge every comment by its "Why is it there?" table. The source is `comment-root-cause`.
- `good`: a business rule, an outside fact with its source, docs, or a tool marker that is true.
- `bad`: a comment that explains what the code does, or covers a shortcut, a workaround, a `TODO`, a suppression with no reason, or a tool marker that is false. A tool marker you cannot confirm has Verdict `unjudged`.
- Count files per kind, not comments.

## In the report

Each `bad` kind is one standard. `Changes` lists the files. The fix is not done here: the person runs `/comment-root-cause <path>`.
