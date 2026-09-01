# Definition of Done

Project-level completion conditions only. Concrete task IDs/status/dependencies/resume state live in `docs/context/TASKS.md`; phase intent lives in `IMPLEMENTATION_ROADMAP.md`.

## Foundation and bibliography

- [x] Official application examined; exact titles/context recorded.
- [x] Raw chat exports excluded and historical chats removed from decision authority.
- [x] `ThesisBibliography` ownership boundary, complete immutable consumer, provenance and citation-ready trust established.
- [x] Protocol-v2 bibliography/source closure consumed from immutable upstream SHA with later-writing source crosswalk retained.
- [x] Confirmed requirements/decisions/constraints/contradictions/open questions documented with stale-state validation.

## Scientific/reproducibility infrastructure

- [x] Python 3.12 + `uv` locked environment and independent `src/resilient_agents/` core.
- [x] Evaluator/agent information boundary and independent deterministic RNG streams.
- [x] Project-owned Gymnasium GridWorld and known-answer/determinism/disturbance tests.
- [x] Filesystem run bundles, provenance/checksums, persistence/resume and guarded publication primitives.
- [x] Historical pilot/v1.0 analysis and immutable final evidence baseline preserved.
- [x] Canonical resumable Codex task/interruption workflow and documentation governance.

## Protocol-v2 scientific contract and execution foundation

- [x] Independent Phase-A learning versus matched Phase-B resilience/adaptation design frozen at the methodology level by DEC-048/050.
- [x] Common task/information/reward/gamma semantics and principal actual-environment-interaction budget contract implemented.
- [x] Q-Learning, SARSA, DQN, PPO and Dyna-Q+ pilot-capable scientific adapters/drivers implemented without forcing neural methods into a Q-table abstraction.
- [x] Standardized isolated no-learning probes implemented with separate interaction accounting.
- [x] Exact scientific checkpoint semantics cover all state required for continuation, including DQN replay/target/optimizer/schedules/RNG, PPO legal update-boundary state and Dyna-Q+ model/recency/planning state.
- [x] `train -> serialize -> destroy -> restore -> continue` and branch-clone conformance is covered by focused tests.
- [x] Exact Frozen/Adaptive Phase-B one-segment branch drivers preserve Frozen learning state and begin Adaptive updates only after the boundary.
- [ ] Physical Windows T-526 feasibility/discrimination and severity-calibration evidence accepted.
- [ ] T-527 freezes retained methods, final task/layout/severity/budget/root/statistical recipe and exact multi-episode Phase-B lifecycle before final reserve access.

## Study-first backend/application API

- [x] Superseded active NiceGUI application/runtime/packaging implementation removed while Git/history and historical scientific evidence remain auditable.
- [x] Immutable `StudyRecipe`, evidence classes, deterministic job DAG, stage barriers and exact Phase-A→Phase-B dependencies implemented.
- [x] Durable filesystem `StudyStore` preserves lifecycle state, attempts, scientific versus infrastructure failure semantics, artifact lineage and finalization integrity.
- [x] Real Phase-A Study executor emits finalized run evidence, exact scientific checkpoint and standardized analysis data for validated core methods.
- [x] Shared no-learning prefix and atomic matched FN/FD/AN/AD Phase-B Study execution are implemented and fail closed when currently unfrozen reset semantics would be required.
- [x] Explicit Random supporting reference execution is available; unknown/oracle reference identities are not silently invented.
- [x] Structural evidence validation reconciles planned jobs, required artifacts, exact checkpoint lineage and retained scientific failures/skips.
- [x] Root/layout analysis foundation computes Phase-A final/time-average learning summaries and Phase-B matched Frozen loss/Adaptive loss/adaptation benefit without composite scoring.
- [x] Analysis retains explicit planned/completed/scientific-failure/skipped/infrastructure denominators and receives interval/layout policy from an explicit recipe.
- [x] Deterministic evidence handoff emits machine-readable root/summary tables, stable `RESULT-*` IDs, result index and integrity manifest from the analysis package.
- [x] Framework-neutral restart-safe `StudyService` exposes planning/status/history/artifacts/execution/retry/finalization and uses the concrete protocol-v2 executor registry by default.
- [x] T-529 final correctness/docs/CI closure completed with no active v1.x/NiceGUI product path competing with the Study API.

## Final application completion

The final UI is deliberately not implemented before T-527 freezes the remaining scientific/runtime contract. T-529's backend contract is complete.

