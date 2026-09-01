# Implementation Roadmap

The roadmap is phase-gated for thesis completion, scientific adequacy, reproducibility and bounded engineering. `TASKS.md` is the concrete task/status/resume registry and always wins on exact current state.

## Completed foundation

The following baseline is implemented/validated and remains reusable:

1. Project/bibliography ownership, immutable generated corpus consumer and provenance.
2. Actual-machine capability inventory; Python 3.12 + locked `uv` environment.
3. Source-traceable research framing and project-owned Gymnasium GridWorld with deterministic information/RNG contracts.
4. Historical resilience/degradation/recovery metrics and known-answer fixtures.
5. Historical F0/C0/R0 implementation, pilots, headless runner and reproducible analysis.
6. Immutable `protocol-v1.0` final evidence and historical thesis-final artifact package.
7. Canonical Codex task registry, documentation governance and interruption recovery.
8. Protocol-v2 scientific execution foundation for Q-Learning, SARSA, DQN, PPO and Dyna-Q+ with exact scientific state/checkpoint semantics.

Historical v1.0 and candidate-v1.1 evidence remain auditable; current work does not retroactively rewrite them.

## Current pre-WP7 path

### Phase V2-1 — Protocol-v2 scientific contract — COMPLETE (`T-524`)

DEC-048/050 freeze the methodology boundary required before implementation/pilots:

- independent Phase-A learning per method/root/layout;
- common semantic task/information/reward/gamma contract;
- principal actual environment-interaction learning budget;
- standardized isolated no-learning probes;
- administrative truncation with bootstrap semantics;
- exact method-native scientific checkpoints;
- optional common no-learning prefix;
- exact FN/FD/AN/AD matched Phase-B fork;
- Adaptive updates only after the boundary;
- root/run independent unit with layout blocking;
- retained scientific failures and no best-seed replacement;
- final-reserve leakage firewall;
- no opaque composite resilience score.

### Phase V2-2 — Multimethod scientific execution foundation — COMPLETE (`T-525`)

Implemented and conformance-tested:

- Q-Learning, SARSA and Dyna-Q+ exact project-state adapters;
- Stable-Baselines3 2.9.0 DQN/PPO exact scientific-state adapters on CPU-only PyTorch 2.9.0;
- actual-interaction Phase-A drivers;
- isolated no-learning evaluation;
- checkpoint `train -> serialize -> destroy -> restore -> continue` conformance;
- DQN replay/target/optimizer/schedule/RNG persistence;
- PPO legal rollout/update checkpoint boundaries;
- exact GridWorld state/RNG fork;
- one-segment Frozen/Adaptive Phase-B branch drivers with Frozen-state mutation guards.

The validated one-segment lifecycle deliberately fails closed rather than inventing multi-episode reset semantics.

### Phase V2-3 — Study-first backend reconstruction — IN PROGRESS (`T-529`)

DEC-051 makes `Study` the final application/backend aggregate.

Current implemented slices:

1. **Study domain / durable envelope**
   - immutable content-addressed `StudyRecipe`;
   - evidence classes, stages, stable job identities and DAG dependencies;
   - durable filesystem `StudyStore`, lifecycle/events/artifact lineage and finalization boundary;
   - scientific versus infrastructure failure semantics.

2. **Deterministic planner**
   - recipe → complete Phase-A/Phase-B/postprocessing plan;
   - one Phase-B matched-set job per method × root × layout × condition;
   - exact Phase-A producer/checkpoint dependency;
   - Random reference support remains non-ranked.

3. **Real protocol-v2 execution ports**
   - Phase-A Study executor over validated Q/SARSA/DQN/PPO/Dyna-Q+ drivers;
   - exact finalized `RunBundle`, scientific checkpoint and standardized analysis record;
   - common no-learning prefix primitive;
   - atomic FN/FD/AN/AD Phase-B Study executor from one exact branch point;
   - explicit Random reference executor; unknown/oracle identities fail closed.

4. **Evidence validation / analysis**
   - planned-vs-produced artifact/checkpoint lineage validation;
   - retained scientific-failure/skipped-unit handling;
   - Phase-A final-probe and equal-grid time-average summaries;
   - matched Phase-B Frozen loss, Adaptive loss and adaptation benefit;
   - equal-weight layout blocking;
   - explicit planned/completed/scientific-failure/skipped/infrastructure denominators;
   - interval behavior supplied by the analysis recipe rather than hidden defaults.

