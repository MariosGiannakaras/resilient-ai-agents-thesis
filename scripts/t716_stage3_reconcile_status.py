#!/usr/bin/env python3
from pathlib import Path


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding='utf-8')
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f'{path}: expected one match, found {count}: {old[:120]!r}')
    path.write_text(text.replace(old, new), encoding='utf-8')


# Root README: T-716 has moved from READY into active full-content reconstruction/audit.
replace_once(
    Path('README.md'),
    '| **T-716 full-content evidence-aware thesis** | **READY / current academic task** |',
    '| **T-716 full-content evidence-aware thesis** | **IN_PROGRESS — stage-3 full-content milestone archived; final evidence/citation audit remains** |',
)

# Archive ledger: retain exact CI archive identity and semantic package identity.
archive = Path('thesis/archive/README.md')
replace_once(
    archive,
    '| `T715_run98_audit_reconciled_reader_scoped.docx` | T-715 DOCX QA run #98 (`33928822577`) | `e06a466e667359486a86f30c561c42b74b4e209ea28bb8d94c2652c9d36616d1` | ≈12,900 | Audit-reconciled reader-scoped milestone. Scientifically corrected and QA-passing, but **not the final thesis** because the user rejected the excessive compression on 2026-09-05. |',
    '| `T715_run98_audit_reconciled_reader_scoped.docx` | T-715 DOCX QA run #98 (`33928822577`) | `e06a466e667359486a86f30c561c42b74b4e209ea28bb8d94c2652c9d36616d1` | ≈12,900 | Audit-reconciled reader-scoped milestone. Scientifically corrected and QA-passing, but **not the final thesis** because the user rejected the excessive compression on 2026-09-05. |\n'
    '| `T716_stage3_full_content_review_ready.docx` | T-716 stage-3 reconstruction workflow run #1 (`33968319566`) | `364b22543cef75dabcc03a003ad538f8873604e85a234a2d71bdbba1c1f7fe8c` | 25,265 | **Current full-content review milestone.** Reconstructed from T-714, integrates T-715 corrections and the 601/129 bibliography layer; semantic package SHA-256 `b7e3cfb98dfc7a9d5b8fb6309b7a9be90c7c89eccd77ae14be20bbc7d8e31e8e`; 92/92-page visual QA passed. |',
)
replace_once(
    archive,
    'The next complete thesis must not grow the compressed T-715 document with filler. It must restore the fuller academic coverage represented by the T-714 baseline and incorporate the validated T-715 audit corrections, frozen T-611/T-612/T-613 evidence, current bibliography authority, and final formatting/QA gates.',
    'The archived T-716 stage-3 milestone is now the current full-content review baseline. It restores and expands the T-714 academic coverage without growing the compressed T-715 document with filler, while incorporating the validated T-715 audit corrections, frozen T-611/T-612/T-613 evidence and the synchronized 601/129 bibliography authority. T-716 itself remains in progress until the final evidence/citation/content audit and acceptance gates close.',
)

