# Execution and Review Workflow

## Operating model

The user provides goals, observed behavior, genuinely academic/product choices, later supervisor feedback, and private material when required. The user is not responsible for routine branches, commits, tests, PRs, CI, review corrections, merges, experiment-result Git publication, or manually remembering unfinished Codex subtasks.

ChatGPT scopes/reviews scientific and technical work and decides merge readiness. Codex executes bounded work from the actual repository state without self-approval or silent scientific scope expansion. GitHub runs repeatable checks; passing CI is necessary but not sufficient.

Normal development flow:

> goal -> task registry -> branch/PR -> CI/review -> corrections -> squash merge -> task/status update

Current supervisor identity, deadlines, and final Word formatting are not implementation blockers. Later feedback is recorded as an explicit change when received.

## Codex continuation and recovery

The tracked canonical and directly executable prompt is `docs/context/CODEX_EXECUTION_PROMPT.md`. The canonical concrete checklist/resume ledger is `docs/context/TASKS.md`; `AGENTS.md` is the project-policy authority.

After cloning/updating the repository on the thesis machine, start Codex with: `Read docs/context/CODEX_EXECUTION_PROMPT.md and execute it completely.`

At the start of every Codex session:

1. inspect Git status/current branch/recent commits, uncommitted work, and relevant PR/check state;
2. read only `AGENTS.md`, `TASKS.md`, and `CURRENT_STATUS.md` as the session-start core;
3. inspect `Resume state` and resume any `IN_PROGRESS` task first unless genuinely blocked;
4. use available session/conversation memory to understand prior work and verify it against durable repository evidence;
5. otherwise select the first dependency-valid `READY` task, never a `BLOCKED` or `DEFERRED` task;
6. read only the active task entry and its relevant task-specific active specifications/evidence, using repository search before broad reading.

The prompt is a lean bootstrap and must not duplicate the domain rules already maintained in `AGENTS.md` or task-specific specifications. Broad context/roadmap/requirements/workflow/governance/historical/generated files are read only when the active task requires them or when a cross-cutting reconciliation is explicitly underway.

`Execute it completely` means progressing one dependency-valid task or coherent work package as far as current permissions, machine, evidence, review, and scientific gates allow. It does not mean attempting the whole thesis in one session, bypassing task states, or reopening completed work.

If model quota or the session ends unexpectedly, the next session inspects branch history, working-tree diff, PR/tests, `Resume state`, and session memory if available. It does not restart the task merely because the previous chat/session ended.

Intermediate branch commits are valid recovery checkpoints. The coherent PR still normally reaches `main` through one squash merge, so quota resilience does not require noisy permanent main-branch history.

Adjacent dependency-valid tasks may share a branch/PR only when they are one coherent implementation unit and no scientific, review, user-decision, external-machine, or protocol-freeze gate separates them. Separate task IDs do not by themselves justify micro-PRs.

## Progress reporting

Codex keeps long executions understandable with concise milestone reporting rather than continuous narration.

- Report after scope is established and after meaningful completed/validated checkpoints, important gates, or a material blocker; do not report every command or tiny edit.
- Use `X/Y` only when the denominator is objectively defined. Completed/validated items count toward `X`; in-progress, failed, or merely attempted work does not.
- The canonical task registry provides the durable high-level count: `Project: X/Y` may count checked versus total `T-*` entries in `TASKS.md`.
- Also report the relevant current work package or major deliverable when useful, such as `WP5 Application: 2/4`, `Thesis: 3/6`, or `Presentation: 1/3`, using the corresponding canonical task entries rather than a second tracker.
- Add an active-task fraction such as `T-510: 3/5` only when the task has a real finite substep set. If no stable denominator exists, report a concise textual state instead of inventing one.
- Keep most updates to one progress line plus one sentence stating what just completed and what comes next. Recompute counts whenever task state changes.

## Testing and CI flow

DEC-029 and DEC-030 keep validation proportional to actual risk while making failure detection early, explicit, and inexpensive.

