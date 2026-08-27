# Confirmed Requirements

This file records requirements established by current explicit user instruction, the approved application, verified official guidance, or accepted repository decisions. Historical requirements that were later superseded remain represented through their current replacement rather than as contradictory active rules.

**Status values:** `CONFIRMED`, `PARTIALLY_CONFIRMED`, `DEFERRED`.

## Academic

| ID | Requirement | Status |
|---|---|---|
| REQ-ACA-001 | Thesis of the Department of Informatics and Computer Engineering, School of Engineering, University of West Attica. | CONFIRMED |
| REQ-ACA-002 | Exact official Greek title: “Σύγκριση και Αξιολόγηση Ανθεκτικών Πρακτόρων Τεχνητής Νοημοσύνης σε Περιβάλλοντα με Αβεβαιότητα”. | CONFIRMED |
| REQ-ACA-003 | Official English title: “Comparison and Evaluation of Resilient AI Agents in Uncertain Environments”. | CONFIRMED |
| REQ-ACA-004 | Topic approved; no current supervisor identity/instruction is required to continue pre-WP7 research/application work. Later real corrections are incorporated explicitly. | CONFIRMED |
| REQ-ACA-005 | Current official Department guidance overrides historical examples/informal formatting references. | CONFIRMED |
| REQ-ACA-006 | No current submission/presentation deadline is known; do not invent one. | CONFIRMED |
| REQ-ACA-007 | Later supplied completed theses may be contextual structure/presentation examples only, not official/scientific authority. | DEFERRED |

## Research

| ID | Requirement | Status |
|---|---|---|
| REQ-RES-001 | Compare resilient decision agents under uncertainty/dynamic change in a simple controlled simulated environment. | CONFIRMED |
| REQ-RES-002 | GridWorld is the accepted simple-environment direction. | CONFIRMED |
| REQ-RES-003 | Evaluation addresses adaptation, resilience/degradation and recovery behavior. | CONFIRMED |
| REQ-RES-004 | Uncertainty mechanisms are explicit, parameterized, seeded and validated. | CONFIRMED |
| REQ-RES-005 | Scientific selections come from current bibliography/prototypes/pilots/evidence, not old-chat shortlists. | CONFIRMED |
| REQ-RES-006 | Application supports the research but is not the main scientific contribution. | CONFIRMED |
| REQ-RES-007 | Research/program/evidence work precedes normal thesis drafting; T-700+ stays gated. | CONFIRMED |
| REQ-RES-008 | Current candidate-v1.1 agent direction is F0 frozen Q-learning, C0 continual Q-learning and D0 Dyna-Q+; historical R0 evidence is preserved but unchanged R0 is not reinstated. | CONFIRMED |
| REQ-RES-009 | Do not add deep RL merely to increase model count; every added regime needs a distinct scientific role and explicit amendment. | CONFIRMED |

## Experimental

| ID | Requirement | Status |
|---|---|---|
| REQ-EXP-001 | Single-run comparison is forbidden; use predefined multiple paired/independent roots/repetitions. | CONFIRMED |
| REQ-EXP-002 | Development/tuning/pilot/exploratory/final evidence remain separated and stage-validated. | CONFIRMED |
| REQ-EXP-003 | Model-specific settings are allowed under a fair documented protocol. | CONFIRMED |
| REQ-EXP-004 | Failed/cancelled/interrupted/incomplete/invalid/excluded and non-recovery outcomes remain recorded. | CONFIRMED |
| REQ-EXP-005 | Complete resolved parameters/configuration identity/provenance are stored for every whole experiment. | CONFIRMED |
| REQ-EXP-006 | Final figures/tables come only from real stored frozen data. | CONFIRMED |
| REQ-EXP-007 | Seeds/repetitions/ranges/budgets/settings are justified by evidence/pilots/resources and frozen before corresponding final outcomes. | CONFIRMED |
| REQ-EXP-008 | Statistical analysis roles/procedures are frozen before final results are inspected. | CONFIRMED |
| REQ-EXP-009 | UI exposes only protocol-approved/scientifically justified settings and combinations. | CONFIRMED |
| REQ-EXP-010 | A run ID is one whole experiment, possibly many seeds/episodes; at most one guarded result commit/push per finalized whole experiment. | CONFIRMED |
| REQ-EXP-011 | Useful large thesis-produced experiment artifacts are retained when storage permits under the configured LFS policy. | CONFIRMED |
| REQ-EXP-012 | Final campaign begins only after protocol freeze + intended application acceptance; fallback uses the identical scientific core/config path. | CONFIRMED |
| REQ-EXP-013 | Development/tuning may execute **multiple approved resolved configurations per agent/regime** where the protocol predeclares them; each configuration uses multiple predefined roots, stable identity/provenance, and predeclared selection rules. No single-run/best-seed/best-final cherry-picking. | CONFIRMED |
| REQ-EXP-014 | Candidate-v1.1 preserves F0/C0 alpha 0.5, gamma 0.96875, epsilon 0.125, 512 training episodes/layout, 16 pre-change, 32 post-change, horizon 48 and 32 paired final roots; only bounded D0 `planning_steps`/`kappa` tuning is currently reopened. | CONFIRMED |
| REQ-EXP-015 | Candidate-v1.1 uses seven single-factor conditions, four fresh held-out final layouts, fresh precommitted final seeds, paired effects/95% CIs, explicit n and primary cumulative-deficit/immediate-degradation/terminal-performance roles; recovery remains secondary/sensitivity. | CONFIRMED |

