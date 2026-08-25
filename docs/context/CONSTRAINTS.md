# Constraints

## Compute and hardware

- The accepted actual-machine inventory is `SYSTEM_CAPABILITY_REPORT.md` plus the generated `system-capability.accepted.json`; Codex regenerates it automatically after material host/runtime changes.
- CPU execution is the required supported baseline. The observed Radeon RX 570 is not treated as a validated scientific-compute backend; NVIDIA/CUDA tooling is absent.
- Do not assume usable ROCm, DirectML, or unlimited compute.
- Compute-dependent model/dependency/budget choices remain unfrozen until relevant prototypes and pilots establish feasibility; historical hardware references are not decision inputs.
- The final experiment matrix must remain practically executable on the measured hardware or an explicitly approved alternative.

## Accepted technical baseline

- Python 3.12 is the current execution baseline.
- Dependency/environment management uses `uv`, `pyproject.toml`, `.python-version`, and committed `uv.lock`.
- Scientific logic lives in `src/resilient_agents/` and works independently of the UI.
- Evaluator ground truth is separated from agent-visible information.
- Randomness uses independently derived deterministic streams.
- Filesystem run bundles are the evidence source of truth; any later database/index is rebuildable cache.
- A run ID represents one whole experiment and may contain many seeds/episodes.
- A finalized whole experiment uses at most one guarded automatic Git commit/push; never one permanent result commit per seed.
- The polished dashboard is a later thin local Streamlit layer unless pilot evidence justifies a different architecture.

## Execution and deployment

- Local, single-user operation.
- No required public deployment, cloud infrastructure, mobile client, multi-user authentication, or distributed orchestration.
- Normal research workflows should work offline after dependencies and required project inputs are installed.
- The user should not need routine manual Git staging/committing/pushing for experiments.

## Testing and validation budget

- Testing is risk-based and proportional to the changed behavior, task acceptance condition, and scientific/reliability impact.
- During implementation, use targeted tests; do not repeatedly run the full suite after every small edit.
- When GitHub Actions is available, PR CI is the canonical full-suite pre-merge guard. Do not run an otherwise unnecessary local full suite merely to duplicate it.
- On successful CI, record the conclusion without repeatedly reading or summarizing logs. On failure, inspect the narrowest failed step first and reproduce only what is useful.
- A local full-suite run is reserved for unavailable CI, CI/test-infrastructure changes where local reproduction is useful, or a specific failure that requires it.
- There is no coverage-percentage target.
- Mutation testing, broad fuzz/property testing, exhaustive parameter matrices, snapshot proliferation, and large end-to-end test suites are out of scope unless a concrete task-specific risk justifies them.
- CI uses tiny deterministic fixtures, known-answer cases, contracts, and representative smoke/integration paths. Pilot and final experiment matrices are never used as tests.
- Test work stops when task acceptance conditions and material risks are covered; theoretical completeness does not justify delaying implementation or consuming model quota.
- Required configuration/contracts/schema/provenance/lifecycle conditions fail closed at clear boundaries; optional unavailability must remain explicit rather than being interpreted as successful evidence.

## Dashboard UX complexity

- The normal dashboard workflow must be self-explanatory through clear labels/messages/units, concise contextual help, semantic status treatment, and actionable states rather than a separate training/manual dependency.
- Tooltips and contextual explanations must stay synchronized with actual scientific definitions and implemented behavior.
- Status meaning must not rely on color alone; text plus consistent symbols/icons and accessible semantic visual treatment are required.
- The first-run onboarding is implemented only after the final dashboard structure is stable and remains short, skippable, replayable, and locally stateful.
- Do not introduce accounts, a new persistence subsystem, or a heavyweight custom JavaScript/DOM coach-mark/tour framework merely for onboarding.
- Exact palette values, decorative motion, and similar visual details are finalized against the real implemented UI; do not create premature design-system complexity that does not improve usability.

## Research scope

- The official topic requires a simple simulated environment, comparison under uncertainty/dynamic change, resilience, and recovery speed.
- Exact research question, GridWorld scientific specification, model set, metrics, severities, seeds, budgets, hyperparameters, thresholds, and statistical protocol remain unfrozen.
- Old conversations are not shortlists/defaults.
- Every scientific selection requires current bibliography evidence, environment validity, feasibility, and/or pilot justification.
- The final matrix must remain small enough to explain and complete.

## GridWorld and third-party code

- There is no requirement to recover an old codebase.
- Third-party code is integrated only after source, license, maintenance, security, API, testability, determinism, and suitability review.
- Every dependency or copied/adapted component requires a pinned version/commit and attribution where applicable.
- A project-owned minimal Gymnasium-compatible environment remains a valid option and is preferred if it reduces total complexity without scientific loss.
- Any selected environment must use the shared contracts rather than introducing a second scientific execution interface.

## Reproducibility, results, and large files

- Every experiment requires resolved config, seeds, source Git commit, software/runtime information, and capability/provenance metadata.
- Finalized raw results are immutable and checksummed.
- Failures, cancellations, interruptions, invalid runs, and exclusions are retained with reasons.
- Final figures/tables are generated only through version-controlled processing from real stored data.
- Useful thesis-produced experiment outputs are retained by default, including large outputs when storage permits.
- Configured large formats use Git LFS. Do not manually discard useful evidence merely to keep Git small.
- Retention/pruning changes require an explicit decision only if real repository/LFS/storage limits become a practical problem.
- Bibliography PDFs and bibliography Git LFS objects remain upstream and are never copied into this repository.

## Lifecycle and evidence handoffs

- The normal final experiment campaign does not begin before both the final protocol and intended application workflow are validated.
- Thesis/presentation writing does not begin from ad-hoc raw final-run inspection; a frozen downstream evidence package is created after final analysis.
- Final thesis and defense materials must not silently contradict frozen evidence or citation-ready bibliography support.
- Any supervisor/reviewer correction that changes a claim, figure, table, method statement, or interpretation requires corresponding evidence/citation revalidation.

## Documentation/source-of-truth consistency

- A material change is incomplete until related active documentation, prompts, tasks, lifecycle handoffs, decisions, status, tests, and workflows are reconciled in the same PR.
- Obsolete active files are deleted; useful old records are marked historical and linked to current authority.
- Generated bibliography content is never manually edited for consistency.
- Follow `docs/context/DOCUMENTATION_GOVERNANCE.md`.

## Privacy and repository

- Repository visibility may be changed temporarily at explicit user direction for CI/Actions. Temporary public visibility is an operational choice, not a permanent public-release or redistribution decision.
- Tokens, passwords, API keys, credentials, and local secrets are forbidden in tracked content regardless of repository visibility.
- Raw conversation exports are not stored in the repository.
- Temporary CI visibility does not waive privacy, personal-data, copyright, licensing, or provenance obligations.
- Any deliberate public release/distribution requires a privacy/license/copyright audit and appropriate redaction or exclusion first.

## Academic delivery and defense

- No final deadline or verified defense schedule is currently known.
- Current final Word template/submission package remains a later verification item.
- Exact current defense duration, required content, presentation language, slide/template rules, live-demo rules, and submission procedure are not assumed; recheck them near delivery.
- The planned defense output is a PowerPoint `.pptx` plus embedded speaker notes and a separate full spoken Greek script, subject to later official requirements.
- Microsoft PowerPoint is the final rendering/rehearsal target for the `.pptx`; optional design tools must be revalidated after export.
- Supervisor-specific instructions, when actually provided, are recorded as explicit changes and override lower-level generic conventions where applicable.