# Confirmed Requirements

This file contains only requirements established by the latest explicit user instruction, the official application, verified official guidance, or accepted current project decisions implementing explicit user direction.

**Status values:** `CONFIRMED`, `PARTIALLY_CONFIRMED`, `BLOCKED_BY_DECISION`, `DEFERRED`.

## Academic

| ID | Requirement | Source / rationale | Status | Acceptance criterion |
|---|---|---|---|---|
| REQ-ACA-001 | The work is a thesis of the Department of Informatics and Computer Engineering, School of Engineering, University of West Attica. | Official application. | CONFIRMED | Consistent use across repository and Word deliverable. |
| REQ-ACA-002 | The exact official Greek title is “Σύγκριση και Αξιολόγηση Ανθεκτικών Πρακτόρων Τεχνητής Νοημοσύνης σε Περιβάλλοντα με Αβεβαιότητα”. | Official application. | CONFIRMED | Exact use until a formal change. |
| REQ-ACA-003 | The official English title is “Comparison and Evaluation of Resilient AI Agents in Uncertain Environments”. | Official application. | CONFIRMED | Exact use until a formal change. |
| REQ-ACA-004 | The topic is approved. No supervisor identity or supervisor-specific instruction is required to continue research, implementation, pilots, or experiments. Later supervisor corrections are incorporated when actually received. | Explicit user clarification, 2026-08-04. | CONFIRMED | Current work is not blocked by missing supervisor details; later feedback is recorded as an explicit change. |
| REQ-ACA-005 | Current official Department instructions override historical examples and informal formatting references. | User decision. | CONFIRMED | Formatting checklist uses verified official sources near submission. |
| REQ-ACA-006 | No current submission or presentation deadline has been provided; the project must not invent dates or delay research and implementation because a schedule is unavailable. | Explicit user clarification, 2026-08-04. | CONFIRMED | Scheduling remains unset until real dates are provided. |
| REQ-ACA-007 | Completed theses supplied later by the user may be used only as contextual examples of structure and presentation, not as authoritative requirements. | Explicit user direction, 2026-08-04. | DEFERRED | Examples are reviewed near writing and never override official guidance. |

## Research

| ID | Requirement | Source / rationale | Status | Acceptance criterion |
|---|---|---|---|---|
| REQ-RES-001 | The research compares resilient decision agents under uncertainty and dynamic change. | Official application. | CONFIRMED | RQs and experiment matrix map directly to the official topic. |
| REQ-RES-002 | Use a simple simulated environment, with GridWorld as the confirmed direction. | Application and user direction. | CONFIRMED | Versioned, validated GridWorld specification. |
| REQ-RES-003 | Evaluation addresses adaptation, resilience, and recovery speed. | Official application. | CONFIRMED | Valid operational definitions and metrics. |
| REQ-RES-004 | Uncertainty mechanisms are defined, parameterized, and tested. | Scientific validity. | CONFIRMED | Schema, severity, seeding, and tests. |
| REQ-RES-005 | Final models are selected after bibliography evidence, environment definition, actual inventory, prototypes, and pilots; historical chats do not define the shortlist. | User decision. | CONFIRMED | Verified inclusion/exclusion decision. |
| REQ-RES-006 | The dashboard supports rather than replaces the research contribution. | User decision. | CONFIRMED | Contribution statement is grounded in protocol/results. |
| REQ-RES-007 | Old chats are not a shortlist or preference source. | User clarification. | CONFIRMED | Fresh evidence drives selections. |
| REQ-RES-008 | GridWorld implementation is selected through a current reuse/adapt/custom comparison. | User clarification. | CONFIRMED | Landscape review, prototype, and ADR. |
| REQ-RES-009 | The research question and experimental design must be clear, bounded, and realistically completable. | User scope refinement. | CONFIRMED | Small explainable matrix within measured resources. |
| REQ-RES-010 | The number of models and uncertainty types remains the minimum scientifically sufficient set. | User scope refinement. | CONFIRMED | Every included factor has distinct RQ value; redundant options are rejected. |
| REQ-RES-011 | Related primary studies are examined for research question, method, experimental design, results, and limitations before final GridWorld/models/metrics/protocol selection. | User research direction. | CONFIRMED | Decision-driving selections trace to verified `ThesisBibliography` analyses/evidence. |
| REQ-RES-012 | Literature research is refreshed before protocol freeze, major writing gates, and submission. | User research direction/freshness control. | CONFIRMED | Dated refresh in `ThesisBibliography` followed by controlled verified sync. |
| REQ-RES-013 | Immediate priority is scientific model/agent research, environment/protocol definition, program implementation, and evidence-producing experiments; normal chapter drafting/final formatting occur later. | Explicit user direction, 2026-08-04. | CONFIRMED | Roadmap prioritizes research/program work while preserving structured writing notes. |