## Functional application

| ID | Requirement | Status |
|---|---|---|
| REQ-APP-001 | Local single-user operation; no authentication/roles/multi-user requirement. | CONFIRMED |
| REQ-APP-002 | No mandatory public deployment/cloud/mobile/enterprise observability. | CONFIRMED |
| REQ-APP-003 | Required experiments are configurable/executable without code/console commands or routine manual Git. | CONFIRMED |
| REQ-APP-004 | Pause/resume/stop/cancel/restart only where technically safe; unsupported capabilities explicit. | PARTIALLY_CONFIRMED |
| REQ-APP-005 | Status/progress/logs/warnings/errors/metrics are truthful backend-derived state. | CONFIRMED |
| REQ-APP-006 | History/comparison/result exploration/artifact export are supported. | CONFIRMED |
| REQ-APP-007 | GridWorld/agent visualization never alters scientific execution. | CONFIRMED |
| REQ-APP-008 | Show real lightweight CPU/RAM/disk and supported GPU/VRAM snapshot where reliable. | CONFIRMED |
| REQ-APP-009 | Final application is polished research software, not a rough demo. | CONFIRMED |
| REQ-APP-010 | Feature set stays bounded to real research/reproducibility/usability/delivery needs. | CONFIRMED |
| REQ-APP-011 | Models, settings/configurations, seeds and uncertainty conditions can be compared clearly through validated charts/tables. | CONFIRMED |
| REQ-APP-012 | Resource telemetry remains lightweight; no monitoring platform/telemetry database. | CONFIRMED |
| REQ-APP-013 | “Complete” means configure -> validate -> launch -> monitor -> history -> compare -> export works end-to-end on real core state; rendered pages alone are insufficient. | CONFIRMED |
| REQ-APP-014 | Root `run_app.bat` remains the normal one-click repository-checkout Windows launcher and must track launch-path changes. | CONFIRMED |
| REQ-APP-015 | Final delivery also includes a validated NiceGUI/PyInstaller `onedir + windowed` Windows folder that opens its own window without recipient-installed Python/Node/browser interaction. | CONFIRMED |
| REQ-APP-016 | After application acceptance, an already-approved research/final configuration is executable directly from the finished application on the validated thesis machine; Codex/console commands are not required merely to run it. | CONFIRMED |
| REQ-APP-017 | GitHub remains source of truth/PR/CI/evidence coordination. GitHub-hosted runners are not automatically the validated final stochastic experiment machine; a self-hosted runner on the thesis machine is optional, not required. | CONFIRMED |

## Architecture and technical

