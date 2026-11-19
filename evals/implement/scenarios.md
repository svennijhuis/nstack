# implement evals

Each scenario tests one rule of [implement](../../skills/implement/SKILL.md). Run them after you change the skill.

## Run

1. `./build.sh <out>` builds one git repo per scenario in `<out>`.
2. Per scenario, start one subagent with a fresh context and the prompt below. A small model is the hard test: if it follows the skill, a larger one will.
3. Check that the agent picked the playbook in the Playbook column, copied its steps to a todo list, and read only that playbook and the references it needs (a missing companion means `fallbacks.md`).
4. Check the result against Pass, by its git log, its files, and its report. Run the repo's tests yourself: never take the report's word for it.

## Prompt

Fill in `<repo>`, `<ticket>`, and the companion line.

```text
You are implementing a ticket in a git repo. Follow the skill in <nstack>/skills/implement/SKILL.md exactly (read it first, plus any file it links under its references/). Its companion skills are NOT installed; follow the skill's fallback rules for that.

Repo: <out>/<repo> (work only inside it; cd into it in every command). Commit with: git -c user.name=agent -c user.email=agent@example.com commit ...
There is no human available. If the skill says to ask the person, write the question in your final report and stop at that point.

Ticket: <ticket>

When done, report: each step of the skill you did and what you decided, every commit (git log --oneline), test results, the safety fact with the tests named, whether you suggested /blast-radius and why, how you proved it works, what you saw outside the ticket, any question you would ask, the playbook you picked, and the list of skill files you read.
```

## Scenarios

| Repo | Ticket | Playbook | Pass |
| --- | --- | --- | --- |
| `feature` | "Add a platinum tier for customers: 15% discount." | feature | The call said before the code ("Refactor first: ..."). A `refactor:` commit first that replaces the `if` chain (a table or a map), the tests green on it. Then the feature commit. `GLOSSARY.md` lists platinum. The test that used `platinum` as the unknown tier is changed and named, not asked about. |
| `trivial` | "The error for an unknown tier should start with a capital letter: 'Unknown tier: <tier>'." | small-change | One commit. No refactor. A red test first. |
| `refactor` | "Refactor: invoice.py and receipt.py format money in two different ways. Make it one way. No behaviour change." | refactor | One formatting function in its own module (not in `pricing.py`: the ADR is about price rules). Both callers use it. Pinning tests written first and passing unchanged. `specs/loyalty-v2.md` named as not this ticket's spec. |
| `expand` | "Ticket 1 of specs/loyalty-v2.md: add the Tier enum (expand step)." | migration-step | A `Tier` enum in `shop/pricing.py`. Strings still work. Callers unchanged. Tests only at the spec's seam. String support not removed. |
| `adr` | "pricing.py will grow. Move each tier's discount rule into its own module under shop/rules/." | refactor or feature | No code change and no commit. One question that names the ADR and gives the options. |
| `overbuild` | "Add a way to export an invoice line as CSV: `name,cents`. We might want JSON later too." | feature | One plain function. No exporter class, no registry, no format parameter, nothing for JSON. |
| `bug` | "Invoice lines show 'EUR 10.5' for a 1005-cent item. It should be 'EUR 10.05'." | bug-fix | A red reproduction before any fix. The receipt pinned first. Then money formatting in one place that both callers use, not the working idiom copied into the invoice. A `refactor:` commit and a `fix:` commit, or one `fix:` commit. |
| `state` | "Customers can cancel an order. A placed or paid order can be cancelled; a cancelled order cannot be paid." Install `verify-flow` and say where it is. | feature + stored-state | `verify-flow before` after the shape, with a triage line. `after` once green, before the review. A missing companion of `verify-flow` stops only that step. The real functions run from a script. |
| `comment` | "The receipt should say 'Grand total' instead of 'Total'." | feature or small-change | The `* 1.0`, the `# type: ignore`, and the `TODO` are gone: the cause is fixed (money stays integer cents), not the comment kept. The receipt output is the same apart from the word. |
| `perf` | "duplicate_names is too slow: about 0.2 s for 5,000 names. It must take under 20 ms for 5,000 names." | perf | A baseline measured with a command, the behaviour pinned (the order of the duplicates), a fix with a set, the same command measured after, the numbers and the percent in the reply. |
| `matt` | The person typed: "/implement 02" | small-change | The ticket found in `.scratch/loyalty/issues/02-*.md` and its title said. One literal changed, with a red test first. The safety fact names real tests. `/blast-radius` suggested, with what could rely on the silver price. The summary names what it saw outside the ticket, or says none. |

## Single steps

| Repo | Prompt | Pass |
| --- | --- | --- |
| `fix` | Do only steps 6 and 7. Ticket: "Add bulk_price_cents(items, tier)". Start commit: the first commit. Findings: (1) bug: the discount is applied per item, not on the sum; (2) bug: the loop skips the first item; (3) the loop reimplements `sum()`; (4) `shop/receipt.py` formats money differently from `shop/invoice.py`. | (1) tested, does not fail, dropped and named. (2) a failing test first, then fixed, the test kept. (3) fixed. (4) named, not fixed: outside the ticket's files. |
| `review` | A subagent with only [design-review.md](../../skills/implement/references/design-review.md), the diff from the first commit, the ticket "Add a way to export an invoice line as CSV: name,cents.", and the paths to the docs. | It finds all five planted faults: the one-class `Exporter` hierarchy, the registry and `fmt` with one entry, the unused `pretty`, `client_name` against the glossary, the copied money formatting. Plus the test that reads `EXPORTERS`. |

## setup-agents-md

| Repo | Prompt | Pass |
| --- | --- | --- |
| `advise` | Run `/setup-agents-md advise` on the repo. Assume Claude Code 2.1.290. | No finding on `CLAUDE.md` with its `## Agent skills` block, on `docs/agents/issue-tracker.md`, or on `docs/agents/domain.md`. |

## What these do not test

- The real companions: `tdd`, `code-review`, `diagnosing-bugs`, `verify-flow` with `statechart`. Every run uses the fallback rules.
- The fresh-context review from inside `implement`, when the subagent cannot start subagents of its own. The `review` scenario tests the reviewer alone.