## Experimental

| ID | Requirement | Source / rationale | Status | Acceptance criterion |
|---|---|---|---|---|
| REQ-EXP-001 | Single-run model comparison is not allowed. | User decision. | CONFIRMED | Multiple predefined independent seeds/repetitions. |
| REQ-EXP-002 | Development/tuning/pilot/exploratory/final evidence remain separated. | User decision + DEC-023. | CONFIRMED | Explicit protocol stage/partition and frozen final set. |
| REQ-EXP-003 | Model-specific settings are allowed under a fair documented protocol. | User decision. | CONFIRMED | Tuning policy and common evaluation. |
| REQ-EXP-004 | Failed, cancelled, interrupted, incomplete, invalid, and excluded runs are retained. | User decision. | CONFIRMED | No run silently disappears; reason is recorded. |
| REQ-EXP-005 | Resolved parameters/provenance are stored for every whole experiment. | User decision + DEC-023. | CONFIRMED | Immutable finalized run manifest/bundle. |
| REQ-EXP-006 | Final figures/tables are produced from real stored data. | User decision. | CONFIRMED | Reproducible artifact manifest. |
| REQ-EXP-007 | Seeds, repetitions, ranges, and budgets are justified by literature, pilots, and actual resources. | User decision. | CONFIRMED | Frozen protocol and compute estimate. |
| REQ-EXP-008 | The statistical analysis plan is frozen before final results are examined. | Bias control. | CONFIRMED | Frozen estimands, intervals, exclusions, and sensitivity plan. |
| REQ-EXP-009 | The UI exposes only approved/scientifically justified settings, not an uncontrolled parameter space. | User scope refinement. | CONFIRMED | Validated forms and progressive disclosure. |
| REQ-EXP-010 | A run ID represents one whole experiment, possibly with many seeds/episodes; there is at most one automatic result commit/push per finalized whole experiment, never one permanent commit per seed. | Explicit user direction, 2026-08-04; DEC-023. | CONFIRMED | Integration test proves multi-seed experiment produces one guarded commit/push. |
| REQ-EXP-011 | Useful large thesis-produced experiment artifacts are retained when storage permits and use configured Git LFS formats rather than being manually excluded solely due to size. | Explicit user direction, 2026-08-04; DEC-023. | CONFIRMED | LFS policy applied; retention changes only after real storage constraint/decision. |
| REQ-EXP-012 | The normal frozen final experiment campaign starts only after both the final protocol and intended user-facing application workflow are validated. Any final-run headless fallback uses the identical scientific core/configuration path and is documented. | Explicit user workflow request, 2026-08-04; current v1.1 refinement. | CONFIRMED | Task dependencies enforce application/protocol gates; final runs do not use an unvalidated alternate scientific path. |

## Functional application

