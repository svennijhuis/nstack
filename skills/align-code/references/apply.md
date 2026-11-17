# Apply

Rewrite the code to match one decided standard at a time. Local branch. Never push.

## Start

1. Status must be `aligned`. If not, run the report gate first.
2. Read the build, test, and lint commands from `AGENTS.md`. No build and no test command: name `/setup-agents-md` and stop. Lint is optional: some languages have no built-in linter.
3. Branch `align/<name>`, made from the current branch. Stop if the working tree is not clean.
4. The person names a standard, or you take the first by danger. One standard per session.

## One standard

1. Show the list: the standard, its exemplar, the files under `Changes`, and any linter rule you would add, change, or remove. Wait for a yes.
2. **Linter first.** If the repo already has a linter, check whether it can enforce the standard. If it can, add, change, or remove rules in its config, with a new rule at `error`, only where they enforce or conflict with this standard, and scope a new rule to the files under `Changes` when it would fail elsewhere. The config change goes in the same commit. No linter in the repo, or it cannot enforce the standard: skip this step and the next, and fix by hand (step 4). Never add a linter or a plugin: use only rules the config and its installed plugins already offer. A linter that `AGENTS.md` does not list: use it, and name `/setup-agents-md` to record it.
3. **Run the linter with its fixer.** Fix every warning and error it reports for this standard in the files under `Changes`, with safe fixes only (the linter marks them auto-fixable, and behavior stays the same). Check the diff: a fix that changes behavior, public API, schema, config names, or UI is undone and done by hand.
4. **Fix by hand** what the linter cannot: change the rest of the files under `Changes` to match the exemplar. Behavior, public API, schema, config names, and UI stay as they are. A change that needs one of them to break: stop, tell the person what would break, and find a solution together. Move it to Out of scope only when they say so.
5. Run build, test, and lint when it exists. Any fail: fix the change or revert it. Never edit a test to make it pass.
6. Call `code-review` on the diff. Fix what it finds.
7. One commit: `align(<area>): <standard>`.
8. Add `Applied: <commit hash>` to the standard in `align.md`, and commit that as `align: record <area>`. Log. Stop.

## End

All standards applied: say so, and name the branch. The person reviews and pushes it. Never push.
