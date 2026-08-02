# Confirmed Requirements

This file contains only requirements established by the latest explicit user instruction, the official application, or verified official guidance.

**Status values:** `CONFIRMED`, `PARTIALLY_CONFIRMED`, `BLOCKED_BY_DECISION`, `DEFERRED`.

## Academic

| ID | Requirement | Source / rationale | Status | Acceptance criterion |
|---|---|---|---|---|
| REQ-ACA-001 | The work is a thesis of the Department of Informatics and Computer Engineering, School of Engineering, University of West Attica. | Official application. | CONFIRMED | Consistent use across repository and Word deliverable. |
| REQ-ACA-002 | The exact official Greek title is “Σύγκριση και Αξιολόγηση Ανθεκτικών Πρακτόρων Τεχνητής Νοημοσύνης σε Περιβάλλοντα με Αβεβαιότητα”. | Official application. | CONFIRMED | Exact use until a formal change. |
| REQ-ACA-003 | The official English title is “Comparison and Evaluation of Resilient AI Agents in Uncertain Environments”. | Official application. | CONFIRMED | Exact use until a formal change. |
| REQ-ACA-004 | Supervisor identity and supervisor-specific requirements must be recorded before methodology is frozen. | Not yet provided. | BLOCKED_BY_DECISION | Updated context and decision entry. |
| REQ-ACA-005 | Current official Department instructions override historical examples. | User decision. | CONFIRMED | Formatting checklist from verified official sources. |

## Research

| ID | Requirement | Source / rationale | Status | Acceptance criterion |
|---|---|---|---|---|
| REQ-RES-001 | The research compares resilient decision agents under uncertainty and dynamic change. | Official application. | CONFIRMED | RQs and experiment matrix map directly to the official topic. |
| REQ-RES-002 | Use a simple simulated environment, with GridWorld as the confirmed direction. | Application and user direction. | CONFIRMED | Versioned, validated GridWorld specification. |
| REQ-RES-003 | Evaluation addresses adaptation, resilience, and recovery speed. | Official application. | CONFIRMED | Valid operational definitions and metrics. |
| REQ-RES-004 | Uncertainty mechanisms are defined, parameterized, and tested. | Scientific validity. | CONFIRMED | Schema, severity, seeding, and tests. |
| REQ-RES-005 | Models are selected from zero after bibliography evidence, environment definition, inventory, prototypes, and pilots. | User decision. | CONFIRMED | Verified inclusion/exclusion decision. |
| REQ-RES-006 | The dashboard supports rather than replaces the research contribution. | User decision. | CONFIRMED | Contribution statement is grounded in protocol/results. |
| REQ-RES-007 | Old chats are not a shortlist or preference source. | User clarification. | CONFIRMED | Fresh evidence drives selections. |
| REQ-RES-008 | GridWorld implementation is selected through a current reuse/adapt/custom comparison. | User clarification. | CONFIRMED | Landscape review, prototype, and ADR. |
| REQ-RES-009 | The research question and experimental design must be clear, bounded, and realistically completable. | Latest user scope refinement. | CONFIRMED | Small explainable matrix within measured resources. |
| REQ-RES-010 | The number of models and uncertainty types remains the minimum scientifically sufficient set. | Latest user scope refinement. | CONFIRMED | Every included factor has distinct RQ value; redundant options are rejected. |
| REQ-RES-011 | Related primary studies are examined for research question, method, experimental design, results, and limitations before GridWorld/models/metrics/protocol are selected. | User research direction. | CONFIRMED | Decision-driving selections trace to verified `ThesisBibliography` analyses/evidence. |
| REQ-RES-012 | Literature research is refreshed before protocol freeze, before major writing gates, and before submission. | User research direction and freshness control. | CONFIRMED | Dated refresh in `ThesisBibliography` followed by controlled verified sync. |

## Experimental

| ID | Requirement | Source / rationale | Status | Acceptance criterion |
|---|---|---|---|---|
| REQ-EXP-001 | Single-run model comparison is not allowed. | User decision. | CONFIRMED | Multiple predefined independent seeds/repetitions. |
| REQ-EXP-002 | Pilot, exploratory, and final runs remain distinct. | User decision. | CONFIRMED | `run_type` and frozen final set. |
| REQ-EXP-003 | Model-specific settings are allowed under a fair documented protocol. | User decision. | CONFIRMED | Tuning policy and common evaluation. |
| REQ-EXP-004 | Failed, cancelled, interrupted, incomplete, and excluded runs are retained. | User decision. | CONFIRMED | No run silently disappears; reason is recorded. |
| REQ-EXP-005 | Resolved parameters are stored for every run. | User decision. | CONFIRMED | Immutable run manifest. |
| REQ-EXP-006 | Final figures/tables are produced from real stored data. | User decision. | CONFIRMED | Reproducible artifact manifest. |
| REQ-EXP-007 | Seeds, repetitions, ranges, and budgets are justified by literature, pilots, and actual resources. | User decision. | CONFIRMED | Frozen protocol and compute estimate. |
| REQ-EXP-008 | The statistical analysis plan is frozen before final results are examined. | Bias control. | CONFIRMED | Frozen estimands, intervals, exclusions, and sensitivity plan. |
| REQ-EXP-009 | The UI exposes only approved or scientifically justified settings, not an uncontrolled parameter space. | User scope refinement. | CONFIRMED | Validated forms and progressive disclosure. |

