# Current Project Status

**Date:** 2026-08-25  
**Status:** Authoritative current-state summary

Active repository files must agree with this state. Historical records may preserve earlier states only when explicitly marked historical. Documentation synchronization is governed by `docs/context/DOCUMENTATION_GOVERNANCE.md`.

## Bibliography integration

The current complete immutable bibliography import is finished and synchronized.

- Requested ref: `bibliography-integration-v3`
- Resolved checkout: `71995373ae0da64149583cae8d7a2c17e5ab1a0a`
- Complete-corpus source commit: `e46693d4201cf47c118eb61c216243f3c5798e28`
- Citation-ready source commit: `822891fb585c98dbe4464602e97998704d1609c5`
- Canonical sources: 585
- Citation-ready selected sources: 113
- Research materials: 19
- Indexed original PDFs: 281, metadata only
- Consumer-recorded corpus files: 1568

The immutable `bibliography-integration-v2` snapshot remains historical and unchanged. Read access succeeded for the v3 synchronization. All upstream validators, both upstream checksum manifests, consumer integrity, contextual source-reference validation, and the full thesis repository test suite passed before the synchronized branch was published. The former HTTP 401 and incomplete-import blockers remain resolved. No bibliography PDF, structured original, or bibliography Git LFS object entered this repository.

## Research implementation architecture

DEC-023 establishes the implementation baseline:

- Python 3.12 + `uv` + committed lockfile;
- independent package at `src/resilient_agents/`;
- evaluator-ground-truth versus agent-visible information boundary;
- deterministic independent RNG streams;
- explicit scenario/experiment/protocol contracts without hidden scientific defaults;
- filesystem-first run bundles with provenance, capability snapshot, checksums, events/traces, and summary;
- one guarded automatic Git commit and push per finalized whole experiment, never per seed;
- selective Git LFS for large thesis-produced artifacts;
- useful large result artifacts retained by default while storage permits;
- future Streamlit dashboard as a thin layer only after core/pilot validation.

DEC-027 fixes the future dashboard UX baseline without implementing it early: the final interface must be self-explanatory through clear labels/messages/units, accurate tooltips/contextual help, semantic text+icon+color status treatment, actionable states and pre-run review. A short skippable/replayable first-run onboarding flow is implemented only after the final dashboard structure is stable, using lightweight/native mechanisms rather than a new frontend subsystem.

The actual target-machine inventory is still required before compute-dependent dependency/model/budget choices. The current base core remains CPU-compatible.

## Codex execution and resumable tasks

`docs/context/CODEX_EXECUTION_PROMPT.md` is the only tracked current Codex prompt and is directly executable from the repository.

DEC-028 optimizes that prompt as a lean bootstrap rather than a duplicate policy manual. Every Codex session now starts by reading only `AGENTS.md`, `docs/context/TASKS.md`, and `docs/context/CURRENT_STATUS.md`, then reads only the task-specific active specifications/evidence required for the selected task. Broad context, roadmap, requirements, workflow, governance, historical records, and generated bibliography are not reread automatically unless the active task genuinely requires them.

DEC-029 makes testing risk-based and proportional. Codex runs targeted tests while implementing, adds tests only for task acceptance conditions/material scientific or reliability risks/concrete regressions, and uses tiny deterministic fixtures rather than experiment matrices. There is no arbitrary coverage target or unjustified mutation/fuzz/property/combinatorial/snapshot expansion.

DEC-030 makes the implementation/validation path quota-efficient and fail-fast without allowing false passes. When GitHub Actions is available, Codex uses targeted local validators/tests and treats PR CI as the canonical full-suite pre-merge guard instead of duplicating the full suite locally. Successful CI is recorded without repeated log analysis; detailed logs are opened only for failed/cancelled/ambiguous checks. Required configuration/contracts/schema/provenance/lifecycle conditions fail closed at clear boundaries before expensive work, optional unavailable capabilities remain explicit rather than looking successful, and finalization is atomic/transactional where practical. Adjacent dependency-valid tasks may share a coherent branch/PR only when no scientific/review/user/external-machine/protocol gate separates them.

