# Apply

Rewrite the code to match one decided standard at a time. Local branch. Never push.

## Start

1. Status must be `aligned`. If not, run the report gate first.
2. Read the build, test, and lint commands from `AGENTS.md`. None: name `/setup-agents-md` and stop.
3. Branch `align/<name>`, made from the current branch. Stop if the working tree is not clean.
4. The person names a standard, or you take the first by danger. One standard per session.

## One standard

1. Show the list: the standard, its exemplar, and the files under `Changes`. Wait for a yes.
2. **Linter first.** If the repo already has a linter, check whether it can enforce the standard. If it can, add or update the rule in its config. No linter: skip this step and the next. Never add a linter.
3. **Run the linter with its fixer.** Fix every error and warning it reports in the files under `Changes`.
4. **Fix by hand** what the linter cannot: change the rest of the files under `Changes` to match the exemplar. Behavior, public API, schema, config names, and UI stay as they are. A change that needs one of them to break: stop, tell the person what would break, and find a solution together. Move it to Out of scope only when they say so.
5. A comments standard: call `comment-root-cause` for each file. If it is missing, say so and name `/setup-nstack-skills`.
6. Run build, test, and lint. Any fail: fix the change or revert it. Never edit a test to make it pass.
7. Call `code-review` on the diff. Fix what it finds.
8. One commit: `align(<area>): <standard>`.
9. Add `Applied: <commit>` to the standard in `align.md`. Log. Stop.

## End

All standards applied: say so, and name the branch. The person reviews and pushes it. Never push.