| ID | Requirement | Source / rationale | Status | Acceptance criterion |
|---|---|---|---|---|
| REQ-APP-001 | Local single-user operation. | User decision. | CONFIRMED | No account service. |
| REQ-APP-002 | No authentication, roles, multi-user support, or required public deployment. | User decision. | CONFIRMED | No auth/cloud-only flows. |
| REQ-APP-003 | The user can create and execute required experiments without code/console commands or routine manual Git operations. | User decision. | CONFIRMED | End-to-end validated UI launch and automatic result persistence/publication. |
| REQ-APP-004 | Pause/resume/stop/cancel/restart only where technically safe and useful. | User decision and scope restraint. | PARTIALLY_CONFIRMED | Capability-based controls; unsupported states are explicit. |
| REQ-APP-005 | Status, progress, logs, warnings, errors, and metrics are real. | Integrity requirement. | CONFIRMED | UI derives from backend state/events. |
| REQ-APP-006 | Run history, comparison, result exploration, and export are supported. | User decision. | CONFIRMED | End-to-end history-to-export workflow. |
| REQ-APP-007 | GridWorld and agent visualization must not alter experiments. | User decision. | CONFIRMED | Read-only observer/trace/event visualization proven not to change scientific execution. |
| REQ-APP-008 | Show real CPU/RAM and supported GPU/VRAM telemetry where reliable. | User decision. | CONFIRMED | Source and unsupported states are visible. |
| REQ-APP-009 | The final application is a polished research dashboard, not a rough minimal demo. | User scope refinement. | CONFIRMED | Modern coherent screenshot-ready UI across essential workflows. |
| REQ-APP-010 | The feature set is limited to real thesis needs. | User scope refinement. | CONFIRMED | Pilot-derived required/optional/out-of-scope feature budget. |
| REQ-APP-011 | Models, seeds, settings, and uncertainty conditions are compared clearly with charts and tables. | User scope refinement. | CONFIRMED | Compatible comparison view with distributions/counts. |
| REQ-APP-012 | Resource telemetry remains a lightweight current snapshot, not an observability subsystem. | Accepted audit remediation. | CONFIRMED | CPU/RAM/disk and optional GPU current values only; no telemetry DB/agents/alerting. |
| REQ-APP-013 | “Application complete” means the real configure/run/monitor/history/compare/export user journey works end to end on the validated scientific core; rendered screens alone are insufficient. | Explicit user journey request, 2026-08-04; DEC-026. | CONFIRMED | Final application validation passes before final campaign unlock. |
| REQ-APP-014 | Root `run_app.bat` remains the normal one-click launcher from a repository checkout, while the final thesis delivery also includes a cleaned standalone Windows application folder that opens in its own desktop window. | Explicit user directions, 2026-08-26 and 2026-08-27; DEC-044. | CONFIRMED | Repository launcher uses the locked environment with actionable failures; final NiceGUI/PyInstaller `onedir + windowed` package runs without requiring the recipient to install Python/Node or interact with a browser/terminal. |
| REQ-APP-015 | The Runs workspace provides a smooth live GridWorld plus real live/provisional graphs so the user can observe and compare how compatible agents or approved settings behave during execution. | Explicit user direction, 2026-08-27; DEC-044/045. | CONFIRMED | Live visualization consumes truthful runtime observer/metric DTOs, supports compatible overlays, clearly labels provisional state, and visualization cadence/animation does not affect experiment timing/actions/RNG. |

## Architecture and technical

| ID | Requirement | Source / rationale | Status | Acceptance criterion |
|---|---|---|---|---|
| REQ-ARCH-001 | The research core works independently from the UI. | User decision. | CONFIRMED | Headless full-experiment smoke test. |
| REQ-ARCH-002 | Lightweight debug/visualization may assist core validation, but polished final dashboard starts after validated core/pilot evidence. | User workflow direction. | CONFIRMED | Scientific logic remains in core; final dashboard gate preserved. |
| REQ-ARCH-003 | Run/result storage does not depend on UI lifecycle. | Reliability. | CONFIRMED | Closing UI cannot corrupt evidence. |
| REQ-ARCH-004 | Avoid microservices, Kubernetes, cloud infrastructure, complex authentication, and production observability. | Local scope. | CONFIRMED | Bounded local architecture. |
| REQ-ARCH-005 | The accepted current stack baseline is Python 3.12 + `uv` + `src/resilient_agents/` + filesystem-first run bundles; final scientific dependencies and optional UI details follow real inventory/prototypes/pilots. | DEC-023. | CONFIRMED | CI lock validation, importable headless package, explicit later amendments only if justified. |
| REQ-ARCH-006 | Production infrastructure/distributed orchestration/enterprise observability are out of scope. | User scope refinement. | CONFIRMED | No such components without formal scope change. |
| REQ-ARCH-007 | Architecture supports a polished UI without exposing internal complexity. | User scope refinement. | CONFIRMED | Small navigation and unified validated workflows. |
| REQ-ARCH-008 | The final application surface is NiceGUI 3.16 native mode over the same headless Python scientific/runtime core; the historical Streamlit baseline and temporary React/Vite exploration are superseded implementation history only. | Explicit standalone-delivery clarification, 2026-08-27; DEC-044. | CONFIRMED | Scientific execution is not duplicated in NiceGUI callbacks; native and CI browser modes consume the same application/service contracts; no active second frontend stack remains. |
| REQ-ARCH-009 | Evaluator ground truth and agent-visible information are explicitly separated; no hidden privileged state/change/disturbance information is leaked without protocol justification. | Scientific fairness + DEC-023. | CONFIRMED | Contract/integration tests enforce boundary. |
| REQ-ARCH-010 | Randomness uses independent deterministic streams for scientifically distinct mechanisms. | Reproducibility + DEC-023. | CONFIRMED | Derived stream seeds deterministic/independent and stored in provenance. |
| REQ-TECH-001 | Do not assume NVIDIA/CUDA or GPU availability before actual-machine inventory. | User decision. | CONFIRMED | Capability report first for compute-dependent decisions. |
| REQ-TECH-002 | Codex automatically collects actual hardware/software/storage information. | User decision. | CONFIRMED | Versioned privacy-minimal inventory without manual transcription. |
| REQ-TECH-003 | Python environment resolution is reproducible from committed `pyproject.toml`, `.python-version`, and `uv.lock`. | DEC-023. | CONFIRMED | `uv lock --check` and `uv sync --locked` pass in CI. |

