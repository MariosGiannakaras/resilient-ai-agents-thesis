# Codex Execution Prompt

## User entrypoint

Give Codex only:

> `/goal Read docs/context/CODEX_EXECUTION_PROMPT.md and execute it completely. Execute T-534, the clean protocol-v2.1 PySide6 UI rebuild, from a fresh branch created from the latest current main. Implement the DEC-061 experiment-first product model with primary surfaces Experiment / Run / Results / Evidence. Do not continue any paused/pre-v2.1 UI branch or worktree. Preserve the scientific methodology and the separate BLOCKED T-610 final-experiment authorization gate. Perform routine Git, PR creation, CI, objective diff review, corrections, documentation reconciliation, and own-PR squash merge as part of T-534 when repository policy permits.`

The previous generic entrypoint “Complete the canonical project task registry autonomously” is not the current goal. The active goal is specifically `T-534`. Repository/Git/GitHub/evidence state beats stale session memory or stale prose.

## Current package

Protocol-v2.1 scientific design and pre-final readiness hardening are complete. DEC-058 remains immutable historical protocol-v2.0 freeze authority; DEC-060 plus `configs/protocols/protocol-v2.1-final.json` are current pre-execution scientific authority.

Current facts:

- retained methods are Q-Learning, SARSA, DQN, PPO and Dyna-Q+;
- final scientific dimensions/configurations/statistics are frozen;
- Study backend, temporal/recovery/direct-comparison evidence contracts, validation, analysis and deterministic exports are implemented;
- the generic Study service denies confirmatory/final execution without the separate explicit authorization token;
- `final_reserve_access=false`; no protocol-v2.1 final outcome has been generated or inspected;
- PySide6 / Qt 6 Widgets is the application framework under DEC-059;
- DEC-061 is the current T-534 product/UX authority and supersedes DEC-059 only where the historical product model/navigation was Study/Runs/Results/Artifacts or protocol-v2.0-specific;
- historical `T-528` and `T-511` remain complete records of the previous PySide6 application/acceptance baseline;
- `T-534` is READY and is the active application task;
- `T-610` remains separately BLOCKED;
- standalone Windows packaging remains deferred until after the thesis.

## Startup / resume

1. Inspect `git status`, current branch, staged/unstaged/untracked work, recent commits, upstream/ahead-behind state, remote head, open PR and CI state. Resume valid `IN_PROGRESS` work only if it belongs to the current `T-534` branch/package.
2. Read only the session-start core:
   - `AGENTS.md`
   - `docs/context/TASKS.md`
   - `docs/context/CURRENT_STATUS.md`
3. Confirm that `T-534` is still the canonical active application task and that current work starts from latest `main`. If an old paused/pre-v2.1 UI branch/worktree exists, treat it as non-authoritative reference only.
4. Read the task-specific authorities needed for T-534: DEC-059, DEC-060, **DEC-061**, `configs/protocols/protocol-v2.1-final.json`, `docs/research/RQ_EVIDENCE_TRACEABILITY.md`, `docs/architecture/UI_INFORMATION_ARCHITECTURE.md`, and other directly relevant active UI/application docs.
5. Work on one bounded scope at a time inside one coherent T-534 implementation branch/PR.

## T-534 clean UI rebuild

Start from a fresh branch created from current `main`. Do not resume or merge the old paused UI implementation wholesale.

Audit `src/resilient_agents/desktop/` before editing:

- preserve still-correct UI-neutral Study/evidence read-model, provenance, execution-supervision and live-observer contracts;
- reuse Qt-native GridWorld drawing primitives when useful, but presentation composition may change;
- presentation windows/pages/widgets/styles/navigation may be rebuilt from scratch;
- historical screenshots/layouts are reference only;
- remove active protocol-v2.0/DEC-058/T-528 presentation assumptions;
- never move scientific configuration, RNG, checkpoint identity, estimand/recovery calculation or evidence finalization into Qt state.

### Product architecture

Implement the DEC-061 four-surface model:

1. **Experiment**
2. **Run**
3. **Results**
4. **Evidence**

Help/onboarding and technical/reproducibility information are contextual/secondary. Do not rebuild a StudyStore/job/artifact-first administrative console.

### Experiment

- Explain the scientific flow: five methods → Phase-A nominal learning → exact checkpoint → matched Phase B → disturbance → Frozen versus Adaptive → RQ1/RQ2/RQ3.
- The final Thesis experiment always contains all five retained methods. Do not expose method deselection for the final frozen experiment.
- DEVELOPMENT/Exploratory method/scope selection is allowed only where the backend supports it and remains clearly non-confirmatory.
- Frozen and Adaptive are matched Phase-B deployment regimes of the same method, not algorithms and not mutually exclusive choices.
- Keep exact roots/layouts/config IDs/checkpoint hashes/job counts under progressive technical disclosure unless needed to explain a blocker/error.

### Run

