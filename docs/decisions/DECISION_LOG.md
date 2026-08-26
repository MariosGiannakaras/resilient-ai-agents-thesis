# Decision Log

Use this file as the current project-wide decision index. Detailed dedicated decision files/ADRs control where present. Older rationale remains available in repository history, but current status/supersession is recorded here so stale decisions cannot masquerade as active guidance.

## DEC-001 — Private repository as source of truth
- **Date:** 2026-07-29
- **Status:** Accepted; bibliography boundary clarified by DEC-017/DEC-021.
- **Decision:** This repository is the source of truth for thesis context, implementation, experiments, results, writing, and deliverables; the canonical bibliography lifecycle is the explicit external-repository exception.

## DEC-002 — Official application controls academic identity
- **Date:** 2026-07-29
- **Status:** Accepted.
- **Decision:** Exact institution and titles come from the official application.

## DEC-003 — Original application retained unchanged
- **Date:** 2026-07-29
- **Status:** Accepted.
- **Decision:** Preserve the original application in the private repository; public release requires privacy review/redaction.

## DEC-004 — Research core precedes polished dashboard
- **Date:** 2026-07-29
- **Status:** Accepted; clarified by DEC-019/DEC-023/DEC-026.
- **Decision:** Scientific/headless execution is independent from UI; small debug visualization may appear early, polished dashboard follows validated workflow/pilots and is later validated as the normal final-experiment user surface.

## DEC-005 — No inherited final scientific matrix
- **Date:** 2026-07-29
- **Status:** Accepted.
- **Decision:** Final models, metrics, severities, seeds, budgets, and protocol are selected from current evidence/prototypes/pilots, not historical chats.

## DEC-006 — No acceleration assumptions before real inventory
- **Date:** 2026-07-29
- **Status:** Accepted; inventory gate satisfied and applied by DEC-031.
- **Decision:** Actual target-machine inventory precedes compute-dependent choices; CPU-compatible operation remains the required supported baseline until a specific acceleration backend is validated.

## DEC-007 — Raw chat exports excluded
- **Date:** 2026-07-29
- **Status:** Accepted.
- **Decision:** Store verified synthesis, not raw transcript archives.

## DEC-008 — Department guidance is rechecked near delivery
- **Date:** 2026-07-29
- **Status:** Accepted.
- **Decision:** Current official guidance controls; final Word/submission/defense rules are refreshed near delivery.

## DEC-009 — Conversation exports are context only
- **Date:** 2026-07-29
- **Status:** Accepted.
- **Decision:** Historical chats do not establish scientific/technical preferences.

## DEC-010 — Fresh GridWorld discovery; no legacy dependency
- **Date:** 2026-07-29
- **Status:** Accepted.
- **Decision:** Compare current custom/reuse/adapt options; integrate only after review/prototype/ADR.

## DEC-011 — Codex/system owns automated inventory
- **Date:** 2026-07-29
- **Status:** Accepted.
- **Decision:** Hardware/software/storage are collected automatically rather than manually transcribed by the user.

## DEC-012 — Corrected bootstrap context supersedes earlier wording
- **Date:** 2026-07-29
- **Status:** Accepted; now historical.
- **Decision:** Corrected bootstrap interpretation controlled the initial next phase. Current state is now governed by `CURRENT_STATUS.md` and later decisions.

## DEC-013 — Thesis-completion-first scope
- **Date:** 2026-07-29
- **Status:** Accepted.
- **Decision:** **Polished outside, bounded inside.** Keep research/engineering small enough to complete while delivering a polished real research UI.

## DEC-014 — Lean agent workflow and staged literature refresh
- **Date:** 2026-07-29
- **Status:** Accepted; local bibliography-acquisition clause superseded by DEC-017.
- **Decision:** Read only relevant docs, repeat bibliography freshness at defined gates, and keep detailed provenance behind progressive disclosure rather than cluttering the UI.

## DEC-015 — Automated technical execution/review
- **Date:** 2026-07-29
- **Status:** Accepted; autonomous Goal/PR continuation clarified by DEC-028 on 2026-08-25.
- **Decision:** The user is not the routine GitHub operator. Codex executes bounded work, performs objective diff review, uses GitHub CI, corrects failures/findings, and may squash-merge its own validated PR when repository policy does not require distinct human approval; it does not submit an `APPROVE` review on its own PR. ChatGPT remains available for independent review, scientific/writing support, and later user-facing review but is not a mandatory routine merge gate. The user is consulted for genuinely non-objective academic/product choices or required external input.

