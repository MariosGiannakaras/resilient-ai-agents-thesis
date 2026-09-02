# Definition of Done

Project-level completion conditions only. Concrete task IDs/status/dependencies/resume state live in `docs/context/TASKS.md`; phase intent lives in `IMPLEMENTATION_ROADMAP.md`.

## Foundation, bibliography and reproducibility

- [x] Official application/titles/context recorded; raw chat exports excluded from decision authority.
- [x] `ThesisBibliography` ownership boundary, immutable generated consumer, provenance and citation-ready trust established.
- [x] Python 3.12 + locked `uv` research environment and independent `src/resilient_agents/` scientific core.
- [x] Evaluator/agent information boundary, independent deterministic RNG streams and project-owned Gymnasium GridWorld.
- [x] Filesystem evidence bundles, provenance/checksums, persistence/resume and guarded publication primitives.
- [x] Historical v1.0/v1.1/pilot evidence remains immutable and auditable.
- [x] Canonical resumable Codex/Git/CI/documentation workflow is established.

## Protocol-v2.1 scientific contract and execution foundation

- [x] Physical feasibility/discrimination, fair tuning/sizing and method selection are complete.
- [x] Retained methods are Q-Learning, SARSA, DQN, PPO and Dyna-Q+ with method-appropriate selected configurations.
- [x] DEC-058 remains immutable historical protocol-v2.0 freeze authority; DEC-060 plus `configs/protocols/protocol-v2.1-final.json` are current pre-execution authority.
- [x] Common task/information/reward semantics and principal actual-environment-interaction fairness budget are frozen.
- [x] Standardized isolated Phase-A no-learning probes/checkpoints and exact method-native continuation are implemented.
- [x] Matched FN/FD/AN/AD Phase-B execution preserves Frozen immutability and Adaptive method-native continuation.
- [x] Protocol-v2.1 passive 32-interaction temporal evidence over horizon 256 is implemented without altering learning boundaries.
- [x] RQ1/RQ2/RQ3 estimands, recovery tolerance/stability/censoring, direct root-paired method contrasts and actual-root Student-t interval policy are frozen.
- [x] Scientific failures/cancellations/invalid/skipped units remain attributable; no outcome-driven root/seed replacement is permitted.
- [x] Concise RQ → evidence → estimand → output traceability is documented.

## Study-first backend and evidence pipeline

- [x] Immutable `StudyRecipe`, deterministic job DAG, stage barriers and exact Phase-A→Phase-B dependencies.
- [x] Durable `StudyStore` with lifecycle state, attempts, failure semantics, artifact lineage and finalization integrity.
- [x] Concrete Phase-A and Phase-B Study executors emit standardized evidence and exact checkpoint lineage.
- [x] Structural/schema-v2 evidence validation covers complete temporal FN/FD/AN/AD records and retained failures/skips.
- [x] Root/layout analysis computes Phase-A final/time-average learning, Phase-B Frozen/Adaptive losses, adaptation benefit, recovery and direct method contrasts.
- [x] Planned/observed denominators remain explicit; repeated layouts/episodes/probes/windows are not treated as independent roots.
- [x] Deterministic evidence handoff exports stable machine-readable summaries/contrasts/recovery records/result index/integrity manifest.
- [x] Framework-neutral restart-safe `StudyService` exposes Study planning/status/history/artifacts/execution/retry/finalization.
- [x] Confirmatory/final Study execution is denied by default unless the separate explicit final-experiment authorization token is supplied.
- [x] Read-only protocol-v2.1 final preflight verifies the frozen matrix/lock and absence of a committed final Study bundle.
- [x] DEVELOPMENT-only synthetic end-to-end smoke validates evidence → validation → v2.1 analysis → deterministic export → finalized/reloaded StudyStore, including recovered and right-censored cases.

## Application architecture and clean rebuild

