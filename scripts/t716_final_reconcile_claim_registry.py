#!/usr/bin/env python3
"""Reconcile the final T-716 claim registry with the evidence-audited manuscript.

The stage-4 manuscript retained formal use of the peer-reviewed Hamadanian et al. ICLR 2025
source for observed-context non-stationarity, catastrophic forgetting and stability/plasticity.
That source was citation-ready but was omitted from the final machine/human claim registry.
This narrow migration adds it to the two claims its verified analysis actually supports.
The migration is idempotent so it can be rerun safely in PR validation.
"""
from __future__ import annotations

from pathlib import Path
import json

MAP = Path('docs/thesis/claim-evidence-map.json')
TREE = Path('docs/thesis/CLAIM_EVIDENCE_TREE.md')
SOURCE = 'SRC-6F4F8BE003'


def update_map() -> None:
    data=json.loads(MAP.read_text(encoding='utf-8'))
    claims={c['id']:c for c in data['claims']}
    for cid in ('LIT-008','LIT-009'):
        if cid not in claims:
            raise RuntimeError(f'missing claim {cid}')
        sources=claims[cid]['formal_sources']
        if SOURCE not in sources:
            sources.append(SOURCE)

    claims['LIT-008']['synthesis']=(
        'Use Khetarpal for continual-RL framing, Padakandla for dynamically varying/non-stationary RL taxonomy, '
        'the existing structured/change-process sources to delimit the thesis setting, Hamadanian 2025 as recent primary '
        'evidence for observed-context online non-stationarity/recurring-context adaptation, and Liu 2025 only as a recent '
        'primary example of model-based continual RL with online world models and planning.'
    )
    claims['LIT-008']['limits']=(
        "Structured SNS-MDP convergence does not imply rapid adaptation to the thesis's persistent remap; Hamadanian 2025 "
        'supplies the current exogenous context to the policy and therefore differs from the hidden thesis remap; Liu 2025 '
        'studies a different shared-dynamics/task-switching regime and MPC/world-model method, so neither source serves as '
        'direct Dyna-Q+ or thesis-remap performance evidence.'
    )
    claims['LIT-009']['synthesis']=(
        'Use plasticity/primacy work as threats-to-validity and mechanism context; use Hamadanian 2025 as recent primary '
        'evidence that catastrophic forgetting and stability–plasticity are deployment concerns in an observed-context '
        'non-stationary online-RL setting, without treating that setting as equivalent to the thesis.'
    )
    claims['LIT-009']['limits']=(
        "Tasks, information assumptions and timescales differ from the small GridWorld; Hamadanian supplies observed context, "
        'and none of these papers establishes that a specific DQN/PPO outcome in the thesis was caused by primacy, forgetting '
        'or plasticity loss.'
    )
    MAP.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def ensure_replace(text: str, old: str, new: str) -> str:
    old_count=text.count(old)
    new_count=text.count(new)
    if old_count==1 and new_count==0:
        return text.replace(old,new,1)
    if old_count==0 and new_count==1:
        return text
    raise RuntimeError(
        f'expected either one old or one new tree text; old={old_count} new={new_count}: {old[:80]!r}'
    )


def ensure_replace_in_section(text: str, start: str, end: str, old: str, new: str) -> str:
    a=text.find(start)
    if a < 0:
        raise RuntimeError(f'missing section start {start!r}')
    b=text.find(end,a+len(start))
    if b < 0:
        raise RuntimeError(f'missing section end {end!r}')
    section=text[a:b]
    old_count=section.count(old)
    new_count=section.count(new)
    if old_count==1 and new_count==0:
        section=section.replace(old,new,1)
        return text[:a]+section+text[b:]
    if old_count==0 and new_count==1:
        return text
    raise RuntimeError(
        f'expected either one old or one new text in {start!r}; old={old_count} new={new_count}: {old[:80]!r}'
    )


