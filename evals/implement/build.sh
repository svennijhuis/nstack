#!/usr/bin/env bash
# Builds one git repo per scenario under <out>. Usage: ./build.sh <out>
set -euo pipefail
out=${1:?usage: build.sh <out dir>}
rm -rf "$out" && mkdir -p "$out/base"
cd "$out/base"
g() { git -c user.name=eval -c user.email=eval@example.com "$@"; }

mkdir -p shop tests docs/adr docs/agents specs
printf '__pycache__/\n.pytest_cache/\n' > .gitignore
cat > AGENTS.md <<'EOF'
# shop

A small order pricing library.

## Commands

- Test: `python3 -m pytest -q`. Run it before you finish a change.

## Read when relevant

- Code standards: `docs/agents/code-standards.md`. Read before you write or change code.
- Terms: `GLOSSARY.md`. Read when a word in the task has a project meaning.
- Decisions: `docs/adr/`. Read before you change something an ADR covers.

## Changes

- Leave the code you touch no worse. Follow the shape it already has. Do not add a second way to do something the code already does.
- When the change needs a refactor to fit, do it first, with the same behaviour. When you commit, the refactor is its own commit before the change.
- Build for the use the code has today. No layer, seam, or option that nothing uses yet.

## Decisions

- When a change makes a real decision, add an ADR in `docs/adr/` in the same change. Use the format of the newest ADR there.
EOF
printf '# Code standards\n\n- Money is in integer cents. Never floats.\n- Public functions have type hints.\n' > docs/agents/code-standards.md
printf '# Glossary\n\n- **Customer**: the person who places an order. Never "client" or "user".\n- **Tier**: the customer'"'"'s loyalty level: `basic`, `silver`, `gold`.\n' > GLOSSARY.md
printf '# One pricing module\n\nStatus: Accepted\n\nAll price rules live in `shop/pricing.py`. We tried one module per rule in 2025; rules drifted apart and nobody could see the full price logic. Keep them in one module.\n' > docs/adr/2026-03-01-one-pricing-module.md
: > shop/__init__.py
cat > shop/pricing.py <<'EOF'
def discount_cents(total_cents: int, tier: str) -> int:
    if tier == "basic":
        return 0
    if tier == "silver":
        return total_cents * 5 // 100
    if tier == "gold":
        return total_cents * 10 // 100
    raise ValueError("unknown tier: " + tier)


def price_cents(total_cents: int, tier: str) -> int:
    return total_cents - discount_cents(total_cents, tier)
EOF
cat > shop/invoice.py <<'EOF'
from shop.pricing import price_cents


def invoice_line(name: str, total_cents: int, tier: str) -> str:
    cents = price_cents(total_cents, tier)
    euros = cents // 100
    rest = cents % 100
    return name + ": EUR " + str(euros) + "." + str(rest).zfill(2)
EOF
cat > shop/receipt.py <<'EOF'
from shop.pricing import price_cents


