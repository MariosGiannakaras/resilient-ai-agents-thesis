# Decision Log

Use this file for project-wide research and architecture decisions. Detailed alternatives may use separate ADRs.

## DEC-001 — Private repository as source of truth
- **Date:** 2026-07-29
- **Status:** Accepted
- **Decision:** `MariosGiannakaras/resilient-ai-agents-thesis` is the permanent version-controlled source of truth.
- **Rationale:** Decisions and evidence must remain available independently of chat history.
- **Consequences:** Context files must be maintained; raw chats remain excluded.

## DEC-002 — Official application controls academic identity
- **Date:** 2026-07-29
- **Status:** Accepted
- **Decision:** Use the exact institution and titles from the official application.
- **Rationale:** It is the primary approved source.
- **Consequences:** Historical degree/title wording is superseded.

## DEC-003 — Original application retained unchanged in private repository
- **Date:** 2026-07-29
- **Status:** Accepted by user
- **Decision:** Store the original application unchanged in the private repository.
- **Consequences:** Repository remains private; public release would require redaction.

## DEC-004 — Research core precedes dashboard
- **Date:** 2026-07-29
- **Status:** Accepted
- **Decision:** Validate independent core/CLI and pilot runs before dashboard implementation.
- **Rationale:** Scientific correctness and reproducibility precede presentation.

## DEC-005 — No final model, metric or experimental matrix yet
- **Date:** 2026-07-29
- **Status:** Accepted
- **Decision:** Build selections from scratch after literature, environment definition, inventory, prototypes and pilots.
- **Consequences:** Historical lists are not candidates by default.

## DEC-006 — No acceleration assumptions before automated inventory
- **Date:** 2026-07-29
- **Status:** Accepted
- **Decision:** Codex records actual system capabilities before compute-dependent choices; CPU-compatible execution is the safe temporary baseline.

## DEC-007 — Raw chat exports excluded
- **Date:** 2026-07-29
- **Status:** Accepted
- **Decision:** Commit verified synthesis only, not transcript archives.
- **Rationale:** Privacy, clarity and source governance.

## DEC-008 — Department guidance snapshot, not frozen final template
- **Date:** 2026-07-29
- **Status:** Accepted
- **Decision:** Record current official guidance now and recheck the final Word template/submission rules near delivery.

## DEC-009 — Conversation exports are context only
- **Date:** 2026-07-29
- **Status:** Accepted by user
- **Decision:** Old conversations do not establish models, metrics, GridWorld rules, stack, hyperparameters, features or preferences.
- **Consequences:** Every research and technical decision needs fresh evidence.

## DEC-010 — Fresh GridWorld discovery; no legacy-code dependency
- **Date:** 2026-07-29
- **Status:** Accepted by user
- **Decision:** Compare current reuse, adapt/wrap and minimal custom implementation; integrate only after audit, prototype and ADR.

## DEC-011 — Codex owns system inventory
- **Date:** 2026-07-29
- **Status:** Accepted by user
- **Decision:** Codex automatically collects CPU, RAM, GPU/VRAM, OS, drivers, runtimes and storage.

## DEC-012 — Final bootstrap re-audit governs the next phase
- **Date:** 2026-07-29
- **Status:** Accepted
- **Decision:** Corrected context files and final audit supersede inconsistent bootstrap wording; implementation remains phase-gated.

## DEC-013 — Thesis-completion-first scope and polished bounded dashboard
- **Date:** 2026-07-29
- **Status:** Accepted by user
- **Context:** Earlier requirements risked drifting toward excessive experiment and platform complexity, while previous attempts exposed too many models/settings and failed to present comparisons clearly.
- **Decision:** Optimize the project for a scientifically adequate and realistically completable thesis. Keep the research question, GridWorld, model set, uncertainty taxonomy and protocol small and justified. Build a polished modern dashboard for the essential thesis workflows, but keep internal architecture and feature count bounded.
- **Product principle:** **Polished outside, bounded inside.**
- **Required UI workflows:** configure and launch experiments, truthful monitoring, GridWorld visualization, run history/details, compatible comparison, metrics/charts/tables and thesis artifact export.
- **Explicit non-goals:** production infrastructure, public/cloud deployment, multi-user/auth/permissions, distributed workers, complex orchestration, enterprise telemetry, plugin systems and non-essential AI.
- **Alternatives rejected:** rough minimal interface; production-grade platform; broad research matrix with many models/settings.
- **Consequences:** UI quality remains a real deliverable, but every feature must map to research, reproducibility, usability or thesis-delivery value. Advanced features remain deferred until a measured need appears.
- **Related requirements:** REQ-RES-009, REQ-RES-010, REQ-EXP-009, REQ-APP-009..011, REQ-ARCH-006..007, REQ-UI-005..006.
- **Files:** `docs/context/SCOPE_REFINEMENT.md`, `AGENTS.md`, `README.md`, `docs/architecture/`, `CODEX_BOOTSTRAP_PROMPT.md`, `IMPLEMENTATION_ROADMAP.md`.