def update_tree() -> None:
    text=TREE.read_text(encoding='utf-8')
    text=ensure_replace(
        text,
        '**Formal:** `SRC-39696F490F`, `SRC-8025C139CE`, `SRC-660560956D`, `SRC-F909CABDEB`, `SRC-95C9DAEE68`, `SRC-70772C0629`, `SRC-0FD9BE81AC`.  ',
        '**Formal:** `SRC-39696F490F`, `SRC-8025C139CE`, `SRC-660560956D`, `SRC-F909CABDEB`, `SRC-95C9DAEE68`, `SRC-70772C0629`, `SRC-0FD9BE81AC`, `SRC-6F4F8BE003`.  '
    )
    text=ensure_replace(
        text,
        '**Ranking:** Khetarpal supplies the continual-RL framing; Padakandla supplies dynamically varying/non-stationary RL taxonomy; the existing structured-change sources delimit specific assumptions; Liu 2025 is a recent supporting primary example of model-based continual RL rather than a taxonomy replacement.  ',
        '**Ranking:** Khetarpal supplies the continual-RL framing; Padakandla supplies dynamically varying/non-stationary RL taxonomy; the existing structured-change sources delimit specific assumptions; Hamadanian 2025 supplies recent primary evidence for observed-context online non-stationarity and recurring-context retention; Liu 2025 is a recent supporting primary example of model-based continual RL rather than a taxonomy replacement.  '
    )
    text=ensure_replace(
        text,
        '**Compare explicitly:** abrupt persistent changepoint; recurring/structured hidden regimes; continual task streams; re-exploration/forgetting assumptions; online world-model planning under task switches.  ',
        '**Compare explicitly:** abrupt persistent changepoint; recurring/structured hidden regimes; observed exogenous context; continual task streams; re-exploration/forgetting assumptions; online world-model planning under task switches.  '
    )
    text=ensure_replace(
        text,
        "**Limit:** the thesis implements a declared persistent-remap/noise family, not a generic model of all non-stationarity. Liu 2025 uses a different shared-dynamics/task-switching regime and MPC/world-model method; it is not evidence about Dyna-Q+ or the thesis remap specifically.",
        "**Limit:** the thesis implements a declared persistent-remap/noise family, not a generic model of all non-stationarity. Hamadanian 2025 supplies current exogenous context to the policy, unlike the hidden thesis remap. Liu 2025 uses a different shared-dynamics/task-switching regime and MPC/world-model method; neither paper predicts Dyna-Q+ or thesis-remap performance."
    )
    start='### 2.6 Plasticity and primacy as threats to continued deep learning — `LIT-009`'
    end='### 2.7 Action uncertainty — `LIT-010`'
    text=ensure_replace_in_section(
        text,start,end,
        '**Formal:** `SRC-4C34DF3E17`, `SRC-46CF36BC1E`, `SRC-F909CABDEB`.  ',
        '**Formal:** `SRC-4C34DF3E17`, `SRC-46CF36BC1E`, `SRC-F909CABDEB`, `SRC-6F4F8BE003`.  '
    )
    text=ensure_replace_in_section(
        text,start,end,
        '**Synthesis:** continued learning can face interference/primacy/plasticity problems over long horizons.  ',
        '**Synthesis:** continued learning can face interference/primacy/plasticity problems over long horizons; Hamadanian 2025 adds recent primary evidence for catastrophic forgetting and stability–plasticity in an observed-context online non-stationary setting.  '
    )
    text=ensure_replace_in_section(
        text,start,end,
        "**Limit:** these sources do not predict that DQN/PPO must fail in the thesis's small GridWorld. Liu 2025 is intentionally not added here because its continual-RL retention framing does not directly establish primacy or plasticity degradation.",
        "**Limit:** these sources do not predict that DQN/PPO must fail in the thesis's small GridWorld. Hamadanian 2025 has a materially different observed-context information regime. Liu 2025 remains intentionally outside this claim because its retention framing does not directly establish primacy or plasticity degradation."
    )
    TREE.write_text(text,encoding='utf-8')


def main() -> None:
    update_map()
    update_tree()
    print(f'T-716 claim registry reconciled/idempotent: {SOURCE} present in LIT-008 and LIT-009')

if __name__=='__main__': main()
