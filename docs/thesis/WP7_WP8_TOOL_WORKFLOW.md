# WP7 / WP8 Thesis, Defense, and Delivery Tool Workflow

**Status:** T-716 review-ready composition COMPLETE. `docs/context/TASKS.md` is the only canonical task/dependency ledger.

**Current next academic task:** T-712 only when actual supervisor/reviewer feedback is received. T-713 remains blocked by T-712 where applicable plus authoritative official metadata/declaration and final Word/submission checks.

## Authority hierarchy

1. T-611/T-612/T-613 accepted evidence for experimental/result claims.
2. Synchronized citation-ready `ThesisBibliography` evidence for formal external claims; current consumer snapshot `27674a566ab55e4491b74243fe077a31ef81ae73`.
3. Accepted repository decisions/configs/code for exact methodology/implementation claims.
4. Current verified Department/University guidance for structure/format/submission/defense rules.
5. Actual supervisor/reviewer instructions when supplied.
6. T-701 example-thesis-derived structure/style guidance as context only.
7. Accepted T-716 Word thesis for review/revision, subordinate to the authorities above.

Chat memory and example theses are never sufficient scientific authority.

## Completed WP7 path

- **T-700 COMPLETE:** dated official guidance recheck; no verified ICE-specific defense duration/slide-count/template/live-demo rule was found, so these remain future T-720/T-722 recheck items.
- **T-701 COMPLETE:** reviewed 22 supplied files representing 21 unique theses for structure/style context only; established the seven-chapter architecture and separate Results/Discussion.
- **T-702 COMPLETE:** completed the 2026-09-03 writing-gate freshness review. Its historical snapshot was `ada0d1aec7511098fd12610ae9e5abe7aea875cd` (599/123). Subsequent governed T-716 source work was synchronized normally; current consumer authority is `27674a566ab55e4491b74243fe077a31ef81ae73` at 601 canonical / 129 citation-ready / 19 research-material records / 281 indexed originals.
- **T-710 COMPLETE:** evidence-grounded Greek manuscript and handoff package.
- **T-711 COMPLETE:** real editable Word composition with governed IEEE numeric citations, registered figures/tables and structural/render QA.
- **T-714 COMPLETE:** bounded academic/compliance hardening and front/end-matter/Word QA.
- **T-715 COMPLETE:** bounded reader/audit reconciliation; its compressed DOCX is historical, not the final composition baseline.
- **T-716 COMPLETE:** restored/expanded full-content thesis plus final evidence-aware audit. Accepted review authority is `thesis/archive/T716_stage4_evidence_audited_review_ready.docx`, semantic SHA-256 `b01f853af794e596f0dfb491a3f5401365ca3f01fd7d410194e539f0b8a10cc1`, 25,327 words, 31/31 governed references, 25/25 preserved scientific media and 92-page visual QA. `docs/thesis/T716_FINAL_ACCEPTANCE_AUDIT.md` records 11/11 PASS.

The three remaining front-matter placeholders are deliberate because authoritative official data have not been supplied. They belong to T-713 and must not be invented.

## T-712 — actual supervisor/reviewer correction cycle

Start only from real feedback. For each request preserve a correction ledger containing the request, affected section, disposition/rationale, evidence/citation impact and resulting artifact identity. Revalidate affected claims, references, frozen values and rendered pages. Internal self-review is not T-712 feedback.

## T-713 — final thesis freeze

Inputs: accepted T-716/T-712 content, authoritative official person/institution/declaration text and final Microsoft Word/submission requirements. Update TOC/list/caption/cross-reference/page fields in Word, verify final references/captions/page numbering, produce the required PDF/deposit copy, run final-mode checks that reject placeholders and record exact Word/PDF identities under `thesis/final/`.

## T-720/T-721/T-722 — defense

Recheck current ICE/UNIWA defense rules first. Build the defense narrative strictly from the final thesis and frozen evidence; create a slide-level evidence map; then produce the final `.pptx`, embedded notes and separate Greek spoken script. Quantitative claims use frozen T-613/T-612-derived assets, not screenshots. Validate PowerPoint rendering, timing, media and static/demo fallback before freeze.

## T-800/T-801/T-802 — final audits and delivery

Recheck final bibliography/citations and official guidance; audit reproducibility/privacy/licensing and cross-artifact consistency; then assemble/verify the exact academic delivery package and record submitted artifact identities.

## T-803 — standalone Windows package

Only after the academic deliverable is stable, package the accepted PySide6 application for Windows and validate launch/close/restart/writable paths/privacy/licensing on the intended environment. This is tracked separately under issue #94.

## Manual application media rule

When a thesis/defense screenshot, GIF or video is actually needed, create an `ASSET-APP-*` instruction with exact application state, visible/hide requirements, purpose/placement, provenance and static fallback. Application media illustrate implementation/workflow; they never replace frozen quantitative evidence.
