# End-to-End Thesis Journey

**Status:** Active lifecycle/handoff guide.  
**Task authority:** `docs/context/TASKS.md` remains the only concrete checklist/status registry. This document explains responsibilities, handoffs, and expected outputs; it is not a second task list.

## Codex journey

Codex always starts from the actual repository state, `CODEX_EXECUTION_PROMPT.md`, and `TASKS.md`. It resumes unfinished work from durable Git/task evidence, uses session memory when available, and advances only through dependency-valid tasks.

The intended lifecycle is:

> repository/inventory -> research framing -> GridWorld/agents/metrics -> pilots -> frozen protocol -> validated application -> final experiments -> frozen evidence -> analysis/artifacts -> thesis -> defense presentation -> final audit/delivery

A phase is not considered handed off merely because code exists. Its task acceptance conditions, tests, source-of-truth reconciliation, and required evidence must be complete.

## User journey

The user should not operate routine Git, maintain task state manually, curate result files, or reconstruct unfinished work from memory.

The normal user responsibilities are intentionally small:

- start/continue Codex from the canonical execution prompt on the thesis machine;
- provide only genuinely academic/product choices, new supervisor/Department instructions, private material, or feedback that cannot be obtained from the repository/system;
- when the application is validated, use the approved UI workflow for real experiment configuration/execution rather than editing configs/results by hand;
- review important scientific interpretations, thesis wording, final formatting, and defense material;
- provide supervisor/reviewer corrections when they arrive and rehearse the final presentation.

## Handoff 1 — Research system to validated application

The application is considered ready only after the selected GridWorld, agents, metrics, protocol-aware experiment path, persistence/recovery, analysis interfaces, and thin dashboard have been validated end to end.

Expected output:

- tested `src/resilient_agents/` research core;
- frozen final protocol/analysis plan;
- polished local dashboard using the same core;
- truthful configure/run/monitor/history/compare/export workflows;
- pilot evidence proving runtime, storage, metric behavior, and operational feasibility;
- no fake data/state and no manual routine Git workflow for the user.

This is the application-completion gate before the frozen final experiment campaign.

## Handoff 2 — Validated application to final experiments

Final experiments use the frozen protocol and the validated application/core without scientific changes after inspecting results.

The user selects/starts the predefined final experiment campaign through the validated workflow. The system handles seeds, persistence, provenance, failures, run bundles, checksums, large artifacts, and one guarded commit/push per whole experiment.

Expected output: a complete, auditable set of final run bundles with explicit completed/failed/excluded status and no cherry-picking.

## Handoff 3 — Final experiments to frozen evidence and analysis

After all predefined runs are accounted for, the accepted final evidence set is frozen before thesis claims are written from it.

Analysis then produces reproducible statistical outputs, figures, tables, diagnostics, captions, and exports from the frozen evidence only.

A dedicated thesis evidence package is produced containing at least:

- final RQs/hypotheses and protocol identity;
- included/excluded run list and reasons;
- result/metric definitions and statistical outputs;
- figure/table IDs with source run IDs;
- methodology/configuration summary tied to versioned files;
- claim-to-result and claim-to-source mapping needed for writing.

This package is the handoff contract to thesis writing and later to the defense presentation.

## Handoff 4 — Frozen evidence to thesis writing

Before final writing, current official Department/University template, citation, submission, and defense requirements are refreshed. Contextual example theses may guide structure only and never override official requirements.

ChatGPT is the preferred tool for evidence-grounded drafting, restructuring, Greek-language explanation, editing, consistency review, and iterative supervisor-feedback incorporation. Codex remains responsible for repository-backed verification, reproducible figures/tables, evidence mappings, and any code/data corrections that are legitimately required.

Expected output:

- review-ready Greek thesis `.docx`;
- citations tied to citation-ready bibliography evidence;
- all result claims tied to frozen experiment evidence;
- supervisor/reviewer corrections incorporated or explicitly recorded as not required;
- final thesis deliverable frozen before the defense deck is finalized.

## Handoff 5 — Final thesis to defense presentation

The defense deck is created only from the final thesis, frozen evidence package, validated figures/tables, and real application screenshots/demo assets. `docs/thesis/PRESENTATION_WORKFLOW.md` defines the process.

Expected output is a defense package containing:

- final PowerPoint `.pptx`;
- embedded slide speaker notes;
- a separate full spoken script in Greek, detailed enough to follow/read during rehearsal or presentation preparation;
- slide-to-thesis/result/source evidence map;
- validated demo/screenshots and a fallback if a live demo is inappropriate or fails;
- rehearsal/timing and factual-consistency checks.

## Handoff 6 — Final audit and delivery

Final audit checks bibliography freshness, citations, thesis/presentation consistency, protocol/result provenance, privacy, licensing, reproducibility, required submission files, and defense readiness.

The finished project should therefore contain four coherent deliverable layers:

1. reproducible research software/application;
2. frozen experiments, analysis, figures, tables, and evidence package;
3. final Greek thesis deliverable;
4. final defense PowerPoint plus speaker notes/script and validated demo material.

No later artifact may silently contradict the frozen evidence or the final thesis.