## UI/UX

| ID | Requirement | Source / rationale | Status | Acceptance criterion |
|---|---|---|---|---|
| REQ-UI-001 | Modern, clean, visually polished appearance. | User decision. | CONFIRMED | Consistent design system/research views. |
| REQ-UI-002 | Aesthetics do not override correctness, reliability, or usability. | Priority rule. | CONFIRMED | No decorative behavior hides scientific state. |
| REQ-UI-003 | No fake progress, mock final metrics, fabricated logs, or inconsistent states. | Integrity rule. | CONFIRMED | Integration tests against real runner state. |
| REQ-UI-004 | Views must be suitable for screenshots/presentation. | User decision. | CONFIRMED | Legible stable labels/export-ready layouts. |
| REQ-UI-005 | Responsive desktop/laptop layouts, consistent cards/charts/filters/tables, and clear loading/error/empty states. | User scope refinement. | CONFIRMED | UX review of essential workflows. |
| REQ-UI-006 | Scientific metadata remains accessible even when complexity is hidden with progressive disclosure. | User scope refinement. | CONFIRMED | Definitions/parameters/provenance reachable from context. |
| REQ-UI-007 | Full checksums/manifests/software/hardware/provenance chains do not clutter primary views. | Accepted audit remediation. | CONFIRMED | Essential provenance in main view; full details expandable/exported. |
| REQ-UI-008 | The final dashboard is self-explanatory through precise human-readable labels, helper text, visible units, consistent terminology, messages and visual hierarchy. | Explicit user direction, 2026-08-04. | CONFIRMED | Primary workflow can be understood without a separate manual; internal codes do not replace understandable names. |
| REQ-UI-009 | Non-obvious scientific/technical terms, metrics and controls provide concise tooltips or contextual help that agrees with the frozen protocol/definitions. | Explicit user direction, 2026-08-04. | CONFIRMED | UX review confirms explanations are present, accurate and non-conflicting across relevant screens. |
| REQ-UI-010 | Status/validation meaning uses consistent text plus symbols/icons and an accessible semantic visual palette; color is never the sole essential signal. | Explicit user direction, 2026-08-04. | CONFIRMED | Success/info/warning/error/disabled/selected states are distinguishable, consistently used and understandable without color alone. |
| REQ-UI-011 | Before launch, the UI presents a clear resolved-configuration/validation summary including the selected experiment setup, protocol identity, run count and blocking issues. | Explicit user direction, 2026-08-04. | CONFIRMED | User can verify what will execute and invalid configurations cannot launch silently. |
| REQ-UI-012 | Empty, loading, disabled, warning and error states are actionable: explain what is happening/affected and the appropriate next step when non-obvious; key workflow boundaries may show a next recommended action. | Explicit user direction, 2026-08-04. | CONFIRMED | No unexplained blank/disabled/error primary state in the normal workflow. |
| REQ-UI-013 | After the final dashboard structure is stable, provide a short first-run onboarding/tutorial for the essential workflow with Previous/Next/Skip/Finish and replay from Help/Getting Started. | Explicit user direction, 2026-08-04. | CONFIRMED | Tutorial is skippable/non-blocking, roughly 5–7 essential steps, and can be replayed later. |
| REQ-UI-014 | Onboarding/help remains lightweight using native NiceGUI/local application-state mechanisms; do not add accounts/new persistence or a heavyweight separate JavaScript/DOM tour subsystem without demonstrated need. | Original scope restraint plus framework amendment DEC-044/046, 2026-08-27. | CONFIRMED | Help/onboarding adds minimal complexity, is local/skippable/replayable, and does not create another frontend stack or duplicate scientific logic. |
| REQ-UI-015 | Confirmation dialogs are reserved for destructive/high-impact actions where accidental activation matters; routine navigation/configuration should remain friction-light. | Explicit user direction, 2026-08-04. | CONFIRMED | UX review finds confirmations proportionate to action risk. |
| REQ-UI-016 | The primary interface is novice-first: a user with no coding, RL, model, configuration, or repository knowledge can understand the main agents, conditions, settings, metrics, units and statuses without a separate manual. | Explicit user direction, 2026-08-27; DEC-046. | CONFIRMED | Plain-language primary labels, secondary technical IDs, concise explanations/tooltips, progressive disclosure and readable pre-run review allow a non-technical intended user to complete the core workflow. |
| REQ-UI-017 | The visual language is modern and compact, with consistent icons, semantic colors, restrained micro-interactions and purposeful animations for selection/status/charts/GridWorld while preserving accessibility and scientific truthfulness. | Explicit user direction, 2026-08-27; DEC-046. | CONFIRMED | Desktop/laptop screens remain information-dense but readable; animations improve comprehension, remain understandable with reduced motion where practical, and never imply progress or data that did not occur. |

