#!/usr/bin/env python3
"""Idempotently reconcile/validate the final T-716 claim registry.

The accepted stage-4 manuscript uses Hamadanian et al. (ICLR 2025) for narrowly scoped
observed-context non-stationarity / forgetting context. The source is citation-ready and
must remain registered in LIT-008/LIT-009. Re-running this script is a no-op once that
state is present apart from deterministic JSON formatting.
"""
from __future__ import annotations

from pathlib import Path
import json
import re

MAP = Path("docs/thesis/claim-evidence-map.json")
TREE = Path("docs/thesis/CLAIM_EVIDENCE_TREE.md")
SOURCE = "SRC-6F4F8BE003"

LIT008_SYNTHESIS = (
    "Use Khetarpal for continual-RL framing, Padakandla for dynamically varying/non-stationary RL taxonomy, "
    "the existing structured/change-process sources to delimit the thesis setting, Hamadanian 2025 as recent primary "
    "evidence for observed-context online non-stationarity/recurring-context adaptation, and Liu 2025 only as a recent "
    "primary example of model-based continual RL with online world models and planning."
)
LIT008_LIMITS = (
    "Structured SNS-MDP convergence does not imply rapid adaptation to the thesis's persistent remap; Hamadanian 2025 "
    "supplies the current exogenous context to the policy and therefore differs from the hidden thesis remap; Liu 2025 "
    "studies a different shared-dynamics/task-switching regime and MPC/world-model method, so neither source serves as "
    "direct Dyna-Q+ or thesis-remap performance evidence."
)
LIT009_SYNTHESIS = (
    "Use plasticity/primacy work as threats-to-validity and mechanism context; use Hamadanian 2025 as recent primary "
    "evidence that catastrophic forgetting and stability–plasticity are deployment concerns in an observed-context "
    "non-stationary online-RL setting, without treating that setting as equivalent to the thesis."
)
LIT009_LIMITS = (
    "Tasks, information assumptions and timescales differ from the small GridWorld; Hamadanian supplies observed context, "
    "and none of these papers establishes that a specific DQN/PPO outcome in the thesis was caused by primacy, forgetting "
    "or plasticity loss."
)


def compact_string_arrays(text: str) -> str:
    """Restore the registry's compact one-line style for keyed arrays of strings."""
    lines = text.splitlines()
    out: list[str] = []
    i = 0
    key_open = re.compile(r'^(\s+)("[^"]+":) \[$')
    string_item = re.compile(r'^\s*("(?:[^"\\]|\\.)*")(,?)$')
    while i < len(lines):
        m = key_open.match(lines[i])
        if not m:
            out.append(lines[i])
            i += 1
            continue
        indent, key = m.groups()
        j = i + 1
        items: list[str] = []
        ok = True
        while j < len(lines) and lines[j].strip() not in {"]", "],"}:
            sm = string_item.match(lines[j])
            if not sm:
                ok = False
                break
            items.append(sm.group(1))
            j += 1
        if ok and items and j < len(lines) and lines[j].strip() in {"]", "],"}:
            suffix = "," if lines[j].strip() == "]," else ""
            out.append(f"{indent}{key} [{', '.join(items)}]{suffix}")
            i = j + 1
        else:
            out.append(lines[i])
            i += 1
    return "\n".join(out) + "\n"


def update_map() -> None:
    data = json.loads(MAP.read_text(encoding="utf-8"))
    claims = {c["id"]: c for c in data["claims"]}
    for cid in ("LIT-008", "LIT-009"):
        if cid not in claims:
            raise RuntimeError(f"missing claim {cid}")
        sources = claims[cid].setdefault("formal_sources", [])
        if SOURCE not in sources:
            sources.append(SOURCE)
    claims["LIT-008"]["synthesis"] = LIT008_SYNTHESIS
    claims["LIT-008"]["limits"] = LIT008_LIMITS
    claims["LIT-009"]["synthesis"] = LIT009_SYNTHESIS
    claims["LIT-009"]["limits"] = LIT009_LIMITS
    rendered = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    MAP.write_text(compact_string_arrays(rendered), encoding="utf-8")


def replace_or_accept(text: str, old: str, new: str) -> str:
    if new in text:
        return text
    if text.count(old) != 1:
        raise RuntimeError(f"claim tree missing expected old/new variant: {old[:100]!r}")
    return text.replace(old, new, 1)


