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
- Added the initial local bibliography acquisition workflow. Its acquisition/storage implementation was later superseded by the dedicated canonical bibliography architecture recorded on 2026-08-02.
- Added DEC-014.

## 2026-07-29 — Automated execution, review and merge workflow

- Established the user/ChatGPT/Codex/GitHub responsibility split in `EXECUTION_WORKFLOW.md` and `AGENTS.md`.
- Removed routine GitHub approval and merge work from the user; ChatGPT reviews and decides technical readiness.
- Added branch, commit, naming, comment and Pull Request conventions.
- Added a Pull Request template with validation, scientific-impact, artifact and scope sections.
- Added lightweight GitHub Actions checks for merge markers, Python compilation, tests and JSON validity.
- Added regression tests for the then-active local bibliography-manifest provenance behavior.
- Added DEC-015.

## 2026-07-29 — Archived PDFs and Markdown-first bibliography workflow

- Established the original in-repository PDF/Markdown/note/excerpt workflow and DEC-016.
- **This workflow is historical and has been superseded by DEC-017.** The underlying preservation and Markdown-first principles now live in the dedicated `ThesisBibliography` repository rather than this thesis repository.

## 2026-08-02 — Canonical ThesisBibliography integration and documentation normalization

- Established `MariosGiannakaras/ThesisBibliography` as the canonical source of truth for source discovery, metadata, original PDFs, OCR/Markdown conversion, scientific analysis, verified citation-ready evidence, source selection and controlled export.
- Limited this repository to the verified generated package under `research/bibliography/`, bound to exact `SOURCE_COMMIT` and SHA-256 import integrity.
- Kept the repositories independent: no submodule and no write path from the thesis repository to `ThesisBibliography`; synchronization remains pull-based and Pull-Request-reviewed.
- Retired local bibliography acquisition/archive/Markdown/note/excerpt paths as compatibility/history markers so older instructions cannot reactivate the superseded workflow.
- Reconciled the Codex bootstrap prompt and implementation roadmap with the verified bibliography import instead of local paper downloads.
- Removed the stale open question that treated the bibliography corpus as missing.
- Recorded the user's language policy: repository-authored operational/technical documentation, prompts, Git/GitHub text, naming and code comments use English.
- Preserved the exact official Greek thesis title and exact official Greek source/work titles where they identify authoritative material.
- Preserved scientific source-derived text and citation-ready evidence in each source's original language; the final thesis remains Greek Microsoft Word.
- Clarified that a lightweight visual/debug surface may support core validation, while the polished final dashboard remains gated behind validated core and pilot evidence.
- Added DEC-017, DEC-018 and DEC-019 and marked DEC-016 as superseded.

## 2026-08-04 — Implementation-first priority and deferred writing-stage inputs

- Recorded that the proposed thesis topic has been approved and that no current supervisor-specific instructions or deadlines exist.
- Removed supervisor identity, supervisor requirements, submission dates, and Word-template availability as current blockers for bibliography integration, model research, GridWorld selection, implementation, pilots, and experiments.
- Established that later supervisor corrections are incorporated when actually received rather than anticipated in advance.
- Prioritized complete bibliography-corpus integration, target-system inventory, model/agent research, GridWorld prototypes, the independent research program, pilots, and experiments before normal chapter drafting.
- Preserved structured writing notes, evidence mappings, method records, captions, and reproducible artifacts during implementation so later writing is not a separate reconstruction exercise.
- Recorded that two or three completed theses may be supplied near the writing phase as contextual examples only; they do not override official Department guidance or become scientific sources.
- Recorded that the user created a fine-grained token and replaced the `BIBLIOGRAPHY_SYNC_TOKEN` Actions secret. Effective access remains to be verified by the migrated complete-corpus synchronization workflow without exposing the token value.
- Added DEC-020 and updated the active requirements and open-question taxonomy.
