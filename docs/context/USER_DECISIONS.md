# User Decisions

This file contains explicit current user decisions. Old conversations do not create decisions by themselves.

## Overall project direction

- The primary goal is a correct, completable, and scientifically adequate thesis.
- The application is not the main research contribution and must not become a production-grade platform.
- The application remains an important deliverable and must be polished, modern, consistent, and easy to use.
- Simplification applies to architecture, feature count, and unnecessary engineering; it does not mean a rough or scientifically incomplete UI.
- The UI should hide irrelevant technical complexity without hiding scientifically important information.
- The repository covers the complete thesis lifecycle: research context, program/application, experiments, results, analysis artifacts, thesis writing, and final deliverables, with bibliography lifecycle ownership as the explicit external-repository exception.

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
- The final interface is a polished bounded research dashboard, not a minimal demo.

## Scope restraint

- Do not implement production infrastructure, microservices, Kubernetes, distributed workers, complex permissions, or enterprise observability.
- Queue priorities, plugin systems, remote execution, complex checkpoint UX, advanced orchestration, and AI assistance remain optional/deferred until a real need is demonstrated.
- Every feature must map to a research, reproducibility, usability, or thesis-delivery requirement.
- Prefer consolidated workflows and fewer screens rather than exposing internal architecture in the UI.

## Research and experiments

- Models, baselines, metrics, GridWorld scientific rules, hyperparameters, seeds, repetitions, severities, and budgets are selected from current evidence/pilots rather than historical chats.
- Old chats are context, not preferences or a shortlist.
- Experimental design must remain small, understandable, executable, and easy to explain.
- The UI must not expose unjustifiably many models or settings.
- Single-run comparison is forbidden.
- Development, tuning, pilot/exploratory, and final runs remain separated.
- Failed, cancelled, interrupted, incomplete, invalid, and excluded runs are recorded.
- Pause/resume/stop/cancel/restart are supported only where genuinely useful and technically safe.
- Resolved parameters and provenance are stored for every experiment.
- Figures and tables are produced from real stored data.

## Experiment Git automation and storage

- A run ID represents one **whole experiment**, potentially containing many seeds/episodes.
- Intermediate data may be persisted continuously, but there must not be one permanent Git commit per seed or episode.
- When an entire experiment finalizes correctly, the system should automatically create one complete, informative Git commit and push for that experiment.
- The user should not have to stage, commit, move, or upload routine experiment data manually.
- Commit/push messages must contain useful experiment identity/provenance rather than generic text.
- Prefer fewer meaningful commits; coherent implementation PRs should normally reach `main` as one squash merge when branch tooling generated many mechanical commits.
- Useful large thesis-produced result files should also be retained when storage permits.
- Git LFS may be used automatically for appropriate large result/artifact formats.
- Do not discard useful result data merely to avoid large files unless a real storage/LFS limit requires a deliberate retention change.

## GridWorld

- The project is built afresh; legacy code is not required.
- Current technical research compares suitable libraries/frameworks with a project-owned minimal implementation.
- Third-party code is integrated only after source, license, maintenance, compatibility, and prototype review.
- There is no legacy preselected GridWorld repository.
- The final solution should be the simplest one that fully supports the approved research design.

## Hardware and tooling

- Codex automatically collects CPU, RAM, GPU/VRAM, OS, drivers, runtimes, and storage from the real execution machine.
- The user does not manually transcribe information the system can inspect.
- NVIDIA/CUDA is not assumed.
- Compute-dependent decisions follow accepted inventory/capability evidence.
- The accepted current technical baseline is Python 3.12 + `uv`/lockfile + the importable `src/resilient_agents/` research core architecture defined by DEC-023.

## Bibliography boundary

- `MariosGiannakaras/ThesisBibliography` is the canonical repository for source discovery, originals, conversion/OCR, scientific analysis, verified evidence, and source selection.
- New PDF/Markdown/NotebookLM bibliography material is processed there, not in this thesis repository.
- This repository consumes the verified generated complete corpus under `research/bibliography/` through controlled immutable synchronization.
- The nested citation-ready layer is the formal citation surface.
- Source-derived scientific text and citation-ready evidence remain in the original language of the source.

## Repository language

- Repository-authored operational and technical material is written in English for consistency with Codex, code, APIs, tests, and technical documentation.
- Preserve exact official Greek text where required.
- Scientific source-derived text/evidence stays in its original language.
- The final thesis itself remains Greek unless official guidance changes.

## Documentation consistency

- When a material implementation, architecture, status, workflow, research, storage, or protocol decision changes, all related active files must be updated in the same change.
- Do not leave old active prompts/status files to be corrected later.
- Delete obsolete files when they are no longer useful; preserve old records only when they have historical value and mark them clearly as historical.
- The current Codex execution prompt must be kept synchronized with the repository state.
- Automated checks should enforce consistency where stale states can be detected mechanically.

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
