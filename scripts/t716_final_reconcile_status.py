#!/usr/bin/env python3
"""Reconcile canonical project status after the T-716 final acceptance audit passes."""
from pathlib import Path

SEMANTIC='b01f853af794e596f0dfb491a3f5401365ca3f01fd7d410194e539f0b8a10cc1'
RAW='08992272e90b0cae6b457a3f4ce66511cc7c337aeea0b6d3645d632f8d66a7f7'


def replace_once(path: str, old: str, new: str) -> None:
    p=Path(path)
    text=p.read_text(encoding='utf-8')
    count=text.count(old)
    if count != 1:
        raise RuntimeError(f'{path}: expected one match, found {count}: {old[:120]!r}')
    p.write_text(text.replace(old,new,1),encoding='utf-8')

# Human entry point.
replace_once(
    'README.md',
    'The scientific experiment/evidence chain is complete and frozen. The active academic task is **T-716**, a full-content thesis reconstruction/expansion after the T-715 reader-scoped version was rejected as too compressed. T-715 remains an auditable completed composition milestone, but **is not the final thesis**.',
    'The scientific experiment/evidence chain is complete and frozen. **T-716 is now COMPLETE as the review-ready full-content thesis task.** The accepted review milestone is the evidence-audited stage-4 DOCX (25,327 words, 31/31 governed citations, 92-page visual QA). T-712 remains externally gated on actual supervisor/reviewer feedback; T-713 remains the later final-submission freeze for official metadata, accepted feedback and final Word/submission checks.'
)
replace_once(
    'README.md',
    '| **T-716 full-content evidence-aware thesis** | **IN_PROGRESS — stage-3 full-content milestone archived; final evidence/citation audit remains** |',
    '| **T-716 full-content evidence-aware thesis** | **COMPLETE — stage-4 evidence-audited review milestone accepted; 11/11 final acceptance gates PASS** |'
)
replace_once(
    'README.md',
    '| T-713 final thesis freeze | DEFERRED until T-716 acceptance + T-712 + official finalization inputs |',
    '| T-713 final thesis freeze | DEFERRED until T-712 + official metadata/declaration + final Word/submission inputs |'
)
replace_once(
    'README.md',
    'The archived T-714 run #66 is the current full-content baseline (about 20.9k whole-document words). T-716 must restore and improve that coverage, integrate all validated T-715 scientific corrections, use the user-restored older drafts where still correct, and strengthen source support without filler or scientific recomputation.',
    f'The accepted T-716 review authority is `thesis/archive/T716_stage4_evidence_audited_review_ready.docx`: 25,327 whole-document words, 23,273 main-body words to bibliography, 31/31 references used, 25/25 scientific media preserved byte-for-byte and 92-page visual QA. Its semantic OOXML package SHA-256 is `{SEMANTIC}`. T-714 remains the historical full-content baseline and T-715 remains the scientific-correction overlay.'
)
replace_once(
    'README.md',
    '1. **T-716 — Full-content thesis reconstruction and evidence-aware rewrite.** Reconcile T-714, useful older-draft material, T-715 corrections, frozen project evidence and the multi-source claim/evidence map. Produce and archive the exact reviewed DOCX + QA identity.',
    '1. **T-716 — Full-content thesis reconstruction and evidence-aware rewrite — COMPLETE.** Accepted review authority: stage-4 evidence-audited DOCX plus persisted 11/11-gate acceptance report. This review-ready milestone is not yet the T-713 final-submission candidate.'
)

