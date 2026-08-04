# User Decisions

This file contains explicit current user decisions. Old conversations do not create decisions by themselves.

## Overall project direction

- The primary goal is a correct, completable, and scientifically adequate thesis.
- The application is not the main research contribution and must not become a production-grade platform.
- The application remains an important deliverable and must be polished, modern, consistent, and easy to use.
- Simplification applies to architecture, feature count, and unnecessary engineering; it does not mean a rough or scientifically incomplete UI.
- The UI should hide irrelevant technical complexity without hiding scientifically important information.
- The repository covers the complete thesis lifecycle: research context, program/application, experiments, results, analysis artifacts, thesis writing, defense presentation, and final deliverables, with bibliography lifecycle ownership as the explicit external-repository exception.

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
- Application completion means the intended real user workflow is validated end to end, not merely that the UI renders.

## Self-explanatory UI and onboarding

- The final UI should be understandable without separate training or a manual for the normal workflow.
- Use clear human-readable labels, helper text, visible units, accurate messages and consistent terminology throughout the application.
- Non-obvious scientific/technical concepts and controls should have concise tooltips; longer explanations should use contextual help/popovers or expandable detail rather than cluttering the primary screen.
- Statuses, warnings, errors and validation states should use understandable text together with consistent symbols/icons and semantic visual treatment.
- Colors must be purposeful, consistent and accessible; color alone must never carry essential meaning.
- Empty/loading/disabled/error states should explain what is happening, why an action/content is unavailable when non-obvious, and what the user can do next.
- Before launch, show a clear summary of the resolved experiment configuration, protocol, run count and blocking validation issues so the user understands what will actually execute.
- Use confirmations only for destructive/high-impact actions where accidental activation matters; avoid unnecessary confirmation friction elsewhere.
- Show a clear next recommended action at important workflow boundaries where one objectively exists.
- After the final dashboard structure is stable, add a short first-run onboarding/tutorial for the essential application flow with Previous, Next, Skip and Finish controls and a Help/Getting Started option to replay it later.
- The onboarding must be lightweight, skippable and non-blocking, with only a local completion/preference flag; it must not require accounts or a new persistence subsystem.
- Prefer native/lightweight Streamlit UI/state/dialog/popover mechanisms. Do not introduce a heavyweight custom JavaScript/DOM coach-mark framework only for onboarding unless the completed dashboard demonstrates a real need that cannot be satisfied simply.

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
- The normal final experiment campaign begins only after both the final protocol and intended user-facing application workflow are validated.
- A headless fallback may exist for reliability, but it must use the same scientific core/configuration path and be explicitly documented if used for final work.

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

## Codex task continuity and quota interruptions

- Maintain one canonical task registry with checkboxes/stable task IDs so required work cannot be forgotten across the long thesis lifecycle.
- Every Codex session must pass through the task registry before selecting or resuming work.
- Codex should use its available session/conversation memory to remember where it left off; the task registry and Git/repository state supplement that memory and provide recovery when the session/model quota ends.
- If a task has started but is unfinished, preserve exactly where it stopped: active branch/PR, last validated point, tests, relevant changed files, and exact next action.
- If model quota ends abruptly, the next session must inspect existing branch commits, working-tree diff, PR/test state, and the registry before assuming the task needs to restart.
- Use intermediate branch checkpoint commits where useful for recovery, while still preferring one coherent squash commit in `main` per completed implementation PR.
- Newly discovered required work must be added to the canonical registry rather than being left only in chat or informal notes.
- The user should not have to manually remember or reconstruct unfinished Codex work between quota windows.
- A task marked `READY` must actually have its required task dependencies complete; future dependency-blocked tasks are not labelled ready just because they are planned.

## Testing effort and model quota

- Testing must be risk-based and proportional; it must not become a parallel project that consumes more implementation time or model quota without meaningful risk reduction.
- During implementation, Codex should run the smallest relevant targeted tests rather than the full suite after every small edit.
- Add tests for task acceptance conditions, scientific invariants, critical reliability/security boundaries, and concrete regressions likely to recur.
- Prefer a small number of strong known-answer, contract, invariant, or representative integration tests over many near-duplicate cases.
- Do not pursue a coverage percentage for its own sake.
- Do not add mutation testing, broad fuzz/property testing, exhaustive parameter combinations, snapshot proliferation, or large end-to-end matrices unless a concrete task-specific risk justifies them.
- CI uses tiny deterministic fixtures/smoke runs; pilot and final experiment matrices are not tests.
- Run the full repository checks when work is ready for review and rerun them only after a later change that could affect the result.
- Stop adding tests when the acceptance condition and material risks are covered.

