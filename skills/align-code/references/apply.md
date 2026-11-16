# Apply

Rewrite the code to match one decided standard at a time. Local branch. Never push.

## Start

1. Status must be `aligned`. If not, run the report gate first.
2. Read the build, test, and lint commands from `AGENTS.md`. None: name `/setup-agents-md` and stop.
3. Branch `align/<name>`, made from the current branch. Stop if the working tree is not clean.
4. The person names a standard, or you take the first by danger. One standard per session.

## One standard

1. Show the list: the standard, its exemplar, and the files under `Changes`. Wait for a yes.
2. Change only those files, to match the exemplar. Behavior, public API, schema, config names, and UI stay as they are. A change that needs one of them to break: stop, and move it to Out of scope.
3. A comments standard: call `comment-root-cause` for each file. If it is missing, say so and name `/setup-nstack-skills`.
4. Run build, test, and lint. Any fail: fix the change or revert it. Never edit a test to make it pass.
5. Call `code-review` on the diff. Fix what it finds.
6. One commit: `align(<area>): <standard>`.
7. Add `Applied: <commit>` to the standard in `align.md`. Log. Stop.

## End

All standards applied: say so, and name the branch. The person reviews and pushes it. Never push.
