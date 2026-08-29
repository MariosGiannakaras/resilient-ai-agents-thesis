# Codex Execution Prompt

## User entrypoint

Give Codex only:

> `/goal Read docs/context/CODEX_EXECUTION_PROMPT.md and execute it completely. Recover the actual repository/Git/GitHub/evidence state first, then complete the canonical project task registry autonomously one bounded dependency-valid task or coherent package at a time. Treat routine Git, PR/CI/objective review, corrections, task reconciliation and next-task selection as work to perform, not reasons to stop. Never bypass BLOCKED/DEFERRED/SUPERSEDED work, fabricate evidence, cross an external approval gate or create a parallel branch when the active package pins one.`

Repository/Git/GitHub/evidence state beats stale chat/session memory or stale prose.

## Active package

DEC-048/050 protocol-v2 methodology, DEC-051 study-first backend reconstruction and issue #95 supersede future execution of the unfrozen protocol-v1.1 candidate.

- Use `feat/pre-wp7-protocol-v1.1-ui-rebuild` / draft PR #92 until explicitly superseded; do not create a parallel main-repo implementation branch or merge the draft early.
- Preserve protocol-v1.0, FINAL-* and historical R0 evidence immutably.
- Candidate v1.1 remains auditable non-final history; **do not execute old T-522 or inspect/generate its final reserve**.
- `T-524`, `T-525` and `T-529` are COMPLETE.
- Current dependency-valid scientific gate: **`T-526` READY**, requiring the predeclared physical Windows feasibility run.
- `T-527` is BLOCKED on T-526. Final methods/layouts/budgets/hyperparameters/severities/roots/statistics remain unfrozen.
- #93 / T-528 is PAUSED/BLOCKED on T-527. Its T-529 backend dependency is satisfied, but no final frontend is selected or implemented yet; the final framework must differ from NiceGUI.
- Final standalone Windows packaging is post-thesis #94 / T-803.
- `T-511` remains a later explicit intended-user acceptance gate; `T-700+` remains blocked until all science/application gates and explicit user approval.

## Startup / recovery

Before modifying anything:

1. Inspect `git status`, staged/unstaged/untracked work, branch, recent local commits, upstream/ahead-behind state and current remote head.
2. Inspect PR #92 and current-head GitHub CI/check state.
3. Read only the session-start core:
   - `AGENTS.md`
   - `docs/context/TASKS.md`
   - `docs/context/CURRENT_STATUS.md`
4. Resume valid unfinished local work before selecting a new READY task.
5. Preserve interrupted work; never use destructive cleanup merely to obtain a clean tree.
6. Read task-specific decisions/research only when the recovered active task requires them.

If repository prose disagrees with objective Git/GitHub/finalized-evidence state, recover the real state first, preserve completed work, then reconcile the docs at the next coherent checkpoint. Never rerun completed work solely because a resume note is stale.

## Current T-526 physical-machine boundary

T-526 must execute only on the validated physical Windows thesis machine through:

`powershell -ExecutionPolicy Bypass -File .\scripts\run_protocol_v2_feasibility_windows.ps1`

The latest physical attempt did **not** execute the scientific runner because mandatory repository preflight failed. The reported checkout was stale and contained an untracked prior PR draft `temp_body.md`; no T-526 output directory or scientific evidence was produced.

Before retrying the one-time pilot:

1. inspect `temp_body.md` and preserve any unique work; if confirmed obsolete, remove it from the repository working tree;
2. fetch and fast-forward the physical `feat/pre-wp7-protocol-v1.1-ui-rebuild` checkout to the reviewed current remote head without destructive reset/force operations;
3. verify native-Windows Git status is clean and the committed T-526 plan/runbook/entrypoint are present;
4. only then execute the predeclared runner exactly once;
5. retain all produced scientific failures and evidence as-is; never replace roots based on outcomes.

Do not independently rerun T-526 in hosted CI/WSL/another machine. Hosted CI is only a repository/conformance guard and cannot substitute for physical runtime evidence.

## Protocol-v2 scientific contract

The thesis compares resilient RL agents under uncertainty/change. GridWorld is the controlled experimental/visualization testbed, not the thesis subject.

### Phase A — nominal learning

Retained methods train independently from method-appropriate fresh initialization under the same semantic environment, agent-visible information, action/reward contract and main **actual environment-interaction/timestep budget**. Do not force equal episode counts, optimizer updates or universal hyperparameters.

Use periodic standardized isolated no-learning evaluation checkpoints so exploratory/stochastic training returns are not treated as directly comparable policy quality.

### Phase B — resilience/adaptation

For each retained method/root/layout, start from that unit's own exact Phase-A scientific checkpoint. Any common pre-change prefix is no-learning. At the exact boundary clone the branch-point scientific state into:

- **FN — Frozen nominal**;
- **FD — Frozen disturbed**;
- **AN — Adaptive nominal**;
- **AD — Adaptive disturbed**.

