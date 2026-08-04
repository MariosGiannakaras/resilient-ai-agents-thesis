# Codex Execution Prompt

## How to use

This file is the single tracked canonical and directly executable Codex prompt for the thesis project.

After cloning or updating the repository on the thesis machine, give Codex only this instruction:

> Read `docs/context/CODEX_EXECUTION_PROMPT.md` and execute it completely.

Do not copy this prompt to another task file and do not delete it after use. Whenever workflow, architecture, responsibilities, project state, or the active next task materially changes, this file must be reconciled in the same Pull Request.

The instructions below are deliberately state-driven. `docs/context/CURRENT_STATUS.md` and the actual current repository state override any phase snapshot that could become outdated later.

---

Work autonomously in the private repository `MariosGiannakaras/resilient-ai-agents-thesis` and continue the thesis project from the **actual current `main` state**.

Do not reconstruct the project from chat history and do not redo work that is already implemented, validated, merged, or recorded as accepted. Inspect first, then execute the next genuinely pending bounded work in dependency order until you reach a real academic/environment-dependent gate or the assigned work is complete.

## Required initial reading

Read first:

1. `AGENTS.md`
2. `README.md`
3. `docs/context/CURRENT_STATUS.md`
4. `docs/context/SCOPE_REFINEMENT.md`
5. `docs/context/PROJECT_CONTEXT.md`
6. `docs/context/CONFIRMED_REQUIREMENTS.md`
7. `docs/context/IMPLEMENTATION_ROADMAP.md`
8. `docs/context/DOCUMENTATION_GOVERNANCE.md`

Then read only task-specific files required by `AGENTS.md`. Historical files are context only and must not override current active files.

## Already accepted baseline — verify, do not redo

Unless the repository itself shows otherwise, the accepted baseline includes:

- the complete immutable bibliography consumer under `research/bibliography/` with the strict nested citation-ready layer;
- verified private bibliography synchronization/authentication and integrity validation;
- Python 3.12 + `uv` + committed `uv.lock`;
- the independent importable package `src/resilient_agents/`;
- evaluator-ground-truth versus agent-visible information separation;
- independently derived deterministic RNG streams;
- scenario/experiment/change/protocol contracts with no hidden scientific defaults;
- filesystem-first self-contained run bundles with provenance/checksums;
- guarded one-commit/one-push publication per finalized **whole experiment**, never per seed;
- selective Git LFS for configured large thesis-produced artifacts;
- development/tuning/pilot/final separation infrastructure;
- the future dashboard as a thin Streamlit layer over the same research core, gated behind validated headless workflow and pilots.

Validate these rather than reimplementing them.

## Current dependency order

Use `CURRENT_STATUS.md` and `IMPLEMENTATION_ROADMAP.md` as the authoritative queue. At the time this prompt was written, the first unresolved gates are expected to be:

1. run and accept the privacy-minimal system inventory on the **actual thesis experiment machine**;
2. complete the bounded GridWorld prototype comparison and ADR;
3. promote the selected environment implementation into `src/resilient_agents/` with known-answer/reference-trace tests;
4. complete source-traceable model/agent-role research using the imported bibliography;
5. operationalize resilience/recovery metrics and validate them on synthetic known-answer fixtures;
6. define the bounded research question/hypotheses and pilot protocol without leakage from final evaluation;
7. implement only the small justified agent set behind the common information-limited interface;
8. run pilots, measure runtime/variance/storage/metric behavior, and freeze the final protocol only after pilot questions are answered;
9. complete the headless experiment runner/analysis pipeline and only then build the dashboard functionality required by the validated workflow;
10. execute final experiments, freeze thesis evidence, generate figures/tables, and defer normal thesis prose until the evidence-producing system is mature.

If the repository shows that any item above is already complete, skip it and continue from the first unresolved item.

## Bibliography rules

`MariosGiannakaras/ThesisBibliography` is the canonical source of truth for source discovery, originals/PDFs, conversion/OCR, scientific analysis, evidence verification, source selection, research materials, notes, and generated exports.

In this repository:

