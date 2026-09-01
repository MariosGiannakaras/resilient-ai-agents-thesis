# UI Information Architecture

**Status:** current application information/interaction contract for the clean PySide6 / Qt 6 Widgets rebuild under DEC-059. Presentation composition may be redesigned, but scientific and Study/evidence boundaries below are authoritative.

The application is a client of the framework-neutral `StudyService`/stored-evidence backend. It exposes research intent, execution state and validated results while the backend owns scientific mechanics such as roots, exact checkpoints, FN/FD/AN/AD construction, validation, root reduction, recovery semantics and evidence lineage.

## Clean-rebuild rule

The paused/pre-v2.1 UI implementation is not the implementation base for continuation. Start from fresh current `main` and classify existing `src/resilient_agents/desktop/` code before editing:

- preserve UI-neutral Study/evidence read-model, provenance and execution-policy behavior that remains correct;
- windows/pages/widgets/styles/navigation may be rebuilt from scratch;
- old screenshots/layouts are reference/history only;
- never move scientific configuration, RNG, checkpoint identity, estimand calculation, recovery thresholds or evidence finalization into Qt state.

## Primary product model

There are two clearly separated experiences.

### Frozen Thesis Study

The confirmatory protocol-v2.1 Study is predeclared and currently **execution-locked** pending the separate explicit final-scientific-experiment authorization.

Primary journey before authorization:

> **Overview → Protocol/Study review → Execution lock explanation → Existing validated evidence/results/export when available**

After legitimate authorization/execution later, the same product area may expose:

> **Run/Monitor → Validate → Results → Export**

The UI never grants or synthesizes authorization.

### DEVELOPMENT / Exploratory Study

Primary configurable journey:

> **Configure → Review → Create → Run → Monitor → Results/Compare → History/Artifacts/Export**

Only authorized development settings are editable. DEVELOPMENT/synthetic evidence remains visibly non-confirmatory.

## Recommended primary navigation

A compact PySide6 navigation model should cover:

1. **Home / Studies** — durable Study state, next actions and recent studies;
2. **New / Exploratory Study** — approved DEVELOPMENT configuration and review;
3. **Run / Monitor** — truthful current execution and lightweight live views;
4. **Results / Compare** — RQ-aligned stored scientific outputs;
5. **History / Artifacts** — study/job/run lineage, states and provenance;
6. **Export / Evidence** — deterministic evidence package/result index/tables;
7. **Help / About** — onboarding, terminology and reproducibility details.

Labels may be refined during implementation if the information model remains clear and complete.

## Self-explanatory UX contract

The application must be usable by a non-programmer with no prior RL/model/configuration/repository knowledge.

- Human-readable primary labels; technical IDs are secondary reproducibility detail.
- Explain retained methods, uncertainty/change conditions, Frozen/Adaptive regimes, study/evidence classes, metrics and interval meanings.
- Use concise helper text, info/tooltips and contextual/expandable help. Required workflow information cannot exist only in tooltips.
- Use consistent terminology across review, execution, history, results and export.
- Important status combines understandable text + stable icon/symbol + accessible semantic visual treatment; color alone is insufficient.
- Warning/error/locked states state what happened, what is affected and the useful next action.
- Empty/loading/disabled/unavailable states explain why and what can be done next.
- Confirm only destructive/high-impact operations; routine interaction remains friction-light.
- Progressive disclosure hides implementation detail, not scientific meaning.
- Never fabricate telemetry, trajectory motion, progress, metrics, comparisons or completed artifacts.

## Scientific configuration boundary

### Frozen protocol-v2.1 mode

The UI loads immutable recipe/read-model values and may not silently alter:

- task/reward/gamma/information semantics;
- retained method configurations;
- roots/seeds and held-out final layouts;
- uncertainty/change families/severities/mappings;
- Phase-A or Phase-B interaction budgets/probe cadence;
- FN/FD/AN/AD branch contract/checkpoint origins;
- recovery window/tolerance/stability/censoring policy;
- root/layout aggregation or statistical contrast/interval policy.

The UI shows those values readably and explains why they are locked.

### DEVELOPMENT / exploratory mode

Only explicitly permitted development settings are editable. Every generated Study/configuration keeps stable identity/provenance and cannot later masquerade as confirmatory evidence.

- distinguish fixed, editable, advanced and unavailable settings;
- validate method-specific settings and compatibility before Study creation;
- avoid a free-form panel capable of constructing invalid protocol combinations;
- never expose “try another seed” as a way to replace a poor scientific outcome.

## Study review / pre-run review

Before creation/execution, present a readable resolved Study summary:

- purpose, evidence class and protocol version;
- selected/permitted methods and roles;
- layouts/conditions at a human-readable level;
- planned independent roots and scientific job/unit counts;
- Phase-A/Phase-B stages;
- known resource implications where evidence supports them;
- locked versus user-selected settings;
- validation/blocking issues;
- explicit label for DEVELOPMENT/non-thesis evidence;
- for frozen final Study, final-experiment authorization/lock state.

The user does not manually enumerate FN/FD/AN/AD or checkpoint IDs.

