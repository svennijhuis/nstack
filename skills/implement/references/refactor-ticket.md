# Refactor ticket

The ticket names the destination. The behaviour stays, so the tests are the contract.

1. Pin the behaviour through the interface the callers use. Run it before you change anything.
2. Shape it: a deeper module, the deletion test, no seam the spec did not name, code where its meaning belongs.
3. Refactor in small green steps until every caller uses the new shape and the old one is gone, or until this expand-contract step is done.
4. The pinning tests pass unchanged. A test you had to change pinned the inside, not the behaviour: say which.
5. Then review, fix, and finish as for any ticket.