- [ ] T-528 selects a frontend framework **different from NiceGUI** and records the selection rationale for local Windows use, scientific visualization, accessibility, maintainability and Python-service integration.
- [ ] Final application is rebuilt from scratch as a client of `StudyService`; scientific orchestration is not duplicated in frontend state.
- [ ] Default journey is study-first: choose study/intent → choose permitted methods/settings → pre-run review → run/monitor → results → export.
- [ ] Frozen thesis-study mode loads immutable recipe values; frontend defaults cannot silently choose gamma/rewards/hyperparameters/seeds/roots/severities/probe cadence/branches/statistical tests.
- [ ] Exploratory/custom mode is permanently distinguishable from confirmatory evidence.
- [ ] Real approved Study execution runs end to end through the application using the same backend/evidence path as headless execution.
- [ ] Live/provisional views use real backend events/data only and cannot alter agent-visible information, actions, timing or RNG.
- [ ] History is study-first with attributable completed/scientific-failed/infrastructure-failed/skipped/cancelled/interrupted units.
- [ ] Results show scientifically compatible Phase-A and matched Phase-B component effects with explicit denominators/interval meanings; no best-run cherry-picking or unlabeled composite score.
- [ ] Evidence/export surfaces expose real result IDs, tables/figures/data and provenance from deterministic backend artifacts.

### Self-explanatory UX

- [ ] A non-programmer with no RL/model/config/repository knowledge can understand the main workflow without a separate manual.
- [ ] Plain-language labels, secondary technical IDs, helper text, visible units/ranges/consequences, tooltips/info icons and contextual explanations accurately describe methods, conditions, study modes and metrics.
- [ ] Advanced settings use progressive disclosure; pre-run review shows readable Study intent, evidence class, planned scientific units, locked/editable settings and blocking issues.
- [ ] Status/loading/empty/warning/error/disabled/unavailable states use understandable text + stable icons/symbols + accessible semantic visual treatment; color is never the sole signal.
- [ ] Modern compact desktop/laptop hierarchy is consistent across cards/charts/tables/filters rather than oversized/decorative.
- [ ] Purposeful interactions/animations never fabricate progress/data, never alter scientific execution and remain understandable with reduced motion.
- [ ] Destructive/high-impact actions use proportionate confirmation; routine interactions remain friction-light.
- [ ] Short first-run onboarding supports Previous/Next/Skip/Finish, is replayable/local/skippable and every page remains understandable if onboarding is skipped.

## Application validation and later standalone delivery

- [ ] T-511 intended-user E2E acceptance is complete; automated screenshots/render/package checks alone are insufficient.
- [ ] Accepted review screenshots use real data/state or explicitly labelled diagnostic fixtures and are never scientific evidence substitutes.
- [ ] Native Windows launch/close/restart and writable-path behavior are validated for the framework chosen at T-528.
- [ ] Post-thesis T-803 produces the cleaned standalone Windows package using delivery technology appropriate to the accepted final framework.
- [ ] Recipient does not need to understand repository internals or manually reconstruct the scientific workflow.

## Final protocol-v2 experimental/evidence phase

- [ ] Frozen protocol-v2 final Study matrix executes only after T-527, T-529 and application acceptance.
- [ ] Required final scientific units complete or are transparently accounted for; scientific failures/cancelled/invalid/skipped units remain attributable according to the frozen protocol.
- [ ] Finalized raw results/checkpoints immutable/checksummed and accepted final evidence set frozen.
- [ ] Predeclared root-level nominal-learning/matched-resilience analysis and sensitivity diagnostics reproduce from frozen evidence.
- [ ] Every final quantitative figure/table has machine-readable provenance and traces to frozen analysis/result IDs.
- [ ] Superseding thesis/defense evidence package maps RQs, protocol/methods, source IDs, run/checkpoint/result IDs, figures/tables/captions and planned claims.

## Mandatory writing gate

- [ ] User explicitly approves starting WP7 **after** final evidence/application acceptance. No technical milestone, green CI, screenshot or package substitutes for this approval.

## Thesis phase

- [ ] Current official thesis/template/submission/defense rules reverified.
- [ ] Bibliography freshness/evidence sync confirmed.
- [ ] User-supplied completed example theses reviewed as contextual structure/style references if provided.
- [ ] Complete Greek thesis drafted from citation-ready sources + frozen protocol-v2 evidence package.
- [ ] Review-ready Word document includes required bilingual/front matter and validated figures/tables/cross-references.
- [ ] Supervisor/reviewer corrections incorporated and affected evidence/citations revalidated.
- [ ] Final thesis `.docx`/required exports frozen/versioned.

## Defense phase

- [ ] Current official defense requirements reverified.
- [ ] Slide narrative/evidence map complete; final `.pptx` grounded in final thesis/frozen evidence.
- [ ] Embedded speaker notes and separate full spoken Greek script synchronized with slide order.
- [ ] Real application screenshots/demo assets and non-live fallback validated.
- [ ] PowerPoint rendering, legibility, factual consistency and timing rehearsal pass.

## Final repository/delivery

- [ ] Privacy/secret/license audit passed.
- [ ] Reproduction guide validated on a clean environment.
- [ ] Thesis, presentation, speaker material, standalone application and frozen evidence agree.
- [ ] Required final delivery files are present, validated and frozen.