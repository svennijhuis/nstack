# Stored state

The ticket creates, updates, or deletes stored state, or changes a status, and `verify-flow` is installed.

1. After Shape: `verify-flow before <resource>`. Its invariants and planned tests join the ticket's tests.
2. When the feature is green, before the review: `verify-flow after <resource>`.
3. A step `verify-flow` cannot finish (a missing companion): it says so, and you go on.