The repository CI remains a single bounded job. Superseded runs are cancelled, a hard timeout prevents runaway use, cheap deterministic preflight checks execute before dependency installation/tests where practical, and successful test/checksum/JSON output is compact while failures retain specific diagnostics. Push-to-`main` verification remains as a safety guard; Codex does not spend model quota re-analysing a successful post-merge repeat.

`docs/context/TASKS.md` remains the canonical concrete task checklist and resume ledger. Codex uses available session/conversation memory together with durable Git/repository evidence. If a session ends because of model quota or another interruption, the next session resumes from any `IN_PROGRESS` task, branch/commits, working-tree diff, PR state, tests, and the registry rather than restarting from chat memory.

The phrase `execute it completely` is explicitly bounded: Codex advances one dependency-valid task/coherent work package at a time and never interprets the instruction as permission to attempt the entire thesis in one session, bypass blocked/deferred work, or ignore review/external-machine/scientific gates.

Intermediate branch commits are allowed as recovery checkpoints; coherent work still normally reaches `main` through one squash merge.

After cloning/updating the repository on the thesis machine, the user only needs to tell Codex: `Read docs/context/CODEX_EXECUTION_PROMPT.md and execute it completely.`

Every material change must reconcile all affected active docs/prompts/tasks/status/decision/workflow files in the same PR. CI validates the lean three-file startup core, bounded execution wording, task/resume invariants, mechanically detectable stale states, and invalid `READY` task dependencies.

## End-to-end lifecycle

DEC-026 defines the complete handoff chain from implementation through final defense. The detailed phase order lives in `IMPLEMENTATION_ROADMAP.md`; execution responsibilities and handoffs live in `EXECUTION_WORKFLOW.md`; concrete status/dependencies live only in `TASKS.md`.

The normal sequence is:

> validated research core/pilots -> frozen protocol -> validated application -> final experiment campaign -> frozen evidence/analysis -> thesis evidence package -> Greek thesis/review/final freeze -> PowerPoint defense package -> final audit/delivery

The application is considered complete only when the intended user-facing configure/run/monitor/history/compare/export workflow and the confirmed self-explanatory UX/onboarding acceptance criteria are validated on the same scientific core. The frozen final experiment campaign then follows that validated workflow.

After final analysis, a dedicated evidence package must be frozen before normal thesis drafting so result/method claims, figures/tables, run IDs, protocol identity, and citation-ready sources are already mapped.

The defense workflow is already defined but remains deferred: after the final thesis is stable it will produce a final `.pptx`, embedded speaker notes, a separate full spoken Greek script, traceable presentation assets/evidence mapping, and rehearsal/PowerPoint/demo-fallback validation according to `docs/thesis/PRESENTATION_WORKFLOW.md`.

## Trust model

`research/bibliography/citation-ready/` is the strict formal-citation layer. The complete corpus remains searchable for internal research, terminology, synthesis, rejected/theory-only context, `MAT-*` material, and notes without silent promotion. Promotion is performed only upstream in `ThesisBibliography`, followed by a new immutable synchronization.

## Active bounded work

The canonical concrete queue is `docs/context/TASKS.md`. Its current first gate is the target-system inventory on the actual thesis experiment machine (`T-100`), followed by the dependency-gated GridWorld/research/metrics/agent/pilot/application/final-evidence work recorded there.

The final research question, hypotheses, model set, GridWorld scientific parameters, uncertainty severities, seeds, budgets, hyperparameters, recovery threshold, and statistical plan remain unfrozen.

## Deferred, non-blocking inputs

Supervisor identity, future supervisor corrections, final deadlines, example theses, Word formatting, and exact defense duration/submission rules remain later-stage inputs and do not block current research or implementation. They are rechecked/incorporated at the explicit writing/defense tasks rather than guessed now.
