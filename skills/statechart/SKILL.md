---
name: statechart
description: Use only when the person types /statechart or asks to create, run, or check TLA+ statecharts for a flow. Creates and runs models in docs/statecharts/. Never start it on your own.
disable-model-invocation: true
---

Statecharts are TLA+ models of a flow whose rules must always hold. The person triggers this skill. Do not offer it, and do not start it on your own.

## Commands

| Typed | Does |
| --- | --- |
| `/statechart setup` | Copies `scripts/statechart.py` from this skill's folder into the repo, adds the `.gitignore` line. Asks first for the TLC version and sha256 pin. |
| `/statechart new <subject> <Name>` | Creates a skeleton `docs/statecharts/<subject>/<Name>.tla` and `.cfg`. The person writes the states and rules. |
| `/statechart run` | Runs every model. Prints only the red ones. |
| `/statechart run <subject>` | Runs one subject. |

Needs Java 11 or newer and Python 3.8 or newer. The commands below work on macOS, Linux, and Windows.

- macOS and Linux: `python3 scripts/statechart.py run`
- Windows: `py scripts\statechart.py run`

## Rules

- The skill never writes a model's states or rules. The person writes them, or copies a `.tla` from the repo.
- Never guess the TLC version or the jar's sha256. Ask the person, who reads them from the TLC release page. Until both are filled in `scripts/statechart.py`, `setup` writes nothing and `run` refuses.
- `setup` adds the `.gitignore` line `.cache/`, and nothing else. No CI job.
- A red model is fixed in the design or the code. Never weaken a rule to make it pass.
- A model changes in the same change as the code it describes. Run `run` before you finish.
- Every rule needs a test at the HTTP seam too. The model checks the design, not the code.

## Script

The script is a file: `scripts/statechart.py` in this skill's folder. Setup copies it to the repo's `scripts/statechart.py`. Do not paste it into anything.

Before copying, ask the person for the two pins in the copied file: `VERSION` and `SHA256`. Take them from the repo's existing pin, or from the TLC release page. Never guess them. Until both are filled, `setup` does not copy the file and `run` refuses.

## Review notes

- A `run` on a red model prints the TLC lines that match `Error`, `violated`, or `Deadlock`. A TLC message that uses other words shows only the `RED` line. Read the full TLC output in that case.
