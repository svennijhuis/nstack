# The revert check

The Decisions rules in `AGENTS.md` reach only agents. A person who clicks Revert on the GitHub site never reads them. This CI check fails a pull request that reverts a commit which recorded a decision, unless the same pull request adds or changes an ADR that marks the revert.

It finds reverts by the line git writes, `This reverts commit <sha>.` A revert made by hand without that line is not caught. Advise still reports what it can see in the log.

## Install

Offer it in the report when the repo has CI and no such check. The example below is for GitHub Actions. For another CI, keep the script and wrap it in that CI's job format. Write it only on a yes, as a plan row. Set `DOCS` to where the repo keeps its decisions.

`.github/workflows/adr-revert-check.yml`:

```yaml
name: adr-revert-check
on: pull_request

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: A revert of a decision needs a revert ADR
        env:
          BASE: ${{ github.event.pull_request.base.sha }}
          HEAD: ${{ github.event.pull_request.head.sha }}
          DOCS: docs/adr DECISIONS.md
        run: |
          set -euo pipefail
          fail=0
          # Lines this pull request adds to decision files that mark a revert.
          marked=$(git diff "$BASE" "$HEAD" --diff-filter=AM -- $DOCS | grep -E '^\+.*(Reverted by|Reverts:)' || true)
          for c in $(git rev-list "$BASE..$HEAD"); do
            for r in $(git log -1 --format=%B "$c" | sed -n 's/.*This reverts commit \([0-9a-f]\{7,40\}\).*/\1/p'); do
              if git show --name-only --format= "$r" -- $DOCS | grep -q .; then
                if [ -z "$marked" ]; then
                  echo "::error::$c reverts $r, which recorded a decision. Add an ADR with 'Reverts:' and set the old ADR's status to 'Reverted by <file>'."
                  fail=1
                fi
              fi
            done
          done
          exit $fail
```

## How it decides

1. Every commit in the pull request whose message says `This reverts commit <sha>` is a revert.
2. If the reverted commit touched a file under `DOCS`, the revert undoes a decision.
3. The pull request then must add a line with `Reverts:` or `Reverted by` to a decision file. Deleting the old ADR does not count. The history must stay.

A git revert of a change that added an ADR deletes that ADR. The fix in the same pull request: restore the old ADR with its status set to `Reverted by <new file>`, and add the revert ADR.

This was tested on a local repo: a plain revert fails, a revert with both ADRs passes, and a revert of a change with no ADR passes.

## Limits

- A squash merge keeps the `This reverts commit` line only if the pull request's merge message keeps it. GitHub's Revert button writes it in the title and body, so the check sees it in the pull request's own commits before the merge.
- A revert of a change whose ADR came in a separate pull request is not linked by git. The rule that an ADR ships in the same change as its code is what makes this check work.