1. During implementation, Codex runs the smallest targeted test subset that validates the changed behavior.
2. New tests are added only for task acceptance conditions, material scientific/reliability/security boundaries, or a concrete regression likely to recur.
3. Tests use tiny deterministic fixtures, known-answer cases, contracts, or representative smoke/integration paths. Pilot and final experiment matrices are never used as CI tests.
4. There is no arbitrary coverage target and no default mutation/fuzz/property/combinatorial/snapshot expansion.
5. Before opening/updating a PR, Codex runs the documentation consistency validator and only the directly affected validators/targeted tests needed for review readiness.
6. When GitHub Actions is available, PR CI is the canonical full-suite pre-merge runner. Codex does not run the full suite locally merely to duplicate it.
7. On successful CI, record the conclusion and continue; do not tail, summarize, or repeatedly re-analyse successful logs. On failure, inspect only the failed step/log, reproduce narrowly when useful, fix the cause, and let CI rerun the complete repository checks.
8. A local full-suite run is reserved for unavailable CI, changes to CI/test infrastructure where local reproduction is useful, or debugging a specific failure.
9. Stop adding tests when the acceptance condition and material risks are covered; do not delay implementation for theoretical completeness.

The repository CI remains one bounded fail-fast job rather than a growing matrix. Cheap deterministic checks run before environment installation/tests where possible, superseded runs are cancelled, successful output is compact, and a timeout prevents a hung check from consuming unbounded Actions time. PRs always receive the complete repository validation. Pushes to `main` also receive it whenever source, config, protocol, bibliography, tests, or active documentation changes; a push that changes only generated `results/**` and/or `artifacts/**` may skip the duplicate full suite because the producing code was already validated and the publisher has its own fail-closed provenance safeguards.

Temporary public repository visibility may be used at explicit user direction to obtain public-repository GitHub Actions. Visibility is an operational CI choice, not a release decision, and does not weaken secret/privacy/copyright/licensing or final-release audits.

GitHub CI execution time is separate from model reasoning quota. The quota-sensitive waste to avoid is repeated test design, expansion, local/full-CI duplication, verbose success-log analysis, and reruns without a concrete risk or code change.

## Fail-fast implementation behavior

Required configuration, contracts, schemas, provenance, lifecycle preconditions, and scientific invariants are validated at clear boundaries before expensive work starts. Invalid or ambiguous required state fails closed with an explicit exception/error or non-zero result; it must never be converted into an empty/default value that looks successful.

Broad exception swallowing and silent fallback are forbidden for required behavior. Optional probes may return an explicit `unavailable`/`unsupported` state only when the capability is genuinely optional, and downstream logic must not treat that state as affirmative evidence. Finalization is atomic/transactional where practical so partial output cannot masquerade as a valid finalized artifact. Validation is kept out of hot inner loops when one trusted boundary check is sufficient, preserving both correctness and runtime efficiency.

## Bibliography material flow

PDFs, Markdown, NotebookLM exports, source lists, and other bibliography inputs go to `MariosGiannakaras/ThesisBibliography`. The thesis repository never writes back upstream. It receives only the committed complete research corpus through the immutable read-only PR-based synchronization contract in `docs/context/BIBLIOGRAPHY_INTEGRATION.md`.

The first complete import is already accepted. Formal citation trust remains confined to `research/bibliography/citation-ready/`; other imported content is internal research context unless promoted upstream and resynchronized.

## Application-to-final-experiment handoff

The application is not considered complete merely because the Streamlit pages render. Application completion requires the real scientific core, frozen protocol, pilot-proven management behavior, and validated user-facing configure/run/monitor/history/compare/export workflow.

The final application also has to satisfy the self-explanatory UX baseline from DEC-027 and `docs/architecture/UI_INFORMATION_ARCHITECTURE.md`: understandable labels/messages/units, accurate contextual help/tooltips, consistent text+icon+semantic-color states, actionable empty/loading/warning/error states, pre-run resolved-configuration/validation review, proportionate confirmations, and clear next actions where useful. Color must not be the only essential signal.

Onboarding is deliberately sequenced after the stable dashboard structure (`T-510 -> T-512 -> T-511`). It remains short, skippable and replayable with Previous/Next/Skip/Finish, uses lightweight local state, and must not create a new frontend/account/persistence subsystem without demonstrated need.

