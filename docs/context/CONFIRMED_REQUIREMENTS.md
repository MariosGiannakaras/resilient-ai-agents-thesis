# Confirmed Requirements

Το παρόν αρχείο περιλαμβάνει μόνο απαιτήσεις που επιβεβαιώνονται από τη νεότερη ρητή οδηγία του χρήστη, την επίσημη αίτηση ή επαληθευμένη επίσημη οδηγία.

**Status values:** `CONFIRMED`, `PARTIALLY_CONFIRMED`, `BLOCKED_BY_DECISION`, `DEFERRED`.

## Academic

| ID | Requirement | Source / rationale | Status | Acceptance criterion |
|---|---|---|---|---|
| REQ-ACA-001 | Η εργασία είναι διπλωματική του Τμήματος Μηχανικών Πληροφορικής και Υπολογιστών, Σχολή Μηχανικών, Πανεπιστήμιο Δυτικής Αττικής. | Επίσημη αίτηση. | CONFIRMED | Συνεπής χρήση σε repository και Word. |
| REQ-ACA-002 | Ο επίσημος ελληνικός τίτλος είναι «Σύγκριση και Αξιολόγηση Ανθεκτικών Πρακτόρων Τεχνητής Νοημοσύνης σε Περιβάλλοντα με Αβεβαιότητα». | Επίσημη αίτηση. | CONFIRMED | Ακριβής χρήση μέχρι formal change. |
| REQ-ACA-003 | Ο επίσημος αγγλικός τίτλος είναι “Comparison and Evaluation of Resilient AI Agents in Uncertain Environments”. | Επίσημη αίτηση. | CONFIRMED | Ακριβής χρήση μέχρι formal change. |
| REQ-ACA-004 | Ο επιβλέπων και οι ειδικές απαιτήσεις του πρέπει να καταγραφούν πριν παγώσει η μεθοδολογία. | Δεν έχουν δοθεί. | BLOCKED_BY_DECISION | Updated context and decision entry. |
| REQ-ACA-005 | Οι ισχύουσες official Department instructions υπερισχύουν historical examples. | User decision. | CONFIRMED | Formatting checklist από verified sources. |

## Research

| ID | Requirement | Source / rationale | Status | Acceptance criterion |
|---|---|---|---|---|
| REQ-RES-001 | Η έρευνα συγκρίνει ανθεκτικούς decision agents υπό uncertainty και dynamic change. | Official application. | CONFIRMED | RQs και matrix συνδέονται άμεσα με το official topic. |
| REQ-RES-002 | Χρησιμοποιείται απλό simulated environment, με GridWorld ως confirmed direction. | Application and user direction. | CONFIRMED | Versioned validated GridWorld specification. |
| REQ-RES-003 | Η αξιολόγηση εξετάζει adaptation, resilience και recovery speed. | Official application. | CONFIRMED | Valid operational definitions and metrics. |
| REQ-RES-004 | Οι uncertainty mechanisms ορίζονται, παραμετροποιούνται και ελέγχονται. | Scientific validity. | CONFIRMED | Schema, severity, seeding and tests. |
| REQ-RES-005 | Models επιλέγονται από μηδενική βάση μετά από literature, environment, inventory, prototypes και pilots. | User decision. | CONFIRMED | Verified inclusion/exclusion decision. |
| REQ-RES-006 | Το dashboard υποστηρίζει και δεν υποκαθιστά το research contribution. | User decision. | CONFIRMED | Contribution statement βασίζεται σε protocol/results. |
| REQ-RES-007 | Old chats δεν αποτελούν shortlist ή preference. | User clarification. | CONFIRMED | Fresh evidence drives selections. |
| REQ-RES-008 | GridWorld implementation επιλέγεται με current reuse/adapt/custom comparison. | User clarification. | CONFIRMED | Landscape review, prototype and ADR. |
| REQ-RES-009 | Το research question και το experimental design πρέπει να είναι σαφή, bounded και realistically completable. | Latest user scope refinement. | CONFIRMED | Small explainable matrix within measured resources. |
| REQ-RES-010 | Ο αριθμός models και uncertainty types παραμένει ο ελάχιστος scientifically sufficient. | Latest user scope refinement. | CONFIRMED | Every included factor has distinct RQ value; redundant options rejected. |
| REQ-RES-011 | Παρόμοιες πρωτογενείς μελέτες εξετάζονται ως προς research question, method, experimental design, results και limitations πριν επιλεγούν GridWorld, models, metrics ή protocol. | Latest user research direction. | CONFIRMED | Updated related-work evidence matrix with full-text status and explicit relevance. |
| REQ-RES-012 | Η literature search επαναλαμβάνεται πριν από protocol freeze, πριν από Related Work/Methodology/Discussion και πριν από submission. | Latest user research direction and freshness control. | CONFIRMED | Dated refresh entries and citation audit at each gate. |

