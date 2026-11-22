# Statechart kit

Optional. Offered in the plan when the repo has a flow with states and rules that must always hold: an order, a payment, a refund, a dispute, a webhook that can arrive out of order. Never added by default. Read [README](../../../docs/skills/setup-agents-md/README.md) chapter 11 for the why.

The kit is three things: a folder of TLA+ models, a runner script, and a `just` recipe (or the repo's own task runner) that calls the runner. The skill writes the kit. The models come from the person, from a `tech-design` design, or from `.tla` files already in the repo. The skill never invents a model or a rule.

## When it is offered

- The inventory finds a state machine, a status enum with transitions, or a flow the docs or the person call "states", and the repo has no statechart folder yet. Offer it once, as one plan row, kind `statechart`, action `ask`.
- The person asks for it.
- A `tech-design` design in `docs/design/` lists rules that must hold. Offer it, and name the design.

Ask first, with three answers, the recommended one first:

1. **Local only** (recommended): the folder, the runner, the recipe. No CI job.
2. **Local plus CI job**: the above, plus a path-filtered job in the existing CI file. Java and the jar download make it slow, so it runs only when `docs/statechart/**` or `scripts/statechart` changes.
3. **Folder only**: the folder and its README. No runner, no recipe yet.

A CI change is a row of its own. Never touch a pipeline without the person's yes.

## Where

- An existing folder with `.tla` files: keep its path and its name. Do not move models that other tools link to.
- No folder yet: `docs/statechart/`.
- The repo has a `docs/` layout with another name for design or model material: follow it, and say so in the plan.

## The files

| File | Action | Content |
| --- | --- | --- |
| `docs/statechart/README.md` | Create | How it works, why, the pinned tool, the rule list. Template below. |
| `docs/statechart/<Name>.tla` and `<Name>.cfg` | Copy only | Copy from the repo or the person. Never write one. |
| `scripts/statechart` | Create, executable | The runner below. |
| `justfile` | Append a recipe, or create it | `check-statechart`. If the repo uses `make`, `npm run`, or another task runner, add the matching target instead, and say which. |
| `.gitignore` | Add a line | `.cache/`, the jar's cache folder. |
| An ADR in `docs/adr/` | Create | One ADR: TLC and Java become a checking tool. See the ADR template in [templates.md](templates.md). |
| CI file | Only on option 2 | A job that runs `just check-statechart`, with `paths:` set to `docs/statechart/**` and `scripts/statechart`. |

## The pin

The runner downloads one jar and checks its sha256. The version and the hash come from the repo's existing pin, if it has one, such as a line in the folder's README. Otherwise ask the person for the version and the sha256 from the release page. Never guess a hash. Until the hash is known, write `<sha256 of tla2tools.jar, 64 hex characters>` and mark the row `ask`. A runner with a placeholder hash does not run.

## The runner

Write `scripts/statechart` as below. Fill the two pin lines from the pin above.

```bash
#!/usr/bin/env bash
# Checks every TLA+ model in docs/statechart. Exit 1 when any rule breaks.
set -euo pipefail

here="$(cd "$(dirname "$0")/.." && pwd)"
dir="$here/docs/statechart"
tlc_version="<version, for example 1.7.4>"
tlc_sha256="<sha256 of tla2tools.jar, 64 hex characters>"
jar="$here/.cache/tla2tools-$tlc_version.jar"
url="https://github.com/tlaplus/tlaplus/releases/download/v$tlc_version/tla2tools.jar"

command -v java >/dev/null || { echo "statechart: java is required (JDK 11 or newer)" >&2; exit 2; }

if [ ! -f "$jar" ]; then
  mkdir -p "$(dirname "$jar")"
  curl -fsSL -o "$jar.tmp" "$url"
  mv "$jar.tmp" "$jar"
fi
if ! shasum -a 256 -c <<<"$tlc_sha256  $jar" >/dev/null 2>&1; then
  rm -f "$jar"
  echo "statechart: tla2tools.jar checksum does not match the pin" >&2
  exit 2
fi

status=0
shopt -s nullglob
for spec in "$dir"/*.tla; do
  name="$(basename "$spec" .tla)"
  echo "== $name"
  java -XX:+UseParallelGC -cp "$jar" tlc2.TLC -workers auto -config "$dir/$name.cfg" "$spec" || status=1
done
exit "$status"
```

The `justfile` recipe:

```just
# Check every TLA+ model in docs/statechart. Fails on any broken rule.
check-statechart:
    scripts/statechart
```

## The folder README

Write this file from the template. Fill the rule list from the models and the tests. A rule with no test yet is marked `no test yet`. It is not dropped.

```markdown
# Statechart models

Models of the states this repo must never leave in a bad place. TLC, the model checker from the TLA+ toolset, explores every reachable state of each model and checks each rule. A broken rule fails the run with exit 1.

## Run

    just check-statechart

Needs Java 11 or newer. The first run downloads `tla2tools.jar` into `.cache/` and checks its sha256 against the pin in `scripts/statechart`.

## Why

The code shows what happens. A model shows that the rules hold in every order the events can come in, including the orders no one tested. The model checks the design. It does not read the Rust, Python, or TypeScript code. So each rule also has a test at the HTTP seam, and the table below links the two.

## Rules

| Rule | Model | Test that proves the code |
| --- | --- | --- |
| `<rule in plain words>` | `<Name>.tla` | `<test path>`, or `no test yet` |

## When you change behaviour

When a change alters an action a model describes, change the model in the same pull request, run `just check-statechart`, and check that every rule still holds. Add a rule to this table for each new guard, and a test for it.
```

## Rules for the person to keep

- The model is updated in the same pull request as the code it describes. A model that drifts is worse than none, because it still looks true.
- Each rule has a test at the HTTP seam, and the table links them. The model says the design is right. The test says the code does it.
- A broken rule is fixed in the design or the code, not by weakening the rule.
- Adding a model is a decision. The ADR from the kit covers the tool, not each model.

## Drift check

On `advise`, report: a `.tla` file with no rule row, a rule row whose test path is gone, a `scripts/statechart` whose pin is still the placeholder, and a `docs/statechart/` folder with no recipe. All medium.
