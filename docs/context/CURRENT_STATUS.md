# Current Project Status

**Date:** 2026-09-01  
**Status:** Authoritative compact current-state summary

`docs/context/TASKS.md` remains the canonical dependency/task ledger. Read task-specific decision/research documents progressively. Objective Git/GitHub/evidence state overrides stale resume prose after interruption.

## Current execution state

- `T-100` target validation and `T-200` framing are complete. Protocol-v1.0, FINAL-* and R0 evidence remain immutable historical evidence; old `T-522` must not execute.
- `T-524`, `T-525`, `T-526`, `T-526A`, `T-527`, `T-528`, `T-529` and `T-511` are COMPLETE. Historical completed work is not reopened by the new scientific requirement.
- DEC-058 and `configs/protocols/protocol-v2.0-final.json` remain immutable historical protocol-v2.0 freeze authority. Their final roots/layouts, five retained methods, hyperparameters, conditions, Phase-A budgets/probes and 256-interaction Phase-B horizon remain unchanged.
- **T-530 is now IN_PROGRESS under issue #98 and DEC-060.** It is an explicit pre-outcome protocol-v2.1 amendment required before T-610, not a silent rewrite of DEC-058.
- DEC-060 / `configs/protocols/protocol-v2.1-amendment.json` freezes final RQ1/RQ2/RQ3, true recovery-speed semantics, right-censoring/non-recovery, direct root-paired method contrasts and estimation-oriented interpretation.
- `final_reserve_access=false` remains mandatory. T-610 has not been authorized or executed and no protocol-v2/T-610 result exists in the canonical run index inspected during T-530 recovery.
- `T-528 — Final Application / Frontend Rebuild` remains COMPLETE under DEC-059. The current application is PySide6 / Qt 6 Widgets over the Study backend; NiceGUI is historical prototype only.
- `T-511 — Intended-user application workflow/self-explanatory UX acceptance` remains COMPLETE. That acceptance does not authorize final-reserve execution or accept future scientific results.
- Master tracker #87 remains 7/8 complete; milestone 8 depends on the final v2 evidence chain.
- PR #92 remains the active draft integration PR on `feat/pre-wp7-protocol-v1.1-ui-rebuild`. Its previously selected merge checkpoint is superseded only in sequencing: T-530 must be completed and validated on the same branch/PR before merge/final authorization.
- **Pre-WP7 approval: NOT APPROVED.** No `T-700+` execution.

## T-530 scientific amendment

### Final research questions

- **RQ1 — Nominal learning:** compare the five retained methods' nominal performance and learning efficiency under the common actual-environment-interaction budget and information contract.
- **RQ2 — Resilience/adaptation:** quantify disturbance-associated Frozen/Adaptive loss and preserve the matched adaptation-benefit estimand `(FN-FD)-(AN-AD)` with metric-direction handling.
- **RQ3 — Recovery speed:** after persistent unannounced change, quantify adaptive recovery trajectory, stable recovery time and non-recovery against matched Adaptive-Nominal behavior.

The five methods remain Q-Learning, SARSA, DQN, PPO and Dyna-Q+. Frozen and Adaptive/Continual remain deployment regimes, not distinct algorithms.

### Recovery-speed freeze

Primary RQ3 conditions are the persistent `action-remap/*` changes. Action-failure and observation-corruption remain supporting robustness/adaptation diagnostics unless a later explicit pre-outcome justification changes that role.

The frozen primary recovery definition is:

- temporal axis: actual post-boundary environment interactions;
- fixed windows: 32 interactions across the unchanged 256-interaction horizon (8 windows), crossing episode boundaries without reset/realignment;
- trajectory metric: mean reward per actual interaction within each window;
- matched reference: Adaptive-Nominal (AN) versus Adaptive-Disturbed (AD), equal layout weighting within each independent root before inference;
- higher-is-better directed recovery gap: `AN - AD`;
- primary tolerance: `0.10` reward per interaction; predeclared sensitivity tolerances `0.05` and `0.20`;
- stability: two consecutive in-tolerance windows;
- recovery time: end of the first window in the first stable run; confirmation time: end of the second required window;
- non-recovery: right-censored at interaction 256 with `recovery_time=null`, never an artificial recovery time of 256.

