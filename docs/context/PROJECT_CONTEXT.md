# Project Context

## Status taxonomy

- **CONFIRMED:** established by the official application, current explicit user instruction, or an accepted repository decision.
- **RESEARCH_REQUIRED:** requires current scientific/technical evidence before selection.
- **PROPOSED:** evidence-backed proposal not yet frozen.
- **OPEN:** unresolved decision or external input still needed.
- **DEFERRED:** valid later-stage input that does not block current research/implementation.
- **HISTORICAL_CONTEXT_ONLY:** retained only to explain earlier reasoning; not active guidance.

## Project identity

This repository is the permanent source of truth for the complete thesis lifecycle:

> **Σύγκριση και Αξιολόγηση Ανθεκτικών Πρακτόρων Τεχνητής Νοημοσύνης σε Περιβάλλοντα με Αβεβαιότητα**

Confirmed academic context:

- University of West Attica, School of Engineering, Department of Informatics and Computer Engineering.
- Official English title: **Comparison and Evaluation of Resilient AI Agents in Uncertain Environments**.
- Topic approved by the supervisor.
- Final thesis remains a Greek Microsoft Word deliverable unless official guidance changes.
- No current supervisor-specific instruction or deadline blocks the research/program work.

The official application defines the broad objective: compare resilient decision-making agents in a simple simulated environment under uncertainty/dynamic change, including examples such as observation/data noise, rule changes, and action-execution failures, with evaluation of resilience and recovery speed.

## Bibliography — current accepted state

`MariosGiannakaras/ThesisBibliography` is the canonical source of truth for source discovery, originals/PDFs, conversion/OCR, canonical Markdown, scientific analysis, evidence verification, source selection, research materials, notes, and generated exports.

The first complete immutable consumer import was accepted by DEC-021/DEC-022. The current synchronized immutable baseline has since advanced without changing the ownership/trust architecture.

Current pinned baseline:

- requested ref: `bibliography-integration-v3`;
- checkout: `71995373ae0da64149583cae8d7a2c17e5ab1a0a`;
- complete-corpus source commit: `e46693d4201cf47c118eb61c216243f3c5798e28`;
- citation-ready source commit: `822891fb585c98dbe4464602e97998704d1609c5`;
- 585 canonical sources;
- 113 citation-ready selected sources;
- 19 research materials;
- metadata for 281 indexed original PDFs;
- 1568 consumer-recorded corpus files.

The immutable `bibliography-integration-v2` baseline remains an unchanged historical snapshot. Read access, upstream validators, SHA-256 manifests, ancestry, consumer integrity, contextual source-reference validation, and the full repository test suite passed for the v3 synchronization before its generated branch was published. The former HTTP 401 and incomplete-import blockers remain resolved.

`research/bibliography/citation-ready/` is the only automatic formal-citation surface. Full-corpus/rejected/theory-only/`MAT-*`/note content remains available for internal research without silent promotion. New formal evidence promotion occurs only upstream in `ThesisBibliography`, followed by a new immutable synchronization.

No bibliography PDF, structured original, or bibliography Git LFS object is imported into this repository.

## Current technical architecture — accepted

DEC-023 establishes the current implementation baseline:

- Python 3.12;
- `uv`, `pyproject.toml`, `.python-version`, and committed `uv.lock`;
- independent importable package at `src/resilient_agents/`;
- strict separation of evaluator ground truth from agent-visible information;
- deterministic independent RNG streams;
- explicit scenario/experiment/change/protocol contracts with no hidden scientific defaults;
- filesystem-first self-contained run bundles with resolved config, capability snapshot, provenance, checksums, events/traces, and summary;
- one guarded automatic Git commit and push per finalized **whole experiment**, never per seed;
- selective Git LFS for configured large thesis-produced artifacts;
- filesystem run bundles as source of truth; any later database/index is rebuildable cache;
- future final dashboard as a thin local Streamlit layer over the same core, after headless workflow/pilot validation.

Large thesis-produced experiment artifacts are retained by default rather than manually excluded merely because they are large. The configured LFS policy handles selected large formats; retention is revisited only if a real storage constraint appears.

## Codex execution continuity — accepted

DEC-025 establishes `docs/context/TASKS.md` as the single concrete execution checklist and resumable progress ledger.

