# Fallbacks

Read once when a companion skill is missing. Say once which are missing, and name `/setup-nstack-skills`. Then follow the rule for each missing one.

| Missing | Do instead |
| --- | --- |
| `codebase-design` | Deep module: a small interface over a lot of behaviour. The deletion test: delete the module in your head; if the complexity does not come back in its callers, it was a pass-through. Size is not the test: a one-function module that two callers would otherwise copy passes. A seam is where tests or adapters swap behaviour from outside; a new function or private helper is not one. Pick the shape that hides the most from its callers. |
| `tdd` | One slice at a time: a failing test through the interface, run it red, then the smallest code that makes it green. |
| `comment-root-cause` | For each comment, `TODO`, `HACK`, or suppression you write or edit, ask: why is it here, and can the code be better? It covers a shortcut or an unfixed cause: reproduce it, fix the cause, delete the comment. A business rule, an outside fact with its source, or true docs: keep it. |
| `code-review` | Run its two reviews yourself as fresh subagents. Standards: the diff against `docs/agents/code-standards.md` and common smells (duplicated code, long function, feature envy, mysterious name). Spec: the diff against the ticket and its spec: missing, partial, or extra behaviour. |
| `diagnosing-bugs` | No fix before a command that goes red on the bug. Then the cause, then a regression test at the right seam, then the fix. |
| `verify-flow` | Skip its steps. Say so once. |

**The wrong `code-review`.** Claude Code ships its own skill with that name. `implement` means Matt Pocock's two-axis review. When the one that loads is not that, treat it as missing.
