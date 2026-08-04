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
- **Status:** Accepted.
- **Decision:** Actual target-machine inventory precedes compute-dependent choices; CPU-compatible operation is the temporary safe baseline.

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
- **Status:** Accepted.
- **Decision:** User is not the routine GitHub operator; Codex executes bounded work, GitHub checks it, ChatGPT reviews/decides readiness, user is consulted for genuine academic/product choices.

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

## DEC-028 — Lean Codex bootstrap and bounded execution
- **Date:** 2026-08-04
- **Status:** Accepted and implemented.
- **Decision:** The canonical Codex prompt is a lean execution bootstrap, not a second copy of `AGENTS.md`. Every session reads only `AGENTS.md`, `TASKS.md`, and `CURRENT_STATUS.md` before selecting/resuming work, then loads only task-specific active specifications/evidence. “Execute it completely” means progressing one dependency-valid task/coherent work package at a time within review, machine, evidence, and scientific gates; it never authorizes an all-thesis attempt, blocked/deferred work, or completed-work reimplementation. CI enforces the three-file startup core, bounded-execution wording, non-duplication of domain-policy sections, and a lean prompt-size budget.

## Pending decisions

Future entries are still required for:

- final research question and hypotheses;
- final GridWorld implementation/scientific specification;
- final uncertainty taxonomy/severities/timing;
- exact selected models/baselines, including whether robust-MDP comparison receives formal evidence support;
- final primary/secondary/diagnostic metrics and statistical plan;
- seeds, repetitions, tuning/resource budgets, and stopping rules;
- final pilot protocol and `protocol-v1.0` freeze/amendments;
- pilot-derived optional dashboard feature budget beyond the accepted self-explanatory UX/onboarding baseline;
- optional AI, if ever justified;
- final citation style/Word template/submission specifics near writing/delivery;
- exact current defense duration, required slide/file rules, and administrative presentation/submission procedure near delivery.

The general Python/core/storage/result-publication/dashboard architectural baseline, task-governance mechanism, lean Codex bootstrap, end-to-end handoff model, and self-explanatory UI/onboarding baseline are **not** pending decisions unless later requirements justify explicit amendments.