Every Codex session reads it before selecting/resuming work. Codex uses available session/conversation memory to continue efficiently, but verifies that memory against durable repository evidence: branch/commits, working-tree diff, PR state, tests, task state, and active docs. If model quota/session interruption occurs, unfinished work is resumed rather than reconstructed or restarted.

DEC-028 makes the directly executable Codex prompt a lean bootstrap rather than a second policy manual. Session startup reads exactly `AGENTS.md`, `TASKS.md`, and `CURRENT_STATUS.md`; additional files/evidence are loaded only for the selected task, using repository search before broad reading. Domain rules stay centralized in `AGENTS.md` and the relevant active specifications.

The canonical `/goal` entrypoint is the persistent long-horizon wrapper over that bounded execution model. Codex advances one dependency-valid task/coherent work package at a time, validates/checkpoints it, performs routine Git/PR/CI/objective diff review/corrections/squash merge/task reconciliation with available permissions, then re-evaluates `TASKS.md` and automatically continues with the next `READY` scope. Completing a task, branch, PR, CI run, or own-PR squash merge is not a reason to clear the goal or ask the user to say “continue”. Codex does not submit an `APPROVE` review on its own PR, but may merge its validated work when no distinct human approval is required by repository policy.

Evidence-backed research, architecture, implementation, testing, and ADR decisions are normal autonomous work when the active task's accepted evidence and acceptance criteria resolve them. Goal persistence does not turn the thesis into one undifferentiated task and never permits `BLOCKED`/`DEFERRED` work, fabricated evidence, or bypassing an explicit user/supervisor/external approval requirement. A genuinely non-objective choice or external input required by the controlling task/specification is a real pause gate; generic “scientific” or “review” labels are not.

A separate startup `/plan` is normally redundant because the repository already contains the roadmap, task dependencies, and acceptance conditions. Plan mode may be used within the active goal for a specific task whose implementation/research approach is genuinely unclear and benefits from investigation before editing.

Intermediate branch commits are allowed as recovery checkpoints. Coherent work still normally reaches `main` through a squash merge, so recovery checkpoints do not create unnecessary permanent main history.

`READY` has a strict meaning: required task dependencies are complete. Future work remains `BLOCKED`/`DEFERRED` until its dependencies/conditions actually permit execution.

## End-to-end lifecycle — accepted

DEC-026 defines how the project continues beyond implementation. `IMPLEMENTATION_ROADMAP.md` explains the phase order, `EXECUTION_WORKFLOW.md` records responsibilities/handoffs, and `TASKS.md` is the only concrete status/dependency ledger.

The intended handoff chain is:

> validated research/pilots -> frozen protocol -> validated application -> final experiments -> frozen evidence/statistics -> thesis/defense evidence package -> Greek thesis/review/final freeze -> PowerPoint defense package -> final audit/delivery

The polished application is not the end of the project. It becomes the validated user-facing execution surface for the frozen final experiment campaign. Final experiments normally wait for both the frozen protocol and validated application workflow so the user does not have to switch to a separate manual execution path.

After final analysis, a dedicated evidence package maps RQs, protocol/method references, citation-ready sources, run/result IDs, figures/tables/captions, and planned claims. Thesis and presentation work consume this package rather than reinterpreting raw runs ad hoc.

The final defense phase is already specified but deferred. `docs/thesis/PRESENTATION_WORKFLOW.md` requires a final `.pptx`, embedded speaker notes, a separate full spoken Greek script, evidence mapping, validated application screenshots/demo fallback, and rehearsal/PowerPoint checks. Codex prepares/verifies repository-backed evidence/assets; ChatGPT is the preferred narrative/Greek-writing/speaker-script layer; PowerPoint-capable tooling creates the file and Microsoft PowerPoint is the final inspection/rehearsal target.

## Research direction — not frozen

The imported evidence supports a bounded direction but does not yet freeze the final protocol:

- distinguish robustness from post-change adaptation/recovery;
- use persistent rule/dynamics change as the leading recovery axis;
- treat observation corruption and action-execution failure as supporting robustness diagnostics unless the final RQ requires more;
- evaluate nominal performance, disruption depth, recovery trajectory/time, post-change performance, non-recovery, and across-run uncertainty rather than one opaque resilience score;
- compare a small number of scientifically distinct capability roles rather than a catalogue of algorithms;
- keep the tuning/pilot/final boundary explicit and leakage-resistant.

