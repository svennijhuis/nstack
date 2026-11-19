# Bug

Before you shape anything:

1. Run `diagnosing-bugs`: a command that goes red on the bug, then the cause.
2. The ticket's example does not reproduce: find the case that does, and say so.
3. Go on from Shape. The fix is shaped like any change.

**A bug caused by duplicated code** is fixed by moving it to one place: one function both callers use, where its meaning belongs. Copying the working idiom into the broken place still leaves two places. Pin the caller that works first, so the move cannot break it. The move is a `refactor:` commit, the fix a `fix:` commit on top.

A test that pinned the bug changes on purpose: say so.