## DEC-016 — Original in-repository bibliography workflow
- **Date:** 2026-07-29
- **Status:** **SUPERSEDED by DEC-017.**
- **Decision:** Historical only; primary bibliography acquisition/preservation no longer occurs in this thesis repository.

## DEC-017 — Dedicated canonical ThesisBibliography repository
- **Date:** 2026-08-02
- **Status:** Accepted; consumer surface extended/completed by DEC-021/DEC-022.
- **Decision:** `MariosGiannakaras/ThesisBibliography` owns source acquisition/originals/conversion/analysis/evidence/selection. This repository consumes verified generated content read-only and never writes upstream.

## DEC-018 — English technical/operational repository language
- **Date:** 2026-08-02
- **Status:** Accepted.
- **Decision:** Technical/agent/code/Git documentation uses English; exact official Greek text and original-language scientific evidence remain unchanged where required; final thesis remains Greek.

## DEC-019 — Early debug visualization allowed
- **Date:** 2026-08-02
- **Status:** Accepted.
- **Decision:** Lightweight validation visualization is allowed before the polished dashboard if it uses the same core interfaces and does not duplicate scientific logic.

## DEC-020 — Implementation-first priority; writing-stage inputs deferred
- **Date:** 2026-08-04
- **Status:** Accepted.
- **Decision:** Missing supervisor identity/deadline/template does not block research/program/pilots; incorporate later feedback when received and defer normal thesis prose until evidence production is mature.

## DEC-021 — Complete research-corpus import with strict citation sublayer
- **Date:** 2026-08-04
- **Status:** Accepted and implemented.
- **File:** `docs/decisions/DEC-021-complete-research-corpus.md`.
- **Decision:** Import the complete committed research corpus while keeping nested `citation-ready/` as the only automatic formal-citation layer; validate immutable provenance/ancestry/checksums and exclude upstream PDFs/LFS/history.

## DEC-022 — Accept first immutable full-corpus baseline
- **Date:** 2026-08-04
- **Status:** Accepted and implemented.
- **File:** `docs/decisions/DEC-022_FULL_CORPUS_BASELINE.md`.
- **Decision:** Accept `bibliography-integration-v2` at checkout `27e325a74722b8f80643e6d1902e4bf3847036f5`, complete-corpus source `ca511a0ff91388e7798e011642cc6b5608b336d8`, citation-ready source `ef44fe3c30e6648f591ad9d3546ffc336fce4287`.

## DEC-023 — Research core, reproducible runs, and automatic publication
- **Date:** 2026-08-04
- **Status:** Accepted and implemented as infrastructure.
- **File:** `docs/decisions/DEC-023_RESEARCH_CORE_AUTOMATION.md`.
- **Decision:** Python 3.12 + `uv`; `src/resilient_agents/`; strict information boundary; independent RNG streams; explicit contracts; filesystem run bundles; one guarded commit/push per finalized whole experiment; selective Git LFS; later thin Streamlit dashboard.
- **Boundary:** Does not freeze final RQ, GridWorld parameters, models, metrics, severities, seeds, budgets, thresholds, hyperparameters, statistics, or protocol.

## DEC-024 — Active-document reconciliation is part of every material change
- **Date:** 2026-08-04
- **Status:** Accepted.
- **File:** `docs/decisions/DEC-024_DOCUMENTATION_GOVERNANCE.md`.
- **Decision:** Material changes reconcile affected active docs/status/prompts/decisions in the same PR; obsolete active files are removed; CI validates mechanically detectable stale state; the tracked Codex prompt is the directly executable entrypoint.

## DEC-025 — Canonical resumable Codex task registry
- **Date:** 2026-08-04
- **Status:** Accepted.
- **File:** `docs/decisions/DEC-025_CODEX_TASK_REGISTRY.md`.
- **Decision:** `docs/context/TASKS.md` is the single concrete execution checklist and resume ledger. Every Codex session reads it before selecting/resuming work; available session memory is used together with durable Git/repository evidence; unfinished tasks retain `IN_PROGRESS` resume state; branch checkpoint commits support quota/interruption recovery while coherent PRs still squash into `main`.