# Compact canonical state.
replace_once(
    'docs/context/CURRENT_STATUS.md',
    '- T-716 remains the active academic task, but its **stage-3 full-content milestone is now archived** as `thesis/archive/T716_stage3_full_content_review_ready.docx`: 25,265 whole-document words, 765 paragraphs, 30/30 used bibliography entries, 25 preserved scientific media items and 92/92-page visual QA. It was reconstructed from the immutable T-714 run #66 baseline and has semantic package SHA-256 `b7e3cfb98dfc7a9d5b8fb6309b7a9be90c7c89eccd77ae14be20bbc7d8e31e8e`. T-714 remains the historical full-content provenance baseline; T-715 remains the scientific-correction overlay.',
    f'- **T-716 is COMPLETE.** Final acceptance is recorded in `docs/thesis/T716_FINAL_ACCEPTANCE_AUDIT.md`: all 11 rewrite-plan gates pass. The accepted review authority is `thesis/archive/T716_stage4_evidence_audited_review_ready.docx` with 25,327 whole-document words, 23,273 main-body words to bibliography, 766 paragraphs, 31/31 governed references used, 25/25 scientific media preserved and 92-page visual QA. Semantic package SHA-256 `{SEMANTIC}`; CI archive raw SHA-256 `{RAW}`. T-714 remains the historical full-content provenance baseline and T-715 the scientific-correction overlay.'
)
replace_once(
    'docs/context/CURRENT_STATUS.md',
    '- `T-712` waits for **actual** supervisor/reviewer feedback; internal audits are not relabelled as external feedback.\n- `T-713` waits for accepted T-716 content, resolved real feedback, authoritative person/declaration metadata and final Microsoft Word fields.',
    '- `T-712` waits for **actual** supervisor/reviewer feedback; internal audits are not relabelled as external feedback. T-716 acceptance satisfies the composition prerequisite but does not fabricate external feedback.\n- `T-713` now has accepted T-716 content but still waits for resolved real feedback, authoritative person/declaration metadata and final Microsoft Word fields/submission-format checks.'
)
replace_once(
    'docs/context/CURRENT_STATUS.md',
    'Use the archived T-716 stage-3 full-content milestone as the review baseline and execute the final evidence-aware audit: verify every substantive external statement against the claim/evidence registry and citation-ready analyses, verify every quantitative/result statement against frozen T-611/T-612/T-613 authority, remove any unsupported or redundant prose, and rerun structural/scientific/visual QA before deciding whether T-716 itself can be marked complete.',
    'Do not reopen T-716 without new evidence or feedback. The next academic action is `T-712` **only when actual supervisor/reviewer feedback exists**. Until then, preserve the accepted T-716 stage-4 review milestone and its acceptance identity; `T-713` remains blocked by real feedback plus authoritative official metadata/declaration and final Word/submission checks.'
)

# Canonical task ledger.
replace_once(
    'docs/context/TASKS.md',
    '- **Current task:** `T-716` is **IN_PROGRESS**. The stage-3 full-content reconstruction is objectively complete and archived at 25,265 whole-document words with 30/30 used references, 25 preserved scientific media items, semantic package SHA-256 `b7e3cfb98dfc7a9d5b8fb6309b7a9be90c7c89eccd77ae14be20bbc7d8e31e8e` and 92/92-page visual QA. T-716 is not yet COMPLETE: the remaining gate is the final claim-by-claim evidence/citation/result-authority audit and acceptance pass. `T-712` remains deferred until actual supervisor/reviewer feedback; `T-713` remains deferred until full-content acceptance and official finalization gates.',
    f'- **Current academic state:** `T-716` is **COMPLETE**. The accepted review authority is `thesis/archive/T716_stage4_evidence_audited_review_ready.docx` (25,327 words; 31/31 governed references used; 25 preserved scientific media; 92 pages; semantic SHA-256 `{SEMANTIC}`), with all 11 final acceptance gates passing in `docs/thesis/T716_FINAL_ACCEPTANCE_AUDIT.md`. `T-712` remains DEFERRED until actual supervisor/reviewer feedback; `T-713` remains DEFERRED until T-712 plus official metadata/declaration and final Word/submission gates.'
)
replace_once(
    'docs/context/TASKS.md',
    '- **Exact next action:** execute the final T-716 evidence-aware audit on the archived stage-3 full-content milestone: claim-by-claim external-source verification, frozen-result/protocol verification, citation/reference consistency, redundancy/unsupported-prose removal, then rerun full DOCX/content/visual QA. Do not start T-712/T-713 until T-716 itself passes these remaining gates.',
    '- **Exact next action:** preserve the accepted T-716 review milestone. Start `T-712` only from actual supervisor/reviewer feedback; do not manufacture or relabel internal review as external feedback. T-713 remains downstream of T-712 plus official metadata/declaration and final Word/submission checks.'
)
replace_once(
    'docs/context/TASKS.md',
    '- [ ] IN_PROGRESS `T-716` — **Restore, expand and evidence-audit the full-content thesis** while preserving validated T-715 audit corrections.',
    '- [x] `T-716` — **Restore, expand and evidence-audit the full-content thesis** while preserving validated T-715 audit corrections. COMPLETE.'
)
replace_once(
    'docs/context/TASKS.md',
    '  - Stage-3 checkpoint: archived `T716_stage3_full_content_review_ready.docx` has 25,265 words, 765 paragraphs, 30/30 used bibliography entries, 25 preserved scientific media items, semantic package SHA-256 `b7e3cfb98dfc7a9d5b8fb6309b7a9be90c7c89eccd77ae14be20bbc7d8e31e8e` and manual 92/92-page visual QA with no recorded defect.\n  - Remaining gate: perform a final claim-by-claim evidence/citation/result-authority audit on the stage-3 milestone and rerun QA after any correction.\n  - Acceptance: complete substantive thesis coverage at or above the prior full-manuscript level where justified; current citations/evidence integrated; no invented official metadata; full structural/scientific/visual QA; exact repository-retained deliverable identity/hash.',
    f'  - Stage-3 checkpoint: archived `T716_stage3_full_content_review_ready.docx` has 25,265 words, 765 paragraphs, 30/30 used bibliography entries, 25 preserved scientific media items, semantic package SHA-256 `b7e3cfb98dfc7a9d5b8fb6309b7a9be90c7c89eccd77ae14be20bbc7d8e31e8e` and manual 92/92-page visual QA with no recorded defect.\n  - Stage-4/final T-716 checkpoint: archived `T716_stage4_evidence_audited_review_ready.docx` has 25,327 words, 766 paragraphs, 31/31 governed references used, 25/25 scientific media preserved, semantic package SHA-256 `{SEMANTIC}`, and 92-page visual QA (79 pixel-identical pages from stage 3 plus manual inspection of all 13 changed pages).\n  - Final acceptance: `docs/thesis/T716_FINAL_ACCEPTANCE_AUDIT.md` records PASS on all 11 `T716_REWRITE_PLAN.md` gates, including citation-ready resolution, claim registration, source precedence, frozen-science/media preservation, DOCX/visual QA and permanent archive identity.\n  - Administrative boundary: three deliberate front-matter placeholders remain for official student/declaration data; these belong to T-713 and were intentionally not invented during T-716.'
)

