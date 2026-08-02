# Decision Log

Use this file for project-wide research and architecture decisions. Detailed alternatives may use separate ADRs.

## DEC-001 — Private repository as source of truth
- **Date:** 2026-07-29
- **Status:** Accepted; bibliography boundary clarified by DEC-017
- **Decision:** `MariosGiannakaras/resilient-ai-agents-thesis` is the permanent version-controlled source of truth for thesis context, implementation, experiments, results, writing, and presentation.
- **Rationale:** Decisions and evidence must remain available independently of chat history.
- **Consequences:** Context files must be maintained; raw chats remain excluded. The complete bibliography lifecycle is the explicit source-of-truth exception defined by DEC-017.

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

## DEC-004 — Research core precedes the polished dashboard
- **Date:** 2026-07-29
- **Status:** Accepted; clarified by DEC-019
- **Decision:** Validate the independent core/CLI and pilot evidence before implementing the polished final dashboard.
- **Rationale:** Scientific correctness and reproducibility precede presentation-layer expansion.
- **Clarification:** DEC-019 permits a lightweight debug/visualization surface during core development when it helps validate behavior and does not duplicate scientific logic.

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
- **Status:** Accepted; local acquisition clause superseded by DEC-017
- **Context:** An external audit correctly identified risks of repeated whole-repository analysis, an oversized first Codex output, stale PDF wording and possible UI drift toward telemetry/provenance-heavy platform behavior. The user also required systematic research of comparable studies and repetition of that research during thesis writing.
- **Decision:**
  - Agents always read a five-file core and add only task-specific files.
  - The first Codex mission produces four integrated outputs rather than eleven separate reports.
  - The fourteen roadmap phases are checkpoints and may be executed as eight bounded work blocks.
  - Literature search is repeated during initial framing, before protocol freeze, before Related Work/Methodology/Discussion, and before submission.
  - UI telemetry is a lightweight current snapshot. Full checksums, manifests, Git/runtime details and provenance chains use progressive disclosure or exports.
  - Bibliography acquisition and verification follow the canonical architecture in DEC-017; the earlier local-download implementation is no longer active.
- **Rationale:** Preserve scientific rigor and source traceability while reducing repeated analysis, process overhead, UI clutter and production-platform scope.
- **Alternatives rejected:** whole-repository reread before every task; one large report per subtopic; one-time literature search; hidden provenance; full observability dashboard; unverified or paywall-bypassing sources.
- **Consequences:** The first research package remains comprehensive but reviewable. The written thesis must use refreshed, verified sources. Primary UI workflows remain clean while detailed evidence remains available.

## DEC-015 — Automated technical execution and review without routine user GitHub approval
- **Date:** 2026-07-29
- **Status:** Accepted by user
- **Context:** The user wants to provide goals, results and supervisor feedback without managing commits, Pull Requests, tests or merges. Codex must not own research, implementation, testing, review and approval simultaneously.
- **Decision:**
  - The user supplies goals, observed results and genuinely academic/product decisions, but is not the routine GitHub approver.
  - ChatGPT scopes tasks, reviews research and repository evidence, addresses or delegates corrections and decides technical merge readiness.
  - Codex executes bounded tasks and produces branches, tests, documentation, commits and Pull Requests; it never self-approves or silently broadens scope.
  - GitHub Actions executes repeatable checks on relevant Pull Requests. CI is necessary but not sufficient; test quality and scientific correctness receive ChatGPT review.
  - Every substantial change uses descriptive naming, reasoned comments, structured commit bodies and the repository Pull Request template.
- **Rationale:** Separate execution from review, reduce user overhead, improve consistency and catch defects before they affect experiments or thesis evidence.
- **Alternatives rejected:** user-managed Git approvals; Codex self-review and self-merge; direct-to-main implementation; test-passing as the sole acceptance criterion; production-grade CI/CD.
- **Consequences:** Routine technical GitHub work is automatic between Codex, GitHub and ChatGPT. The user is interrupted only for meaningful thesis-direction decisions or required private material.
- **Files:** `AGENTS.md`, `README.md`, `docs/context/EXECUTION_WORKFLOW.md`, `.github/pull_request_template.md`, `.github/workflows/repository-checks.yml`, tests and relevant scripts.