## Experimental

| ID | Requirement | Source / rationale | Status | Acceptance criterion |
|---|---|---|---|---|
| REQ-EXP-001 | Δεν επιτρέπεται single-run model comparison. | User decision. | CONFIRMED | Multiple predefined independent seeds/repetitions. |
| REQ-EXP-002 | Pilot, exploratory and final runs παραμένουν διακριτά. | User decision. | CONFIRMED | `run_type` and frozen final set. |
| REQ-EXP-003 | Model-specific settings επιτρέπονται με fair documented protocol. | User decision. | CONFIRMED | Tuning policy and common evaluation. |
| REQ-EXP-004 | Failed, cancelled, interrupted, incomplete and excluded runs καταγράφονται. | User decision. | CONFIRMED | No run disappears; reason recorded. |
| REQ-EXP-005 | Resolved parameters αποθηκεύονται ανά run. | User decision. | CONFIRMED | Immutable run manifest. |
| REQ-EXP-006 | Final figures/tables προκύπτουν από real stored data. | User decision. | CONFIRMED | Reproducible artifact manifest. |
| REQ-EXP-007 | Seeds, repetitions, ranges and budgets βασίζονται σε literature, pilots and resources. | User decision. | CONFIRMED | Frozen protocol and estimate. |
| REQ-EXP-008 | Statistical analysis plan παγώνει πριν εξεταστούν final results. | Bias control. | CONFIRMED | Frozen estimands, intervals, exclusions and sensitivity plan. |
| REQ-EXP-009 | Το UI εκθέτει μόνο approved ή scientifically justified settings και όχι ανεξέλεγκτο parameter space. | Latest user scope refinement. | CONFIRMED | Validated forms and progressive disclosure. |

## Functional application

| ID | Requirement | Source / rationale | Status | Acceptance criterion |
|---|---|---|---|---|
| REQ-APP-001 | Local single-user operation. | User decision. | CONFIRMED | No account service. |
| REQ-APP-002 | No authentication, roles, multi-user or public deployment. | User decision. | CONFIRMED | No auth/cloud-only flows. |
| REQ-APP-003 | Ο χρήστης δημιουργεί και εκτελεί required runs χωρίς code/console. | User decision. | CONFIRMED | End-to-end validated UI launch. |
| REQ-APP-004 | Pause/resume/stop/cancel/restart μόνο όπου technically safe and useful. | User decision and scope restraint. | PARTIALLY_CONFIRMED | Capability-based controls; unsupported states explicit. |
| REQ-APP-005 | Real status, progress, logs, warnings, errors and metrics. | Integrity requirement. | CONFIRMED | UI derives from backend state/events. |
| REQ-APP-006 | Run history, comparison, result exploration and export. | User decision. | CONFIRMED | End-to-end history-to-export workflow. |
| REQ-APP-007 | GridWorld and agent visualization without altering experiments. | User decision. | CONFIRMED | Trace/event-based optional visualization. |
| REQ-APP-008 | Real CPU/RAM and supported GPU/VRAM telemetry. | User decision. | CONFIRMED | Source and unsupported states visible. |
| REQ-APP-009 | Το final application είναι polished research dashboard, όχι rough minimal demo. | Latest user scope refinement. | CONFIRMED | Modern coherent screenshot-ready UI across essential workflows. |
| REQ-APP-010 | Η feature set περιορίζεται στις πραγματικές ανάγκες της διπλωματικής. | Latest user scope refinement. | CONFIRMED | Required/optional/out-of-scope feature budget approved before UI implementation. |
| REQ-APP-011 | Models, seeds, settings and uncertainty conditions συγκρίνονται καθαρά με charts and tables. | Latest user scope refinement. | CONFIRMED | Compatible comparison view with distributions and counts. |
| REQ-APP-012 | Το resource telemetry παραμένει lightweight current snapshot και όχι observability subsystem. | Accepted audit remediation under user authorization. | CONFIRMED | CPU/RAM/disk and optional GPU current values only; no telemetry database, agents or alerting platform. |

