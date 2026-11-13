# setup-agents-md

How to handle docs in a repo an agent works in: what to write, what to delete, and why the code should explain itself. The skill applies these rules for you. Say "set up AGENTS.md" or type `/setup-agents-md`.

## The short version

1. **The code is the source of truth.** Make it explain itself.
2. **Docs hold only what the code cannot say:** why something was chosen, what words mean, how to run it, and where to start.
3. **Everything else is deleted.** Git keeps it if you ever need it back.

## Why not docs about the code

A doc that explains the code is a second copy of the truth. The code is run and tested on every change. The doc is not. So the code changes, the doc does not, and now the two disagree.

A person who reads a stale doc gets confused once. An agent reads `AGENTS.md` on every request and believes it. When the doc and the code disagree, the agent cannot tell which one is right, so it guesses, and it often picks the doc. A wrong doc is worse than no doc. Markdown in the repo is not run and not tested against the code, so nothing tells you when it drifts.

There is a cost even when the doc is right. `AGENTS.md` loads on every request. Every line costs tokens, and the more instructions it holds, the worse the agent follows all of them, not only the new ones. Frontier models follow roughly 150 to 200 instructions reliably, and the harness's own system prompt already uses part of that.

## Let the code be the docs

The agent reads code well. Code that explains itself needs no doc beside it, and it cannot drift, because it *is* the thing.

| Instead of a doc that says | Do this in the code |
| --- | --- |
| "This function returns null if the user is not found" | A return type that says so: `User \| null`, or `findUser` vs `getUser` |
| "Orders go through these five states" | A type or enum with those five states, and a test per transition |
| "Call `init()` before `send()`" | Make the wrong order impossible: `send` takes what `init` returns |
| "The payments folder handles Stripe" | Name it `stripe-payments/`, or put it behind a `PaymentProvider` interface |
| "This 3,000-line file has three parts" | Split it into reasonable chunks, one concern per file, in the folder where you would look for it. Format it. |
| "How the checkout works" | A small public interface, with the implementation behind it. The agent reads the interface, not the 2,000 lines |
| "Use this pattern for new endpoints" | One clean example endpoint the agent can copy. Agents follow the patterns they see |
| "Do not import from `legacy/`" | A lint rule that fails the build |
| "Format with 2 spaces, sort imports" | A formatter, run by a hook or CI |
| "This edge case exists because of a bank bug" | A short comment on that line that says **why**. A comment for why is fine. A comment for what is noise. |
| "This must stay under 100 ms" | A test that fails when it does not |

The rule: **if it can be checked by a compiler, a test, or a linter, put it there.** A doc can only hope to be read. A check is enforced on every change.

## What goes in the docs

| Keep | Where | Example |
| --- | --- | --- |
| One sentence on what the project is | `AGENTS.md` | "Storefront for Acme, Next.js, deployed on Vercel." |
| A thin map: the main parts and what each does, three to six lines | `AGENTS.md` | "Checkout: cart to payment, in `checkout/`." |
| The package manager, when it is not npm and not pinned with corepack | `AGENTS.md` | "Use pnpm." |
| Commands that are not the standard ones | `AGENTS.md` | "Test: `pnpm test:unit`" |
| Rules for every task that no tool can enforce | `AGENTS.md` | "Call the payments API only from the server." |
| One line per topic file | `AGENTS.md` | "Testing: `docs/agents/testing.md`. Read before you write a test." |
| Rules for one area only | `docs/agents/<topic>.md` | How tests are set up, API conventions |
| A procedure with steps | A skill | Releasing, migrating a database |
| Why something was chosen, and what was rejected | `docs/adr/` | "Postgres over MongoDB, because reporting needs joins." |
| Words with a project meaning | `GLOSSARY.md` | "Order: a paid cart. Before payment it is a cart, not an order." |

Why these survive: the code shows *what* and *how*. It never shows *why*, what was *rejected*, what a word *means* to the business, or how to *start*.

## What does not