- [x] DEC-059 selects PySide6 / Qt 6 Widgets over the framework-neutral Study backend.
- [x] DEC-061 defines the T-534 experiment-first product/UX model while preserving DEC-059's framework/runtime/scientific-firewall clauses.
- [x] Historical Streamlit/React/NiceGUI product paths are superseded; Git history retains them as history/reference only.
- [x] UI-neutral Study/evidence read-model, provenance and execution-policy contracts exist and are testable independently of presentation layout.
- [x] Previous PySide6 application work established the architecture/workflow/read-model foundation and intended-user acceptance history.
- [ ] A fresh protocol-v2.1 UI rebuild starts from current `main`, not the paused/pre-v2.1 working branch/worktree.
- [ ] Existing `src/resilient_agents/desktop/` is classified before replacement: UI-neutral Study/results/evidence/provenance/execution/live-observer behavior is preserved where correct; presentation windows/pages/widgets/styles/navigation may be rebuilt.
- [ ] Active desktop presentation no longer depends on stale protocol-v2.0/DEC-058-only/T-528 labels, root discovery, help or execution messages.
- [ ] Primary application navigation is **Experiment / Run / Results / Evidence**; Help/onboarding and technical/reproducibility detail are contextual/secondary.
- [ ] Frozen Thesis experiment clearly explains the five fixed methods, Phase-A nominal learning, exact checkpoint handoff, disturbances, matched Frozen/Adaptive regimes, FN/FD/AN/AD and RQ1/RQ2/RQ3 while remaining read-only and execution-locked.
- [ ] The final Thesis experiment never exposes method deselection; DEVELOPMENT/Exploratory method/scope selection appears only where backend-supported and remains clearly non-confirmatory.
- [ ] Frozen and Adaptive are never presented as algorithms or mutually exclusive choices; matched Phase-B live presentation shows both regimes simultaneously when exact paired frames exist.
- [ ] Run prioritizes the scientific process: Phase A has one large nominal GridWorld, Phase B has two large exact-matched Frozen/Adaptive GridWorlds, and compact method status does not rank methods.
- [ ] Primary live information is method/phase/condition/interaction/intended→executed action/reward; roots/layouts/states/observations/IDs/flags/hashes are secondary technical detail.
- [ ] Results are explicitly organized as **RQ1 Learning / RQ2 Resilience & Adaptation / RQ3 Recovery** and use only validated stored outputs.
- [ ] RQ1 uses real interaction-axis stored learning/probe trajectory information where scientifically supported, without UI-side scientific aggregation.
- [ ] RQ2 keeps primary adaptation benefit `(FN-FD)-(AN-AD)` separate from Frozen `FN-FD` and Adaptive `AN-AD` losses, with stored intervals/denominators/direct contrasts.
- [ ] RQ3 presents stored AN-vs-AD trajectory, recovery/non-recovery status, observed recovery time conditional on recovery, separately named restricted fixed-horizon delay and right-censoring; censored horizon 256 is never shown as observed recovery time.
- [ ] Evidence leads with validation/evidence/analysis/export readiness and user-facing outputs; Study history/artifact IDs/paths/hashes/lineage remain available under progressive disclosure rather than dominating the interface.
- [ ] Historical schema-v1 evidence remains truthful and is not silently assigned v2.1 recovery semantics.
- [ ] Qt presentation code never owns scientific RNG, checkpoint identity, root/layout reduction, thresholds, recovery decisions, estimands, intervals, direct comparisons, evidence finalization or final-experiment authorization.
- [ ] UI never invents winner/best-algorithm/significance/statistical-superiority claims unsupported by stored analysis.

### Self-explanatory UX

- [ ] A non-programmer with no RL/model/config/repository knowledge can understand the main experiment and workflow without a separate manual.
- [ ] Plain-language labels, secondary technical IDs, concise helper text, visible units/consequences and contextual help accurately describe methods, disturbances, Frozen/Adaptive, study/evidence classes and RQ metrics.
- [ ] Advanced/technical details use progressive disclosure; required workflow/scientific information is not tooltip-only.
- [ ] Loading/empty/warning/error/disabled/unavailable/locked states are truthful, accessible and explain the useful next action.
- [ ] Modern compact desktop/laptop hierarchy is consistent across the four primary surfaces, GridWorlds, charts, tables and filters.
- [ ] Permanent cards/banners/help text are restrained enough to preserve hierarchy and information density.
- [ ] Purposeful animation/interaction never fabricates progress/data or alters scientific execution/RNG.
- [ ] DEVELOPMENT/synthetic/test fixtures are clearly labelled and never visually promoted as thesis evidence.

## Application validation and later standalone delivery

- [ ] Clean UI rebuild has targeted contract tests plus representative workflow/render/screenshot validation on DEVELOPMENT/synthetic fixtures.
- [ ] Representative UI validation includes Phase-A large GridWorld, exact matched Phase-B Frozen/Adaptive side-by-side, RQ1/RQ2/RQ3 stored-results states and a right-censored RQ3 example.
- [ ] Repository CI is green on the exact UI PR head and affected active docs are reconciled.
- [ ] Native Windows launch/close/restart/writable-path behavior is revalidated for the accepted rebuilt UI.
- [ ] Post-thesis issue #94 produces the final cleaned standalone Windows package; this is not a pre-UI or pre-final-experiment requirement.

## Final protocol-v2.1 experimental/evidence phase

- [x] User explicitly authorized the separate final scientific experiment and narrow DEC-062 clean replacement; `final_reserve_access=false` and the backend guard remain unchanged.
- [x] Frozen protocol-v2.1 final Study matrix executed only after authorization on the accepted execution path.
- [x] The first 216-job attempt remains immutable, unfinalized and excluded; the replacement started from zero on one corrected source commit with explicit lineage and the unchanged recipe/plan.
- [x] Required final scientific units completed or were transparently accounted for without replacement/cherry-picking.
- [ ] Finalized raw results/checkpoints are immutable/checksummed and accepted final evidence is frozen.
- [ ] Predeclared root-level RQ1/RQ2/RQ3 analysis and sensitivity diagnostics reproduce from frozen evidence.
- [ ] Every final quantitative figure/table has machine-readable provenance to frozen analysis/result IDs.
- [ ] Thesis/defense evidence handoff maps RQs, protocol/methods, source IDs, run/checkpoint/result IDs, figures/tables/captions and planned claims.

## Mandatory writing gate

- [ ] User explicitly approves starting Results/Discussion/WP7 writing after final evidence/application acceptance. No technical milestone, green CI, screenshot, cleanup or package substitutes for this approval.

## Thesis, defense and final delivery

- [ ] Current official thesis/template/submission/defense rules are reverified near delivery.
- [ ] Bibliography freshness/evidence sync is confirmed and any supplied example theses are used only as contextual structure/style references.
- [ ] Complete Greek thesis is drafted/reviewed/frozen in Microsoft Word from citation-ready sources plus frozen protocol-v2.1 evidence.
- [ ] Supervisor/reviewer corrections are incorporated with affected evidence/citations revalidated.
- [ ] Final PowerPoint narrative, evidence map, speaker notes/script, app media/fallback, rendering and timing rehearsal pass.
- [ ] Privacy/secret/license/reproducibility audit passes on final repository/delivery state.
- [ ] Thesis, presentation, speaker material, standalone application and frozen scientific evidence agree.