## End-to-end lifecycle and user journey

- The repository workflow must continue reliably beyond application implementation through final experiments, statistical analysis, thesis writing/review, defense presentation, and final delivery.
- `TASKS.md` remains the concrete execution checklist; `IMPLEMENTATION_ROADMAP.md` and `EXECUTION_WORKFLOW.md` explain the phase order, responsibilities and handoffs without duplicating task status.
- After final runs and analysis, create a frozen thesis/defense evidence package mapping research questions, protocol/method references, citation-ready sources, result/run IDs, figures/tables, captions, and planned claims.
- Thesis and presentation work should consume that frozen evidence package rather than reconstructing conclusions later from raw results or memory.
- The user should not manage routine Git, result-file movement, provenance, task state, analysis regeneration, or presentation evidence mapping.
- The user's later responsibilities are mainly academic/product choices, providing/relaying supervisor or official guidance, reviewing scientific interpretation/thesis wording, and rehearsing the defense.

## Thesis writing and review

- The thesis is written in Greek and final delivery is Microsoft Word unless official guidance changes.
- Current official instructions override historical examples.
- Normal chapter drafting/final styling occur after evidence-producing research is mature and the final evidence package exists.
- A review-ready Word thesis should be produced before final freeze.
- Supervisor/reviewer corrections received later must be incorporated through an explicit revision cycle; affected citations, figures, tables, result claims, and methodology descriptions must be revalidated.
- Final thesis claims use only citation-ready bibliography evidence and frozen experiment evidence as appropriate.

## Defense presentation

- After the thesis is stable/finalized, create a complete PowerPoint presentation for the examination/defense.
- The presentation must contain the necessary thesis context, methodology, experiments, main results, conclusions, limitations, and appropriate application/demo material without becoming a chapter-by-chapter copy of the thesis.
- The final defense package must include a `.pptx`, embedded speaker notes, and a separate full spoken Greek script detailed enough to follow/read during rehearsal or presentation preparation.
- The presentation must remain traceable to the final thesis, citation-ready bibliography, frozen results, and repository-generated figures/screenshots.
- Speaker notes/script must be synchronized with slide order and use spoken, presentation-appropriate Greek rather than pasted thesis prose.
- Final presentation duration/content/file requirements must be rechecked from current official guidance near the defense; do not invent them now.
- Rehearsal/timing, PowerPoint rendering, legibility, factual/numerical consistency, and demo fallback must be validated before presentation freeze.
- Preferred tool split: Codex prepares/verifies repository-backed evidence, figures, tables, screenshots, evidence mappings, and reproducible assets; ChatGPT prepares/refines the slide narrative, Greek slide copy, speaker notes/full script, and consistency review; PowerPoint-capable generation tooling produces the `.pptx`; Microsoft PowerPoint is the final inspection/rehearsal surface.
- Canva or similar tools are optional visual-polish tools only. If used, the exported `.pptx` must be revalidated and presentation tooling must never become the scientific source of truth.

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
- The final thesis and expected defense-language materials remain Greek unless official guidance changes.

## Documentation consistency

- When a material implementation, architecture, status, workflow, research, storage, protocol, task-state, lifecycle-handoff, thesis, presentation, or UX decision changes, all related active files must be updated in the same change.
- Do not leave old active prompts/status/task files to be corrected later.
- Delete obsolete files when they are no longer useful; preserve old records only when they have historical value and mark them clearly as historical.
- The current Codex execution prompt, task registry, roadmap/workflow, UI architecture, and presentation workflow must be kept synchronized with repository state.
- Automated checks should enforce consistency where stale states can be detected mechanically.

## Thesis and repository

- This repository remains private and is the source of truth for thesis context, code, experiments, results, writing, defense presentation, and final deliverables, with the explicit bibliography boundary above.
- The official application is stored unchanged in the private repository.
- Raw chat exports are not committed.
- Fabricated citations, data, results, presentation claims, and conclusions are forbidden.

## Optional AI

- Add an AI feature only if measurable practical value is demonstrated.
- It must not alter experimental data, replace statistics, or present hypotheses as facts.
