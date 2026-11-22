---
name: statechart
description: Use only when the person types /statechart or asks to create, run, or check TLA+ statecharts for a flow. Creates and runs models in docs/statecharts/. Never start it on your own.
disable-model-invocation: true
---

Statecharts are TLA+ models of a flow whose rules must always hold. The person triggers this skill. Do not offer it, and do not start it on your own.

## Commands

| Typed | Does |
| --- | --- |
| `/statechart setup` | Writes `scripts/statechart.py` and the `.gitignore` line. Asks first for the TLC version and sha256 pin. |
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

## The script

`scripts/statechart.py`. Fill the two pin lines first, then write it exactly as below.

```python
#!/usr/bin/env python3
"""TLA+ statecharts. Commands: new, run. Needs Java 11+ and Python 3.8+."""
import hashlib, pathlib, subprocess, sys, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIR = ROOT / "docs" / "statecharts"
VERSION = "<tlc version>"
SHA256 = "<sha256 of tla2tools.jar, 64 hex characters>"
JAR = ROOT / ".cache" / f"tla2tools-{VERSION}.jar"
URL = f"https://github.com/tlaplus/tlaplus/releases/download/v{VERSION}/tla2tools.jar"
RED = ("Error", "violated", "Deadlock")

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def ensure_jar():
    if JAR.exists() and sha(JAR) == SHA256:
        return
    JAR.parent.mkdir(parents=True, exist_ok=True)
    part = JAR.with_suffix(".part")
    urllib.request.urlretrieve(URL, part)
    if sha(part) != SHA256:
        part.unlink()
        sys.exit("tla2tools.jar does not match the pin")
    part.replace(JAR)

def new(subject, name):
    folder = DIR / subject
    folder.mkdir(parents=True, exist_ok=True)
    (folder / f"{name}.tla").write_text(
        f"---- MODULE {name} ----\nEXTENDS Naturals\nVARIABLE state\n"
        'Init == state = "start"\nNext == FALSE\nSpec == Init /\\ [][Next]_state\n====\n')
    (folder / f"{name}.cfg").write_text("SPECIFICATION Spec\n")
    print(f"created {folder / name}.tla and .cfg")

def run(subject):
    specs = sorted((DIR / subject if subject else DIR).rglob("*.tla"))
    if not specs:
        sys.exit("no models found")
    ensure_jar()
    failed = 0
    for spec in specs:
        cmd = ["java", "-cp", str(JAR), "tlc2.TLC", "-workers", "auto",
               "-config", str(spec.with_suffix(".cfg")), str(spec)]
        out = subprocess.run(cmd, capture_output=True, text=True)
        if out.returncode == 0:
            print(f"ok   {spec.relative_to(ROOT)}")
            continue
        failed += 1
        print(f"RED  {spec.relative_to(ROOT)}")
        for line in (out.stdout + out.stderr).splitlines():
            if any(word in line for word in RED):
                print(f"     {line}")
    print(f"{len(specs) - failed} ok, {failed} red")
    return 1 if failed else 0

if __name__ == "__main__":
    args = sys.argv[1:]
    if args[:1] == ["new"] and len(args) == 3:
        new(args[1], args[2])
    elif args[:1] == ["run"]:
        sys.exit(run(args[1] if len(args) > 1 else None))
    else:
        sys.exit("usage: statechart.py new <subject> <Name> | run [subject]")
```

## Review notes

- A `run` on a red model prints the TLC lines that match `Error`, `violated`, or `Deadlock`. A TLC message that uses other words shows only the `RED` line. Read the full TLC output in that case.