## Functional application

| ID | Requirement | Source / rationale | Status | Acceptance criterion |
|---|---|---|---|---|
| REQ-APP-001 | Local single-user operation. | User decision. | CONFIRMED | No account service. |
| REQ-APP-002 | No authentication, roles, multi-user support, or required public deployment. | User decision. | CONFIRMED | No auth/cloud-only flows. |
| REQ-APP-003 | The user can create and execute required runs without code/console commands. | User decision. | CONFIRMED | End-to-end validated UI launch. |
| REQ-APP-004 | Pause/resume/stop/cancel/restart only where technically safe and useful. | User decision and scope restraint. | PARTIALLY_CONFIRMED | Capability-based controls; unsupported states are explicit. |
| REQ-APP-005 | Status, progress, logs, warnings, errors, and metrics are real. | Integrity requirement. | CONFIRMED | UI derives from backend state/events. |
| REQ-APP-006 | Run history, comparison, result exploration, and export are supported. | User decision. | CONFIRMED | End-to-end history-to-export workflow. |
| REQ-APP-007 | GridWorld and agent visualization must not alter experiments. | User decision. | CONFIRMED | Trace/event-based optional visualization. |
| REQ-APP-008 | Show real CPU/RAM and supported GPU/VRAM telemetry where reliable. | User decision. | CONFIRMED | Source and unsupported states are visible. |
| REQ-APP-009 | The final application is a polished research dashboard, not a rough minimal demo. | User scope refinement. | CONFIRMED | Modern coherent screenshot-ready UI across essential workflows. |
| REQ-APP-010 | The feature set is limited to real thesis needs. | User scope refinement. | CONFIRMED | Required/optional/out-of-scope feature budget before final dashboard implementation. |
| REQ-APP-011 | Models, seeds, settings, and uncertainty conditions are compared clearly with charts and tables. | User scope refinement. | CONFIRMED | Compatible comparison view with distributions and counts. |
| REQ-APP-012 | Resource telemetry remains a lightweight current snapshot, not an observability subsystem. | Accepted audit remediation. | CONFIRMED | CPU/RAM/disk and optional GPU current values only; no telemetry database, agents, or alerting platform. |

## Architecture and technical

| ID | Requirement | Source / rationale | Status | Acceptance criterion |
|---|---|---|---|---|
| REQ-ARCH-001 | The research core works independently from the UI. | User decision. | CONFIRMED | Headless run smoke test. |
| REQ-ARCH-002 | A lightweight debug/visualization surface may assist core validation, but the polished final dashboard starts only after validated core and pilot evidence. | User workflow direction and scope control. | CONFIRMED | Scientific logic remains in the core; final dashboard gate is preserved. |
| REQ-ARCH-003 | Run/result storage does not depend on the UI lifecycle. | Reliability. | CONFIRMED | Closing the UI does not corrupt evidence. |
| REQ-ARCH-004 | Avoid microservices, Kubernetes, cloud infrastructure, and complex authentication. | Local scope. | CONFIRMED | Bounded local architecture. |
| REQ-ARCH-005 | Final stack follows compatibility/prototype review. | Conflicting historical proposals. | CONFIRMED | ADR with evidence. |
| REQ-ARCH-006 | Production infrastructure, distributed orchestration, and enterprise observability are out of scope. | User scope refinement. | CONFIRMED | No such components without formal scope change. |
| REQ-ARCH-007 | Architecture must support a polished UI without exposing internal complexity to the user. | User scope refinement. | CONFIRMED | Small top-level navigation and unified validated workflows. |
| REQ-TECH-001 | Do not assume NVIDIA/CUDA or GPU availability before inventory. | User decision. | CONFIRMED | Capability report first. |
| REQ-TECH-002 | Codex automatically collects actual hardware/software/storage information. | User decision. | CONFIRMED | Versioned inventory without manual transcription. |

## UI/UX

| ID | Requirement | Source / rationale | Status | Acceptance criterion |
|---|---|---|---|---|
| REQ-UI-001 | Modern, clean, and visually polished appearance. | User decision. | CONFIRMED | Consistent design system and research views. |
| REQ-UI-002 | Aesthetics do not override correctness, reliability, or usability. | Priority rule. | CONFIRMED | No decorative behavior hides scientific state. |
| REQ-UI-003 | No fake progress, mock final metrics, fabricated logs, or inconsistent states. | Integrity rule. | CONFIRMED | Integration tests against real runner state. |
| REQ-UI-004 | Views must be suitable for screenshots and presentation. | User decision. | CONFIRMED | Legible stable labels and export-ready layouts. |
| REQ-UI-005 | Responsive desktop/laptop layouts, consistent cards/charts/filters/tables, and clear loading/error/empty states. | User scope refinement. | CONFIRMED | UX review of all essential workflows. |
| REQ-UI-006 | Scientific metadata remains accessible even when complexity is hidden with progressive disclosure. | User scope refinement. | CONFIRMED | Definitions, parameters, and provenance reachable from context. |
| REQ-UI-007 | Full checksums, manifests, software/hardware details, and provenance chains do not clutter primary views. | Accepted audit remediation. | CONFIRMED | Essential provenance in main view; full technical details in expandable panels or exports. |

