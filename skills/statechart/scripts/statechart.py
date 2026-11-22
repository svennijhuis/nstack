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