## DEC-026 — End-to-end lifecycle handoffs and defense package
- **Date:** 2026-08-04
- **Status:** Accepted.
- **File:** `docs/decisions/DEC-026_END_TO_END_LIFECYCLE_AND_DEFENSE.md`.
- **Decision:** Define explicit Codex/user/artifact handoffs from validated application through final experiments, frozen evidence/analysis, thesis/review, defense presentation, and delivery. Final experiments normally require both frozen protocol and validated application workflow; final analysis creates a thesis/defense evidence package before writing; the final defense package contains a PowerPoint `.pptx`, embedded speaker notes, separate full spoken Greek script, evidence mapping, real demo/screenshots with fallback, and rehearsal/PowerPoint validation. Codex prepares/verifies repository-backed evidence/assets, ChatGPT handles narrative/language/script work, and PowerPoint-capable tooling produces the deck with Microsoft PowerPoint as final inspection/rehearsal surface.

## DEC-027 — Self-explanatory UI and lightweight onboarding
- **Date:** 2026-08-04
- **Status:** Accepted; implementation deferred to the final dashboard phase.
- **Decision:** The final dashboard must be self-explanatory through clear labels/helper text/units, accurate tooltips/contextual help, consistent terminology, actionable states, pre-run configuration review, and text+icon+accessible semantic-color status treatment where color is never the sole signal. After the final dashboard structure is stable, add a short skippable/replayable first-run onboarding flow with Previous/Next/Skip/Finish using lightweight local/native Streamlit mechanisms. Do not introduce a heavyweight custom JavaScript/DOM tour framework, accounts, or a new persistence subsystem merely for onboarding unless a later demonstrated requirement justifies the complexity.

## DEC-028 — Lean Codex bootstrap, persistent goal, and bounded execution
- **Date:** 2026-08-04
- **Status:** Accepted and implemented; autonomous full-project Goal continuation refined 2026-08-25.
- **Decision:** The canonical Codex prompt is a lean execution bootstrap, not a second copy of `AGENTS.md`. Every session reads only `AGENTS.md`, `TASKS.md`, and `CURRENT_STATUS.md` before selecting/resuming work, then loads only task-specific active specifications/evidence. The canonical `/goal` keeps the complete project-lifecycle objective active while Codex executes one bounded dependency-valid task/coherent package at a time. Routine Git, PR creation, CI, objective own-diff review, corrections, squash merge, task/status reconciliation, and next-`READY` selection are autonomous execution steps and do not clear/pause the Goal when available permissions and repository policy allow them. Codex does not submit an `APPROVE` review on its own PR, but may squash-merge after green CI, objective review, and resolution of findings when distinct human approval is not required. Evidence-backed research/architecture/ADR decisions also proceed autonomously when task evidence and acceptance criteria resolve them. Goal persistence never authorizes `BLOCKED`/`DEFERRED` work, fabricated evidence, or bypassing an explicit external approval; it pauses only for genuinely non-objective user choices, required supervisor/Department/private input, required evidence on another machine, unavailable access/credentials, safety/privacy/legal/licensing blockers, or explicit external approval requirements. A separate startup `/plan` is unnecessary because the repository already has the roadmap/task ledger; plan mode is reserved for a specific task whose approach genuinely needs investigation. CI enforces the three-file startup core, bounded-execution wording, non-duplication of domain-policy sections, autonomous-continuation invariants, and a lean prompt-size budget.

## DEC-029 — Risk-based proportional testing
- **Date:** 2026-08-04
- **Status:** Accepted; refined by DEC-030.
- **Decision:** Testing protects scientific validity, task acceptance conditions, critical reliability/security boundaries, and concrete regressions, but must not become an independent scope-expansion project. Codex uses targeted tests during implementation, tiny deterministic fixtures/smoke runs in CI, and the full repository checks at review readiness rather than after every small edit. There is no arbitrary coverage-percentage target and no mutation/fuzz/property/combinatorial/snapshot expansion without a concrete task-specific risk. Stop adding tests once material risks and acceptance conditions are covered; never run pilot/final experiment matrices as CI tests.

## DEC-030 — Quota-efficient fail-fast validation
- **Date:** 2026-08-25
- **Status:** Accepted.
- **File:** `docs/decisions/DEC-030_QUOTA_EFFICIENT_FAIL_FAST_VALIDATION.md`.
- **Decision:** Use targeted local validation and GitHub PR CI as the canonical full-suite pre-merge guard when available; do not duplicate full-suite runs or analyse successful logs without cause. Keep CI bounded, quiet on success and explicit on failure. Validate required inputs/contracts/schema/provenance at boundaries before expensive work, fail closed on invalid/ambiguous required state, keep optional unavailability explicit, prefer atomic finalization, and allow adjacent dependency-valid tasks to share a coherent PR when no real gate separates them.

