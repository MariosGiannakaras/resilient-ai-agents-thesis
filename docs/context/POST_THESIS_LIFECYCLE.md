# Post-thesis lifecycle

**Status:** canonical companion to `TASKS.md` for the work that follows review-ready thesis composition  
**Date:** 2026-09-05

This file exists so downstream academic/delivery work cannot disappear when the repository enters a writing-heavy phase. `TASKS.md` remains the canonical dependency ledger; this document explains the retained sequence and acceptance boundary for each downstream package.

## T-716 — Full-content evidence-aware thesis — COMPLETE

Completed on 2026-09-05. Accepted review authority: `thesis/archive/T716_stage4_evidence_audited_review_ready.docx`, semantic SHA-256 `b01f853af794e596f0dfb491a3f5401365ca3f01fd7d410194e539f0b8a10cc1`. The final acceptance audit passes all 11 T-716 gates: substantive full-content coverage, frozen-science/media preservation, claim/citation governance, source precedence, structural/scientific QA, 92-page visual QA and permanent archive identity.

This completes review-ready scientific/content composition only. T-712 still requires actual supervisor/reviewer feedback; T-713 still owns official metadata/declaration text and final Word/submission-format freezing.

## T-712 — Actual supervisor/reviewer corrections

Input gate: real supervisor or reviewer feedback on a usable full-content thesis. Internal audits, automated QA and self-review do not count as T-712 feedback.

For every requested change, preserve a correction ledger: request, affected section, resolution, evidence/citation impact, accepted/rejected rationale and resulting artifact identity.

## T-713 — Final thesis freeze

Input gates: accepted full-content thesis, T-712 resolved where applicable, authoritative student/person/institution metadata, authoritative declaration wording, and final Microsoft Word field updates.

Freeze the final editable Word thesis and submission PDF, verify TOC/list/cross-reference/page-number fields, references, captions, final official requirements and exact checksums. `thesis/final/` is reserved for this accepted submission candidate.

## T-720 — Defense narrative and evidence map

Recheck current ICE/UNIWA defense-specific requirements rather than borrowing rules from other departments. Build the defense storyline from the frozen thesis and evidence: problem → research questions → design → implementation → results → interpretation → limitations → contribution.

Create a slide-level evidence map so every numerical/result claim has an accepted source artifact and every external claim resolves through the final bibliography.

## T-721 — Final PowerPoint and speaker material

Produce the actual defense deck plus speaker notes/script. Use frozen quantitative assets, authentic application illustrations where useful and readable backup/static material for anything otherwise dependent on live software.

The deck must not introduce new estimands, post-hoc rankings or uncited claims that do not exist in the final thesis/evidence.

## T-722 — Rehearsal and defense validation

Validate current presentation-duration/file/demo rules, timing, visual readability, slide/notes synchronization, charts/tables, media playback and live-demo fallback. Essential scientific conclusions must remain communicable if the live application cannot be demonstrated.

## T-800 — Final bibliography, citation and official-guidance audit

Recheck bibliography freshness and citation-ready status after the thesis/deck are stable. Validate every final external claim/citation, bibliography identity and current official submission/defense guidance. Resolve any stale URL/publication metadata only through bibliography governance.

## T-801 — Reproducibility, privacy, licensing and consistency audit

Audit repository, thesis, defense, final figures/tables, application screenshots/assets and distributable files together. Check reproducibility instructions, hashes/lineage, sensitive/local information, third-party licenses, attribution and consistency between prose and evidence.

## T-802 — Academic delivery readiness

Assemble and verify the required academic delivery package: final Word/PDF, administrative/deposit requirements, any required declarations/forms, filenames, metadata and final checklist. Record exact submitted artifact identities.

## T-803 — Standalone Windows package

Only after the academic deliverable is stable, produce the clean standalone Windows application package. Re-run packaging/runtime checks on the intended Windows environment, include only required runtime/resources and preserve the scientific boundary that the UI presents/executes validated workflows but does not replace frozen evidence.

## Dependency summary

```text
T-716 full-content thesis
   └── external review arrives -> T-712 corrections
          └── official metadata/Word-field gates -> T-713 final thesis freeze
                 ├── T-720 defense narrative/evidence map
                 │      └── T-721 PowerPoint + speaker material
                 │             └── T-722 rehearsal/validation
                 ├── T-800 final bibliography/guidance audit
                 ├── T-801 reproducibility/privacy/licensing consistency audit
                 └── T-802 academic delivery readiness

T-803 standalone Windows package: post-thesis deliverable; does not block T-713.
```

No downstream package may reinterpret the frozen T-612 estimands or silently replace accepted T-611/T-613 evidence.