## Repository and provenance

| ID | Requirement | Source / rationale | Status | Acceptance criterion |
|---|---|---|---|---|
| REQ-REPO-001 | This repository is the permanent source of truth for thesis context, code, experiments, results, writing, and presentation; bibliography lifecycle ownership is the explicit exception. Repository visibility may be changed temporarily for CI/Actions when explicitly chosen by the user and does not alter the source-of-truth or release/privacy rules. | User decision/current architecture; explicit visibility clarification 2026-08-25. | CONFIRMED | Context/decisions/configs/results/deliverables remain versioned and the bibliography boundary remains explicit regardless of temporary repository visibility. |
| REQ-REPO-002 | The official application is stored unchanged. | User decision. | CONFIRMED | Repository SHA-256 recorded. |
| REQ-REPO-003 | Raw chat exports are not committed. | User decision. | CONFIRMED | Content scan passes. |
| REQ-REPO-004 | Do not store secrets, credentials, virtual environments, caches, or useless artifacts. | Security. | CONFIRMED | Ignore/scan/review. |
| REQ-REPO-005 | Useful large thesis-produced binaries/datasets/checkpoints/results may be committed automatically using the configured Git LFS policy; do not require per-run manual approval solely because files are large. | User direction + DEC-023. | CONFIRMED | LFS tracked formats/publisher safeguards; retention changed only for real storage constraints. |
| REQ-REPO-006 | Complete bibliography lifecycle belongs to `ThesisBibliography`; this repository consumes the complete generated corpus and enforces nested citation-ready formal trust. | Current bibliography architecture. | CONFIRMED | No new primary-source ingestion here; immutable provenance/integrity; no bibliography PDF/LFS import. |
| REQ-REPO-007 | Repository-authored operational/technical material is English; exact official Greek text/original-language scientific evidence remain unchanged where required. | Explicit user instruction, 2026-08-02. | CONFIRMED | Agent-facing docs/prompts/comments/naming English; source evidence not translated. |
| REQ-REPO-008 | Every material change reconciles all affected active source-of-truth/status/decision/workflow/prompt/task/lifecycle files in the same PR; obsolete files are deleted or explicitly marked historical. | Explicit user instruction, 2026-08-04; DEC-024/DEC-025/DEC-026. | CONFIRMED | PR checklist + documentation/task/lifecycle governance + CI validator. |
| REQ-REPO-009 | Prefer fewer meaningful permanent commits; coherent implementation PRs normally squash to one `main` commit and each finalized experiment produces at most one result commit. | Explicit user preference, 2026-08-04. | CONFIRMED | Squash merges/experiment publisher behavior. |
| REQ-REPO-010 | Maintain one canonical resumable task registry; every Codex session must inspect it before work, use available session memory plus durable Git/repository evidence, and preserve unfinished-task resume state so quota/session interruption does not lose work. | Explicit user direction, 2026-08-04; DEC-025. | CONFIRMED | `TASKS.md`, canonical prompt/AGENTS startup rules, checkpoint/resume policy, and CI validation. |
| REQ-REPO-011 | During long Codex execution, provide concise progress updates at meaningful completed/validated checkpoints. Use `X/Y` only when the denominator is objectively defined, report both an appropriate overall/current-deliverable view and a lower-level active section/task view when useful, and derive counts from canonical task state rather than invented percentages or a second tracker. | Explicit user direction, 2026-08-25; DEC-030. | CONFIRMED | Progress updates remain brief, checked work only counts as complete, `TASKS.md` is the source for project/work-package/deliverable counts, and task-level fractions are shown only for real finite substeps. |
| REQ-PROV-001 | Every result maps to run ID, resolved configuration, source files, processing code, and source Git commit. | Provenance. | CONFIRMED | Machine-readable manifest/bundle. |
| REQ-PROV-002 | Finalized raw results are immutable. | Reproducibility. | CONFIRMED | Checksums and no silent edits. |
| REQ-PROV-003 | Automatic result publication must refuse mixed provenance/unrelated tracked changes/unsafe remote state rather than forcing a commit; local run data survives publication failure. | DEC-023 safety requirement. | CONFIRMED | Publisher integration/failure tests. |
| REQ-PROV-004 | Final analysis must produce a frozen downstream evidence package mapping RQs/methods, citation-ready sources, runs/results, figures/tables/captions, and planned thesis/defense claims. | Explicit user lifecycle request, 2026-08-04; DEC-026. | CONFIRMED | `T-604`/successor evidence package is versioned and traceable before normal thesis drafting. |