| Delete | Why | Do this instead |
| --- | --- | --- |
| Explanations of how the code works | Goes stale on the next change | Make the code explain itself, see above |
| Folder trees and deep file paths | Files move. The biggest source of drift. | The thin map, top-level folders at most. The agent finds the rest. |
| Specs, PRDs, and plans for features that shipped | They describe an old intent, not the code | Move the decisions into ADRs. Git keeps the rest. |
| Pasted code snippets | Differ from the code within weeks | Name the module that shows the pattern |
| Style rules | A linter is faster, cheaper, and always right | Linter config, a formatter, or a hook |
| Obvious advice: "write clean code", "be careful" | The agent does it already | Nothing |
| ALL CAPS, "IMPORTANT!!!", "ALWAYS" | Shouting adds noise, not obedience | One plain sentence |
| A rule added after one bad session | They pile up into a ball of mud | Fix the cause: a test, a type, a lint rule |
| Text from `/init` or another generator | Aims for complete, not for useful | Write each line on purpose |

The test for every line: **would the agent do worse without it?** If not, delete it.

## Decisions (ADRs)

An ADR records a decision on a date: what was chosen, why, and what was rejected. It does not describe the code, so a code change does not make it wrong. It can go wrong in two other ways:

| Risk | What stops it |
| --- | --- |
| A decision never gets written | `AGENTS.md` tells every agent to write an ADR in the same pull request as the code, and to ask before it finishes: did this change contain a decision? |
| Code gets reverted, the ADR stays | `AGENTS.md` tells agents to add a revert ADR. For people who revert on the GitHub site, an optional CI check fails the pull request until a revert ADR is added. |

Rules for ADRs:

- One file per decision in `docs/adr/`, named `<yyyy-mm-dd>-<slug>.md`. Two agents working at once do not conflict.
- The body stays as merged. Only the status line changes: `Accepted`, `Superseded by <file>`, or `Reverted by <file>`.
- A changed mind is a new ADR that supersedes the old one. A revert is a new ADR that says why. History stays true.
- A git revert deletes the old ADR along with the code. Restore it and set its status to `Reverted by`, so the history keeps both.
- Each ADR names the pull request or commit that made it, so you can check whether that change is still in the code.

## Where docs live: home repo or repo

With a home repo from `setup-home-repo`:

| Thing | Lives in |
| --- | --- |
| The skills, this one included | The home repo's skills folder, so every repo can use them |
| ADRs, glossary, topic files about a repo's code | That repo. Never the home repo. |
| Designs from `tech-design` | The repo the design is about. Start `tech-design` there. |
| ADRs about the home repo itself | The home repo |
| A decision that spans repos | Full ADR in the repo that owns the change, a short linking ADR in the others |

A decision belongs next to the code it changes. That is where a reader finds it and where a revert can be checked against it.

## With the other nstack skills

```text
setup-home-repo          one home for skills, pointers, MCP, hooks
   ↓ trims each child repo's AGENTS.md, adds the pointer to home
setup-agents-md <repo>   makes that AGENTS.md lean, sets up ADRs and the glossary
   ↓
tech-design              start it in the child repo. Designs land in docs/design/
   ↓ build
setup-agents-md advise   once shipped: decisions → ADRs, design folder → offered for deletion
```

- **`setup-home-repo`** owns the home repo's `## Repos`, `## Sources`, `## Tools`, and `## Environment`. This skill never touches them. Its advise mode now also reports an ADR or glossary in the home repo that belongs to a child repo.
- **`tech-design`** designs are live while they are `draft`, `discussion`, or `ready`, and while `committed` and not yet shipped. This skill leaves them alone. After the feature ships, each line of Decisions so far becomes an ADR and the folder is offered for deletion. An `abandoned` design leaves one ADR that says what was not built and why.

## Commands

```text
/setup-agents-md               create or trim this repo's AGENTS.md, ADRs, and glossary
/setup-agents-md <repo>        from a home repo: the same, in that repo
/setup-agents-md advise        audit, change nothing
/setup-agents-md help          the card
```

Nothing is written before you approve the plan. Nothing is pushed.

## Sources

- Matt Pocock, "Delete (most of) your docs": https://www.youtube.com/watch?v=Fj8DKMbdIzU. The keep list (ADRs for the alternatives considered, a glossary for domain language, a thin navigation layer) and the code advice (formatted, well organised, reasonable chunks, interfaces separate from implementations) come from this video.
- Matt Pocock, A complete guide to AGENTS.md: https://www.aihero.dev/a-complete-guide-to-agents-md
- Matt Pocock, The home repo pattern: https://www.aihero.dev/the-home-repo-pattern
- HumanLayer, Writing a good CLAUDE.md: https://www.humanlayer.dev/blog/writing-a-good-claude-md

The ADR, revert, and home repo placement rules are nstack's own. The sources do not cover them.
