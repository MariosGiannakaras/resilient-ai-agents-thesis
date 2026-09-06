# T-718 Evidence-Threshold Thesis Correction Plan

**Status:** IN_PROGRESS  
**Date:** 2026-09-06  
**Baseline:** `thesis/archive/T717_pre_freeze_content_refined_review_ready.docx`  
**Baseline raw SHA-256:** `57d6de352eef6147fa24179f87a3f8e9ee39f65a90ad8b85777cac8f541f57c5`

## Purpose

T-718 is a bounded internal author-directed correction pass after T-717. It exists only to correct reader-facing ambiguity that survived the accepted T-715/T-716/T-717 composition chain and that is directly contradicted or underspecified by stronger frozen project authority.

T-718 is **not** supervisor/reviewer feedback, does not reopen T-712, and does not alter the scientific protocol, experiment, estimands, thresholds, roots/layouts, frozen evidence, T-612 analysis, or T-613 quantitative assets.

## Evidence threshold

A manuscript change is permitted only when all of the following hold:

1. the current T-717 reader-facing wording is materially ambiguous, incomplete, or misleading;
2. a stronger accepted project authority fixes the intended meaning;
3. the correction requires no new experiment, re-analysis, new estimand, changed threshold, or post-hoc method ranking;
4. the smallest viable wording/label correction is sufficient; and
5. no current T-717 visual is removed.

Stylistic preference, optional expansion, or a merely nicer explanation is insufficient.

## Approved minimal corrections

### C1 — Define Phase-B `return_sum` operationally for RQ2

Current T-715/T-717 wording states only that RQ2 uses Phase-B `return_sum` before the FN/FD/AN/AD equations.

Required correction: state that each branch value is the **undiscounted cumulative task reward over the fixed 256 actual post-boundary environment interactions**, accumulated across episode boundaries. This is a reader-facing definition of the already frozen scalar, not a new metric.

Primary authority:
- `src/resilient_agents/protocol_v2_1_tabular_phase_b.py`
- `src/resilient_agents/study/pre_t610.py`
- accepted T-715 metric block in `scripts/t715_audit_hardening.py`

### C2 — Correct Frozen-regime wording and distinguish learning freeze from action selection

Current methodology describes disturbance-associated loss under a "σταθερή πολιτική". That wording is too strong. Frozen branches disable scientific learning-state updates, but behavior/inference RNG may continue and method-native action selection remains in force. Phase-A standardized probes are a distinct greedy/deterministic no-learning evidence surface.

Required correction: replace the misleading "σταθερή πολιτική" wording with wording that explicitly means **learning state frozen / updates disabled**, and add only the minimum sentence needed to distinguish Frozen Phase-B deployment from deterministic standardized probes.

Primary authority:
- `src/resilient_agents/protocol_v2_tabular_phase_b.py`
- `src/resilient_agents/protocol_v2_sb3_phase_b.py`
- `src/resilient_agents/protocol_v2_tabular_driver.py`
- `src/resilient_agents/study/protocol_v2_1_phase_b_executor.py`
- `docs/context/CONFIRMED_REQUIREMENTS.md` REQ-EXP-021

### C3 — Replace ambiguous "held-out layouts" reader-facing terminology

The two final layouts were reserved from development/tuning until the final reserve was opened, but they are used during the final Phase-A training itself. Bare "held-out" can therefore be misread as test-only/unseen generalization evaluation.

Required correction:
- first use: explain that the two **final reserved layouts** were withheld from development/tuning and then used in the final campaign;
- subsequent reader-facing uses: prefer "final layouts";
- T-717 explanatory Figure 1 labels: change `Held-out layout A/B` to `Final layout A/B` without removing or replacing the figure concept.

This is terminology clarification only. Layout identities, generation seeds, geometry, training/evaluation use, and all evidence remain unchanged.

Primary authority:
- frozen protocol/final-reserve separation in project requirements and task authorities;
- `gw-l1-final-a` / `gw-l1-final-b` final campaign identities;
- T-717 Figure 1 construction in `scripts/t717_final_content_refinement.py`.

### C4 — Scope the observation-corruption conclusion to the tested condition

Current conclusion wording generalizes from the observed result to learning signals "under observation noise" more broadly.