## DEC-016 — Original PDF archive with Markdown-first bibliography workflow
- **Date:** 2026-07-29
- **Status:** **SUPERSEDED by DEC-017**
- **Historical context:** This decision established local PDF archival copies, complete Markdown, source-centric notes and thematic excerpts inside this thesis repository.
- **Supersession:** The retention and Markdown-first principles were moved into the dedicated canonical bibliography repository. The thesis repository must no longer ingest or curate primary bibliography material directly.
- **Historical alternatives rejected:** discard PDFs after conversion; use PDFs as the normal working corpus; keep only summaries; trust AI summaries without source verification.
- **Current rule:** Follow DEC-017 and `docs/context/BIBLIOGRAPHY_INTEGRATION.md`.

## DEC-017 — Dedicated canonical ThesisBibliography repository and controlled import
- **Date recorded:** 2026-08-02
- **Status:** Accepted / current architecture
- **Context:** Bibliography acquisition, preservation, conversion, analysis and evidence extraction form a substantial lifecycle that should remain complete and independently auditable without bloating or duplicating the thesis implementation repository.
- **Decision:**
  - `MariosGiannakaras/ThesisBibliography` is the canonical source of truth for source discovery, metadata, original PDFs, conversion/OCR, full-source Markdown, scientific analysis, verified citation-ready evidence, inclusion/exclusion decisions and controlled export.
  - `MariosGiannakaras/resilient-ai-agents-thesis` consumes only the verified generated package under `research/bibliography/`.
  - The import is bound to an exact `SOURCE_COMMIT` and `IMPORT_INTEGRITY.json`; canonical source references use exported `SRC-XXXXXXXXXX` identifiers.
  - Synchronization is pull-based and reviewable through a Pull Request. There is no submodule and no write path from the thesis repository into `ThesisBibliography`.
  - PDFs, raw originals, conversion workspaces, unverified analyses and unverified evidence are not imported into the thesis repository.
  - New user-provided PDF/Markdown/NotebookLM bibliography material is processed in `ThesisBibliography`, not here.
  - Source-derived scientific evidence remains in the original source language.
- **Rationale:** Preserve complete source provenance and reusable bibliography analysis while keeping the thesis repository bounded, deterministic and focused on research design, implementation, experiments, results and writing.
- **Alternatives rejected:** duplicated bibliography lifecycle in both repositories; Git submodule coupling; thesis-repository write access into the bibliography repository; manual copying of selected evidence; translation of canonical source evidence.
- **Consequences:** Legacy `bibliography/original/`, `bibliography/markdown/`, `bibliography/notes/`, `bibliography/excerpts/` and local acquisition instructions are compatibility/history markers only. Freshness gates execute in `ThesisBibliography` and enter this repository through a new verified export/sync.
- **Files:** `docs/context/BIBLIOGRAPHY_INTEGRATION.md`, `bibliography/README.md`, `research/bibliography/`, synchronization/validation scripts and workflows, `AGENTS.md`, `README.md`.

## DEC-018 — English operational and technical repository documentation
- **Date:** 2026-08-02
- **Status:** Accepted by user
- **Context:** The user does not require repository documentation to be in Greek and prefers Codex-facing material to use the language most consistent with code, APIs, tests and technical documentation.
- **Decision:**
  - Repository-authored operational and technical documentation is written in English.
  - Agent prompts/instructions, architecture/protocol/test documentation, code comments, identifiers, filenames, branches, commits and Pull Request text use English.
  - Exact official Greek text is preserved where it identifies or quotes an authoritative source, including the official Greek thesis title.
  - Scientific source-derived text and citation-ready evidence remain in the original language of the source and are not translated merely for repository uniformity.
  - The final thesis remains a Greek Microsoft Word deliverable unless official guidance changes.
- **Rationale:** Use a single technical language for clearer agent execution and lower terminology ambiguity without altering primary evidence or official academic wording.
- **Consequences:** Existing mixed-language operational files are normalized progressively; source material and generated canonical bibliography evidence are excluded from translation.

## DEC-019 — Early debug visualization allowed; polished dashboard remains gated
- **Date:** 2026-08-02
- **Status:** Accepted by user
- **Context:** A basic visual surface is useful early for observing GridWorld and agent behavior, debugging, and understanding whether the system works, while a polished application before scientific validation would be premature.
- **Decision:**
  - A lightweight debug/visualization surface may be implemented alongside the research core when it directly assists validation.
  - It must consume the same core state/trace interfaces and must not duplicate scientific logic or become a second execution path.
  - The polished bounded dashboard and final user workflows remain gated behind a validated independent core and pilot evidence.
- **Rationale:** Improve development observability and reduce debugging friction without making UI work drive the scientific architecture.
- **Consequences:** DEC-004 is interpreted as a gate on the polished final dashboard, not a ban on small validation-oriented visualization.

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