# Compact status summary.
status = Path('docs/context/CURRENT_STATUS.md')
replace_once(
    status,
    '- The archived T-714 run #66 (`70c897dcda432c3bc3f5b66b3714d701fd895c9ed2e6ce8ff14b19bc46f9ba77`) is the current full-content baseline at approximately 20.9k whole-document words. The active academic task is **T-716 — full-content evidence-aware thesis reconstruction/expansion**, integrating useful restored-draft material plus all validated T-715 scientific corrections.',
    '- T-716 remains the active academic task, but its **stage-3 full-content milestone is now archived** as `thesis/archive/T716_stage3_full_content_review_ready.docx`: 25,265 whole-document words, 765 paragraphs, 30/30 used bibliography entries, 25 preserved scientific media items and 92/92-page visual QA. It was reconstructed from the immutable T-714 run #66 baseline and has semantic package SHA-256 `b7e3cfb98dfc7a9d5b8fb6309b7a9be90c7c89eccd77ae14be20bbc7d8e31e8e`. T-714 remains the historical full-content provenance baseline; T-715 remains the scientific-correction overlay.',
)
replace_once(
    status,
    '- Full repository/bibliography audits are retained under `docs/thesis/audits/`, including the 599-source/599-analysis corpus scan and the new multi-source re-audit.',
    '- Full repository/bibliography audits are retained under `docs/thesis/audits/`. The earlier 599-source/599-analysis scan remains historical audit evidence; the final synchronized consumer corpus now contains 601 canonical sources, 129 citation-ready sources, 19 research materials and 281 indexed originals.',
)
replace_once(
    status,
    'The immutable bibliography writing-gate checkout remains `ada0d1aec7511098fd12610ae9e5abe7aea875cd`. Historical label `bibliography-integration-v3` remains prior-snapshot provenance only. Formal final-thesis citations must resolve to the synchronized citation-ready layer. Important analyzed records outside that layer remain visible as promotion candidates; if T-716 requires one formally, it must be promoted upstream in `ThesisBibliography` and re-synchronized rather than bypassed locally. Talks/transcripts may guide discovery/synthesis but cannot independently support exact equations, guarantees or numerical claims.',
    'The immutable bibliography writing-gate consumer snapshot is `27674a566ab55e4491b74243fe077a31ef81ae73`, synchronized and validated at 601 canonical sources, 129 citation-ready sources, 19 research materials and 281 indexed originals. The earlier `ada0d1aec7511098fd12610ae9e5abe7aea875cd` / `bibliography-integration-v3` state is prior-snapshot provenance only. Watkins–Dayan, Sutton 1990, Khetarpal and Padakandla are now formal citation-ready sources; Liu 2025 and Cadet 2025 are scoped supporting formal sources. Talks/transcripts remain discovery/synthesis material only and cannot independently support exact equations, guarantees or numerical claims.',
)
replace_once(
    status,
    'Produce T-716 from the T-714 full baseline plus reconciled restored-draft content, all T-715 scientific corrections, frozen T-611/T-612/T-613 authorities and the validated multi-source claim/evidence tree. Apply the quality-first, recency-aware source-selection policy to every literature claim. Preserve or increase substantive academic coverage without filler, keep every result claim bounded to frozen evidence, and commit each delivered DOCX/QA milestone to `thesis/archive/` before handoff.',
    'Use the archived T-716 stage-3 full-content milestone as the review baseline and execute the final evidence-aware audit: verify every substantive external statement against the claim/evidence registry and citation-ready analyses, verify every quantitative/result statement against frozen T-611/T-612/T-613 authority, remove any unsupported or redundant prose, and rerun structural/scientific/visual QA before deciding whether T-716 itself can be marked complete.',
)

