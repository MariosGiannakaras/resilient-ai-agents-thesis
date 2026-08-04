# DEC-026 — End-to-End Lifecycle Handoffs and Defense Package

**Status:** Accepted by explicit user instruction  
**Date:** 2026-08-04

## Context

The repository already defined the scientific/software phases and a resumable Codex task registry, but the handoff from validated application to final experiments, frozen analysis evidence, thesis writing, supervisor/reviewer revision, and final defense presentation was not explicit enough from either the Codex or user perspective.

The presentation task was especially underspecified: it did not require a final PowerPoint file, speaker notes/full spoken script, evidence mapping, or rehearsal/format validation.

## Decision

- `docs/context/END_TO_END_JOURNEY.md` is the active lifecycle/handoff guide; `TASKS.md` remains the only concrete checklist/status authority.
- Final experiments normally begin only after the frozen protocol **and** validated user-facing application workflow are complete, so the intended application -> experiments user journey is explicit.
- After final analysis, a thesis evidence package is created as the formal handoff to writing and presentation. It maps claims, methods, figures/tables, source IDs, result IDs, run IDs, and protocol identity.
- Thesis writing proceeds from frozen evidence and citation-ready bibliography, followed by a review/revision cycle when supervisor/reviewer feedback exists, then a frozen final thesis deliverable.
- The defense presentation is a separate final phase after the thesis is stable. It produces a PowerPoint `.pptx`, embedded speaker notes, a separate full spoken Greek script, evidence mapping, validated screenshots/demo fallback, and rehearsal/timing checks.
- Preferred role split: Codex prepares/verifies repository-backed evidence/assets and reproducible exports; ChatGPT develops the defense narrative, slide copy, spoken script, and consistency review; PowerPoint-capable presentation tooling creates the `.pptx`; Microsoft PowerPoint is the final inspection/rehearsal surface. Canva/other design tools are optional polish only and must be revalidated after export.
- Official current Department/University presentation/submission requirements are refreshed near delivery rather than guessed now.

## Consequences

The end of the application is no longer an ambiguous project endpoint. It is a validated handoff into final experiment execution. Likewise, the thesis and defense presentation become traceable downstream products of the same frozen evidence chain rather than independent manual artifacts.

The user is not expected to manage routine Git/results/task state. User involvement remains focused on academic/product choices, later official/supervisor feedback, review of thesis/presentation content, and rehearsal.

## Alternatives rejected

- treat application completion as the end of the repository workflow;
- run final experiments before validating the intended user-facing experiment workflow without recording an exception;
- write the thesis directly from ad-hoc result inspection without a frozen evidence package;
- create a presentation manually after writing with no evidence mapping or speaker-note workflow;
- rely on Canva/design tooling as the scientific source of truth.