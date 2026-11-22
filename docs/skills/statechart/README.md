# statechart

Checks the rules of a flow that must always hold, with TLA+ models. You trigger it with `/statechart`. It never starts on its own.

## Why

Some flows must never reach a bad state: an order paid twice, a refund after a lost dispute, a webhook that overwrites a newer status. Tests cover the cases you thought of. The model checker, TLC, explores every order the events can arrive in, and reports the first order that breaks a rule.

A statechart in prose goes stale like any doc. A model runs on every check, so it cannot drift quietly.

## Layout

```text
docs/statecharts/<subject>/<Name>.tla   the states and rules
docs/statecharts/<subject>/<Name>.cfg   what TLC checks
scripts/statechart.py                   the one command
```

A subject is a flow in the code, such as `payments` or `orders`.

## Commands

| Typed | Does |
| --- | --- |
| `/statechart setup` | Writes the script and the `.gitignore` line. Needs the TLC version and sha256 pin. |
| `/statechart new <subject> <Name>` | Creates a skeleton model. You write the rules. |
| `/statechart run` | Checks every model. Prints only the red ones. Exit 1 if any is red. |
| `/statechart run <subject>` | Checks one subject. |

Needs Java 11+ and Python 3.8+. Commands in a terminal:

- macOS and Linux: `python3 scripts/statechart.py run`
- Windows: `py scripts\statechart.py run`

## What it does not check

The model checks the design, not the code. A model that passes says the design is right. Each rule also needs a test at the HTTP seam, which proves the code does it.

## Rules

- A model changes in the same change as the code it describes.
- A red model is fixed in the design or the code. Never weaken a rule to make it pass.
- The skill never writes a model's rules. You write them, or copy a `.tla` from the repo.
- Its details for the agent are in [SKILL.md](../../../skills/statechart/SKILL.md).