Adaptive learning begins only on the first post-boundary transition. Frozen learning state cannot mutate. Do not reset learning rate, exploration, replay, optimizer, warm-up, target-network, model, recency, counters, schedules or RNG state at the change boundary unless a later frozen protocol explicitly defines such an intervention.

The primary adaptation-benefit estimand is the matched four-branch difference-in-differences. Root/run is the independent unit; layouts/checkpoints/episodes are blocked/repeated measurements, not independent replicates. Scientific failures are retained and seeds are never replaced based on outcomes.

### Candidate method roles — pilot-gated

Strong core candidates: **Q-Learning, SARSA, DQN, PPO, Dyna-Q+**.

**Dyna-Q** is a targeted planning-vs-recency ablation, not an automatic full final arm. **A2C is conditional/pilot-gated** and is promoted only if non-final evidence establishes distinct scientific value beyond PPO at acceptable matrix/runtime cost. Random is a supporting calibration/reference policy, not a ranked learning method.

Use maintained deep-RL library adapters where scientifically appropriate; do not reimplement DQN/PPO merely for ownership. The project wrapper preserves provenance, RNG, checkpoint and information boundaries.

## Completed T-529 backend authority

DEC-051/T-529 makes `Study`, not one run or UI session, the application-facing aggregate.

The implemented framework-neutral chain is:

> immutable recipe -> deterministic study plan -> Phase-A scientific jobs/checkpoints -> optional common no-learning prefix -> atomic FN/FD/AN/AD Phase-B jobs -> validation -> root/layout analysis -> deterministic evidence export

Key invariants:

- stable recipe/plan/job identities and exact Phase-A producer dependencies;
- durable restart-safe `StudyStore`/`StudyService`;
- method-native exact scientific checkpoints;
- scientific vs infrastructure failures remain distinct;
- scientific failures and downstream skips remain attributable;
- explicit planned/observed/failure/skipped denominators;
- deterministic machine-readable CSV/JSON/result-ID/provenance handoff;
- no final frontend logic in scientific orchestration;
- no thesis prose, final thesis figures or PPTX generation at T-529.

Do not re-audit or rebuild T-529 without new objective evidence of a regression.

## Fairness / environment / statistics

- Bounded method-specific tuning uses predeclared literature-backed ranges, tuning-only roots/partitions, equivalent fixed opportunity and a frozen selection metric/tie rule. Seeds are randomization units, never tunable parameters; library defaults are not automatically fair.
- Pilot a small **ordered** set of project-owned GridWorld complexity levels. Predeclare the discrimination rule and retain the simplest level that is not universally trivial or universally unsolved, supports the uncertainty contract and remains CPU-feasible. Do not choose a level because it favors a method.
- Persistent action remapping is the primary adaptation claim. Action-execution failure is a stochastic actuation-robustness diagnostic; observation corruption is a perceptual-uncertainty diagnostic. Do not pool them into one undifferentiated claim.
- Phase-B primary components are immediate degradation, cumulative deficit versus matched same-regime nominal reference and terminal performance/gap. Recovery remains secondary/sensitivity; no composite resilience score.
- Use paired root-level comparisons where common randomness is valid, effect sizes and 95% intervals, and only predeclared primary contrasts. If p-values are used, multiplicity handling must be frozen first.
- Final methods, environment, roots, budgets and contrasts freeze only from non-final variance/precision/runtime evidence before final access. Historical v1.0/v1.1 evidence is reported separately and never numerically pooled into v2 confirmatory estimates.

## Task order

Current dependency chain:

`T-526 physical feasibility/severity/runtime evidence -> T-527 fair tuning/statistics/protocol-v2 freeze -> T-528 new-framework final UI -> T-511 intended-user acceptance -> T-610..T-613 final v2 evidence -> explicit user approval -> WP7`.

`T-529` is already complete and remains a satisfied dependency throughout the later chain.

Do not use hosted CI as a substitute for T-526's required physical-machine runtime evidence.

## Validation and Git

For each bounded scope, validate dependencies/acceptance, implement the smallest complete solution, run the smallest relevant deterministic checks, inspect the diff, reconcile docs/issues and push coherent recoverable checkpoints.

Testing is proportional: information boundaries, determinism, serialization/checkpoint fidelity, configuration, statistical known answers, lifecycle/provenance and representative integration. Scientific pilot/final matrices are not CI tests. PR CI is the canonical full-repository guard.

Do not submit an `APPROVE` review on your own PR. This active package remains draft/unmerged until its integration gates allow it.

Report `Project: X/Y` only from a real canonical finite denominator. In-progress/failed work never counts as complete.

## Stop conditions

Continue repository reading, implementation, routine Git/GitHub, CI diagnosis, objective review, reconciliation and dependency-valid next-task selection autonomously. Stop only when the next valid action genuinely requires unavailable physical-machine evidence, access/credentials, a safety/privacy/legal/licensing boundary, a user-reserved subjective choice, mandatory intended-user/supervisor acceptance or the explicit pre-WP7 approval gate.