## Architecture and technical

| ID | Requirement | Source / rationale | Status | Acceptance criterion |
|---|---|---|---|---|
| REQ-ARCH-001 | Research core works independently from UI. | User decision. | CONFIRMED | Headless run smoke test. |
| REQ-ARCH-002 | Dashboard starts after validated core and pilot evidence. | User priority. | CONFIRMED | Roadmap gate enforced. |
| REQ-ARCH-003 | Run/result storage does not depend on UI lifecycle. | Reliability. | CONFIRMED | UI close does not corrupt evidence. |
| REQ-ARCH-004 | Avoid microservices, Kubernetes, cloud and complex auth. | Local scope. | CONFIRMED | Bounded local architecture. |
| REQ-ARCH-005 | Final stack follows compatibility/prototype review. | Conflicting historical proposals. | CONFIRMED | ADR with evidence. |
| REQ-ARCH-006 | Production infrastructure, distributed orchestration and enterprise observability are out of scope. | Latest user scope refinement. | CONFIRMED | No such components without formal scope change. |
| REQ-ARCH-007 | The architecture must support a polished UI without exposing internal complexity to the user. | Latest user scope refinement. | CONFIRMED | Small top-level navigation and unified validated workflows. |
| REQ-TECH-001 | No NVIDIA/CUDA or GPU assumption before inventory. | User decision. | CONFIRMED | Capability report first. |
| REQ-TECH-002 | Codex automatically collects actual hardware/software/storage. | User decision. | CONFIRMED | Versioned inventory without manual transcription. |

## UI/UX

| ID | Requirement | Source / rationale | Status | Acceptance criterion |
|---|---|---|---|---|
| REQ-UI-001 | Modern, clean and visually polished appearance. | User decision. | CONFIRMED | Consistent design system and research views. |
| REQ-UI-002 | Aesthetics do not override correctness, reliability or usability. | Priority rule. | CONFIRMED | No decorative behavior hides scientific state. |
| REQ-UI-003 | No fake progress, mock final metrics, fabricated logs or inconsistent states. | Integrity rule. | CONFIRMED | Integration tests against real runner state. |
| REQ-UI-004 | Views must be suitable for screenshots and presentation. | User decision. | CONFIRMED | Legible stable labels and export-ready layouts. |
| REQ-UI-005 | Responsive desktop/laptop layouts, consistent cards/charts/filters/tables and clear loading/error/empty states. | Latest user scope refinement. | CONFIRMED | UX review of all essential workflows. |
| REQ-UI-006 | Scientific metadata remains accessible even when complexity is hidden with progressive disclosure. | Latest user scope refinement. | CONFIRMED | Definitions, parameters and provenance reachable from context. |
| REQ-UI-007 | Full checksums, manifests, software/hardware details and provenance chains do not clutter primary views. | Accepted audit remediation. | CONFIRMED | Essential provenance in main view; full technical details in expandable panels or exports. |

