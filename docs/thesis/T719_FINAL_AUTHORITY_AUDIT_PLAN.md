# T-719 Final Authority Audit Plan

**Status:** IN_PROGRESS  
**Date:** 2026-09-06  
**Baseline:** `thesis/archive/T718_evidence_threshold_corrected_review_ready.docx`  
**Baseline raw SHA-256:** `60f92b1cb9994ff2964e551d09bf5a9ee14c7a37e30d49b92435bcea90c957de`

## Purpose

T-719 is a second independent, author-directed pre-freeze audit of the accepted T-718 manuscript. The user's audit list is treated only as hypotheses to verify against stronger authority. T-719 is not supervisor/reviewer feedback and does not reopen T-712.

## Non-negotiable scientific boundary

T-719 may not change any frozen scientific decision, numerical result, threshold, estimand, condition, root, layout, seed, budget, method configuration, statistical result, T-612 analysis output, or registered T-613 quantitative asset. New experiments, re-analysis and post-hoc scientific redesign are forbidden.

Bibliography claims use `MariosGiannakaras/ThesisBibliography`, with the citation-ready layer as the formal eligibility boundary. Protocol/implementation claims use DEC records, frozen protocol/configuration, actual code, accepted manifests and validated T-611/T-612/T-613 evidence.

All current T-718 visuals must remain present. No quantitative registered visual may be regenerated unless a stronger repository authority explicitly permits it.

## Confirmed corrections after independent re-check

The following hypotheses have survived authority review and may be corrected with the smallest viable reader-facing change:

1. **RQ3 directed recovery wording consistency.** DEC-060 defines `AN-AD <= 0.10`; better-than-AN AD values qualify. Several broad prose phrases still read like symmetric distance/neighborhood language and must be tightened without changing the criterion.
2. **RQ1 trapezoidal time-average definition.** The canonical T-718 Section 3.7 lacks the exact frozen equation. The final analysis uses `return_mean` and `trapezoidal_time_average` over the actual interaction axis.
3. **Development root-sizing wording.** T527 sizing uses equal-layout trapezoidal time-average `terminated_rate` for Phase A and equal-layout adaptation benefit divided by the selected Phase-B horizon for Phase B; the selector is `maximum_half_width <= 0.20`. This must remain distinct from the final cumulative RQ2 `return_sum` estimand.
4. **Primary recovery-tolerance rationale.** DEC-060 predeclares 0.10 from the task reward scale and uses an absolute task-scale tolerance to avoid unstable percentage denominators for signed returns. One concise methodology clarification is allowed.
5. **Residual observation-corruption overgeneralization.** A small number of Chapter 5/6 statements remain broader than the tested `observation-corruption-0.05` mechanism and frozen RQ2 estimand.
6. **RQ2 Table 1 caption.** The actual table caption remains generic and is not self-contained enough for the central RQ2 result table.
7. **Repository locator.** Appendix D records exact commit/runtime identities but still refers only to 'the repository of the work' without naming the repository.
8. **Official declaration.** The Department's official regulation and thesis-writing guidance provide the exact required declaration text; the T-718 placeholder may therefore be resolved without inventing personal metadata.
9. **IEEE numeric citation ordering.** The Department permits IEEE 2006 and requires strict adherence to the selected referencing style. The manuscript uses IEEE-style numeric citations but current first appearance is not numeric order. Any correction must be a single deterministic global renumbering preserving source identity and claim fit.
10. **TOC / List of Figures / List of Tables cached field results.** The DOCX contains three live TOC-family fields but the T-718 rendered result lacks page numbers/dot leaders. A field refresh proves this is stale cached field content. Any permanent fix must preserve live Word fields and registered media bytes.

## Confirmed already-correct / no-change findings

- Frozen does not mean deterministic action selection; T-718 is consistent with the Phase-B and probe implementations.
- Final-layout terminology no longer implies statistical independence or unseen test-only layouts.
- Right-censoring, observed recovery time versus restricted delay, and the small-n Student-t support explanation are already adequate.
- T-610 failed-attempt provenance is already explicit and does not require expansion.
- Figure 8 remains readable in the rendered A4 document; no registered T-613 asset change is justified.
- The existing Chapter 4 architecture/provenance flow is adequate; no new diagram or pseudocode block is justified.
- The awkward B.3 page break is presentation-only and not worth shrinking or altering the scientific figure.
- Reference [9] has distinct citation-ready traceability as the verified Sutton & Barto Q-learning excerpt and is retained.
- ThesisBibliography currently exposes a DOI locator for `SRC-0A594EACC0`, but its citation-ready checked identity remains the verified arXiv 2024 version. Thesis bibliography metadata will not be changed until upstream citation-ready authority is reconciled.

## Optional but not approved as necessary edits

- adding a `-0.100` shortest-path-return explanation to RQ1;
- adding a competence-matched checkpoint caveat beyond the existing fairness/validity limits;
- adding a new Chapter 4 operational-flow visual/table;
- manual pagination surgery for Appendix B.3.

These may be revisited only if the full post-patch audit exposes a concrete reader-facing error.

## Final acceptance gates

T-719 is acceptable only if:

1. the T-718 baseline hash is exact;
2. every text correction is anchored fail-closed to canonical Word-visible content;
3. all numerical results and frozen protocol values are byte/text identical where not explicitly reader-facing metadata;
4. all 25 existing visuals remain present and all T-613 quantitative media remain byte-identical;
5. bibliography renumbering preserves exactly the same 32 source identities and claim-to-source relationships;
6. live TOC/LoF/LoT fields remain present and their cached results show correct page numbers after final pagination;
7. official declaration text comes only from Department authority; unresolved personal metadata remains unresolved;
8. a fresh full manuscript audit passes against protocol-v2.1, T-612, T-613, execution manifests and citation-ready bibliography authority;
9. the final DOCX is rendered in full and every page is visually inspected before archival acceptance.