Decision-driving citation-ready evidence currently includes `SRC-70772C0629`, `SRC-9464421E55`, `SRC-76B2247457`, `SRC-52E62452B8`, `SRC-FC42D9798A`, and `SRC-3C0F7CC819`. The robust-MDP records support finite rectangular robust dynamic programming and the conceptual distinction between declared-set robustness and online changepoint adaptation, but do not establish recovery superiority. DEC-034 records the resulting bounded comparator and evidence boundaries.

## GridWorld — current state

GridWorld remains the confirmed simple controlled environment direction. DEC-032's project-owned schema-v1 implementation now uses locked Gymnasium 1.3.0 through the accepted core contracts and passes deterministic known-answer/invariant validation. The completed `pilot-v0.2` matrix diagnoses pre-final layouts/conditions only; final scenario values remain unfrozen until `protocol-v1.0`.

The completed bounded comparison evaluated two prototype paths against the same accepted contract and fixed fixture:

1. a small project-owned Gymnasium-compatible environment;
2. a MiniGrid adaptation that translated or bypassed inherited orientation, mission, observation, action, and reward conventions.

Both prototypes passed deterministic semantic parity checks on the native target baseline. `GRIDWORLD_PROTOTYPE_COMPARISON.md` records why DEC-032 selected the smaller project-owned path. The final core validates explicit layout/action/reward/lifecycle/change/disturbance configuration, independent seeds, versioned serialization, evaluator-only truth, and agent information projection; MiniGrid/Pygame remain prototype-only.

## Models and metrics — current state

The implementation/pilot algorithm shortlist and operational metric schema are selected and validated. The completed pilot keeps C0/F0 feasible for freeze consideration but shows that R0's current prior/policy/horizon combination cannot be retained unchanged because approximately 96% of its nominal evaluation episodes truncate. Final post-pilot retention, metric roles/parameters, seed count, severity set, hyperparameters, and statistical plan remain unfrozen.

The bounded implementation/pilot set is implemented as two methods in three roles: one versioned common tabular Q-learning checkpoint evaluated as F0 frozen and C0 continual, plus R0 frozen finite s,a-rectangular robust value iteration with its stronger model/uncertainty-set prior declared. Deterministic replay, exact updates/backups, checkpoint/plan stability, frozen-state behavior, probability/model validation, and strict rejection of evaluator-only information have focused tests. Context-memory, detector-reset, extra tabular variants, deep methods, and dedicated diagnostic-specific agents are excluded unless a recorded reopening condition is met. Final retention and all hyperparameters/budgets remain pilot/freeze decisions.

Operational metric schema v1 and hand-calculated tests now define matched-reference nominal performance, signed immediate/worst/terminal gaps, cumulative deficit, stabilization-based recovery, `NO_DEGRADATION`, `RECOVERED`, and real `NOT_RECOVERED` with no artificial horizon time. Numeric windows/tolerance/stability, primary/secondary roles, aggregation, intervals, and final statistical plan remain pilot/freeze decisions.

## Experiments and repository automation

A run ID represents one whole experiment and may contain many seeds/episodes.

The validated headless CLI/core resolves the full `pilot-v0.1` authority and bounded `pilot-v0.2` amendment into root-specific common Q checkpoints, layout-specific R0 plans, matched nominal/disrupted branches, schema-v1 metrics, continuously appended events, and atomic completed-root state. External interruption resumes only with identical config/source/log integrity and reruns an incomplete root deterministically; ordinary failure is finalized and retained. Successful multi-root execution finalizes one bundle and optionally invokes the guarded publisher once after all roots.

The validated analysis core consumes only finalized, checksum/index-consistent bundles; semantically reconstructs completed requests, checkpoints, matched curves, and primary metrics; and deterministically emits immutable unit, aggregate, operational, and predeclared sensitivity diagnostics. Noncompleted runs remain explicit without becoming scientific units, and these pre-final outputs carry no inferential or final-claim status.

The intended user workflow is:

> configure experiment -> run -> automatic persistence/provenance -> finalize -> one guarded commit/push

The user should not manually stage, commit, move, or upload routine experiment artifacts. Publication safety may block the Git operation when provenance/working-tree/remote conditions are unsafe, but local run data is preserved.