## Repository and provenance

| ID | Requirement | Source / rationale | Status | Acceptance criterion |
|---|---|---|---|---|
| REQ-REPO-001 | Private repository is permanent source of truth. | User decision. | CONFIRMED | Context, decisions and configs versioned. |
| REQ-REPO-002 | Official application stored unchanged. | User decision. | CONFIRMED | Repository SHA-256 recorded. |
| REQ-REPO-003 | Raw chat exports are not committed. | User decision. | CONFIRMED | Content scan passes. |
| REQ-REPO-004 | No secrets, credentials, venvs, caches or useless artifacts. | Security. | CONFIRMED | Ignore/scan/review. |
| REQ-REPO-005 | Large binaries/datasets/checkpoints reviewed before commit. | Maintainability. | CONFIRMED | Storage/LFS policy. |
| REQ-REPO-006 | Research papers are acquired lawfully with stable source metadata and SHA-256; paywalls are not bypassed. | Latest user acquisition request and copyright/provenance requirement. | CONFIRMED | Source manifest records access/version/checksum; unavailable sources are requested from the user through lawful channels. |
| REQ-PROV-001 | Every result maps to run ID, config, source files, processing code and commit. | Provenance. | CONFIRMED | Machine-readable manifest. |
| REQ-PROV-002 | Raw results are immutable. | Reproducibility. | CONFIRMED | Checksums and append-only corrections. |

## Tests

| ID | Requirement | Source / rationale | Status | Acceptance criterion |
|---|---|---|---|---|
| REQ-TEST-001 | Deterministic GridWorld tests for transitions, rewards, termination and disturbances. | Scientific validity. | CONFIRMED | Reference and invariant tests pass. |
| REQ-TEST-002 | Model adapters need contract tests. | Fair interface. | CONFIRMED | Agent contract verified. |
| REQ-TEST-003 | Runner needs lifecycle, persistence, recovery and failure tests. | Reliability. | CONFIRMED | Interruption tests preserve valid state. |
| REQ-TEST-004 | Processing/aggregation code uses known synthetic fixtures. | Statistical correctness. | CONFIRMED | Hand-calculated values match. |
| REQ-TEST-005 | Reproducibility tests distinguish deterministic replay and statistical repeatability. | Honest reporting. | CONFIRMED | Modes and tolerances documented. |

## Thesis and deliverables

| ID | Requirement | Source / rationale | Status | Acceptance criterion |
|---|---|---|---|---|
| REQ-THESIS-001 | Thesis main language is Greek. | User decision. | CONFIRMED | Greek main text. |
| REQ-THESIS-002 | Final deliverable is Microsoft Word. | User decision. | CONFIRMED | Validated `.docx`. |
| REQ-THESIS-003 | Final results/conclusions use only frozen real data. | User decision. | CONFIRMED | Claims map to artifacts. |
| REQ-THESIS-004 | No fabricated sources, DOI, measurements or conclusions. | Integrity. | CONFIRMED | Citation and provenance audit. |
| REQ-THESIS-005 | Figures and tables generated automatically from real data. | User decision. | CONFIRMED | Rebuild command reproduces artifacts. |
| REQ-THESIS-006 | Greek summary/keywords and English abstract/keywords. | Department guidance. | CONFIRMED | Both present. |
| REQ-THESIS-007 | Related Work, Methodology and Discussion are drafted only after focused literature refresh and full-text review of decision-driving papers. | Latest user direction. | CONFIRMED | Evidence matrix and notes include exact methods/results/limitations and writing-use mapping. |
| REQ-DELIV-001 | Final repository includes code, configs, tests, literature, thesis material, results, figures/tables/exports and reproduction scripts. | User requirement. | DEFERRED | Final checklist complete. |