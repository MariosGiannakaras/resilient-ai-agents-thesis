# Context Changelog

Record only material changes to the project source of truth. Do not duplicate ordinary Git history.

## 2026-07-29 — Initial bootstrap

- Added official Greek and English titles.
- Corrected historical degree/title wording.
- Established repository-as-source-of-truth policy.
- Established core-first architecture and experiment provenance rules.
- Excluded raw conversation exports.
- Added Department writing-guideline snapshot.

## 2026-07-29 — Final bootstrap re-audit

- Corrected the role of old chats to historical context only.
- Reset model, metric and GridWorld selection to fresh research.
- Removed legacy-code and manual-hardware blockers.
- Assigned automated system inventory to Codex.
- Corrected recent-thesis metadata and added final audit.

## 2026-07-29 — Official application confirmation

- Verified the PDF at the expected private repository path.
- Recorded user confirmation that it is the same authoritative file.
- Delegated direct repository SHA-256 calculation to Codex after clone.
- Marked bootstrap complete.

## 2026-07-29 — Thesis-completion-first scope refinement

- Added `SCOPE_REFINEMENT.md` as the authoritative product/scope direction.
- Set the priority order to bounded research question, validated GridWorld, small justified model/uncertainty set, reproducible protocol, reliable results and polished dashboard.
- Clarified that application simplicity applies to internal architecture and feature count, not to visual or interaction quality.
- Defined the target as a polished bounded research dashboard rather than a rough minimal UI or production-grade platform.
- Consolidated the UI architecture into essential thesis workflows.
- Explicitly deferred cloud, multi-user/auth, distributed orchestration, enterprise infrastructure and non-essential AI.
- Added DEC-013.

## 2026-07-29 — Lean agent workflow and staged literature evidence

- Replaced universal whole-repository rereading with a small permanent core plus task-specific reading.
- Clarified lightweight UI telemetry and progressive disclosure for provenance.
- Added staged literature refresh gates.
- Added the initial local bibliography acquisition workflow, later superseded by the dedicated canonical bibliography architecture.
- Added DEC-014.

## 2026-07-29 — Automated execution, review and merge workflow

- Established the user/ChatGPT/Codex/GitHub responsibility split in `EXECUTION_WORKFLOW.md` and `AGENTS.md`.
- Removed routine GitHub approval and merge work from the user.
- Added branch/commit/PR conventions and repository checks.
- Added DEC-015.

## 2026-07-29 — Archived PDFs and Markdown-first bibliography workflow

- Established the original in-repository PDF/Markdown/note/excerpt workflow and DEC-016.
- This workflow was later superseded by DEC-017; preservation/Markdown-first principles moved to `ThesisBibliography`.

## 2026-08-02 — Canonical ThesisBibliography integration and documentation normalization

- Established `MariosGiannakaras/ThesisBibliography` as canonical source of truth for source discovery, originals, conversion/OCR, analysis, verified evidence, selection and controlled export.
- Limited this repository to controlled generated bibliography consumption.
- Kept repositories independent: no submodule and no thesis-to-bibliography write path.
- Retired local bibliography acquisition/archive paths as historical/compatibility markers.
- Recorded English technical/operational documentation policy while preserving exact Greek official text and original-language scientific evidence.
- Clarified early debug visualization versus later polished dashboard.
- Added DEC-017, DEC-018 and DEC-019; DEC-016 became superseded.

## 2026-08-04 — Implementation-first priority and deferred writing-stage inputs

- Recorded approved topic and absence of current supervisor-specific instructions/deadlines.
- Removed supervisor identity/deadline/template as blockers for research/program/pilots.
- Prioritized bibliography integration, target-system inventory, model/agent research, GridWorld prototypes, research core, pilots and experiments before normal chapter drafting.
- Kept structured writing/evidence notes throughout implementation.
- Recorded contextual-only role of later example theses.
- Recorded replacement of the `BIBLIOGRAPHY_SYNC_TOKEN` credential without exposing its value.
- Added DEC-020.

## 2026-08-04 — Complete immutable bibliography consumer and accepted baseline

- Replaced the old citation-only imported-surface assumption with the complete `research-corpus/` consumer while preserving nested `citation-ready/` as the formal citation boundary.
- Added provenance/ancestry/checksum/forbidden-artifact validation and deterministic trust-aware search.
- Preserved bounded byte-level legacy PDF-conversion artifacts without weakening trust-sensitive validation.
- Verified the current private read credential successfully.
- Imported and accepted `bibliography-integration-v2` at checkout `27e325a74722b8f80643e6d1902e4bf3847036f5`.
- Recorded 583 canonical sources, 112 citation-ready sources, 19 research materials, metadata for 280 indexed original PDFs and 1561 consumer-recorded corpus files.
- Resolved the former HTTP 401/incomplete-import blockers.
- Added DEC-021 and DEC-022.

## 2026-08-04 — Reproducible research-core and automatic experiment publication architecture

- Adopted Python 3.12 + `uv` + committed lockfile.
- Established the independent importable `src/resilient_agents/` package.
- Added evaluator-ground-truth/agent-visible-information separation and independent deterministic RNG streams.
- Added explicit scenario/experiment/change/protocol contracts without hidden scientific defaults.
- Added development/tuning/pilot/final partition infrastructure and known-answer resilience metric primitives.
- Added filesystem-first experiment run bundles with config, capability snapshot, provenance, checksums, events/traces and summary.
- Added guarded one-commit/one-push publication per finalized whole experiment, never per seed.
- Changed repository policy so useful experiment outputs are tracked; configured large formats use selective Git LFS.
- Accepted the future dashboard as a thin Streamlit layer after headless core/pilot validation.
- Added DEC-023.

## 2026-08-04 — Repository-wide active-document reconciliation

- Audited active project/context/research/workflow files against the current accepted repository state.
- Found and removed stale statements that still treated the full bibliography import/authentication and pre-DEC-023 architecture as pending.
- Deleted the obsolete `CODEX_BOOTSTRAP_PROMPT.md` and created state-driven `CODEX_EXECUTION_PROMPT.md`.
- Corrected `POSTIMPORT_EVIDENCE_SYNTHESIS.md`: robust-MDP full-corpus records are internal candidates, not citation-ready anchors.
- Reconciled active GridWorld/model/metrics/research workspaces with the actual imported evidence and current infrastructure without freezing scientific choices.
- Added `DOCUMENTATION_GOVERNANCE.md`, stronger PR/contributor/agent consistency rules, and automated documentation-consistency validation in CI.
- Marked `FINAL_BOOTSTRAP_AUDIT.md` explicitly historical rather than leaving obsolete blockers as active-looking guidance.
- Added DEC-024: material changes must reconcile all affected active documentation/prompts/status/decisions in the same PR.

## 2026-08-04 — Canonical Codex prompt made directly executable

- Clarified that `docs/context/CODEX_EXECUTION_PROMPT.md` is not merely a template; it is the single canonical prompt Codex should read directly after the repository is cloned or updated.
- Removed the normal requirement to copy the prompt into a disposable `CODEX_TASK.md` file.
- Recorded that future material project/workflow changes must update the tracked canonical prompt in the same PR.
- Updated README, current status, execution workflow, documentation governance, DEC-024, decision index, ignore rules and consistency validation accordingly.