- GridWorld is the dominant live surface, not a small widget below Study-history tables.
- Phase A: one large nominal GridWorld for the current method.
- Phase B: when exact matched frames are available, two large simultaneous side-by-side panels: **Frozen — learning off** and **Adaptive — learning continues**.
- Never pair unrelated frames. If an exact matched pair is unavailable in the lossy presentation stream, show a truthful waiting/unavailable state.
- Keep a compact method-status strip so pending/running/complete/failed state across the five methods is understandable without ranking them.
- Primary live facts: method, phase, condition, interaction, intended action → executed action, reward.
- Root/layout identity, episode/environment step, true state, delivered observation, branch/regime IDs, flags/change IDs/hashes are technical details, not the main Run copy.

### Results

Organize exactly by:

- **RQ1 — Learning**
- **RQ2 — Resilience / Adaptation**
- **RQ3 — Recovery**

RQ1:
- prefer a real interaction-axis learning curve when validated stored Phase-A probe outputs support it;
- do not invent a new UI-side root/layout aggregate merely to draw a curve;
- also show stored final performance, trajectory/time-average evidence, intervals/denominators and direct method contrasts where available.

RQ2:
- primary adaptation benefit `(FN-FD)-(AN-AD)`;
- Frozen loss `FN-FD` and Adaptive loss `AN-AD` as separate supporting views;
- condition filtering, denominators, intervals and direct contrasts from stored analysis.

RQ3:
- stored AN-vs-AD recovery trajectory;
- recovered/non-recovered status;
- observed recovery time conditional on recovery;
- separately named restricted fixed-horizon recovery delay;
- right-censoring, stored sensitivities and direct contrasts when available;
- never show a right-censored non-recovery as `recovery time = 256`.

Never introduce winner/best-algorithm/significance/superiority language unsupported by the frozen analysis contract.

### Evidence

- Lead with evidence/validation/analysis/export readiness and available user-facing results/exports/thesis-ready outputs when legitimate.
- Keep Study history, artifact IDs, paths, SHA-256, producer jobs, recipe/checkpoint/result IDs and lineage available under progressive technical detail.
- Only registered backend evidence is displayed; no arbitrary filesystem browsing.

## Scientific boundary to preserve

- Phase A independently trains each retained method under the common semantic task/information contract and actual-environment-interaction fairness budget.
- Phase B branches exact scientific state into FN/FD/AN/AD.
- Frozen and Adaptive are matched regimes, not methods.
- Root is the independent unit; layouts/episodes/probes/windows are repeated observations.
- RQ2 primary adaptation benefit is `(FN-FD)-(AN-AD)`.
- RQ3 uses AN versus AD passive 32-interaction windows over horizon 256, primary tolerance 0.10, sensitivity 0.05/0.20, two-window stable recovery and right-censoring with `recovery_time=null` for non-recovery.
- Direct method contrasts are root-paired after equal layout reduction; pointwise Student-t intervals use the predeclared critical value for actual independent-root count.
- Scientific failures remain outcomes; roots/seeds are never replaced from outcomes.
- Qt presentation consumes validated stored analysis/read-model outputs. It does not recompute thresholds, root reductions, estimands, censoring, intervals or conclusions.
- Live observer events are transient/presentation-only and cannot alter actions, observations, RNG, checkpoints, timing, metrics or evidence.

Historical schema-v1 evidence remains historical and must not be silently assigned v2.1 recovery semantics.

## UX requirements

The application must be novice-first, modern, compact, information-dense without clutter and usable on ordinary laptop/desktop sizes.

Use plain-language primary labels, progressive disclosure for technical IDs/provenance, restrained contextual help, lightweight replayable/skippable onboarding, clear keyboard/focus behavior and actionable empty/loading/disabled/warning/error/locked states. Required workflow/scientific information must not exist only in tooltips. Avoid excessive permanent cards/banners/help paragraphs. Motion must never fabricate progress or data.

## Validation and Git

Use DEVELOPMENT/synthetic fixtures for implementation tests/screenshots.

Prefer targeted contract/widget/integration tests, representative workflow checks, bounded render/screenshot validation and launcher checks when affected. The representative visual set must include Phase-A large GridWorld, exact matched Phase-B Frozen/Adaptive side-by-side, RQ1/RQ2/RQ3 Results and a right-censored RQ3 state. Avoid broad redundant test proliferation without a concrete regression risk.

For each bounded scope, implement the smallest complete solution, run targeted deterministic checks, inspect the diff, reconcile affected active docs/tests/workflows, then use PR CI as the canonical full-repository guard. Fix actual failures narrowly rather than expanding test scope for reassurance.

Do not submit an `APPROVE` review on your own PR. When T-534 is coherent, repository CI is green on the exact head, and repository policy permits it, perform the routine own-PR squash merge.

Report `Project: X/Y` only from a real canonical finite denominator in `TASKS.md`. In-progress/failed work never counts as complete.

## Final-experiment gate

T-534 completion, repository cleanup, UI implementation, CI, screenshots and synthetic smoke do not authorize the final scientific experiment.

Do not enable final-reserve access, inspect final outcomes, run the final protocol-v2.1 matrix, tune from final identities or begin Results/Discussion writing. `T-610` remains BLOCKED until the separate explicit scientific authorization is supplied.

## Stop conditions

Complete T-534 autonomously through implementation, targeted validation, PR creation, CI diagnosis/correction, active-document reconciliation and own-PR squash merge when permitted. Stop after T-534 is objectively complete if the next scientific action is T-610, because that action genuinely requires separate explicit scientific authorization.
