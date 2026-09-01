# Codex Execution Prompt

## User entrypoint

For ordinary repository continuation, Codex should recover current repository state and follow the canonical authority rather than a historical chat/session:

> Read `AGENTS.md`, `docs/context/TASKS.md`, and `docs/context/CURRENT_STATUS.md` first. Inspect actual Git/GitHub/CI state, then execute only the current dependency-valid work. Historical protocol-v1.x, old UI branches and superseded prompts are context only. Never cross an explicit scientific/user approval gate.

Repository/Git/GitHub/evidence state beats stale session memory or stale prose.

## Current package

The protocol-v2.1 scientific design and pre-final readiness hardening are complete. DEC-058 remains immutable historical protocol-v2.0 freeze authority; DEC-060 plus `configs/protocols/protocol-v2.1-final.json` are current pre-execution authority.

Current facts:

- retained methods: Q-Learning, SARSA, DQN, PPO and Dyna-Q+;
- final protocol dimensions/configurations/statistics are frozen;
- the framework-neutral Study backend and deterministic evidence pipeline are implemented;
- protocol-v2.1 temporal/recovery/direct-comparison evidence contracts are implemented;
- the generic Study service denies confirmatory/final execution unless the separate explicit authorization token is supplied;
- final reserve remains sealed and no protocol-v2.1 final outcome has been generated or inspected;
- PySide6 / Qt 6 Widgets is the current application architecture under DEC-059;
- the paused/pre-v2.1 UI implementation is not an implementation base for continuation;
- final standalone Windows packaging remains deferred until after the thesis.

## Startup / resume

1. Inspect `git status`, branch, recent commits, upstream/ahead-behind state and current PR/check state.
2. Read exactly the session-start core:
   - `AGENTS.md`
   - `docs/context/TASKS.md`
   - `docs/context/CURRENT_STATUS.md`
3. Resume valid current work from objective Git state; never recreate completed work because an old note says it is incomplete.
4. Read only task-specific decisions/specifications needed for the recovered task.
5. Preserve unique interrupted work; do not use destructive cleanup merely to obtain a clean tree.

## Clean UI restart

When the active goal is the application rebuild/restart:

1. start from a **fresh branch from current `main`**; do not continue an old paused UI branch/worktree;
2. additionally read:
   - `docs/decisions/DEC-059_PYSIDE6_FINAL_APPLICATION_ARCHITECTURE.md`
   - `docs/decisions/DEC-060_PROTOCOL_V2_1_RECOVERY_AND_COMPARISON_AMENDMENT.md`
   - `configs/protocols/protocol-v2.1-final.json`
   - `docs/research/RQ_EVIDENCE_TRACEABILITY.md`
   - relevant `docs/architecture/` UI guidance;
3. audit `src/resilient_agents/desktop/` before editing:
   - preserve current UI-neutral read-model, Study/evidence adapter, provenance and execution-policy contracts;
   - presentation widgets/windows/pages/styles may be replaced from scratch;
4. derive UI behavior from current Study/evidence contracts, not pre-v2.1 assumptions or historical screenshots;
5. use only DEVELOPMENT/synthetic fixtures for implementation tests/screenshots unless real evidence has already been separately validated and is read-only;
6. never calculate scientific thresholds, root reductions, estimands or conclusions inside Qt presentation code;
7. never access or authorize the final reserve from the UI.

The UI should be novice-first, self-explanatory, compact and coherent. Primary labels are plain language; technical IDs/provenance use progressive disclosure. Empty/loading/disabled/warning/error/locked states must explain the useful next action. Motion must not fabricate progress/data.

## Scientific contract that UI/backend work must preserve

- Phase A independently trains each retained method under the common semantic task/information contract and actual-environment-interaction fairness budget.
- Phase B branches exact scientific state into FN/FD/AN/AD; Frozen state cannot learn and Adaptive learning follows the frozen method-native contract.
- Root is the independent unit; layouts/episodes/probes/windows are repeated observations.
- RQ2 primary adaptation benefit is `(FN-FD)-(AN-AD)`.
- RQ3 uses AN versus AD passive 32-interaction reward windows over horizon 256, primary tolerance 0.10, sensitivity 0.05/0.20, two-window stable recovery and right-censoring with `recovery_time=null` for non-recovery.
- Direct method contrasts are root-paired on common roots after equal layout reduction.
- Pointwise Student-t intervals use the predeclared critical value for the actual independent-root count.
- Scientific failures remain outcomes; seeds/roots are not replaced from outcomes.

## Final-experiment gate

The final scientific experiment is **not authorized** by repository cleanup, UI implementation, CI, screenshots, synthetic smoke or completion of pre-final work.

Do not:

- enable `final_reserve_access`;
- inspect final outcomes;
- run the final protocol-v2.1 matrix;
- tune from final roots/layouts/seeds;
- begin Results/Discussion writing.

Stop at the separate explicit authorization gate if final execution becomes the next scientific action.

## Validation and Git

For each bounded scope:

1. implement the smallest complete solution;
2. run targeted deterministic checks during development;
3. inspect the diff and reconcile affected active docs/tests/workflows;
4. use PR CI as the canonical full-repository guard;
5. fix actual failures narrowly rather than expanding test scope for reassurance;
6. normally squash-merge one coherent validated PR.

Do not submit an `APPROVE` review on your own PR. Do not create parallel implementation branches for the same active package.

## Stop conditions

Continue routine Git/GitHub, implementation, CI diagnosis, objective review and documentation reconciliation autonomously. Stop only when the next action genuinely requires an explicit user/supervisor/external-machine/scientific authorization or another non-resolvable external boundary.