| ID | Requirement | Status |
|---|---|---|
| REQ-ARCH-001 | `src/resilient_agents/` scientific core works independently from UI. | CONFIRMED |
| REQ-ARCH-002 | Run/result storage is independent from UI lifecycle. | CONFIRMED |
| REQ-ARCH-003 | Avoid microservices/Kubernetes/distributed platform/auth/enterprise observability. | CONFIRMED |
| REQ-ARCH-004 | Python 3.12 + `uv` + filesystem-first run bundles remain the core baseline. | CONFIRMED |
| REQ-ARCH-005 | Evaluator truth and agent-visible information are strictly separated. | CONFIRMED |
| REQ-ARCH-006 | Randomness uses independent deterministic streams for scientifically distinct mechanisms. | CONFIRMED |
| REQ-ARCH-007 | Current UI framework is **NiceGUI 3.16 native mode (`pywebview`)**, superseding historical Streamlit and temporary React/Vite. | CONFIRMED |
| REQ-ARCH-008 | T-530 supplies UI-independent active-run DTO/services; NiceGUI never reimplements scientific execution. | CONFIRMED |
| REQ-ARCH-009 | Final native delivery uses NiceGUI/PyInstaller onedir+windowed validated on the target Windows machine. | CONFIRMED |
| REQ-TECH-001 | Native Windows CPU execution is the required scientific baseline; no assumed NVIDIA/CUDA/GPU backend. | CONFIRMED |
| REQ-TECH-002 | Hardware/software/storage inventory is collected automatically where possible. | CONFIRMED |
| REQ-TECH-003 | Environment resolution is reproducible from committed project/lock files. | CONFIRMED |

## UI / UX

| ID | Requirement | Status |
|---|---|---|
| REQ-UI-001 | Modern, clean, polished appearance. | CONFIRMED |
| REQ-UI-002 | Aesthetics never override correctness/reliability/usability. | CONFIRMED |
| REQ-UI-003 | No fake progress, mock final metrics, fabricated logs, trajectory or inconsistent states. | CONFIRMED |
| REQ-UI-004 | Views are suitable for screenshots/presentation where scientifically appropriate. | CONFIRMED |
| REQ-UI-005 | Responsive desktop/laptop layouts and coherent cards/charts/filters/tables/states. | CONFIRMED |
| REQ-UI-006 | Scientific metadata/provenance remains accessible through progressive disclosure. | CONFIRMED |
| REQ-UI-007 | Full checksums/manifests/hardware details do not clutter primary views. | CONFIRMED |
| REQ-UI-008 | Self-explanatory human-readable labels/helper text/units/terminology/messages/hierarchy. | CONFIRMED |
| REQ-UI-009 | Non-obvious scientific/technical terms/metrics/settings/controls provide accurate tooltips/contextual help. | CONFIRMED |
| REQ-UI-010 | Status/validation uses text + icon/symbol + accessible semantic color; color is never sole signal. | CONFIRMED |
| REQ-UI-011 | Clear readable pre-run resolved-configuration summary includes selected agent/config identity, protocol/stage, conditions, seeds/repetitions, relevant settings, run count/retention/evidence class and blockers. | CONFIRMED |
| REQ-UI-012 | Empty/loading/disabled/warning/error/unavailable states are actionable. | CONFIRMED |
| REQ-UI-013 | Short skippable/replayable first-run onboarding with Previous/Next/Skip/Finish after stable screen structure. | CONFIRMED |
| REQ-UI-014 | Onboarding/help uses lightweight native/local NiceGUI state; no account/persistence/tour subsystem without demonstrated need. | CONFIRMED |
| REQ-UI-015 | Confirmation dialogs only for destructive/high-impact actions. | CONFIRMED |
| REQ-UI-016 | Interface must be understandable by a non-programmer with no RL/model/settings/repository knowledge; technical IDs remain secondary detail. | CONFIRMED |
| REQ-UI-017 | Modern **compact** hierarchy with consistent icons, restrained hover/focus/selection micro-interactions and purposeful GridWorld/chart/status animations; motion never fabricates data/progress or affects execution and remains understandable with reduced motion where practical. | CONFIRMED |
| REQ-UI-018 | New Experiment/Compare/Runs explicitly handle compatible **multiple agent configuration/settings identities** where the active protocol allows them and explain fixed vs tunable settings and repetition meaning. | CONFIRMED |
| REQ-UI-019 | Plotly = stored/final scientific views, ECharts = real live/provisional telemetry, Mermaid = explanations, AG Grid Community = analytical tables; live/provisional/final evidence classes are visibly distinct. | CONFIRMED |

## Repository / provenance / continuity