Required correction: bind the claim to the **specific `observation-corruption-0.05` mechanism and the RQ2 adaptation-benefit estimand**. Preserve the frozen numerical result and the conclusion that Q-Learning and SARSA had negative adaptation benefit in this condition; do not generalize to observation noise as a class.

Primary authority:
- `docs/research/T612_FINAL_STATISTICAL_ANALYSIS.md`
- frozen T-612/T-613 RQ2 outputs.

### C5 — Explain support-unconstrained Student-t recovery-time intervals

Conditional recovery-time Student-t intervals with very small recovered `n` can extend outside the physically possible 0–256 interaction range. These are the frozen predeclared ordinary Student-t intervals and must not be truncated or recomputed.

Required correction: add one concise interpretation note stating that such endpoints express sampling uncertainty of the ordinary Student-t summary and are not physically possible recovery times; recovered `n` and censoring remain essential to interpretation.

Primary authority:
- `docs/research/T612_FINAL_STATISTICAL_ANALYSIS.md`
- protocol-v2.1 recovery/censoring contract.

### C6 — Add exact accepted final-execution identity to reproducibility appendix

The current appendix describes Python 3.12 + locked `uv` and asks for the accepted replacement source commit, but the final reader-facing reproducibility material should expose the exact immutable accepted execution identity already stored in the final Study manifest.

Required correction: concisely record:
- execution instance `protocol-v2.1-final--t610-recovery-01`;
- source commit `86fb01a13fd77b98ea0b8d8fa6d5c5d6e2cbd730`;
- Windows `10.0.19045`;
- CPython `3.12.13`;
- clean tracked/untracked source state recorded by the manifest;
- frozen recipe SHA-256 `8f21075ad2bc7a7944dbac4ba2ee2f3255ec0157706b94f99174b6d9ef99b154`;
- frozen plan SHA-256 `073779d18f45caeab2ab725e7dce6b54b70394102d45de81e1974c7efaece0f4`;
- scientific dependency identities needed for execution context: Gymnasium `1.3.0`, Stable-Baselines3 `2.9.0`, Torch `2.9.0` under the locked `uv` environment.

PySide6 `6.11.2` may be mentioned only as a separate presentation/UI overlay, not as part of the scientific-execution identity.

Primary authority:
- `results/studies/protocol-v2.1-final--t610-recovery-01/manifest.json`
- `pyproject.toml`
- `requirements/application-ui.txt`.

## Explicit no-change decisions

T-718 will **not** add or change any of the following unless a new contradiction is discovered during deterministic validation:

- RQ1 mathematical equation;
- RQ3 directed recovery definition, tolerance, two-window rule, or censoring;
- tuning objective/rationale or tuning search space;
- root-sizing rationale or `n=12`;
- method shortlist, method-comparison table, or method ranking;
- severity/frequency limitation already added by T-717;
- explicit-detector/detection-latency discussion already present;
- repeated/recurrent-disruption limitation already added by T-717;
- T-610 failed-attempt narrative, which is already sufficiently explicit;
- uncertainty/UQ subsection;
- the interpretation that `-0.100` equals the shortest-path nominal return, because this is optional explanatory context rather than a correction of an inaccurate statement;
- Figure 8 or any other existing scientific result visual absent a demonstrated legibility failure;
- any new scientific result figure, new table derived from raw evidence, or new analysis;
- any removal of a current T-717 visual.

## Visual preservation contract

The T-717 baseline contains 25 media items. T-718 must preserve all 25 media positions/concepts. Only the existing T-717 introductory GridWorld/disturbance explanatory figure may have its **layout labels** regenerated to remove the ambiguous word `Held-out`. No T-613 quantitative visual may change bytes.

## Acceptance gates

T-718 is acceptable only if deterministic QA proves:

1. baseline is the canonical T-717 DOCX with the recorded raw SHA-256;
2. only intended `word/document.xml` changes plus the one explanatory Figure 1 media update occur;
3. all 25 media remain present;
4. all T-613 quantitative media remain byte-identical;
5. no experiment, re-analysis, estimand, threshold, result value, root/layout identity, protocol field, or T-612/T-613 artifact changes;
6. all 32 governed references remain present/used unless no citation-bearing paragraph is touched;
7. Word fields, placeholders, comments/tracked-change state and unresolved source-residue gates remain valid;
8. a full rendered page-by-page visual QA passes before archival acceptance.
