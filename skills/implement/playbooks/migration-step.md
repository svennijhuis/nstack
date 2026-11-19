# Migration step

One step of an expand-contract plan, from the spec or `to-tickets`. **Do this step, not the plan.** The ticket is done when this step is in and every caller still works.

1. Read. Find the step in the plan, and the steps before and after it.
2. Shape. Say the call. Follow the plan's shape: it outranks your taste.
3. Do the step:
   - **Expand:** add the new shape beside the old. Old callers keep working unchanged. Leave the old shape in place.
   - **Migrate:** move callers to the new shape, a few at a time, each green.
   - **Contract:** no caller of the old shape is left: show it with a search. Then delete the old shape.
4. Build test-first: the new shape through its interface, the old one still pinned until contract.
5. Review with fresh eyes. The old shape left on purpose is not a finding until its contract step.
6. Fix.
7. Finish. Suggest `/blast-radius` on a contract step.

**Reply:** which step of which plan, what the old callers see now, what the next step is.