# Archive authority.
replace_once(
    'thesis/archive/README.md',
    'The archived T-716 stage-4 evidence-audited milestone is now the current full-content review authority. It inherits the stage-3 restoration/expansion of the T-714 academic coverage, preserves all validated T-715 scientific corrections and frozen T-611/T-612/T-613 evidence, and completes the dedicated source-attribution/precedence pass without changing experiments, estimands, results or registered scientific media. T-716 itself remains in progress until the final acceptance audit closes.',
    'The archived T-716 stage-4 evidence-audited milestone is the accepted T-716 full-content review authority. It inherits the stage-3 restoration/expansion of T-714, preserves all validated T-715 corrections and frozen T-611/T-612/T-613 evidence, and completes the source-attribution/precedence pass without changing experiments, estimands, results or registered media. `docs/thesis/T716_FINAL_ACCEPTANCE_AUDIT.md` records PASS on all 11 completion gates. T-716 is therefore COMPLETE; T-713 final-submission freezing remains downstream.'
)

# Turn the execution contract into a retained completed contract without rewriting its criteria.
replace_once(
    'docs/thesis/T716_REWRITE_PLAN.md',
    '**Status:** controlled pre-composition contract',
    f'**Status:** COMPLETE — all 11 acceptance gates passed on 2026-09-05; accepted review semantic SHA-256 `{SEMANTIC}`'
)

# Lifecycle companion: record completion, keep dependency order intact.
replace_once(
    'docs/context/POST_THESIS_LIFECYCLE.md',
    '## T-716 — Full-content evidence-aware thesis\n\nReconstruct and expand the thesis from the T-714 full-content baseline, useful reconciled material in restored historical drafts, all validated T-715 corrections, the frozen T-611/T-612/T-613 evidence chain and the multi-source claim/evidence map.\n\nCompletion requires a substantive full thesis rather than reader-scope compression; unchanged frozen scientific values/media; claim-level source traceability; structural DOCX QA; page-by-page visual QA; and permanent archive of the exact delivered DOCX/QA identity before handoff.',
    f'## T-716 — Full-content evidence-aware thesis — COMPLETE\n\nCompleted on 2026-09-05. Accepted review authority: `thesis/archive/T716_stage4_evidence_audited_review_ready.docx`, semantic SHA-256 `{SEMANTIC}`. The final acceptance audit passes all 11 T-716 gates: substantive full-content coverage, frozen-science/media preservation, claim/citation governance, source precedence, structural/scientific QA, 92-page visual QA and permanent archive identity.\n\nThis completes review-ready scientific/content composition only. T-712 still requires actual supervisor/reviewer feedback; T-713 still owns official metadata/declaration text and final Word/submission-format freezing.'
)

print('T-716 final status reconciliation complete')