## DEC-031 — Target-machine runtime and acceleration baseline
- **Date:** 2026-08-25
- **Status:** Accepted.
- **File:** `docs/decisions/DEC-031_TARGET_MACHINE_BASELINE.md`.
- **Decision:** Accept the actual Windows target-machine capability report; use native Windows CPython 3.12 via the locked `uv` environment; require CPU-compatible execution; do not infer a validated scientific-compute backend from the Radeon display adapter; use compatible Windows Git/Git LFS for LFS-sensitive operations.

## DEC-032 — Project-owned Gymnasium GridWorld implementation
- **Date:** 2026-08-26
- **Status:** Accepted and implemented; `T-212`/`T-213` core and invariant validation complete.
- **File:** `docs/decisions/DEC-032_GRIDWORLD_IMPLEMENTATION.md`.
- **Decision:** Implement a small project-owned GridWorld using the locked Gymnasium 1.3.0 API through the accepted core contracts. Do not make MiniGrid a core dependency; it adds translation, dependency/platform, and tag-license uncertainty without a demonstrated required RQ capability. This selects the implementation strategy but leaves all scientific environment/protocol parameters unfrozen.

## DEC-033 — Curve-based operational resilience estimands
- **Date:** 2026-08-26
- **Status:** Accepted and implemented by `T-300`/`T-301`; numeric parameters/statistical roles remain pilot/freeze decisions.
- **Decision:** Use aligned higher-is-better disrupted and predeclared matched-reference curves to report separate nominal, signed immediate/worst/terminal gap, cumulative deficit, and stabilization-based recovery estimands. Preserve `NO_DEGRADATION`, `RECOVERED`, and `NOT_RECOVERED` as distinct outcomes; non-recovery has no fabricated horizon time. Do not create a composite resilience score. Detailed formulas and interpretation boundaries live in `docs/research/METRICS_CANDIDATES.md`.

## DEC-034 — Bounded tabular agent capability set
- **Date:** 2026-08-26
- **Status:** Accepted and implemented by `T-312` for pilots; final role retention and hyperparameters remain pilot/protocol-freeze decisions.
- **Decision:** Implement one tabular Q-learning method evaluated from a common nominal checkpoint as F0 frozen and C0 continual regimes, plus R0 frozen finite s,a-rectangular robust value iteration with explicit stronger model/uncertainty-set prior. Exclude context-memory, detector-reset, oracle, duplicate tabular, deep/function-approximation, and diagnostic-specific agents unless their recorded reopening conditions are met. Citation-ready `SRC-52E62452B8` sufficiently supports the retained robust Bellman claims, so conditional `T-311` requires no upstream promotion. Detailed method/fairness/evidence boundaries live in `docs/research/MODEL_CANDIDATES.md`.

## DEC-035 — Versioned pre-final pilot protocol
- **Date:** 2026-08-26
- **Status:** Accepted and validated for headless-runner implementation/pilots; not final evidence and amendable before `protocol-v1.0`.
- **Decision:** Use machine-readable `pilot-v0.1` with two disjoint same-scale layouts per development/tuning/pilot/final-reserve stage; a matched 16-episode nominal plus 32-episode post-change block lifecycle; minimal in-set and maximal out-of-set action remaps; bounded single-factor diagnostics; precommitted disjoint seeds; an 18-configuration staged dyadic Q search; fixed pre-pilot R0 prior; explicit metric sensitivity, CPU preflight/timeout, failure/exclusion, and artifact rules. Final-reserve execution remains forbidden. The complete rationale and config contract live in `docs/experiments/PILOT_PROTOCOL_V0_1.md` and `configs/protocols/pilot-v0.1.json`.

## DEC-036 — One resumable headless scientific execution path
- **Date:** 2026-08-26
- **Status:** Accepted and implemented by `T-401`; exercised by the completed T-410 campaign.
- **Decision:** Resolve the validated protocol through one CLI/core path that trains a root-specific nominal Q checkpoint shared by F0/C0, derives R0 from the fixed rectangular prior, executes matched reference/disrupted episode branches, computes schema-v1 metrics, persists events per episode and state atomically per completed root, and finalizes one whole-experiment bundle. Resume is supported only at verified root boundaries with identical config/source/content/log integrity; an incomplete root is deterministically rerun. Publication occurs at most once after all roots and bundle finalization. Detailed contract lives in `docs/experiments/HEADLESS_RUNNER.md`.

## DEC-037 — Deterministic finalized-bundle pilot analysis

