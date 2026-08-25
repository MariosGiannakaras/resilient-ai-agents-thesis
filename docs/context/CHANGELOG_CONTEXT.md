# Context Changelog

Record only material changes to the project source of truth. Detailed commit-by-commit history remains in Git; accepted decisions remain indexed in `docs/decisions/DECISION_LOG.md`.

## 2026-07-29 — Corrected bootstrap and thesis-completion-first scope

- Established the repository as the thesis project source of truth and preserved the official Greek/English thesis identity.
- Corrected historical-chat treatment: old conversations are context only, not scientific/technical decisions.
- Removed legacy GridWorld/manual-hardware assumptions; target hardware is inspected automatically.
- Established a core-first, scientifically reproducible workflow and the “polished outside, bounded inside” scope principle.
- Excluded raw chat exports from the repository and kept current official guidance as the delivery authority.
- Established the automated user/ChatGPT/Codex/GitHub responsibility split and branch/PR/CI workflow.

## 2026-08-02 — Canonical bibliography boundary and repository language

- Established `MariosGiannakaras/ThesisBibliography` as the canonical bibliography lifecycle repository for source discovery, originals, OCR/conversion, analysis, verification, selection, materials, notes, and exports.
- Restricted this repository to controlled read-only/generated bibliography consumption; no thesis-to-bibliography write path.
- Standardized repository-authored technical/operational content in English while preserving exact official Greek text and original-language scientific evidence.
- Confirmed that early lightweight validation visualization may precede the later polished dashboard when it uses the same scientific core.

## 2026-08-04 — Reproducible research infrastructure and immutable bibliography consumer

- Adopted Python 3.12 + `uv` + committed lockfile and the independent `src/resilient_agents/` research package.
- Established strict ground-truth/agent-visible separation, independent deterministic RNG streams, explicit contracts, protocol partitions, metric primitives, filesystem run bundles, provenance/checksums, selective Git LFS, and guarded one-commit/one-push publication per whole experiment.
- Replaced citation-only consumption with the complete immutable bibliography corpus while retaining nested `citation-ready/` as the strict formal-citation layer; provenance/checksum/trust validation and no-PDF/no-bibliography-LFS import rules were established.
- Added active-document governance, the directly executable canonical Codex prompt, and automated documentation consistency checks; stale bootstrap instructions/compatibility structures began being retired.
- Added `TASKS.md` as the sole detailed task/dependency/resume ledger with `IN_PROGRESS` recovery state and checkpoint-friendly squash-PR workflow.
- Audited the full application → final experiments → evidence → thesis/review → defense → delivery lifecycle, including frozen evidence handoff and final PowerPoint/speaker-script workflow.
- Confirmed the self-explanatory dashboard baseline, contextual help/tooltips, semantic status treatment, pre-run review, and later lightweight skippable/replayable onboarding.
- Reduced mandatory Codex startup to the three-file core (`AGENTS.md`, `TASKS.md`, `CURRENT_STATUS.md`) with task-specific progressive disclosure.
- Established risk-based proportional testing: targeted implementation checks, tiny deterministic CI fixtures, no arbitrary coverage target, and no unjustified mutation/fuzz/property/combinatorial/snapshot expansion.
- Deferred normal thesis prose/supervisor-specific formatting/deadline inputs until their explicit later-stage gates rather than blocking implementation.

## 2026-08-21 — Pre-Codex repository cleanup

- Removed retired top-level `core/` and `bibliography/` compatibility structures; `src/resilient_agents/` and `research/bibliography/` are the only current surfaces.
- Reconciled contributor/PR workflow documentation and removed stale visibility/lifecycle assumptions from active guidance.
- Extended consistency validation so obsolete compatibility paths and stale active references cannot silently return.

## 2026-08-25 — Quota-efficient, fail-closed execution hardening

- Made targeted local validation + GitHub PR CI the normal validation path, avoiding duplicate full-suite runs and successful-log analysis while preserving complete pre-merge checks.
- Added concise objective `X/Y` progress reporting derived from `TASKS.md`; no invented percentages or second tracker.
- Added fail-closed boundaries for required config/contracts/schema/provenance/lifecycle state and explicit optional `unavailable`/`unsupported` outcomes.
- Hardened run finalization/publication with a last-written `FINALIZED` marker, post-finalization mutation rejection, marker/manifest/checksum/run-index agreement, source-provenance revalidation, and single-writer publication requirements for future batch execution.
- Standardized successful terminal execution status to `completed`; preserved `excluded` as a later analysis/inclusion status rather than overwriting execution outcome.
- Extended clean-source provenance so untracked non-output inputs prevent automatic publication without exposing filenames; generated/local `results/**` and `artifacts/**` remain allowed.
- Reordered/bounded the single repository-checks Actions job for earlier cheap failures, compact successful output, and explicit failure diagnostics; pure generated output pushes may skip duplicate full CI while PRs and material source/config/docs/test changes remain fully checked.
- Recorded temporary public thesis-repository visibility as an operational CI choice only, without waiving later privacy/copyright/licensing/release review.

## 2026-08-25 — Final Codex context compaction and cleanup

- Revalidated the Codex/AI repository setup against current OpenAI agent-harness guidance and recent developer practice.
- Replaced the oversized root `AGENTS.md` domain encyclopedia with a compact always-on control/routing map; detailed contracts remain in existing task-specific source-of-truth docs.
- Compressed `CODEX_EXECUTION_PROMPT.md` and `CURRENT_STATUS.md` to execution semantics and current state instead of repeated policy/history.
- Added CI-enforced line/word budgets for always-read Codex context so future edits cannot silently recreate context bloat.
- Kept `TASKS.md` complete because its dependency/acceptance/resume ledger and objective progress denominator are active execution data rather than redundant narrative.
- Removed superseded `FINAL_BOOTSTRAP_AUDIT.md` and `SOURCE_AUDIT.md` from the current tree; their history remains available in Git and their durable decisions are represented in current authorities/decision records.
- Compacted this changelog to material context milestones instead of duplicating ordinary Git history.
- Kept both active GitHub Actions workflows: bounded repository validation and controlled immutable bibliography synchronization remain required.
- Did not add nested `AGENTS.md`, generic skill packs, extra planning/status files, or multi-agent infrastructure because the current single-repository structure does not demonstrate a need that justifies their extra context/maintenance cost.