# Canonical task ledger: T-716 is now active with a completed stage-3 checkpoint, not merely READY.
tasks = Path('docs/context/TASKS.md')
replace_once(
    tasks,
    '- **Current task:** `T-716` is **READY** — restore and expand the full-content thesis. T-715 remains COMPLETE as its bounded audit/reconciliation task, but its reader-scoped v27 DOCX is not the final thesis after the user\'s 2026-09-05 rejection of excessive compression. Use the archived T-714 run #66 full-content baseline (approximately 20,925 whole-document words) plus all validated T-715 scientific corrections and current repository authorities. `T-712` remains deferred until actual supervisor/reviewer feedback; `T-713` remains deferred until full-content acceptance and official finalization gates.',
    '- **Current task:** `T-716` is **IN_PROGRESS**. The stage-3 full-content reconstruction is objectively complete and archived at 25,265 whole-document words with 30/30 used references, 25 preserved scientific media items, semantic package SHA-256 `b7e3cfb98dfc7a9d5b8fb6309b7a9be90c7c89eccd77ae14be20bbc7d8e31e8e` and 92/92-page visual QA. T-716 is not yet COMPLETE: the remaining gate is the final claim-by-claim evidence/citation/result-authority audit and acceptance pass. `T-712` remains deferred until actual supervisor/reviewer feedback; `T-713` remains deferred until full-content acceptance and official finalization gates.',
)
replace_once(
    tasks,
    '- **Bibliography:** current immutable writing-gate consumer checkout is upstream SHA `ada0d1aec7511098fd12610ae9e5abe7aea875cd`, synchronized through thesis PR #130 and validated in the integrated repository at 599 canonical sources, 123 citation-ready sources, 19 research materials and 281 indexed originals. Historical SHA `f10afcc41e3e1bd877d884cf7a5ae6b5284046f5` and label `bibliography-integration-v3` remain immutable prior-snapshot provenance only.',
    '- **Bibliography:** current immutable writing-gate consumer checkout is upstream SHA `27674a566ab55e4491b74243fe077a31ef81ae73`, synchronized through thesis PR #143 / merge commit `2b302173be855c914af34555a8470015085662d8` and validated at 601 canonical sources, 129 citation-ready sources, 19 research materials and 281 indexed originals. Earlier SHA `ada0d1aec7511098fd12610ae9e5abe7aea875cd`, historical SHA `f10afcc41e3e1bd877d884cf7a5ae6b5284046f5` and label `bibliography-integration-v3` remain immutable prior-snapshot provenance only.',
)
replace_once(
    tasks,
    '- **Exact next action:** execute `T-716`: produce a substantively complete full-length thesis from the T-714 baseline plus T-715 corrections, without filler or scientific changes; run full DOCX/content/visual QA and commit the exact delivered DOCX plus QA identity to the repository before handoff.',
    '- **Exact next action:** execute the final T-716 evidence-aware audit on the archived stage-3 full-content milestone: claim-by-claim external-source verification, frozen-result/protocol verification, citation/reference consistency, redundancy/unsupported-prose removal, then rerun full DOCX/content/visual QA. Do not start T-712/T-713 until T-716 itself passes these remaining gates.',
)
replace_once(
    tasks,
    '- [ ] READY `T-716` — **Restore and expand the full-content thesis** while preserving validated T-715 audit corrections.',
    '- [ ] IN_PROGRESS `T-716` — **Restore, expand and evidence-audit the full-content thesis** while preserving validated T-715 audit corrections.',
)
replace_once(
    tasks,
    '  - Persistence gate: every user-facing DOCX/PDF/QA milestone must be committed under `thesis/archive/` or `thesis/final/` before handoff; `/mnt/data` and Actions artifacts are transient working copies only.\n  - Acceptance: complete substantive thesis coverage at or above the prior full-manuscript level where justified; current citations/evidence integrated; no invented official metadata; full structural/scientific/visual QA; exact repository-retained deliverable identity/hash.',
    '  - Persistence gate: every user-facing DOCX/PDF/QA milestone must be committed under `thesis/archive/` or `thesis/final/` before handoff; `/mnt/data` and Actions artifacts are transient working copies only.\n  - Stage-3 checkpoint: archived `T716_stage3_full_content_review_ready.docx` has 25,265 words, 765 paragraphs, 30/30 used bibliography entries, 25 preserved scientific media items, semantic package SHA-256 `b7e3cfb98dfc7a9d5b8fb6309b7a9be90c7c89eccd77ae14be20bbc7d8e31e8e` and manual 92/92-page visual QA with no recorded defect.\n  - Remaining gate: perform a final claim-by-claim evidence/citation/result-authority audit on the stage-3 milestone and rerun QA after any correction.\n  - Acceptance: complete substantive thesis coverage at or above the prior full-manuscript level where justified; current citations/evidence integrated; no invented official metadata; full structural/scientific/visual QA; exact repository-retained deliverable identity/hash.',
)

print('T-716 stage-3 status reconciliation complete')