## Tests

| ID | Requirement | Source / rationale | Status | Acceptance criterion |
|---|---|---|---|---|
| REQ-TEST-001 | Deterministic GridWorld tests cover transitions, rewards, termination, and disturbances. | Scientific validity. | CONFIRMED | Reference/invariant tests pass. |
| REQ-TEST-002 | Model adapters require contract/information-boundary tests. | Fair interface. | CONFIRMED | Agent contract verified. |
| REQ-TEST-003 | Runner requires lifecycle, persistence, recovery, publication, and failure tests. | Reliability. | CONFIRMED | Interruption/publication tests preserve valid state/data. |
| REQ-TEST-004 | Processing/aggregation/metrics code uses known synthetic fixtures. | Statistical correctness. | CONFIRMED | Hand-calculated values match. |
| REQ-TEST-005 | Reproducibility tests distinguish deterministic replay from statistical repeatability. | Honest reporting. | CONFIRMED | Modes/tolerances documented. |
| REQ-TEST-006 | CI checks mechanically detectable stale active-document states, including obsolete Codex prompt paths and incorrect formal-evidence labelling. | DEC-024. | CONFIRMED | `scripts/validate_documentation_consistency.py` passes. |
| REQ-TEST-007 | CI checks that the canonical task registry exists, contains unique task IDs/resume state, and is required by the canonical Codex startup flow. | DEC-025. | CONFIRMED | Documentation consistency validator fails on missing/broken task-registry invariants. |
| REQ-TEST-008 | CI checks that a task labelled `READY` does not reference incomplete required task-ID dependencies and that required lifecycle/presentation control files remain present/linked. | DEC-026 workflow audit. | CONFIRMED | Documentation consistency validator fails on invalid READY dependency state or missing required control files. |
| REQ-TEST-009 | Final application validation covers the self-explanatory UX contract and onboarding/help behavior in addition to backend correctness. | Explicit user direction, 2026-08-04. | CONFIRMED | Automated checks where practical plus documented visual/end-to-end UX review verify `REQ-UI-008` through `REQ-UI-017`. |
| REQ-TEST-010 | Test work is risk-based and proportional: add tests for task acceptance conditions, scientific invariants, critical reliability/security boundaries, and concrete regressions—not for arbitrary coverage or theoretical completeness. | Explicit user direction, 2026-08-04; quota/time restraint. | CONFIRMED | No coverage-percentage target or unjustified mutation/fuzz/property/combinatorial/snapshot expansion; test scope is explained by material risk. |
| REQ-TEST-011 | During implementation Codex runs targeted tests; tiny deterministic fixtures/smoke runs are used in CI, and the full repository checks are run when work is ready for review rather than repeatedly after every small edit. | Explicit user direction, 2026-08-04; quota/time restraint. | CONFIRMED | No pilot/final experiment matrix is executed as CI testing; passing full checks are not repeatedly rerun or re-analysed without a relevant change. |

