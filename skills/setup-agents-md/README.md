# setup-agents-md

How to handle docs in a repo an agent works in. The first five chapters follow Matt Pocock's video ["Delete (most of) your docs"](https://www.youtube.com/watch?v=Fj8DKMbdIzU), in his order. The rest is how this skill puts it into practice. Say "set up AGENTS.md" or type `/setup-agents-md`.

**Part 1: the idea**

1. [The problem](#1-the-problem)
2. [Make the code explain itself](#2-make-the-code-explain-itself)
3. [Why a layer of docs makes it worse](#3-why-a-layer-of-docs-makes-it-worse)
4. [What the code cannot explain](#4-what-the-code-cannot-explain)
5. [Docs are never the source of truth](#5-docs-are-never-the-source-of-truth)

**Part 2: in practice**

6. [What goes in AGENTS.md](#6-what-goes-in-agentsmd)
7. [Decisions that stay true](#7-decisions-that-stay-true)
8. [Home repo or repo](#8-home-repo-or-repo)
9. [With the other nstack skills](#9-with-the-other-nstack-skills)
10. [Commands](#10-commands)

---

## 1. The problem

Many teams write a layer of markdown docs that explains their code, then let the agent rely on those docs instead of the code. It feels helpful. It makes the agent's output worse and costs tokens on every request.

## 2. Make the code explain itself

When an agent explores a repo, the code is what it has to go on. So the code carries the burden. It has to be formatted, sit in the right place, be split into chunks an agent can read, and keep interfaces apart from implementations so the agent takes only what it needs.

| Instead of a doc that says | Do this in the code |
| --- | --- |
| "This 3,000-line file has three parts" | Split it: one concern per file, in the folder where you would look for it. Format it. |
| "How the checkout works" | A small public interface with the implementation behind it. The agent reads the interface, not the 2,000 lines. |
| "This function returns null if the user is not found" | A return type that says so: `User \| null`, or `findUser` vs `getUser` |
| "Orders go through these five states" | A type or enum with those five states, and a test per transition |
| "Call `init()` before `send()`" | Make the wrong order impossible: `send` takes what `init` returns |
| "The payments folder handles Stripe" | Name it `stripe-payments/`, or put it behind a `PaymentProvider` interface |
| "Use this pattern for new endpoints" | One clean example endpoint. Agents follow the patterns they see. |
| "Do not import from `legacy/`" | A lint rule that fails the build |
| "Format with 2 spaces, sort imports" | A formatter, run by a hook or CI |
| "This must stay under 100 ms" | A test that fails when it does not |
| "This edge case exists because of a bank bug" | A short comment on that line that says **why**. A comment for why is fine. A comment for what is noise. |

The rule: **if a compiler, a test, or a linter can check it, put it there.** A doc can only hope to be read. A check runs on every change.

## 3. Why a layer of docs makes it worse

Markdown in the repo is not run and not tested against the code. So it drifts. The doc says one thing, the code says another, and nothing tells you.

Now there are two sources of truth that disagree. The agent cannot tell which one is real. It guesses, and often it picks the doc. A wrong doc is worse than no doc.

Even a correct doc costs something. `AGENTS.md` loads on every request. Every line costs tokens, and the more instructions it holds, the worse the agent follows all of them. Frontier models follow roughly 150 to 200 instructions reliably, and the harness's own system prompt already uses part of that.

## 4. What the code cannot explain

This is not "delete all docs". Some things the code cannot say. Those three stay.

### Decisions: ADRs

Code shows what was built. It cannot show what was considered instead, or why that lost. An architectural decision record (ADR) holds that: the decision, the reason, and the rejected alternatives. Keep them in `docs/adr/`. See [chapter 7](#7-decisions-that-stay-true).

### Domain language: a glossary

Does the agent know what an "order" means in your codebase? Probably not. Is it a cart, a paid cart, a shipment? A glossary says so. Keep it in `GLOSSARY.md`, one line per term, only terms with a meaning special to this project.

```markdown
- **Order**: a paid cart. Before payment it is a cart, not an order.
- **Tenant**: a paying organisation, not a user.
```

### A thin navigation layer

A few lines that name the main parts of the project and what each does. It speeds up the agent's exploration. Keep it in `AGENTS.md`, three to six lines, top-level folders at most. No folder trees and no deep paths: files move, and the agent finds the rest itself.

```markdown
## Shape

- Checkout: cart to payment, in `checkout/`.
- Catalog: products and search, in `catalog/`.
```

## 5. Docs are never the source of truth

The code is the thing you read to understand the code. Docs support it. They never replace it. So delete:

| Delete | Why | Do this instead |
| --- | --- | --- |
| Explanations of how the code works | Goes stale on the next change | [Chapter 2](#2-make-the-code-explain-itself) |
| Folder trees and deep file paths | Files move. The biggest source of drift. | The thin navigation layer |
| Specs, PRDs, and plans for features that shipped | They describe an old intent, not the code | Move the decisions into ADRs. Git keeps the rest. |
| Pasted code snippets | Differ from the code within weeks | Name the module that shows the pattern |
| Style rules | A linter is faster, cheaper, and always right | Linter config, a formatter, or a hook |
| Obvious advice: "write clean code", "be careful" | The agent does it already | Nothing |
| ALL CAPS, "IMPORTANT!!!", "ALWAYS" | Shouting adds noise, not obedience | One plain sentence |
| A rule added after one bad session | They pile up into a ball of mud | Fix the cause: a test, a type, a lint rule |
| Text from `/init` or another generator | Aims for complete, not for useful | Write each line on purpose |

The test for every line: **would the agent do worse without it?** If not, delete it.

---

## 6. What goes in AGENTS.md

From Matt Pocock's [guide to AGENTS.md](https://www.aihero.dev/a-complete-guide-to-agents-md): keep the root file as small as possible, and point at the rest. Aim for under 60 lines.

| Keep | Where | Example |
| --- | --- | --- |
| One sentence on what the project is | `AGENTS.md` | "Storefront for Acme, Next.js, deployed on Vercel." |
| The thin navigation layer | `AGENTS.md` | "Checkout: cart to payment, in `checkout/`." |
| The package manager, when it is not npm and not pinned with corepack | `AGENTS.md` | "Use pnpm." |
| Commands that are not the standard ones | `AGENTS.md` | "Test: `pnpm test:unit`" |
| Rules for every task that no tool can enforce | `AGENTS.md` | "Call the payments API only from the server." |
| One line per topic file | `AGENTS.md` | "Testing: `docs/agents/testing.md`. Read before you write a test." |
| Code standards: conventions no linter checks | `docs/agents/code-standards.md`, created by default | "Return errors as a `Result`, do not throw, in domain code." |
| Rules for one area only | `docs/agents/<topic>.md` | How tests are set up, API conventions |
| A procedure with steps | A skill | Releasing, migrating a database |
| Decisions | `docs/adr/` | "Postgres over MongoDB, because reporting needs joins." |
| Terms | `GLOSSARY.md` | "Order: a paid cart." |

This is progressive disclosure: the root file holds one line per topic, and the agent opens a topic file only when the task needs it.

**Code standards by default.** The AI Hero guide moves language and coding rules out of the root file into their own file, such as `docs/TYPESCRIPT.md`. This skill always proposes one: `docs/agents/code-standards.md`, linked from the root file with "Read before you write or change code." It holds only what no tool checks. A rule a linter can enforce goes into the linter config instead. With more than one language, or past about 50 lines, it splits into one file per language. If the repo already has such a file, the skill points at it and keeps its name.

Claude Code reads `CLAUDE.md`, not `AGENTS.md`. The skill writes a `CLAUDE.md` with one line, `@AGENTS.md`, so the two never differ. In a monorepo, each package gets its own short `AGENTS.md` that the harness merges with the root one.

## 7. Decisions that stay true

An ADR records a decision on a date. It does not describe the code, so a code change does not make it wrong. It can go wrong in two other ways. The video does not cover these. The rules below are nstack's own.

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

## 8. Home repo or repo

With a home repo from `setup-home-repo`:

| Thing | Lives in |
| --- | --- |
| The skills, this one included | The home repo's skills folder, so every repo can use them |
| ADRs, glossary, topic files about a repo's code | That repo. Never the home repo. |
| A design from `tech-design` for one repo | That repo. Start `tech-design` there. |
| A design from `tech-design` that spans repos | The home repo, while it is open. Start `tech-design` there. |
| ADRs about the home repo itself | The home repo |
| A decision that spans repos | Full ADR in the repo that owns the change, a short linking ADR in the others |

A decision belongs next to the code it changes. That is where a reader finds it and where a revert can be checked against it.

A design is different: it is a plan, and a plan for several repos has no single repo to live in. So it may stay in the home repo while it is open. When the feature ships, its decisions move out as ADRs into each repo they change, and the design folder is offered for deletion.

## 9. With the other nstack skills

```text
setup-home-repo          one home for skills, pointers, MCP, hooks
   ↓ trims each child repo's AGENTS.md, adds the pointer to home,
   ↓ and asks: set up AGENTS.md in the child repos too?
setup-agents-md <repo>   makes that AGENTS.md lean, sets up code standards, ADRs, glossary
   ↓
tech-design              one repo: start it there. Several repos: start it in the home repo
   ↓ build
setup-agents-md advise   once shipped: decisions → ADRs, design folder → offered for deletion
```

- **`setup-home-repo`** owns the home repo's `## Repos`, `## Sources`, `## Tools`, and `## Environment`. This skill never touches them. Its advise mode also reports an ADR or glossary in the home repo that belongs to a child repo.
- **`setup-home-repo` asks during setup** whether to run this skill on each child repo, and runs it one repo at a time, each with its own plan. Adding a repo later with `/setup-home-repo add` offers it too.
- **`tech-design`** designs are live while they are `draft`, `discussion`, or `ready`, and while `committed` and not yet shipped. This skill leaves them alone. After the feature ships, each line of Decisions so far becomes an ADR and the folder is offered for deletion. An `abandoned` design leaves one ADR that says what was not built and why.

## 10. Commands

```text
/setup-agents-md               create or trim this repo's AGENTS.md, ADRs, and glossary
/setup-agents-md <repo>        from a home repo: the same, in that repo
/setup-agents-md advise        audit, change nothing
/setup-agents-md help          the card
```

Nothing is written before you approve the plan. Nothing is pushed.

## Sources

- Matt Pocock, "Delete (most of) your docs": https://www.youtube.com/watch?v=Fj8DKMbdIzU. Chapters 1 to 5.
- Matt Pocock, A complete guide to AGENTS.md: https://www.aihero.dev/a-complete-guide-to-agents-md. Chapter 6 and the delete list.
- Matt Pocock, The home repo pattern: https://www.aihero.dev/the-home-repo-pattern
- HumanLayer, Writing a good CLAUDE.md: https://www.humanlayer.dev/blog/writing-a-good-claude-md. The instruction budget and "use a linter, not the agent".

Chapters 7 to 9 are nstack's own. The sources do not cover them.