Only after the complete `T-511` application gate should the frozen final experiment campaign begin in the normal user journey. The final campaign uses the same validated core/configuration path as pilots; a headless fallback is allowed only when needed and explicitly documented, never as a scientifically different execution path.

## Experiment result flow

A run ID means one whole experiment and may include many seeds/episodes.

1. The experiment persists data/provenance safely while running.
2. The run bundle is finalized at the whole-experiment lifecycle boundary.
3. The guarded publisher stages only the finalized bundle and required run index/registry metadata.
4. One informative commit is created and pushed for the whole experiment.
5. No permanent commit is created per seed/episode.
6. If publication is unsafe or fails, local result data is preserved and the Git action is blocked rather than forced.
7. Configured large result/artifact formats use Git LFS; useful evidence is not manually discarded merely because it is large.

After the final campaign, all predefined runs are accounted for before the accepted final evidence set is frozen.

## Analysis-to-writing handoff

Frozen evidence is analyzed only through the version-controlled frozen analysis definitions. Final figures, tables, summaries, diagnostics, and captions are generated from that evidence.

Before normal thesis drafting, a thesis/defense evidence package is frozen. It maps research questions, protocol/method references, citation-ready sources, result/run IDs, figures/tables, and planned claims. This prevents the thesis or presentation from being reconstructed later from memory or ad-hoc raw-result browsing.

## Thesis review and defense handoff

ChatGPT is the preferred writing/restructuring/review layer for the Greek thesis, while Codex continues to own reproducible repository-backed figures, tables, evidence checks, and legitimate code/data corrections. Current official guidance is rechecked near writing/delivery.

A review-ready Word thesis is produced before final freeze. Supervisor/reviewer corrections are incorporated when they are actually received, with affected evidence/citations/figures revalidated.

After the final thesis is stable, the defense package follows `docs/thesis/PRESENTATION_WORKFLOW.md`: evidence-mapped PowerPoint, embedded speaker notes, a separate full spoken Greek script, real screenshots/demo assets, and rehearsal/timing/factual-consistency validation.

## User journey summary

The intended user workflow is deliberately small:

1. clone/update the repository on the thesis machine and start Codex from the canonical prompt;
2. answer only genuinely academic/product questions or provide new official/supervisor input when needed;
3. use the finished self-explanatory application, contextual help and optional/replayable onboarding without needing a separate usage manual;
4. once the application is validated, execute the predefined final experiment campaign through the approved UI workflow;
5. review the final scientific interpretation/analysis outputs rather than manually manipulating result files;
6. review the thesis and provide/relay supervisor feedback;
7. review and rehearse the final PowerPoint and speaking script.

Routine Git, task bookkeeping, result-file movement, provenance, analysis regeneration, and presentation evidence mapping remain automated/repository-managed.

## Documentation and task reconciliation

Every material change follows `docs/context/DOCUMENTATION_GOVERNANCE.md`. A change is not ready to merge if related active docs/status/prompts/tasks/decisions still describe the previous state.

Every material PR reviews `TASKS.md`. Starting, completing, blocking, unblocking, superseding, or discovering work must update the corresponding task and `Resume state` in the same PR when applicable.

Delete obsolete files when they have no continuing value. Preserve useful historical records only with a clear historical/superseded notice. Generated bibliography files are never hand-edited for consistency.

## Git and review rules

Use descriptive lowercase branches with `research/`, `feat/`, `fix/`, `test/`, `docs/`, or `chore/`. Branch tooling may create several mechanical/checkpoint commits, but one coherent PR should normally reach `main` as one squash commit.

Substantial PRs state task IDs, scope, rationale, validation, scientific/protocol impact, limitations, deferred work, and documentation/task reconciliation. Merge only when scope is correct, tests meaningfully cover the change, CI passes, review findings are resolved, source-of-truth docs agree, and no data/results/logs/metrics/citations/progress are fabricated.

## Current project sequence

The detailed concrete queue is maintained only in `docs/context/TASKS.md`. `IMPLEMENTATION_ROADMAP.md` explains the phase/dependency structure. This workflow records responsibilities and major handoffs without becoming a second checklist.

Structured research notes, decisions, evidence mappings, figures, captions, task progress, presentation mappings, and implementation explanations are preserved throughout so later work and thesis/defense preparation are not reconstructed from memory.