def update_tree() -> None:
    text = TREE.read_text(encoding="utf-8")
    variants = [
        (
            '**Formal:** `SRC-39696F490F`, `SRC-8025C139CE`, `SRC-660560956D`, `SRC-F909CABDEB`, `SRC-95C9DAEE68`, `SRC-70772C0629`, `SRC-0FD9BE81AC`.  ',
            '**Formal:** `SRC-39696F490F`, `SRC-8025C139CE`, `SRC-660560956D`, `SRC-F909CABDEB`, `SRC-95C9DAEE68`, `SRC-70772C0629`, `SRC-0FD9BE81AC`, `SRC-6F4F8BE003`.  ',
        ),
        (
            '**Ranking:** Khetarpal supplies the continual-RL framing; Padakandla supplies dynamically varying/non-stationary RL taxonomy; the existing structured-change sources delimit specific assumptions; Liu 2025 is a recent supporting primary example of model-based continual RL rather than a taxonomy replacement.  ',
            '**Ranking:** Khetarpal supplies the continual-RL framing; Padakandla supplies dynamically varying/non-stationary RL taxonomy; the existing structured-change sources delimit specific assumptions; Hamadanian 2025 supplies recent primary evidence for observed-context online non-stationarity and recurring-context retention; Liu 2025 is a recent supporting primary example of model-based continual RL rather than a taxonomy replacement.  ',
        ),
        (
            '**Compare explicitly:** abrupt persistent changepoint; recurring/structured hidden regimes; continual task streams; re-exploration/forgetting assumptions; online world-model planning under task switches.  ',
            '**Compare explicitly:** abrupt persistent changepoint; recurring/structured hidden regimes; observed exogenous context; continual task streams; re-exploration/forgetting assumptions; online world-model planning under task switches.  ',
        ),
        (
            "**Limit:** the thesis implements a declared persistent-remap/noise family, not a generic model of all non-stationarity. Liu 2025 uses a different shared-dynamics/task-switching regime and MPC/world-model method; it is not evidence about Dyna-Q+ or the thesis remap specifically.",
            "**Limit:** the thesis implements a declared persistent-remap/noise family, not a generic model of all non-stationarity. Hamadanian 2025 supplies current exogenous context to the policy, unlike the hidden thesis remap. Liu 2025 uses a different shared-dynamics/task-switching regime and MPC/world-model method; neither paper predicts Dyna-Q+ or thesis-remap performance.",
        ),
        (
            '**Formal:** `SRC-4C34DF3E17`, `SRC-46CF36BC1E`, `SRC-F909CABDEB`.  ',
            '**Formal:** `SRC-4C34DF3E17`, `SRC-46CF36BC1E`, `SRC-F909CABDEB`, `SRC-6F4F8BE003`.  ',
        ),
        (
            '**Synthesis:** continued learning can face interference/primacy/plasticity problems over long horizons.  ',
            '**Synthesis:** continued learning can face interference/primacy/plasticity problems over long horizons; Hamadanian 2025 adds recent primary evidence for catastrophic forgetting and stability–plasticity in an observed-context online non-stationary setting.  ',
        ),
        (
            "**Limit:** these sources do not predict that DQN/PPO must fail in the thesis's small GridWorld. Liu 2025 is intentionally not added here because its continual-RL retention framing does not directly establish primacy or plasticity degradation.",
            "**Limit:** these sources do not predict that DQN/PPO must fail in the thesis's small GridWorld. Hamadanian 2025 has a materially different observed-context information regime. Liu 2025 remains intentionally outside this claim because its retention framing does not directly establish primacy or plasticity degradation.",
        ),
    ]
    for old, new in variants:
        text = replace_or_accept(text, old, new)
    TREE.write_text(text, encoding="utf-8")


def main() -> None:
    update_map()
    update_tree()
    data = json.loads(MAP.read_text(encoding="utf-8"))
    claims = {c["id"]: c for c in data["claims"]}
    assert SOURCE in claims["LIT-008"]["formal_sources"]
    assert SOURCE in claims["LIT-009"]["formal_sources"]
    print(f"T-716 claim registry reconciliation PASS: {SOURCE} registered in LIT-008/LIT-009")


if __name__ == "__main__":
    main()
