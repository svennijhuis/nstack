---
name: principle-naming
description: Use when you write, review, or refactor code in any language and add or change a name for a variable, function, class, constant, or file. Applies the Clean Code naming principles so every new name shows its intent.
---

Before you add a name, stop and check it against the rules below. Casing (`snake_case`, `camelCase`, `PascalCase`) follows the language and the repo. Never invent a new convention.

Check only names you add or change. Leave other names alone unless the person asks for a path.

## Rules

1. **Reveal intent.** A reader knows what it is, why it exists, and how it is used without reading the code. A name that needs a comment needs a better name.
   `d`, `list1`, `data`, `temp` become `daysSinceCreation`, `activeCustomers`, `unpaidInvoices`.
2. **No abbreviations or encodings.** Write the words out. No type prefixes or noise words (`strName`, `m_count`, `theList`). Well-known short forms (`id`, `url`) are fine.
3. **Pronounceable and searchable.** No single letters outside a tiny loop (`i`). A magic number becomes a named constant (`MAX_RETRIES`, not `5`).
4. **Length follows scope.** Small scope, short name. Public API, module level, and fields get a descriptive name.
5. **One word per concept.** Pick `fetch` or `get` and use it everywhere. Never use one word for two ideas.
6. **Make real distinctions.** No `ProductData` next to `ProductInfo`, no `user1` and `user2`. Two names that differ must mean different things.
7. **Do not mislead.** `accountList` that is not a list, or `isValid` that also saves, lies to the reader.
8. **Use the domain language.** `Invoice`, not `DataRecord`. Use the terms in the repo's glossary when it has one.

## By kind of name

| Kind | Do |
| --- | --- |
| Function, method | A verb phrase for the one thing it does (`calculateTotal`). An "and" or "or" in the name means it does too much: split it. Name what it does, not how. |
| Boolean, predicate | Reads as a yes/no question (`isActive`, `hasPermission`, `canRetry`). Positive form: `isEnabled`, not `isNotDisabled`. |
| Class, type | A noun (`Customer`, `PaymentProcessor`). Avoid `Manager`, `Handler`, `Helper`, `Util` unless it names the real role. |
| Collection | Plural or descriptive (`users`, `orderById`). |
| Constant | The meaning, not the value (`DEFAULT_TIMEOUT_SECONDS`, not `THIRTY`). |
| File, module | The main thing it holds. |

## Workflow

1. At each new name, ask: does it show its intent, and would a new teammate understand it?
2. Match the casing and words already in the code.
3. After you write, read every new or changed name against the rules and rename where needed.
4. A name that is wrong in code you touch: fix it in that area. Do not start a sweeping rename the person did not ask for. An unclear name you cannot fix without a decision (a public API, a name other code depends on): ask the person in one short question.