| ID | Requirement | Status |
|---|---|---|
| REQ-REPO-001 | Repository is permanent thesis lifecycle source of truth, with bibliography lifecycle as explicit external exception. | CONFIRMED |
| REQ-REPO-002 | Official application retained unchanged. | CONFIRMED |
| REQ-REPO-003 | Raw chat exports/secrets/credentials/caches/virtualenvs/useless artifacts are not tracked. | CONFIRMED |
| REQ-REPO-004 | Useful thesis-produced large files may use configured Git LFS rather than being discarded solely for size. | CONFIRMED |
| REQ-REPO-005 | Repository-authored technical/operational material is English; official Greek/original-language scientific evidence preserved where required. | CONFIRMED |
| REQ-REPO-006 | Material changes reconcile all affected active source-of-truth/status/task/prompt/decision/workflow files; obsolete active alternatives are removed or marked historical. | CONFIRMED |
| REQ-REPO-007 | Prefer fewer meaningful permanent commits; coherent implementation PRs normally squash when governing gates allow. | CONFIRMED |
| REQ-REPO-008 | `TASKS.md` is the canonical resumable task registry; session/branch/PR/test state protects against quota/chat interruption. | CONFIRMED |
| REQ-REPO-009 | Progress `X/Y` comes only from objective finite canonical denominators; in-progress/failed work never counts complete. | CONFIRMED |
| REQ-PROV-001 | Every result maps to run/config/protocol/source commit/software/capability/artifact identity. | CONFIRMED |
| REQ-PROV-002 | Finalized raw results are immutable/checksummed. | CONFIRMED |
| REQ-PROV-003 | Automatic publication fails closed on unsafe provenance/Git state while preserving local run data. | CONFIRMED |
| REQ-PROV-004 | Final analysis produces a frozen downstream thesis/defense evidence package before writing. | CONFIRMED |

## Testing

| ID | Requirement | Status |
|---|---|---|
| REQ-TEST-001 | Deterministic GridWorld/agent/runner/metric contracts receive focused known-answer/invariant tests. | CONFIRMED |
| REQ-TEST-002 | Information-boundary/determinism/serialization/lifecycle/provenance critical behavior is tested proportionally. | CONFIRMED |
| REQ-TEST-003 | CI validates mechanically detectable documentation/task/config consistency. | CONFIRMED |
| REQ-TEST-004 | Test work is risk-based/proportional, not a coverage/mutation/fuzz/exhaustive-matrix project. | CONFIRMED |
| REQ-TEST-005 | During implementation use targeted checks; PR CI is canonical full-suite guard; pilot/final experiment matrices are never CI tests. | CONFIRMED |
| REQ-TEST-006 | Final application validation includes novice-first UX/help/onboarding and real end-to-end behavior, not only rendering. | CONFIRMED |

## Thesis / defense / manual assets

| ID | Requirement | Status |
|---|---|---|
| REQ-THESIS-001 | Final thesis main language Greek; required final artifact `.docx`. | CONFIRMED |
| REQ-THESIS-002 | Final claims use citation-ready bibliography and frozen accepted experiment evidence only. | CONFIRMED |
| REQ-THESIS-003 | Figures/tables are generated from real versioned data; no fabricated sources/results. | CONFIRMED |
| REQ-THESIS-004 | Greek summary/keywords and English abstract/keywords required under current snapshot, subject to T-700 recheck. | CONFIRMED |
| REQ-THESIS-005 | Review-ready Word thesis precedes final freeze; supervisor/reviewer corrections trigger affected-evidence revalidation. | CONFIRMED |
| REQ-THESIS-006 | Word workflow uses real heading styles/automatic TOC, caption fields, cross-references, lists of figures/tables and final field update rather than manual numbering where practical. | CONFIRMED |
| REQ-THESIS-007 | User may capture real application screenshots/GIF/video, but every requested capture receives an exact `ASSET-*` record: page/state/run/config/crop, purpose, chapter/section/slide, caption/placement/size, evidence ID and static fallback. | CONFIRMED |
| REQ-THESIS-008 | Essential thesis claims remain understandable in static print/PDF form; animation/live demo never replaces quantitative/static evidence. | CONFIRMED |
| REQ-THESIS-009 | Final defense package includes `.pptx`, embedded speaker notes and separate full spoken Greek script grounded in final thesis/evidence. | DEFERRED |
| REQ-THESIS-010 | Microsoft PowerPoint is final deck inspection/rehearsal surface; Canva is optional polish only and any PPTX round trip is revalidated in PowerPoint. | DEFERRED |
| REQ-THESIS-011 | ChatGPT is preferred later for Greek thesis/slide narrative/review/placement guidance; Codex/repository automation owns traceable evidence/assets/technical consistency. | DEFERRED |
| REQ-THESIS-012 | `docs/thesis/WP7_WP8_TOOL_WORKFLOW.md` plans T-700+ ownership but does not unlock WP7; explicit user approval remains mandatory. | CONFIRMED |