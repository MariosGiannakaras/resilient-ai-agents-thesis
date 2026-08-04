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
- **Status:** Accepted; clarified by DEC-019/DEC-023.
- **Decision:** Scientific/headless execution is independent from UI; small debug visualization may appear early, polished dashboard follows validated workflow/pilots.

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
- **Decision:** Current official guidance controls; final Word/submission rules are refreshed near delivery.

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
- **Status:** Accepted by explicit user instruction.
- **Context:** A later audit found active files that still described completed bibliography migration/authentication and pre-DEC-023 architecture as pending. A stale Codex bootstrap prompt also remained tracked.
- **Decision:**
  - A material change is incomplete until all affected active context/status/research/architecture/workflow/prompt files are reconciled in the same PR.
  - `CURRENT_STATUS.md` is the shortest current-state authority but does not excuse contradictions elsewhere.
  - Obsolete files are deleted; useful historical records are retained only with prominent historical/superseded labels.
  - There is one tracked current Codex prompt: `docs/context/CODEX_EXECUTION_PROMPT.md`; local `CODEX_TASK.md` is git-ignored and disposable.
  - `docs/context/DOCUMENTATION_GOVERNANCE.md` defines the minimum dependency matrix.
  - CI runs `scripts/validate_documentation_consistency.py` for mechanically detectable stale-state errors.
- **Rationale:** Repository context must remain trustworthy for future Codex/ChatGPT work and must not require the user to remember which active-looking file is obsolete.
- **Alternatives rejected:** rely only on a current-status overlay; fix stale docs only when noticed manually; keep multiple tracked phase-specific Codex prompts.

## Pending decisions

Future entries are still required for:

- final research question and hypotheses;
- final GridWorld implementation/scientific specification;
- final uncertainty taxonomy/severities/timing;
- exact selected models/baselines, including whether robust-MDP comparison receives formal evidence support;
- final primary/secondary/diagnostic metrics and statistical plan;
- seeds, repetitions, tuning/resource budgets, and stopping rules;
- final pilot protocol and `protocol-v1.0` freeze/amendments;
- pilot-derived optional dashboard feature budget;
- optional AI, if ever justified;
- final citation style/Word template/submission specifics near writing/delivery.

The general Python/core/storage/result-publication/dashboard architectural baseline is **not** a pending decision unless later measured requirements justify an explicit amendment to DEC-023.