The 0.10 primary tolerance was frozen before final outcomes from the known task reward scale (`step=-0.1`, `collision=-0.25`, `goal=1.0`), avoiding unstable percentage denominators for signed returns.

### Direct method comparison

Method comparison is root-paired and estimation-oriented. Layouts, episodes, probes and temporal windows are not independent samples.

- Primary contrasts: RQ1 final nominal performance, RQ2 adaptation benefit, RQ3 recovery time/status on action-remap conditions.
- Secondary: RQ1 time-average performance, RQ2 Frozen loss and Adaptive loss.
- Exploratory/supporting: other disturbance diagnostics, computational observations and recovery sensitivity thresholds.
- Report effect estimates with root-level pointwise uncertainty intervals. Pointwise intervals are not simultaneous inference and must not be relabeled post hoc as “statistically significant.” No formal p-value superiority family is authorized by DEC-060.

No composite resilience score is introduced. Nominal capability, immediate degradation/resistance, adaptation benefit, recovery profile/time and non-recovery remain distinct constructs.

## Existing Study/backend invariants retained

- immutable recipes/evidence, stable-ID DAG barriers and restart-safe `StudyStore`/`StudyService`;
- independent Phase-A learning with actual-interaction accounting and isolated no-learning probes;
- exact method-native scientific checkpoints for all five retained methods;
- exact shared-prefix FN/FD/AN/AD Phase-B branching with adaptive updates only after the boundary;
- replay/optimizer/exploration/warm-up/model/recency/schedule/counter/RNG continuity rather than silent reset;
- scientific failures retained with reasons and no outcome-driven seed/root replacement;
- filesystem evidence/provenance remains scientific authority; UI/index/database layers are derived/read-only.

## Application state

DEC-059 remains application authority. The UI consumes Study/read-model/evidence boundaries and must not own scientific protocol logic.

Existing stored-evidence learning/adaptation/loss views remain valid. T-530 may extend Results with recovery trajectory/status/time and method contrasts only from validated stored analysis/export artifacts; thresholds/estimands must not be recomputed or selected inside the UI. Aesthetic redesign unrelated to the research correction is out of scope.

## Computational evidence

Actual environment interactions remain the primary fairness axis. Existing wall-clock and process-CPU evidence, plus method-specific update counts where scientifically interpretable, are secondary descriptive computational observations rather than a new primary RQ.

## Bibliography and public-repository constraints

Canonical bibliography remains `MariosGiannakaras/ThesisBibliography` / `research/bibliography/citation-ready/` under the existing synchronization rules. `bibliography-integration-v3` remains immutable historical terminology; no parallel bibliography system is permitted.

The repository remains **public** by explicit user decision. `thesis/source-material/ThesisApplication.pdf` and the existing source-material structure remain unchanged. File removal, history rewrite or private-repository migration is neither required nor a blocker for thesis completion.

## Still intentionally unfrozen

- `final_reserve_access=false`; final-reserve execution itself remains intentionally unfrozen and unauthorized.
- T-610 and all final-reserve scientific outcomes remain blocked until T-530 implementation, deterministic validation, affected CI, documentation reconciliation and objective review are complete.
- No final roots/layouts/seeds may be used to tune recovery thresholds or analysis choices.
- WP7 remains blocked by the later explicit pre-WP7 gate.
- Final Windows standalone packaging remains deferred to `T-803` / issue #94.

## Exact next action

Complete T-530 on the existing PR #92 branch: finish the isolated protocol-v2.1 temporal execution path, produce recovery/root-paired contrast analysis and deterministic exports, expose those stored results in PySide6 where required, reconcile active methodology/task documents, and pass affected CI. Then stop at the explicit authorization gate immediately before T-610. Do **not** access the final reserve or begin Results/Discussion writing.
