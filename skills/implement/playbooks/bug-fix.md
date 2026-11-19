# Bug fix

Something is broken. **No fix before a red reproduction.** The ticket is done when the cause is fixed, not the symptom.

1. Read.
2. Reproduce with `diagnosing-bugs`: a command that goes red on the bug. The ticket's example does not reproduce: find the case that does, and say so.
3. Find the cause. Confirm it before you fix: `git log` on the files often shows the commit that broke it.
4. Shape the fix. Say the call. A bug that exists because the code does one thing in two places is fixed by moving it to one place: one function both callers use, where its meaning belongs. Copying the working idiom into the broken place still leaves two places.
5. Refactor first: pin the caller that works, then the move, as `refactor:`. Skip when the call says the fix fits.
6. Build the fix test-first. The regression test goes red on the old code. A test that pinned the bug changes on purpose: say so. Commit as `fix:`.
7. Review with fresh eyes.
8. Fix.
9. Finish.

**Reply:** what was broken, the cause and the commit that caused it, the red then green output, where the fix lives and why there.
