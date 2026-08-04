# Constraints

## Compute and hardware

- Actual hardware/software inventory is not a user-supplied blocker. Codex must collect it automatically from the **actual thesis experiment machine**.
- Until that inventory and any required capability benchmarks are accepted, compute-dependent model/dependency/budget choices remain CPU-compatible and unfrozen.
- Do not assume NVIDIA, CUDA, usable ROCm, or unlimited compute.
- Historical hardware references are not decision inputs until verified on the real system.
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

- The repository remains private while it contains the unredacted official application/personal academic information.
- Tokens, passwords, API keys, credentials, and local secrets are forbidden in tracked content.
- Raw conversation exports are not stored in the repository.
- Any public release requires privacy/license audit and redaction first.

## Academic delivery and defense

- No final deadline or verified defense schedule is currently known.
- Current final Word template/submission package remains a later verification item.
- Exact current defense duration, required content, presentation language, slide/template rules, live-demo rules, and submission procedure are not assumed; recheck them near delivery.
- The planned defense output is a PowerPoint `.pptx` plus embedded speaker notes and a separate full spoken Greek script, subject to later official requirements.
- Microsoft PowerPoint is the final rendering/rehearsal target for the `.pptx`; optional design tools must be revalidated after export.
- Supervisor-specific instructions, when actually provided, are recorded as explicit changes and override lower-level generic conventions where applicable.