## Thesis and deliverables

| ID | Requirement | Source / rationale | Status | Acceptance criterion |
|---|---|---|---|---|
| REQ-THESIS-001 | Thesis main language is Greek. | User decision. | CONFIRMED | Greek main text. |
| REQ-THESIS-002 | Final thesis deliverable is Microsoft Word. | User decision. | CONFIRMED | Validated `.docx`. |
| REQ-THESIS-003 | Final results/conclusions use only frozen real data. | User decision. | CONFIRMED | Claims map to artifacts. |
| REQ-THESIS-004 | No fabricated sources, DOI values, measurements, or conclusions. | Integrity. | CONFIRMED | Citation/provenance audit. |
| REQ-THESIS-005 | Figures/tables are generated automatically from real data. | User decision. | CONFIRMED | Rebuild command reproduces artifacts. |
| REQ-THESIS-006 | Greek summary/keywords and English abstract/keywords. | Department guidance. | CONFIRMED | Both present. |
| REQ-THESIS-007 | Related Work, Methodology, and Discussion are drafted from verified imported evidence after required bibliography freshness/full-evidence gates. | User research direction/current bibliography architecture. | CONFIRMED | Claims map to verified citation-ready `SRC-*` evidence and limitations. |
| REQ-THESIS-008 | Normal chapter drafting/final Word styling are deferred until research program/model study/protocol/evidence-producing experiments are mature; structured notes/evidence mappings/captions/method records are collected during implementation. | Explicit user direction, 2026-08-04. | CONFIRMED | Roadmap prioritizes research/program work without losing writing provenance. |
| REQ-THESIS-009 | Two or three completed theses supplied later may inform presentation/structure only; they are not scientific sources or official formatting authority. | Explicit user direction, 2026-08-04. | DEFERRED | Examples clearly labelled and checked against official guidance near writing. |
| REQ-THESIS-010 | A review-ready thesis precedes final freeze; supervisor/reviewer corrections received later are incorporated through an explicit revision cycle with affected evidence/citations/figures/method statements revalidated. | Explicit user journey request, 2026-08-04; DEC-026. | CONFIRMED | `T-711`/`T-712` complete or absence of required review cycle is recorded before final thesis freeze. |
| REQ-THESIS-011 | After the final thesis is stable, create a complete PowerPoint defense deck grounded in the final thesis, frozen experiment evidence, citation-ready sources, and real application assets. | Explicit user request, 2026-08-04; DEC-026. | DEFERRED | Final `.pptx` has a slide evidence map and no unsupported scientific/result claims. |
| REQ-THESIS-012 | The defense package includes embedded speaker notes and a separate full spoken Greek script synchronized slide-by-slide and detailed enough for rehearsal/following/reading during preparation. | Explicit user request, 2026-08-04; DEC-026. | DEFERRED | Notes/script match final slide order and thesis/evidence; final files are versioned. |
| REQ-THESIS-013 | The defense package is validated for current official duration/content/file requirements, PowerPoint rendering, legibility, timing with margin, factual/numerical consistency, and a tested fallback for any live demo. | Explicit user request/workflow decision, 2026-08-04; DEC-026. | DEFERRED | `T-722` passes before final delivery readiness. |
