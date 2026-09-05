#!/usr/bin/env python3
"""Temporary fail-closed T-717 post-merge authority normalizer.

This helper exists only on PR #149. It records T-717 COMPLETE after PR #148
merged and restores T-712 DEFERRED as the real external-feedback gate. Remove this
helper before PR #149 merges.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / "docs/context/TASKS.md"
STATUS = ROOT / "docs/context/CURRENT_STATUS.md"
STATE = ROOT / "docs/context/WORK_STATE.json"
MERGE_SHA = "84b9b1165a64fd9fbd79f25890473d3e624e12d1"
DOCX_SHA = "57d6de352eef6147fa24179f87a3f8e9ee39f65a90ad8b85777cac8f541f57c5"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)


def normalize_tasks() -> None:
    text = TASKS.read_text(encoding="utf-8")
    normalized_current = (
        "- **Current task:** `T-712` is **DEFERRED** pending actual supervisor/reviewer feedback. "
        "T-010, T-716 and T-717 are COMPLETE. T-713 remains downstream of resolved real feedback "
        "plus authoritative official metadata/declaration and final Word/submission gates."
    )
    if normalized_current not in text:
        text = replace_once(
            text,
            "- **Current task:** `T-717` is **IN_PROGRESS** as a bounded author-directed pre-freeze content refinement. `T-712` remains **DEFERRED** pending actual supervisor/reviewer feedback; T-010 and T-716 remain COMPLETE, and T-713 stays downstream of resolved real feedback plus authoritative official metadata/declaration and final Word/submission gates.",
            normalized_current,
            "TASKS current task",
        )
    normalized_next = (
        "- **Exact next action:** wait for actual supervisor/reviewer feedback for `T-712`; do not fabricate "
        "or substitute internal review for external feedback. When real feedback arrives, record it durably, "
        "move T-712 to IN_PROGRESS, incorporate the corrections and revalidate before T-713."
    )
    if normalized_next not in text:
        text = replace_once(
            text,
            "- **Exact next action:** finish `T-717`: persist the reproducible DOCX/QA artifact, claim-evidence registration and all CI gates on `thesis/t717-final-content-refinement`; merge only when green, then normalize the operational pointer back to the real `T-712` external-feedback gate.",
            normalized_next,
            "TASKS exact next action",
        )
    old_task = "- [ ] IN_PROGRESS `T-717` — **Final pre-freeze content refinement after whole-manuscript audit.**"
    new_task = (
        "- [x] `T-717` — **Final pre-freeze content refinement after whole-manuscript audit. COMPLETE via PR #148 / "
        f"`{MERGE_SHA}`.**"
    )
    if new_task not in text:
        text = replace_once(text, old_task, new_task, "TASKS T-717 checklist state")
    old_gate = (
        "  - Persistence gate: archive the generated DOCX and QA JSON under `thesis/archive/`, validate claim evidence and prompt-free continuity, open a PR, review exact diff/check state and squash-merge only when green. After merge, mark T-717 COMPLETE and restore `T-712 DEFERRED` as the operational pointer."
    )
    new_gate = (
        "  - Completion: PR #148 passed the deterministic DOCX/QA, claim-evidence, continuity, documentation and repository gates and was squash-merged as "
        f"`{MERGE_SHA}`. Canonical CI DOCX raw SHA-256 `{DOCX_SHA}`; T-712 DEFERRED is restored as the operational external-feedback gate."
    )
    if new_gate not in text:
        text = replace_once(text, old_gate, new_gate, "TASKS T-717 completion gate")
    TASKS.write_text(text, encoding="utf-8")


def normalize_status() -> None:
    text = STATUS.read_text(encoding="utf-8")
    old_continuity = (
        "- `T-716` remains COMPLETE as the accepted review-ready provenance milestone. **T-717 is IN_PROGRESS** as a bounded author-directed pre-freeze content refinement; `T-712` remains intentionally DEFERRED until actual supervisor/reviewer feedback exists."
    )
    new_continuity = (
        "- `T-716` remains COMPLETE as the accepted review-ready provenance milestone. **T-717 is COMPLETE** as the bounded author-directed pre-freeze content refinement merged through PR #148. The current academic gate is `T-712`, intentionally DEFERRED until actual supervisor/reviewer feedback exists."
    )
    if new_continuity not in text:
        text = replace_once(text, old_continuity, new_continuity, "CURRENT_STATUS continuity state")
    old_milestone = (
        "- **T-717 is IN_PROGRESS.** The approved refinement changes exposition/visual explanation only: AI-agent→RL-agent scope bridge; exact GridWorld/disturbance and authority/data-flow figures; explicit non-sweep severity and single-change/recurrent-disruption limitations; Robust-Gymnasium as governed reference [32]. No experiment, re-analysis or frozen quantitative result/asset change is permitted. The historical development Phase-B screenshot is intentionally excluded."
    )
    new_milestone = (
        "- **T-717 is COMPLETE.** PR #148 was squash-merged as `"
        + MERGE_SHA
        + "`. The final pre-freeze author-directed refinement is archived as `thesis/archive/T717_pre_freeze_content_refined_review_ready.docx` with canonical CI raw SHA-256 `"
        + DOCX_SHA
        + "`, 32/32 governed references used, 25 media with 23/25 prior media byte-identical and only the two intended explanatory figures replaced, and no experiment/re-analysis or frozen quantitative result/asset change. Robust-Gymnasium reference [32]/LIT-018 remains bounded to the perturbation-axis limitation; the historical Phase-B development screenshot remains intentionally excluded."
    )
    if new_milestone not in text:
        text = replace_once(text, old_milestone, new_milestone, "CURRENT_STATUS T-717 milestone")
    old_next = (
        "Finish T-717 reproducible archival/CI integration on `thesis/t717-final-content-refinement`, merge only after all DOCX/claim/continuity/repository gates pass, then mark T-717 COMPLETE and restore T-712 DEFERRED as the operational external-feedback gate. Do not relabel T-717 as supervisor/reviewer feedback."
    )
    new_next = (
        "Wait for actual supervisor/reviewer feedback for `T-712`. Do not relabel T-717 or any internal audit as external feedback. When real feedback arrives, record it in the repository, move T-712 to IN_PROGRESS, incorporate the corrections and revalidate before T-713 finalization."
    )
    if new_next not in text:
        text = replace_once(text, old_next, new_next, "CURRENT_STATUS exact next action")
    STATUS.write_text(text, encoding="utf-8")


def normalize_state() -> None:
    data = json.loads(STATE.read_text(encoding="utf-8"))
    data.update(
        {
            "updated_at_utc": "2026-09-05T21:05:00Z",
            "active_task": "T-712",
            "task_status": "DEFERRED",
            "work_package": "Supervisor/reviewer feedback incorporation and revalidation",
            "branch": "main-after-merge",
            "base_branch": "main",
            "pull_request": 149,
            "phase": "EXTERNAL_GATE",
            "last_completed_checkpoint": (
                "T-717 is objectively complete. PR #148 passed its final four CI gates and was squash-merged as "
                f"{MERGE_SHA}. The deterministic review-ready DOCX is archived with canonical CI raw SHA-256 {DOCX_SHA}; "
                "32/32 references are used, 23/25 prior media are byte-identical, only the two intended explanatory figures changed, "
                "and no experiment, re-analysis, protocol, frozen result, T-612 analysis or T-613 quantitative asset was modified. "
                "PR #149 is the bounded post-merge authority normalization and contains no thesis/scientific change."
            ),
            "next_action": (
                "Wait for actual supervisor/reviewer feedback for T-712. Do not fabricate or substitute internal review for external feedback. "
                "When real feedback arrives, record it durably, create or recover the T-712 implementation branch, move T-712 to IN_PROGRESS, incorporate the corrections and revalidate before T-713."
            ),
            "blockers": ["Actual supervisor/reviewer feedback has not been provided."],
            "completed_substeps": [
                "T-716 accepted review-ready thesis milestone remains immutable and PASS 11/11",
                "T-717 author-directed final pre-freeze refinement completed",
                "T-717 deterministic DOCX/QA archive and permanent builder persisted",
                "LIT-018 bounded Robust-Gymnasium claim governance persisted",
                f"PR #148 squash-merged as {MERGE_SHA}",
                "T-717 changed no protocol, experiment, frozen result, T-612 analysis or T-613 quantitative asset",
                "Post-merge authorities reconciled so T-712 is again the real external-feedback gate",
            ],
            "pending_substeps": [
                "Receive actual supervisor/reviewer feedback",
                "Record the feedback durably and move T-712 to IN_PROGRESS",
                "Incorporate only the actual corrections and revalidate before T-713",
            ],
            "validation": {
                "t716_prior_acceptance": "PASS_11_OF_11",
                "t717_pr_148": f"MERGED_{MERGE_SHA}",
                "t717_canonical_ci_raw_sha256": DOCX_SHA,
                "t717_second_ci_build": "PASS_BYTE_IDENTICAL",
                "t717_references": "PASS_32_OF_32_USED",
                "t717_media_preservation": "PASS_23_OF_25_UNCHANGED_TWO_INTENTIONAL_REPLACEMENTS",
                "t717_final_repository_checks": "PASS_33991594978",
                "t717_final_project_continuity": "PASS_33991594984",
                "t717_final_claim_evidence": "PASS_33991595005",
                "t717_final_t716_stage3": "PASS_33991594992",
                "post_merge_normalization_pr": 149,
                "scientific_results_modified": "NO",
                "new_experiment_or_reanalysis": "NO",
            },
            "resume_rule": (
                "Repository/Git/GitHub evidence overrides chat or model memory. T-717 is complete. T-712 remains DEFERRED until actual supervisor/reviewer feedback is provided; do not manufacture feedback."
            ),
            "notes": [
                "TASKS.md remains the canonical task/dependency ledger; this file is the operational resume pointer.",
                "T-717 was author-directed pre-freeze refinement, not supervisor/reviewer feedback.",
                "T-713 remains downstream of resolved real feedback plus official metadata/declaration and final Word/submission gates.",
                "branch=main-after-merge is the validator-supported transient value for PR #149; after merge WORK_STATE must be changed immediately to branch=main and pull_request=null.",
            ],
        }
    )
    STATE.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    normalize_tasks()
    normalize_status()
    normalize_state()
    print("T-717 post-merge normalization complete and idempotent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