- **Date:** 2026-08-26
- **Status:** Accepted and implemented by `T-402`; inferential roles and final statistical plan remain unfrozen.
- **Decision:** Analyze only finalized, integrity-consistent run bundles through one version-controlled core path that semantically reconstructs completed requests, state/checkpoint invariants, matched curves, and schema-v1 metrics. Treat one run/layout/condition/root/agent as the preliminary scientific unit; keep operational attempts and noncompleted runs explicit but outside scientific aggregates; reproduce the entire predeclared metric-sensitivity grid; and write immutable checksummed analysis bundles. Pilot summaries are diagnostic only and cannot support final claims or silently freeze post-pilot statistical choices. Detailed contract lives in `docs/experiments/ANALYSIS_PIPELINE.md`.

## DEC-038 — Durable-main predeclared pilot campaign execution

- **Date:** 2026-08-26
- **Status:** Accepted and fully exercised by the completed T-410 campaign.
- **Decision:** Expand `pilot-v0.1` deterministically into 36 tuning and 14 pilot whole-experiment children; use one full tuning child as preflight for the declared timeout rule; enforce graceful recorded deadlines inside the runner; select tuning configurations only through semantically reproduced completed bundles and the predeclared ordered score; and automatically commit/push every child from durable `main`. Stable identities plus exact-request/integrity validation provide resume without overwrite. The central stored metric setting is fixed pre-outcome while all 54 sensitivity definitions remain mandatory. Detailed contract lives in `docs/experiments/PILOT_CAMPAIGN_EXECUTION.md`.

## DEC-039 — R0 active terminal-observation alias amendment

- **Date:** 2026-08-26
- **Status:** Accepted and fully exercised by the completed 14-child amended pilot rerun.
- **Decision:** A delivered observation equal to a modeled terminal state cannot prove true termination under observation corruption. When the runner asks R0 to act in an active episode, robust-plan schema v2 assigns the absorbing value zero to every action and applies the existing seeded tie rule, without evaluator truth. Preserve all v0.1 attempts; reuse the unaffected F0-only tuning evidence and selected configuration; retain the pilot seed bank for a paired implementation retry; and rerun the complete 14-child matrix under `pilot-v0.2`/`PV02-*` identities. Only the complete v0.2 matrix enters amended pilot analysis; the v0.1 failure remains explicit operational evidence. Detailed amendment is `docs/experiments/PILOT_PROTOCOL_V0_2.md`.

## DEC-040 — Post-pilot freeze constraints

- **Date:** 2026-08-26
- **Status:** Accepted diagnostic conclusion from `T-410`; final choices remain reserved for `T-411`/`T-412`.
- **Decision:** Accept the complete `pilot-v0.2` matrix and validated analysis as feasibility/protocol evidence only. C0 and F0 remain feasible final candidates, with both layouts required because F0 shows material layout/seed variance. Do not freeze the current R0 prior/policy/horizon combination unchanged because approximately 96% of its nominal evaluation episodes truncate. Do not select a favorable recovery threshold because recovery counts vary across predeclared settings in 33 of 42 agent-condition-layout cells. Preserve full curves, explicit censored non-recovery, component estimands, and the final-reserve firewall. T-411 must refresh decision-driving evidence; T-412 must then justify/validate any bounded R0 revision or remove/reframe the role and predeclare the metric/sample-size/statistical decisions before final outcomes. Detailed evidence is `docs/experiments/PILOT_REPORT_V0_2.md`.

## Pending decisions

Future entries are still required for:

- final research question and hypotheses;
- final GridWorld scientific parameters and validated specification;
- final uncertainty taxonomy/severities/timing;
- final post-pilot retention and hyperparameters of the selected model/baseline regimes;
- final primary/secondary/diagnostic metric roles, numeric parameters, and statistical plan;
- seeds, repetitions, tuning/resource budgets, and stopping rules;
- pilot-derived amendments and final `protocol-v1.0` freeze;
- pilot-derived optional dashboard feature budget beyond the accepted self-explanatory UX/onboarding baseline;
- optional AI, if ever justified;
- final citation style/Word template/submission specifics near writing/delivery;
- exact current defense duration, required slide/file rules, and administrative presentation/submission procedure near delivery.

The general Python/core/storage/result-publication/dashboard architectural baseline, accepted target-machine/runtime baseline, task-governance mechanism, lean Goal-mode Codex bootstrap, proportional testing discipline, quota-efficient fail-fast validation, end-to-end handoff model, and self-explanatory UI/onboarding baseline are **not** pending decisions unless later requirements justify explicit amendments.
