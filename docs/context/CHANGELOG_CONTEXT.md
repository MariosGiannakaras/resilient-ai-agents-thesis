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
- Consolidated the UI architecture into Dashboard, New Experiment, Runs, Compare and Artifacts.
- Split features into required, justified-later and out-of-scope tiers.
- Explicitly deferred cloud, multi-user/auth, distributed orchestration, enterprise infrastructure and non-essential AI.
- Updated Codex bootstrap criteria to require a small completable research design and a dashboard feature budget before implementation.
- Added DEC-013 and new confirmed requirements for scope, UI quality and architectural restraint.

## 2026-07-29 — Lean agent workflow and staged literature evidence

- Replaced universal whole-repository rereading with five permanent core files plus task-specific reading.
- Compressed the first Codex mission from eleven standalone deliverables into four reviewable outputs without removing the required evidence.
- Corrected `SOURCE_REGISTER.md`: the official PDF identity is user-confirmed; only local repository SHA-256 calculation remains pending.
- Clarified that UI resource telemetry is a lightweight current snapshot, not a monitoring/observability subsystem.
- Moved complete checksums, manifests, runtime details and provenance chains behind expandable details or export metadata.
- Clarified that the fourteen roadmap phases are checkpoints and can be operated as eight larger work blocks.
- Added literature refresh gates for initial framing, protocol freeze, thesis writing and final submission.
- Added `RELATED_WORK_EVIDENCE_MATRIX.md` with comparable papers and institutional theses, reported results, limitations, implications and writing-structure lessons.
- Added `SOURCE_ACQUISITION_WORKFLOW.md` and `scripts/download_open_access_bibliography.py` for lawful open-access paper/thesis acquisition, PDF validation, SHA-256 and a source manifest.
- Established user-assisted lawful acquisition for paywalled or non-direct sources; no unofficial or paywall-bypassing sources.
- Added DEC-014.

## 2026-07-29 — Automated execution, review and merge workflow

- Established the user/ChatGPT/Codex/GitHub responsibility split in `EXECUTION_WORKFLOW.md` and `AGENTS.md`.
- Removed routine GitHub approval and merge work from the user; ChatGPT reviews and decides technical readiness.
- Added branch, commit, naming, comment and Pull Request conventions.
- Added a Pull Request template with validation, scientific-impact, artifact and scope sections.
- Added lightweight GitHub Actions checks for merge markers, Python compilation, tests and JSON validity.
- Added regression tests for bibliography-manifest provenance behavior.
- Corrected automated-review findings so manual source records, acquisition timestamps and full-text review status are preserved safely by checksum.
- Added DEC-015.

## 2026-07-29 — Archived PDFs and Markdown-first bibliography workflow

- Added `bibliography/README.md` as the authoritative source-storage and usage policy.
- Retained original PDFs as immutable archival/verification copies rather than routine agent input.
- Established complete searchable Markdown with matching basenames as the default full-text working archive.
- Strengthened per-source notes with checksums, conversion/review states, topics and decision relevance.
- Added `bibliography/excerpts/` for small, topic-centric, verified evidence used in research, writing and slides.
- Added immediate processing rules for user-uploaded PDF/Markdown/NotebookLM source batches.
- Defined canonical renaming, duplicate/version detection, semantic classification and coverage-gap analysis.
- Added bibliography transient-file ignore rules and DEC-016.