5. **Deterministic evidence handoff**
   - method/root/condition CSV tables;
   - stable `RESULT-*` identifiers;
   - result index and evidence-handoff manifest;
   - complete lineage to the validated analysis package;
   - final figure rendering intentionally deferred until the figure/statistical recipe is frozen downstream.

6. **Framework-neutral facade**
   - restart-safe `StudyService`;
   - concrete default protocol-v2 executor registry;
   - status/list/artifact/run/retry/finalize APIs;
   - evidence-package lookup for the later frontend.

Remaining T-529 work is bounded to correctness/CI closure, active-document reconciliation and any missing framework-neutral application API needed to satisfy the acceptance contract. It may not invent T-526/T-527 scientific values.

### Phase V2-4 — Physical Windows feasibility — READY external gate (`T-526`)

Run the predeclared non-final feasibility package exactly once on the validated physical Windows thesis machine:

- ordered GridWorld complexity discrimination;
- three explicit roots;
- five core methods;
- common actual interaction budget and standardized probes;
- CPU/wall/checkpoint/failure evidence;
- then only the already-predeclared Phase-B severity candidates after level selection.

Hosted CI cannot substitute for this gate. Poor/failing outcomes are retained. No final reserve is accessed.

### Phase V2-5 — Fair tuning + protocol freeze — BLOCKED on T-526 (`T-527`)

Use non-final evidence only to freeze:

- retained method set;
- final layouts/task complexity;
- bounded method-specific hyperparameters with equivalent predeclared opportunity;
- final action-remap/action-failure/observation-corruption conditions;
- actual training and deployment budgets/probe grid;
- root count from precision/runtime sizing;
- exact Phase-B reset/lifecycle semantics;
- root/layout statistical aggregation, interval/sensitivity and any multiplicity rule;
- final-reserve identities/firewall.

No best-seed or best-final-checkpoint selection is allowed.

### Phase V2-6 — Final application rebuild — BLOCKED (`T-528`)

Begins only after T-527 and T-529 are stable.

- select a **different framework from NiceGUI** for the final local application;
- rebuild from scratch rather than restyle historical prototype code;
- consume only framework-neutral `StudyService` DTO/events/artifacts;
- default user workflow is study-first and intent-oriented rather than branch/config plumbing;
- support truthful monitoring/history/results/export and synchronized resilience views;
- preserve novice-first/self-explanatory/accessibility principles from DEC-046;
- select visualization/component libraries here based on the frozen backend and thesis needs, not historical DEC-045 tooling.

No scientific parameter is supplied silently by frontend defaults.

### Phase V2-7 — Intended-user acceptance (`T-511`)

Human acceptance is required for the final configure/run/monitor/history/compare/export/help/error workflow. Automated screenshots/browser checks never close this gate.

## Final protocol-v2 evidence path

Only after T-527, T-529 and T-511 gates are satisfied:

1. `T-610` — execute the frozen protocol-v2 final Study matrix on the accepted execution path.
2. `T-611` — validate/freeze complete final evidence and integrity.
3. `T-612` — execute the predeclared root-level nominal-learning/matched-resilience analysis and sensitivity diagnostics.
4. `T-613` — render final figures/tables/data, freeze evidence/result/claim identifiers and create the thesis/defense evidence handoff.

Failed/cancelled/invalid/scientific-failure outcomes remain visible and attributable. Final figures/tables derive only from frozen real evidence.

## Mandatory pre-WP7 approval

Completing application/evidence does **not** authorize thesis writing. T-511 and T-613 must be satisfactory and the user must explicitly approve starting WP7. Until then all `T-700+` work remains blocked.

## Deferred downstream phases

After explicit approval:

- recheck current official thesis/Word/submission/defense requirements;
- review any user-supplied completed example theses as contextual structure/style references;
- draft/review/freeze the Greek Word thesis from citation-ready bibliography plus frozen evidence;
- incorporate supervisor/reviewer corrections with affected-evidence revalidation;
- build the final PowerPoint defense narrative/deck/evidence map, embedded speaker notes and separate full spoken Greek script per `docs/thesis/PRESENTATION_WORKFLOW.md`;
- validate PowerPoint rendering, factual consistency, rehearsal timing and demo/screenshot fallback;
- run final bibliography/reproducibility/privacy/licensing/delivery audits;
- build the accepted post-thesis standalone Windows application package at `T-803` using the framework chosen at T-528.

## Completion rule

The project is complete only when the research question is answered with reliable reproducible evidence, the bounded final application supports the real Study workflow, and the final thesis/defense package communicates the same frozen evidence. Production-platform engineering is not required; concrete progress is governed by `TASKS.md`.
