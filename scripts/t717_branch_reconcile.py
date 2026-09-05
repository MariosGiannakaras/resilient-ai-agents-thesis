#!/usr/bin/env python3
"""Branch-only reconciliation for the T-717 pre-freeze thesis refinement.

This helper is intentionally temporary. It must be removed before T-717 merges to
main. It moves the durable authorities from the externally gated T-712 state to
T-717 IN_PROGRESS, registers the one new bounded literature claim, and does not
modify protocol/results/experiments.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / "docs/context/TASKS.md"
STATUS = ROOT / "docs/context/CURRENT_STATUS.md"
STATE = ROOT / "docs/context/WORK_STATE.json"
CLAIM_JSON = ROOT / "docs/thesis/claim-evidence-map.json"
CLAIM_TREE = ROOT / "docs/thesis/CLAIM_EVIDENCE_TREE.md"


def replace_once(text: str, pattern: str, replacement: str, label: str, flags: int = 0) -> str:
    new, n = re.subn(pattern, replacement, text, count=1, flags=flags)
    if n != 1:
        raise RuntimeError(f"{label}: expected exactly one match, found {n}")
    return new


def reconcile_tasks() -> None:
    text = TASKS.read_text(encoding="utf-8")
    if "`T-717`" not in text:
        text = replace_once(
            text,
            r"- \*\*Current task:\*\* `T-712` is \*\*DEFERRED\*\* pending actual supervisor/reviewer feedback\. T-010 and T-716 are COMPLETE\. T-713 remains downstream of resolved real feedback plus authoritative official metadata/declaration and final Word/submission gates\.",
            "- **Current task:** `T-717` is **IN_PROGRESS** as a bounded author-directed pre-freeze content refinement. `T-712` remains **DEFERRED** pending actual supervisor/reviewer feedback; T-010 and T-716 remain COMPLETE, and T-713 stays downstream of resolved real feedback plus authoritative official metadata/declaration and final Word/submission gates.",
            "TASKS current task",
        )
        text = replace_once(
            text,
            r"- \*\*Exact next action:\*\* wait for actual supervisor/reviewer feedback for `T-712`; do not fabricate or substitute internal review for external feedback\. When real feedback arrives, record it durably, move T-712 to IN_PROGRESS, incorporate the corrections and revalidate before T-713\.",
            "- **Exact next action:** finish `T-717`: persist the reproducible DOCX/QA artifact, claim-evidence registration and all CI gates on `thesis/t717-final-content-refinement`; merge only when green, then normalize the operational pointer back to the real `T-712` external-feedback gate.",
            "TASKS exact next action",
        )
        block = """- [ ] IN_PROGRESS `T-717` — **Final pre-freeze content refinement after whole-manuscript audit.**\n  - Depends on: `T-716` — satisfied.\n  - User direction: on 2026-09-05 the user requested one final whole-thesis review before content freeze and explicitly authorized only additions that close real gaps without unnecessary expansion. This is internal author-directed work, not supervisor/reviewer feedback and not `T-712`.\n  - Scope: add the bounded AI-agent→RL-agent bridge; replace the two redundant introductory diagrams with an exact held-out GridWorld/disturbance composite and a layered scientific-authority/data-flow figure; state that action-failure `p=0.15` and observation-corruption `p=0.05` are frozen severity points rather than a sweep; add bounded external-validity limitations for severity/frequency and single-change/fixed-horizon versus repeated/recurrent disruptions; register Robust-Gymnasium only for the perturbation-axis limitation.\n  - Explicit exclusions: no new experiment, re-analysis, result plot, estimand, ranking, code listing, pseudocode, uncertainty-quantification subsection or duplicate change-detection theory. The recovered historical Phase-B UI fixture is excluded because `condition_unavailable`/`not-executed` state is not representative thesis illustration material.\n  - Scientific boundary: protocol-v2.1, T-611 evidence, T-612 results and T-613 quantitative assets remain immutable. Of the 25 embedded media, only the two explanatory introductory figures may change; the other 23 must remain byte-identical to T-716.\n  - Reproducibility gate: `scripts/t717_final_content_refinement.py` must regenerate the candidate from `thesis/archive/T716_stage4_evidence_audited_review_ready.docx`, preserving 32/32 used references, 27 SEQ + 3 TOC + 1 PAGE fields, zero comments/tracked changes/unresolved `SRC-*`, the three deliberate administrative placeholders and all frozen scientific sentinels.\n  - Visual gate: 94-page render QA is complete; reproducible-build comparison must retain 92/94 pages pixel-identical to the fully reviewed candidate, with the only intentional visual differences on the two new figure pages.\n  - Persistence gate: archive the generated DOCX and QA JSON under `thesis/archive/`, validate claim evidence and prompt-free continuity, open a PR, review exact diff/check state and squash-merge only when green. After merge, mark T-717 COMPLETE and restore `T-712 DEFERRED` as the operational pointer.\n"""
        text = replace_once(
            text,
            r"(?m)^- \[ \] DEFERRED `T-712` — Incorporate supervisor/reviewer corrections and revalidate\.$",
            block + "- [ ] DEFERRED `T-712` — Incorporate supervisor/reviewer corrections and revalidate.",
            "TASKS insert T-717",
        )
    else:
        required = [
            "- [ ] IN_PROGRESS `T-717`",
            "**Current task:** `T-717` is **IN_PROGRESS**",
            "**Exact next action:** finish `T-717`",
        ]
        missing = [x for x in required if x not in text]
        if missing:
            raise RuntimeError(f"TASKS has partial/stale T-717 reconciliation: {missing}")
    TASKS.write_text(text, encoding="utf-8")


def reconcile_status() -> None:
    text = STATUS.read_text(encoding="utf-8")
    if "**T-717 is IN_PROGRESS.**" not in text:
        text = replace_once(
            text,
            r"- `T-716` remains COMPLETE and immutable as the accepted review-ready thesis milestone\. The current academic gate is `T-712`, intentionally DEFERRED until actual supervisor/reviewer feedback exists\.",
            "- `T-716` remains COMPLETE as the accepted review-ready provenance milestone. **T-717 is IN_PROGRESS** as a bounded author-directed pre-freeze content refinement; `T-712` remains intentionally DEFERRED until actual supervisor/reviewer feedback exists.",
            "CURRENT_STATUS continuity state",
        )
        marker = "- **T-716 is COMPLETE.** Final acceptance is recorded in `docs/thesis/T716_FINAL_ACCEPTANCE_AUDIT.md`:"
        idx = text.find(marker)
        if idx < 0:
            raise RuntimeError("CURRENT_STATUS T-716 milestone marker not found")
        line_end = text.find("\n", idx)
        if line_end < 0:
            raise RuntimeError("CURRENT_STATUS malformed T-716 milestone line")
        insertion = "\n- **T-717 is IN_PROGRESS.** The approved refinement changes exposition/visual explanation only: AI-agent→RL-agent scope bridge; exact GridWorld/disturbance and authority/data-flow figures; explicit non-sweep severity and single-change/recurrent-disruption limitations; Robust-Gymnasium as governed reference [32]. No experiment, re-analysis or frozen quantitative result/asset change is permitted. The historical development Phase-B screenshot is intentionally excluded."
        text = text[: line_end] + insertion + text[line_end:]
        text = replace_once(
            text,
            r"## Exact next action\n\nWait for actual supervisor/reviewer feedback for `T-712`\. Do not relabel internal audits as external feedback\. When real feedback arrives, record it in the repository, move T-712 to IN_PROGRESS, incorporate the corrections and revalidate before T-713 finalization\.\s*$",
            "## Exact next action\n\nFinish T-717 reproducible archival/CI integration on `thesis/t717-final-content-refinement`, merge only after all DOCX/claim/continuity/repository gates pass, then mark T-717 COMPLETE and restore T-712 DEFERRED as the operational external-feedback gate. Do not relabel T-717 as supervisor/reviewer feedback.\n",
            "CURRENT_STATUS exact next action",
            flags=re.DOTALL,
        )
    else:
        for required in ("T-717 reproducible archival/CI integration", "T-712 remains intentionally DEFERRED"):
            if required not in text:
                raise RuntimeError(f"CURRENT_STATUS has partial T-717 reconciliation: missing {required}")
    STATUS.write_text(text, encoding="utf-8")


def reconcile_state() -> None:
    data = json.loads(STATE.read_text(encoding="utf-8"))
    if data.get("active_task") != "T-717":
        raise RuntimeError(f"WORK_STATE must already point to T-717, got {data.get('active_task')!r}")
    data.update(
        {
            "updated_at_utc": "2026-09-05T19:30:00Z",
            "task_status": "IN_PROGRESS",
            "pull_request": 148,
            "phase": "REPRODUCIBLE_BUILD_AND_PR_INTEGRATION",
            "last_completed_checkpoint": (
                "T-717 content/visual refinement is complete locally and reproducible from the accepted T-716 archive. "
                "Full 94-page render QA passed; 92/94 reproducible pages are pixel-identical to the fully reviewed candidate, "
                "with only the two intended explanatory figure pages differing. Structural QA passes at 32/32 references, "
                "25 media with 23/25 prior media byte-identical, 27 SEQ + 3 TOC + 1 PAGE fields, zero comments/tracked changes/SRC residue."
            ),
            "next_action": (
                "Run the branch-only T-717 reconciliation/build workflow to persist canonical TASKS/CURRENT_STATUS/claim governance, "
                "generate and archive the deterministic T-717 DOCX + QA report from T-716, validate continuity/documentation/claim evidence, "
                "then remove the temporary transition helper/workflow and merge PR #148 only when all final checks are green."
            ),
            "blockers": [],
            "completed_substeps": [
                "Whole-manuscript content/visual/bibliography audit completed against accepted T-716",
                "Approved narrow refinement implemented without experiment or result changes",
                "Exact held-out GridWorld/disturbance composite created from frozen protocol facts",
                "Layered scientific/execution/analysis/presentation authority figure created",
                "Historical Phase-B development fixture rejected as misleading screenshot material",
                "AI-agent-to-RL-agent scope bridge added",
                "Fixed-severity-not-sweep and single-change/recurrent-disruption limitations added",
                "Robust-Gymnasium added as thesis reference [32] for the bounded perturbation-axis claim",
                "Word-native Figure 1/Figure 2 SEQ captions and List-of-Figures TOC field restored",
                "94-page visual QA and structural/accessibility QA completed",
                "Deterministic builder reproduced 92/94 pages pixel-identically with differences restricted to the two new figure pages",
                "Draft PR #148 opened early as the durable review surface",
            ],
            "pending_substeps": [
                "Persist T-717 task/status authorities and LIT-018 claim governance",
                "Persist deterministic builder and generated review-ready DOCX/QA archive",
                "Validate claim map, project continuity, documentation consistency and reproducible second build",
                "Inspect exact PR #148 diff/review/check state",
                "Remove branch-only transition helper/workflow and re-run final PR checks",
                "Squash-merge T-717 and normalize main back to T-712 DEFERRED",
            ],
        }
    )
    validation = data.setdefault("validation", {})
    validation.update(
        {
            "t717_reproducible_build": "PASS_94_PAGES_92_PIXEL_IDENTICAL_TWO_INTENTIONAL_FIGURE_PAGES",
            "t717_local_docx": "PASS_CONTENT_STRUCTURE_AND_94_PAGE_VISUAL_QA",
            "word_fields": "PASS_27_SEQ_3_TOC_1_PAGE",
            "references": "PASS_32_OF_32_USED",
            "media_preservation": "PASS_23_OF_25_UNCHANGED_TWO_INTENTIONAL_REPLACEMENTS",
            "comments_tracked_changes": "PASS_ZERO",
            "scientific_results_modified": "NO",
            "new_experiment_or_reanalysis": "NO",
        }
    )
    STATE.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def reconcile_claim_json() -> None:
    data = json.loads(CLAIM_JSON.read_text(encoding="utf-8"))
    data["purpose"] = "Claim-centred evidence registry for accepted T-716 and governed T-717 thesis writing. Citation-ready status is eligibility, not source-of-truth status."
    claims = data.get("claims", [])
    ids = [c.get("id") for c in claims]
    claim = {
        "id": "LIT-018",
        "chapter": "3,6",
        "type": "literature",
        "claim": "Perturbation target/type, application mode, severity and temporal frequency are distinct robustness-evaluation axes; testing one fixed severity/frequency point does not establish behavior over a severity sweep.",
        "formal_sources": ["SRC-A3D907D882"],
        "context_sources": [],
        "single_source_exception_reason": "Robust-Gymnasium is the directly relevant peer-reviewed benchmark source for this specific perturbation-axis taxonomy; the thesis uses it only to delimit external validity, not to import its algorithms or numerical results.",
        "synthesis": "Use Robust-Gymnasium only to motivate separating disturbance type/target, mode, severity and frequency when stating why thesis p=0.15 action failure and p=0.05 observation corruption are two frozen points rather than a severity-response study.",
        "limits": "Do not transfer Robust-Gymnasium rankings, continuous-control results or robustness magnitudes to the thesis GridWorld; the exact thesis probabilities and disturbance semantics remain project authority.",
    }
    if "LIT-018" not in ids:
        pos = next((i + 1 for i, c in enumerate(claims) if c.get("id") == "LIT-017"), None)
        if pos is None:
            raise RuntimeError("claim map missing LIT-017 insertion anchor")
        claims.insert(pos, claim)
    else:
        current = claims[ids.index("LIT-018")]
        if current != claim:
            raise RuntimeError("claim map contains non-canonical LIT-018")
    CLAIM_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def reconcile_claim_tree() -> None:
    text = CLAIM_TREE.read_text(encoding="utf-8")
    text = text.replace("# T-716 claim → evidence tree", "# T-716/T-717 claim → evidence tree", 1)
    text = text.replace(
        "**Status:** accepted T-716 claim/evidence authority; reopen only for governed later revision",
        "**Status:** accepted claim/evidence authority through governed T-717 pre-freeze refinement; later changes require another governed revision",
        1,
    )
    if "`LIT-018`" not in text:
        marker = "## Chapter 3 — Methodology and experimental design\n\n"
        if marker not in text:
            raise RuntimeError("claim tree Chapter 3 marker not found")
        addition = """## Chapter 3 — Methodology and experimental design\n\n### 3.0 Perturbation axes and severity-sweep boundary — `LIT-018`\n\n**Formal:** `SRC-A3D907D882` (Robust-Gymnasium, ICLR 2025).  \n**Synthesis:** perturbation target/type, application mode, severity and temporal frequency are separate experimental axes; use this only to explain why thesis action-failure `p=.15` and observation-corruption `p=.05` are fixed frozen points rather than a severity-response sweep.  \n**Single-source exception:** this is the directly relevant peer-reviewed benchmark source for the narrow taxonomy claim; no algorithmic or numerical result is imported.  \n**Limit:** Robust-Gymnasium uses materially different tasks/algorithms; exact thesis probabilities, disturbance semantics and conclusions remain bounded by project protocol/evidence.\n\n"""
        text = text.replace(marker, addition, 1)
    CLAIM_TREE.write_text(text, encoding="utf-8")


def main() -> int:
    reconcile_tasks()
    reconcile_status()
    reconcile_state()
    reconcile_claim_json()
    reconcile_claim_tree()
    print("T-717 branch reconciliation complete and idempotent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
