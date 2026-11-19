# Perf

Too slow, against a number. **Measure before and after, or it did not happen.** The ticket is done when the number is met and the behaviour is the same.

1. Read. Find the number the ticket asks for. None: ask for it.
2. Pin the behaviour of the slow path, as for a refactor.
3. Measure the baseline: the same input, several runs, the median. Keep the command.
4. Find where the time goes: a profile or a timer, not a guess.
5. Try the cheapest fix first and stop when the number is met: do not do it, do it once, do less, do it later, do it cheaper.
6. Measure again with the same command. Inconclusive is not a pass.
7. Review with fresh eyes.
8. Fix.
9. Finish.

**Reply:** the baseline, the result, the change in percent, the command that measured both, the fix and why it is the cheapest that met the number.