def receipt_total(total_cents: int, tier: str) -> str:
    cents = price_cents(total_cents, tier)
    return "Total: EUR %d.%02d" % (cents // 100, cents % 100)
EOF
cat > tests/test_pricing.py <<'EOF'
import pytest
from shop.pricing import discount_cents, price_cents


def test_gold_gets_ten_percent():
    assert price_cents(10000, "gold") == 9000


def test_unknown_tier_fails():
    with pytest.raises(ValueError):
        discount_cents(100, "platinum")
EOF
cat > tests/test_invoice.py <<'EOF'
from shop.invoice import invoice_line


def test_invoice_line():
    assert invoice_line("Mug", 1050, "basic") == "Mug: EUR 10.50"
EOF
cat > specs/loyalty-v2.md <<'EOF'
# Spec: loyalty v2

## Implementation Decisions

- Tiers move from strings to a `Tier` enum in `shop/pricing.py`. Migration is expand-contract:
  - Ticket 1 (expand): add the `Tier` enum and make `discount_cents` accept a `Tier` or a string. Callers keep passing strings.
  - Ticket 2: move callers to `Tier`.
  - Ticket 3 (contract): remove string support.

## Testing Decisions

- Agreed seam: `price_cents` and `discount_cents` in `shop/pricing.py`. Test there, nowhere else.
EOF
git init -q && git add -A && g commit -qm initial
cd ..

for s in feature trivial refactor expand adr overbuild; do cp -r base "$s"; done

# bug: invoice cents lose their leading zero
cp -r base bug && (cd bug && sed -i 's/str(rest).zfill(2)/str(rest)/' shop/invoice.py \
  && sed -i 's/1050/1000/; s/EUR 10.50/EUR 10.0/' tests/test_invoice.py && git add -A && g commit -qm "invoice tweak")

# state: orders with a status
cp -r base state && (cd state && cat > shop/orders.py <<'EOF'
_ORDERS: dict[int, dict] = {}


def place_order(order_id: int, total_cents: int) -> None:
    _ORDERS[order_id] = {"total_cents": total_cents, "status": "placed"}


def pay_order(order_id: int) -> None:
    order = _ORDERS[order_id]
    if order["status"] != "placed":
        raise ValueError("only a placed order can be paid")
    order["status"] = "paid"


def order_status(order_id: int) -> str:
    return _ORDERS[order_id]["status"]
EOF
printf 'from shop.orders import order_status, pay_order, place_order\n\n\ndef test_pay_order():\n    place_order(1, 500)\n    pay_order(1)\n    assert order_status(1) == "paid"\n' > tests/test_orders.py
git add -A && g commit -qm orders)

# fix: a feature with a real bug, for the fix step alone
cp -r base fix && (cd fix && printf '\n\ndef bulk_price_cents(items: list[int], tier: str) -> int:\n    total = 0\n    for item in items[1:]:\n        total = total + item\n    return price_cents(total, tier)\n' >> shop/pricing.py \
  && printf '\n\ndef test_bulk_price():\n    from shop.pricing import bulk_price_cents\n    assert bulk_price_cents([0, 2000], "gold") == 1800\n' >> tests/test_pricing.py \
  && git add -A && g commit -qm "feat: bulk price")

# review: a diff with five planted design faults
cp -r base review && (cd review && cat > shop/exporters.py <<'EOF'
from shop.pricing import price_cents


class Exporter:
    def export(self, name: str, cents: int) -> str:
        raise NotImplementedError


class CsvExporter(Exporter):
    def export(self, name: str, cents: int) -> str:
        return name + "," + str(cents)


EXPORTERS = {"csv": CsvExporter()}


def export_line(client_name: str, total_cents: int, tier: str, fmt: str = "csv", pretty: bool = False) -> str:
    cents = price_cents(total_cents, tier)
    return EXPORTERS[fmt].export(client_name, cents)


def export_total(total_cents: int, tier: str) -> str:
    cents = price_cents(total_cents, tier)
    return "EUR %d.%02d" % (cents // 100, cents % 100)
EOF
printf 'from shop.exporters import EXPORTERS, export_line\n\n\ndef test_csv_exporter_class():\n    assert EXPORTERS["csv"].export("Mug", 1050) == "Mug,1050"\n\n\ndef test_export_line():\n    assert export_line("Mug", 1050, "basic") == "Mug,1050"\n' > tests/test_exporters.py
git add -A && g commit -qm "feat: export invoice line as CSV")

# matt: setup-matt-pocock-skills files and a local tracker
cp -r base matt && (cd matt && printf '@AGENTS.md\n\n## Agent skills\n\n### Issue tracker\n\nLocal markdown in .scratch/. See `docs/agents/issue-tracker.md`.\n\n### Domain docs\n\nSingle-context. See `docs/agents/domain.md`.\n' > CLAUDE.md \
  && printf '# Issue tracker\n\nLocal markdown. Each feature is `.scratch/<feature-slug>/`. Tickets are `.scratch/<feature-slug>/issues/<NN>-<slug>.md`. Fetch a ticket by reading that file.\n' > docs/agents/issue-tracker.md \
  && printf '# Domain docs\n\nRead `GLOSSARY.md` and the ADRs in `docs/adr/` for the area you touch. Proceed silently if absent.\n' > docs/agents/domain.md \
  && mkdir -p .scratch/loyalty/issues \
  && printf '# Silver tier gets 7 percent\n\nStatus: ready-for-agent\n\n## What to build\n\nSilver customers get 7%% instead of 5%%.\n\n## Acceptance criteria\n\n- [ ] A silver total of 10000 cents prices at 9300.\n\nBlocked by: none\n' > .scratch/loyalty/issues/02-silver-seven-percent.md \
  && printf '# Gold note\n\nStatus: ready-for-agent\n' > .scratch/loyalty/issues/01-gold-note.md \
  && git add -A && g commit -qm "matt setup and tickets")
cp -r matt advise
cp -r base prompt
cp -r base pbi

# perf: a quadratic duplicate finder
cp -r base perf && (cd perf && printf 'def duplicate_names(names: list[str]) -> list[str]:\n    dups: list[str] = []\n    for i, a in enumerate(names):\n        for b in names[i + 1:]:\n            if a == b and a not in dups:\n                dups.append(a)\n    return dups\n' > shop/catalog.py \
  && printf 'from shop.catalog import duplicate_names\n\n\ndef test_duplicate_names():\n    assert duplicate_names(["a", "b", "a", "c", "b"]) == ["a", "b"]\n' > tests/test_catalog.py \
  && git add -A && g commit -qm catalog)

# comment: a suppression and a TODO that hide floats in money, on a line the ticket edits
cp -r base comment && (cd comment && printf 'from shop.pricing import price_cents\n\n\ndef receipt_total(total_cents: int, tier: str) -> str:\n    cents = price_cents(total_cents, tier) * 1.0  # type: ignore  # TODO: why is this a float?\n    return "Total: EUR %%d.%%02d" %% (cents // 100, cents %% 100)\n' > shop/receipt.py \
  && git add -A && g commit -qm "receipt")
rm -rf base
ls "$out"