Development, tuning, pilot, exploratory, and final evidence remain separated. Final figures/tables are generated only from real stored data by version-controlled code. Final experiment execution is followed by explicit run-completeness validation and evidence freeze before statistical interpretation/writing.

The completed `pilot-v0.2` campaign reused the unaffected 36-run F0 tuning evidence and reran all 14 pilot children under one corrected implementation. Its validated report records 336 units, 18,144 sensitivity records, runtime/storage feasibility, strong F0 layout variance, widespread recovery-parameter sensitivity, and R0 nominal censoring. Final-reserve layouts remain unexecuted and forbidden before the later freeze/application gates.

## Dashboard, thesis writing, and defense

The dashboard is a supporting local single-user tool, not the scientific contribution. A small debug surface may be used during environment/core validation; the polished Streamlit dashboard follows pilot-established workflows and must not duplicate scientific logic.

DEC-027 fixes the required dashboard UX baseline while leaving exact implementation-level styling for the real UI: clear human-readable labels/helper text/units, accurate tooltips/contextual help, consistent terminology, understandable text+icon+semantic-color statuses, actionable empty/loading/warning/error states, a pre-run resolved-configuration/validation review, proportionate confirmations, and next-action guidance where useful. Color cannot be the sole essential signal.

A short first-run onboarding flow is added only after the final dashboard structure is stable. It is skippable and replayable, uses Previous/Next/Skip/Finish, stores only lightweight local completion state, and must not create a new account/persistence system or heavyweight custom JavaScript/DOM tour framework without demonstrated need.

Application completion requires the actual user workflow—not only rendered screens—to work on real backend state: configure, run/monitor, history, compare/detailed analysis, artifacts/export, contextual help, and onboarding/help validation. The `T-510 -> T-512 -> T-511` task chain enforces this order before final experiments.

Normal chapter drafting and final Word styling remain later stages. Structured evidence mappings, method records, captions, figures, tables, provenance, and task progress are collected during implementation; a formal evidence package is frozen after final analysis so writing is not reconstructed from memory.

A review-ready thesis precedes final thesis freeze. Supervisor/reviewer corrections are incorporated when received and affected evidence/citations/figures/method descriptions are revalidated.

The final presentation is a distinct downstream deliverable after thesis stability, not an independent manual summary. It inherits the same evidence mappings and is finalized only after speaker notes/script, PowerPoint rendering, timing, factual consistency, and demo fallback checks pass.

## Current genuine gates

The canonical concrete task/dependency list is `docs/context/TASKS.md`. The actual-machine baseline/provenance, research framing/GridWorld, metrics, bounded agents, pilot protocol, headless orchestration, reproducible analysis, and pilot execution tasks (`T-100` through `T-410`) are complete. The decision-driving bibliography refresh (`T-411`) is next, followed by the evidence-backed final protocol/statistical freeze. Application, final experiments/evidence, writing/review, presentation, and audits follow the registry's remaining dependencies and acceptance conditions. Routine PR/CI/merge boundaries do not interrupt the persistent goal; only controlling task/specification requirements for genuinely external/user-only input do.

Deferred, non-blocking inputs remain later supervisor corrections, eventual submission/presentation dates, a current official Word template, exact defense duration/file rules, and optional contextual example theses supplied near writing.

## Current authority

Use:

- `AGENTS.md` for Codex/project policy;
- `docs/context/CODEX_EXECUTION_PROMPT.md` as the lean Goal-mode execution bootstrap;
- `docs/context/CURRENT_STATUS.md` for the shortest current-state summary;
- `docs/context/TASKS.md` for concrete task status/resume/next action;
- `docs/context/IMPLEMENTATION_ROADMAP.md` for phase/dependency explanation;
- `docs/context/EXECUTION_WORKFLOW.md` for responsibilities and major handoffs;
- `docs/context/DOCUMENTATION_GOVERNANCE.md` for keeping related files synchronized;
- `docs/architecture/UI_INFORMATION_ARCHITECTURE.md` for the bounded dashboard information/UX contract;
- `docs/thesis/PRESENTATION_WORKFLOW.md` for the deferred defense workflow.

Historical bootstrap/pre-import records must not be used as current blockers or instructions.
