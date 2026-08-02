# User Decisions

This file contains only explicit current user decisions. Old conversations do not create decisions by themselves.

## Overall project direction

- The primary goal is a correct, completable, and scientifically adequate thesis.
- The application is not the main research contribution and must not become a production-grade platform.
- The application remains an important deliverable and must be polished, modern, consistent, and easy to use.
- Simplification applies to architecture, feature count, and unnecessary engineering; it does not mean a rough, outdated, or scientifically incomplete UI.
- The UI should hide irrelevant technical complexity without hiding scientifically important information.

## Priority order

1. Clear and bounded research question.
2. Simple and properly validated GridWorld.
3. Small, scientifically justified set of models and uncertainty types.
4. Fair and reproducible experimental protocol.
5. Reliable and comparable results.
6. Modern complete UI for execution, monitoring, and understanding.
7. Advanced features only when there is a real need and low completion risk.

## Application scope

- Local single-user application.
- No authentication, roles, or multi-user support.
- No required public deployment, mandatory cloud, mobile application, or live public demo.
- The user must be able to execute required experiments without code or console commands.
- The dashboard must support real configuration, execution, progress, logs, GridWorld visualization, history, comparison, metrics, charts, tables, and export.
- Screenshots and real results will be used in the thesis and presentation.
- A lightweight visual/debug surface may be used early for validation; the polished final dashboard follows a functional validated independent core and pilot evidence.
- The final interface is not a minimal demo; it is a polished bounded research dashboard.

## Scope restraint

- Do not implement production infrastructure, microservices, Kubernetes, distributed workers, complex permissions, or enterprise observability.
- Queue priorities, plugin systems, remote execution, complex checkpoint UX, advanced orchestration, and AI assistance remain optional/deferred until a real need is demonstrated.
- Every feature must map to a research, reproducibility, usability, or thesis-delivery requirement.
- Prefer consolidated workflows and fewer screens rather than exposing internal architecture in the UI.

## Research and experiments

- Models, baselines, metrics, GridWorld rules, stack, hyperparameters, seeds, repetitions, and budgets are selected from zero using current evidence.
- Old chats are context, not preferences or a shortlist.
- Experimental design must remain small, understandable, executable, and easy to explain.
- The UI must not expose unjustifiably many models or settings.
- Multiple runs/settings are required where scientifically justified.
- Single-run comparison is forbidden.
- Pilot, exploratory, and final runs remain distinct.
- Failed, cancelled, interrupted, incomplete, and excluded runs are recorded.
- Pause, resume, stop, cancel, restart, and rerun are supported only where genuinely useful and technically safe.
- Resolved parameters are stored for every run.
- Figures and tables are produced from real stored data.

## GridWorld

- The project is built afresh; legacy code is not required.
- Codex performs fresh research on current libraries/frameworks and custom implementation.
- Third-party code is integrated only after source, license, maintenance, compatibility, and prototype review.
- There is no preselected GridWorld repository.
- The final solution should be the simplest one that fully supports the approved research design.

## Hardware and tooling

- Codex automatically collects CPU, RAM, GPU/VRAM, OS, drivers, runtimes, and storage.
- The user does not provide manual inventory when the system can inspect it directly.
- NVIDIA/CUDA is not assumed.
- Compute-dependent decisions follow inventory and capability benchmarks.

## Bibliography boundary

- `MariosGiannakaras/ThesisBibliography` is the canonical repository for source discovery, originals, conversion/OCR, scientific analysis, verified evidence, and source selection.
- New PDF/Markdown/NotebookLM bibliography material is processed there, not in this thesis repository.
- This repository consumes only the verified generated export under `research/bibliography/` through the controlled synchronization workflow.
- Source-derived scientific text and citation-ready evidence remain in the original language of the source.

## Repository language

- Repository-authored operational and technical material may be written in English; the user does not require Greek repository documentation.
- Codex-facing instructions, prompts, technical documentation, code comments, identifiers, filenames, branches, commits, and Pull Request text should use English for consistency.
- Preserve exact official Greek text when it must be quoted faithfully.
- The final thesis itself remains Greek unless official guidance changes.

## Thesis and repository

- The thesis is written in Greek.
- The final deliverable is Microsoft Word.
- Current official instructions override historical examples.
- This repository remains private and is the source of truth for thesis context, code, experiments, results, writing, and presentation, with the explicit bibliography boundary above.
- The official application is stored unchanged in the private repository.
- Raw chat exports are not committed.
- Fabricated citations, data, results, and conclusions are forbidden.

## Optional AI

- Add an AI feature only if measurable practical value is demonstrated.
- It must not alter experimental data, replace statistics, or present hypotheses as facts.