## DEC-014 — Lean agent workflow, staged literature refresh and progressive disclosure
- **Date:** 2026-07-29
- **Status:** Accepted implementation of the user's audit/remediation request
- **Context:** An external audit correctly identified risks of repeated whole-repository analysis, an oversized first Codex output, stale PDF wording and possible UI drift toward telemetry/provenance-heavy platform behavior. The user also required systematic research of comparable studies and repetition of that research during thesis writing.
- **Decision:**
  - Agents always read a five-file core and add only task-specific files.
  - The first Codex mission produces four integrated outputs rather than eleven separate reports.
  - The fourteen roadmap phases are checkpoints and may be executed as eight bounded work blocks.
  - Literature search is repeated during initial framing, before protocol freeze, before Related Work/Methodology/Discussion, and before submission.
  - Lawful open-access or author-provided papers may be downloaded automatically with source metadata and SHA-256; paywalled papers require lawful user acquisition.
  - UI telemetry is a lightweight current snapshot. Full checksums, manifests, Git/runtime details and provenance chains use progressive disclosure or exports.
- **Rationale:** Preserve scientific rigor and source traceability while reducing repeated analysis, process overhead, UI clutter and production-platform scope.
- **Alternatives rejected:** whole-repository reread before every task; one large report per subtopic; one-time literature search; hidden provenance; full observability dashboard; unverified or paywall-bypassing downloads.
- **Consequences:** The first research package remains comprehensive but reviewable. The written thesis must use refreshed, fully read sources. Primary UI workflows remain clean while detailed evidence remains available.
- **Files:** `AGENTS.md`, `README.md`, `CODEX_BOOTSTRAP_PROMPT.md`, `IMPLEMENTATION_ROADMAP.md`, `SOURCE_REGISTER.md`, `docs/architecture/`, `docs/research/RELATED_WORK_EVIDENCE_MATRIX.md`, `bibliography/SOURCE_ACQUISITION_WORKFLOW.md`, `scripts/download_open_access_bibliography.py`.

## DEC-015 — Automated technical execution and review without routine user GitHub approval
- **Date:** 2026-07-29
- **Status:** Accepted by user
- **Context:** The user wants to provide goals, results and supervisor feedback without managing commits, Pull Requests, tests or merges. Codex must not own research, implementation, testing, review and approval simultaneously.
- **Decision:**
  - The user supplies goals, observed results and genuinely academic/product decisions, but is not the routine GitHub approver.
  - ChatGPT scopes tasks, reviews research and repository evidence, addresses or delegates corrections and decides technical merge readiness.
  - Codex executes bounded tasks and produces branches, tests, documentation, commits and Pull Requests; it never self-approves or silently broadens scope.
  - GitHub Actions executes repeatable checks on relevant Pull Requests. CI is necessary but not sufficient; test quality and scientific correctness receive human/ChatGPT review.
  - Every substantial change uses descriptive naming, reasoned comments, structured commit bodies and the repository Pull Request template.
- **Rationale:** Separate execution from review, reduce user overhead, improve consistency and catch defects before they affect experiments or thesis evidence.
- **Alternatives rejected:** user-managed Git approvals; Codex self-review and self-merge; direct-to-main implementation; test-passing as the sole acceptance criterion; production-grade CI/CD.
- **Consequences:** Routine technical GitHub work is automatic between Codex, GitHub and ChatGPT. The user is interrupted only for meaningful thesis-direction decisions or required private material.
- **Files:** `AGENTS.md`, `README.md`, `docs/context/EXECUTION_WORKFLOW.md`, `.github/pull_request_template.md`, `.github/workflows/repository-checks.yml`, tests and relevant scripts.

## Pending decisions

Future entries are required for:

- final research questions and hypotheses,
- GridWorld reuse/adapt/custom selection,
- final uncertainty taxonomy,
- selected models and baselines,
- primary metrics and statistical plan,
- seeds, repetitions and budgets,
- final application stack/storage/runner,
- exact required versus optional dashboard features after pilots,
- optional AI,
- citation style and final Word template.
