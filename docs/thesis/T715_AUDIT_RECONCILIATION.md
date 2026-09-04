# T-715 Audit Reconciliation

**Date:** 2026-09-05  
**Scope:** Reader-facing thesis composition only  
**Repository task:** T-715  
**Active PR:** #138

## Purpose

This record reconciles the supplied thesis audit and the accompanying prior answer against the repository authorities before carrying any recommendation into the reader-facing Word thesis.

The audit is used as a review checklist, not as a scientific authority. The prior answer is likewise not treated as authoritative where it conflicts with the frozen protocol, implementation, tuning/sizing decisions or predeclared analysis. Repository evidence wins.

## Scientific boundary

T-715 does not rerun experiments, reopen the final reserve, change an estimand, change a recovery classification, introduce a new statistical test, alter a reported numerical result or replace a registered T-613 scientific asset. The two application screenshots remain deterministic DEVELOPMENT-only explanatory captures and are not scientific evidence.

The audit hardening is composition-only and is applied after the accepted T-715 v26 reader composition by `scripts/t711_build_entry_v27.py` through `scripts/t715_audit_hardening.py`.

## Reconciled facts carried into the thesis

### Tuning and selected configurations

Authority: `docs/decisions/DEC-055_PROTOCOL_V2_FAIR_TUNING_AND_SIZING_AUTHORITY.md` and `configs/protocols/protocol-v2-t527-tuning-sizing-v0.1.json`.

- Five methods, six method-appropriate candidates per method, three tuning-only roots and two development layouts produce 5 × 6 × 3 × 2 = 180 tuning units.
- The common actual-interaction budget is 8,192 and the same isolated probe structure is used for candidate comparison.
- Seeds are randomization variables and are not tuned.
- Selection is method-local and mechanical: time-average standardized success curve first, then final success, then time-average evaluation return, then lexicographically smaller config ID.
- Selected configurations are `q-c06`, `sarsa-c06`, `dqn-c05`, `ppo-c06` and `dyna-c03`.
- The bounded tuning search is explicitly not an exhaustive claim about the maximum attainable performance of DQN, PPO or any other method.

### Final roots and precision sizing

Authority: `docs/decisions/DEC-058_PROTOCOL_V2_FINAL_SCIENTIFIC_FREEZE.md`.

- Candidate final root counts were 12, 16, 20 and 24.
- The selected rule was the smallest count satisfying Student-t 95% interval half-width < 0.20 for both Phase-A AUC and Phase-B adaptation benefit.
- Twelve roots already satisfied the rule; maximum half-width at 12 was 0.1428.

### Final protocol and seeds

Authority: `configs/protocols/protocol-v2.1-final.json`.

- Final layout generation seeds are 57001 and 57002.
- For roots r01–r12, the six seed streams are initialization 71001–71012, exploration 72001–72012, scenario 73001–73012, environment 74001–74012, action disturbance 75001–75012 and observation disturbance 76001–76012.
- Phase-B conditions remain exactly: `action-remap-swap-right-down`, `action-remap-cycle-clockwise`, `action-failure-0.15` and `observation-corruption-0.05`.

### Disturbance semantics

Authority: `src/resilient_agents/gridworld.py` and `src/resilient_agents/study/protocol_v2_phase_b_executor.py`.

- `swap-right-down`: up→up, right→down, down→right, left→left.
- `cycle-clockwise`: up→right, right→down, down→left, left→up.
- Action failure is an independent p=0.15 event; failure executes a no-op, leaves the real position unchanged, reports no collision and receives the normal step reward −0.1 unless another terminal/reward rule applies.
- Observation corruption is an independent p=0.05 event after the real transition; the delivered observation is sampled uniformly from in-bounds, non-obstacle cells excluding the current true position. Goal and start are not categorically excluded.
- The corruption changes the delivered observation only; it does not change the ground-truth transition or reward. Adaptive learning consumes the delivered observation through the normal learning path.

### RQ1, RQ2 and RQ3 definitions

Authority: `src/resilient_agents/evidence_v2/statistics.py`, `src/resilient_agents/evidence_v2/recovery.py` and `docs/research/RQ_EVIDENCE_TRACEABILITY.md`.

- RQ1 primary final nominal performance is the last no-learning Phase-A probe; the secondary learning summary is the trapezoidal time-average over the actual interaction axis.
- RQ2 adaptation benefit is `(FN − FD) − (AN − AD)` for the higher-is-better return quantity.
- RQ3 uses 32-interaction windows over a 256-interaction horizon and the directed gap `nominal − disturbed`.
- A window is within the primary tolerance when directed gap ≤ 0.10; this is not an absolute-gap rule.
- Stable recovery requires two consecutive within-tolerance windows.
- `recovery_time` is the end of the first window in the first qualifying pair; `confirmation_time` is the end of the second.
- Failure to recover by 256 is right-censored with `recovery_time = null`.

### Statistical presentation boundary

- Continuous root-level quantities retain the predeclared equal-layout reduction and pointwise Student-t interval treatment using the actual independent-root count.
- Recovery proportions are reported descriptively as x/12 with the denominator visible.
- No post-hoc binomial confidence interval, significance family, composite ranking, survival analysis or new recovery test is introduced by this audit pass.

## Corrections to the prior answer

The prior answer contained several statements that are not carried forward because they conflicted with repository authorities. In particular, recovery stability is two windows rather than three; the action-remapping semantics are those listed above; action-failure no-op reward is −0.1 rather than −0.01; observation corruption does not categorically exclude the goal; the tuning design is 3 tuning roots × 2 development layouts with 180 total units rather than a different repetition/layout scheme; and the selected configuration IDs are the frozen IDs listed above.

## Reader-facing changes accepted from the audit

The bounded composition pass adds: a concise tuning/search-space and generalization subsection; exact disturbance semantics; explicit RQ1/RQ2/RQ3 mathematical definitions; the root-count sizing rationale and interval convention; final seed-stream information; explicit bounded-tuning and finite-recovery-horizon limitations; and a self-contained appendix reminder of tuning, seeds and disturbance behavior.

These additions are implemented as 26 reader-visible paragraphs, including three Heading-3 subsections, with fail-closed exact anchors and sentinel checks.

## Validation gates

`T-711/T-714/T-715 thesis DOCX QA` now builds through `scripts/t711_build_entry_v27.py` and requires:

- exactly 26 audit-hardening paragraphs and three audit-hardening headings;
- exact sentinel presence;
- 180 tuning units and the five frozen selected configuration IDs;
- 12 final roots and sizing half-width 0.1428;
- recovery window 32, horizon 256, tolerance 0.10 and two-window stability;
- action-failure p=0.15 with step reward −0.1;
- observation-corruption p=0.05 excluding current true state but not categorically excluding goal;
- preserved inline-shape count and identical DOCX media hashes across the audit text insertion;
- `scientific_values_modified=false`, `registered_asset_bytes_modified=false`, no new post-hoc binomial test and no new experiment/reanalysis.

The four-file thesis rewrite workbook is also rebuilt from the v27 artifact so its methodology text reflects the reconciled thesis rather than the older v26 composition.

## Remaining delivery boundary

T-715 is an internal reader-scope/audit-hardening cycle explicitly authorized by the user; it is not relabelled as supervisor feedback. T-712 remains reserved for actual supervisor/reviewer corrections. T-713 remains blocked by the intentionally unresolved official-person/declaration placeholders and final Microsoft Word field/update checks.