- consume the verified import under `research/bibliography/`;
- treat `research/bibliography/citation-ready/` as the only automatic formal-citation layer;
- use full-corpus/rejected/theory-only/`MAT-*`/notes for internal research only unless promoted upstream and resynchronized;
- do not acquire or edit bibliography sources locally;
- do not fabricate bibliographic identity, DOI, source status, evidence, or conclusions;
- if final support is needed from a non-citation-ready item, record an exact upstream verification/promotion requirement instead of locally promoting it.

## Scientific rules

- Keep the research design small and completable.
- Do not freeze a model, severity, seed count, budget, threshold, hyperparameter, or statistical method without evidence/pilot justification.
- No single-run model comparison.
- Keep development, tuning, pilot, and final evaluation separated.
- No agent receives hidden regime/change/disturbance/ground-truth information unless the protocol explicitly gives the same scientifically justified signal.
- Preserve non-recovery explicitly; do not convert it to an artificial recovery time at the horizon.
- Retain failures, cancellations, interruptions, invalid runs, and exclusions with reasons.
- Do not inspect final evidence and then silently retune/redefine primary outcomes.

## Experiment and Git automation rules

A run ID represents one **whole experiment**, potentially containing many seeds/episodes.

- Persist results continuously and safely during execution.
- Finalize the self-contained run bundle only at the correct lifecycle boundary.
- Use the existing guarded publisher for one complete commit/push per finalized experiment.
- Never create a commit per seed/episode.
- Stage only the finalized experiment data and its required registry/index metadata.
- Preserve local results if publication fails.
- Do not force-push, hide unrelated tracked changes, or publish mixed provenance.
- Large thesis-produced outputs should be retained; use the configured Git LFS policy instead of manually excluding useful evidence because of file size. Revisit retention only when a real storage limit requires it.

## Architecture/UI rules

- Scientific logic lives in `src/resilient_agents/`, not in UI callbacks.
- The headless workflow must remain fully usable and testable without the dashboard.
- Filesystem run bundles are the source of truth; any later database/index is rebuildable cache.
- Avoid microservices, Kubernetes, cloud-only infrastructure, distributed workers, authentication systems, or production observability.
- A lightweight debug visualization is allowed when useful for validation.
- The polished dashboard is implemented only after pilots establish the real workflow and remains a thin local Streamlit layer unless measured requirements justify a different decision.

## Documentation consistency — mandatory

For every material change, follow `docs/context/DOCUMENTATION_GOVERNANCE.md`.

Do not update only code and leave related documentation stale. In the same PR:

- search for the old assumption/status/path/count/architecture statement;
- update all affected active source-of-truth files;
- update `CURRENT_STATUS.md`, `OPEN_QUESTIONS.md`, `DECISION_LOG.md`, and `CHANGELOG_CONTEXT.md` when affected;
- update this canonical Codex prompt when workflow, architecture, responsibilities, or the active next task materially changes;
- delete obsolete files or mark useful historical records prominently as historical;
- never rewrite generated bibliography evidence by hand.

Run the documentation consistency validator before merge.

## Testing and review

Use a branch and Pull Request for substantive work. Run the relevant tests plus the repository checks. Tests must cover the scientific/behavioral invariants affected by the change, not only syntax.

Do not treat passing CI as sufficient if the implementation or scientific assumptions are wrong. Record rationale, validation, exclusions, and remaining gates.

Prefer one logical squash merge to `main` for one coherent change rather than many permanent tiny commits.

## Stop conditions

Do not stop for routine Git operations, documentation updates, tests, or decisions that can be resolved from repository evidence, the actual local system, verified bibliography, prototypes, or authoritative technical documentation.

Stop and report clearly only when continuation truly requires one of the following:

- an academic/product choice that cannot be resolved objectively;
- new supervisor/Department guidance that only the user can supply;
- access/credential failure that cannot be fixed from the available environment;
- execution on the actual thesis machine when the current Codex environment is not that machine and the result would materially affect the next decision;
- a safety/legal/licensing blocker;
- a frozen-protocol change requiring explicit amendment.

When blocked, leave the repository internally consistent and state the exact next executable task.

## Final report

At the end of the session report only:

- what was completed;
- PR(s) and merge commit(s);
- important files/systems changed;
- tests/validators run and results;
- scientific/architecture decisions accepted or still unfrozen;
- real remaining blockers/gates;
- the exact next bounded task.

This tracked file remains in the repository as the canonical prompt. Do not delete or replace it without updating all related active documentation and recording the change in the same PR.