## Repository and provenance

| ID | Requirement | Source / rationale | Status | Acceptance criterion |
|---|---|---|---|---|
| REQ-REPO-001 | This private repository is the permanent source of truth for thesis context, code, experiments, results, writing, and presentation; bibliography lifecycle ownership is the explicit exception defined by `BIBLIOGRAPHY_INTEGRATION.md`. | User decision and current architecture. | CONFIRMED | Context/decisions/configs are versioned; bibliography boundary remains explicit. |
| REQ-REPO-002 | The official application is stored unchanged. | User decision. | CONFIRMED | Repository SHA-256 recorded. |
| REQ-REPO-003 | Raw chat exports are not committed. | User decision. | CONFIRMED | Content scan passes. |
| REQ-REPO-004 | Do not store secrets, credentials, virtual environments, caches, or useless artifacts. | Security. | CONFIRMED | Ignore/scan/review. |
| REQ-REPO-005 | Large binaries/datasets/checkpoints are reviewed before commit. | Maintainability. | CONFIRMED | Storage/LFS policy. |
| REQ-REPO-006 | Complete source acquisition, original PDFs, OCR/Markdown conversion, source analysis, and verified evidence belong to `ThesisBibliography`; this repository consumes only the verified generated package. | Current bibliography architecture. | CONFIRMED | No new primary-source ingestion here; import is bound to `SOURCE_COMMIT` and integrity validation. |
| REQ-REPO-007 | Repository-authored operational/technical material is written in English; exact official Greek text and original-language scientific evidence remain unchanged where required. | Explicit user instruction, 2026-08-02. | CONFIRMED | Agent-facing docs/prompts/comments/naming are English; source evidence is not translated. |
| REQ-PROV-001 | Every result maps to run ID, configuration, source files, processing code, and commit. | Provenance. | CONFIRMED | Machine-readable manifest. |
| REQ-PROV-002 | Raw results are immutable. | Reproducibility. | CONFIRMED | Checksums and append-only corrections. |

## Tests

| ID | Requirement | Source / rationale | Status | Acceptance criterion |
|---|---|---|---|---|
| REQ-TEST-001 | Deterministic GridWorld tests cover transitions, rewards, termination, and disturbances. | Scientific validity. | CONFIRMED | Reference and invariant tests pass. |
| REQ-TEST-002 | Model adapters require contract tests. | Fair interface. | CONFIRMED | Agent contract verified. |
| REQ-TEST-003 | Runner requires lifecycle, persistence, recovery, and failure tests. | Reliability. | CONFIRMED | Interruption tests preserve valid state. |
| REQ-TEST-004 | Processing/aggregation code uses known synthetic fixtures. | Statistical correctness. | CONFIRMED | Hand-calculated values match. |
| REQ-TEST-005 | Reproducibility tests distinguish deterministic replay from statistical repeatability. | Honest reporting. | CONFIRMED | Modes and tolerances documented. |

## Thesis and deliverables

| ID | Requirement | Source / rationale | Status | Acceptance criterion |
|---|---|---|---|---|
| REQ-THESIS-001 | Thesis main language is Greek. | User decision. | CONFIRMED | Greek main text. |
| REQ-THESIS-002 | Final deliverable is Microsoft Word. | User decision. | CONFIRMED | Validated `.docx`. |
| REQ-THESIS-003 | Final results/conclusions use only frozen real data. | User decision. | CONFIRMED | Claims map to artifacts. |
| REQ-THESIS-004 | No fabricated sources, DOI values, measurements, or conclusions. | Integrity. | CONFIRMED | Citation and provenance audit. |
| REQ-THESIS-005 | Figures and tables are generated automatically from real data. | User decision. | CONFIRMED | Rebuild command reproduces artifacts. |
| REQ-THESIS-006 | Greek summary/keywords and English abstract/keywords. | Department guidance. | CONFIRMED | Both present. |
| REQ-THESIS-007 | Related Work, Methodology, and Discussion are drafted from verified imported evidence after the required `ThesisBibliography` freshness/full-evidence gates. | User research direction and current bibliography architecture. | CONFIRMED | Claims map to verified `SRC-*` evidence and recorded limitations at a pinned `SOURCE_COMMIT`. |
| REQ-DELIV-001 | Final repository includes code, configs, tests, imported verified bibliography evidence, thesis material, results, figures/tables/exports, and reproduction scripts. | User requirement. | DEFERRED | Final checklist complete. |