## Home / Studies

Purpose: durable Study state and objective next actions.

- frozen Thesis Study card/state, including execution lock when applicable;
- current/ready/running/recent DEVELOPMENT studies;
- protocol/evidence class/frozen state;
- current stage and truthful completed/failed/skipped/pending counts;
- actionable failures/warnings;
- quick actions to create/open/inspect results/evidence.

Resource status remains a lightweight current snapshot, not an observability platform.

## Run / Monitor

Purpose: observe real execution without influencing it.

- truthful Study stage/job state from durable backend data;
- method/root/layout/condition currently executing when useful;
- progress based on real scientific interaction/job counters, never elapsed-time animation pretending to be progress;
- read-only GridWorld/trajectory data only when scientifically isolated backend observation is available;
- real warnings/errors/events and lightweight resources;
- cancellation/retry only where lifecycle semantics permit; unsupported controls remain explicit.

If historical evidence lacks step-level replay, say so rather than synthesizing it.

## History / Artifacts

- Search/filter by Study, method, configuration/root/layout/condition, state, evidence class and date when available.
- Completed/scientific-failed/infrastructure-failed/skipped/cancelled/interrupted units remain attributable.
- Study-first primary hierarchy with drill-down to jobs/runs/artifacts.
- Retry/rerun respects scientific identity; no favorable-seed replacement shortcut.
- Provenance, checksums, recipe/checkpoint/result identifiers use progressive disclosure.

## Results / Compare

The UI consumes validated stored analysis/read-model outputs. It never recomputes scientific estimands from raw evidence.

### RQ1 — Nominal learning

Show, where available:

- final standardized Phase-A no-learning performance;
- learning trajectory/time-average summary;
- root-level distributions and explicit denominators;
- direct root-paired method contrasts/pointwise intervals emitted by the validated analysis;
- resource/computational evidence separately from policy quality.

### RQ2 — Resilience/adaptation

Show component effects separately:

- Frozen disturbance loss `FN-FD`;
- Adaptive disturbance loss `AN-AD`;
- primary adaptation benefit `(FN-FD)-(AN-AD)`;
- branch-level FN/FD/AN/AD details on demand;
- condition-family separation;
- direct method contrasts and denominators/failure state from stored analysis.

### RQ3 — Recovery speed

For protocol-v2.1 schema-v2 evidence, show stored:

- AN-vs-AD 32-interaction recovery trajectories;
- recovery status by method/condition/root where appropriate;
- observed recovery time conditional on recovery;
- separately named restricted fixed-horizon recovery delay;
- right-censored non-recovery without inventing a 256-step observed recovery time;
- primary action-remap family plus supporting diagnostics;
- sensitivity outputs when present;
- direct method contrasts emitted by analysis.

Do not derive the 0.10/0.05/0.20 thresholds, stable-window logic or root reductions in the UI. They come from validated stored evidence/metadata.

Historical schema-v1 packages remain truthful historical evidence and do not expose synthetic v2.1 recovery semantics.

### Comparison rules

- Compare only scientifically compatible protocol/evidence definitions.
- Show effect sizes/intervals only when emitted by validated analysis.
- Never relabel SD as CI or pointwise intervals as formal superiority tests.
- No best-run-only view, unlabeled composite resilience score or post-hoc best-setting selection.
- Explain incomplete/common-root blocks and retained failures rather than silently dropping them.

## Evidence / Export

Purpose: inspect and hand off reproducible stored evidence.

- evidence-handoff manifest and result index;
- deterministic analysis/root/recovery/direct-comparison CSV/JSON outputs;
- stable result/evidence IDs and source Study/recipe/protocol/evidence-class summary;
- full checksums/provenance/lineage under progressive disclosure;
- thesis-ready tables/figures only when generated from validated/frozen evidence;
- clear separation between scientific evidence and illustrative UI screenshots/GIF/video;
- empty states explain which upstream stage is required.

Whatever happens to be visible on screen is never the authoritative export source.

## Help and onboarding

Provide short replayable/skippable onboarding after the main structure stabilizes: orientation, Thesis Study versus DEVELOPMENT, review, run/monitor, results, evidence/export/help. Every page remains understandable if onboarding is skipped.

Contextual help should explain:

- the five retained methods;
- Frozen/Adaptive and FN/FD/AN/AD methodology;
- RQ1/RQ2/RQ3 metrics/estimands/interval/censoring concepts;
- evidence classes and final-experiment lock;
- provenance/checksums/recipe hashes;
- advanced DEVELOPMENT configuration and resource/storage warnings.

## Visual principles

- Stable small navigation and clear hierarchy.
- Modern compact desktop/laptop density rather than oversized decoration.
- Consistent typography, spacing, icons, tables and charts.
- Method identity consistent across GridWorld/charts/tables without relying on color alone.
- Restrained hover/focus/selection feedback and purposeful chart/GridWorld animation may improve comprehension.
- Respect reduced motion and never animate fabricated scientific progress/data.
- Separate execution controls, provisional interpretation and finalized evidence interpretation.
- Every visible scientific value comes from real backend/read-model data and a versioned definition.
