# Experimental Requirements

**Status:** Active protocol-v2.1 experimental requirements under DEC-058 + DEC-060.  
**Scientific authority:** `configs/protocols/protocol-v2.1-final.json`  
**Final-reserve state:** sealed; `final_reserve_access=false`.

These requirements govern final scientific execution and evidence handling. Historical pilot/development protocols remain auditable but do not override the current final authority.

## Current T-610 execution state

The first authorized `protocol-v2.1-final` Study remains fail-closed and unfinalized at 216/603 after a deterministic SARSA checkpoint-boundary implementation failure. DEC-062 makes it immutable historical failed/incomplete evidence, ineligible for T-611 or any final claim. The replacement `protocol-v2.1-final--t610-recovery-01` started from zero on clean source commit `86fb01a13fd77b98ea0b8d8fa6d5c5d6e2cbd730` and finalized all 603/603 planned jobs with the exact same frozen recipe and plan hashes. T-611 validated and froze only the replacement under manifest SHA-256 `2d3f9e47b998b7e76b5a9fa984427d87e4bc5f038e4adbabbef9635e419cd2db`; T-612 is the next scientific-use gate.

## Run classes and separation

### Development / exploratory
- Used for implementation debugging, synthetic known-answer checks, UI validation and non-final workflow verification.
- Must use non-final identities/layouts/root namespaces when scientific execution could occur.
- Outcomes may change implementation mechanics but cannot be promoted into final evidence.

### Tuning / pilot / sizing
- Historical completed evidence remains immutable.
- May justify method-specific hyperparameters, feasibility and resource sizing only within their accepted decision boundaries.
- Must never be merged with final-reserve evidence or rerun selectively from favorable outcomes.

### Final confirmatory
- Executed only after T-533 completes and a separate explicit T-610 authorization is granted.
- Uses the frozen protocol-v2.1 recipe, final roots/layouts, selected configurations, conditions and analysis contract exactly as committed.
- No outcome-driven seed/root replacement, threshold adjustment, metric redesign, condition removal or selective rerun is allowed.

## Final experiment matrix

The final matrix is fixed to:

- methods: Q-Learning, SARSA, DQN, PPO, Dyna-Q+;
- independent roots: 12;
- held-out layouts: 2;
- Phase-A actual-environment-interaction budget: 8,192 per method/root/layout;
- Phase-A no-learning probes: exact committed interaction checkpoints;
- Phase-B matched-set conditions: 4;
- matched branch roles: exact `FN`, `FD`, `AN`, `AD`;
- common nominal no-learning prefix: 1 interaction;
- Phase-B post-boundary horizon: 256 actual interactions per branch;
- primary final matrix dimensions: 120 Phase-A units, 480 matched Phase-B sets, 1,920 branches.

The self-contained machine-readable source is `configs/protocols/protocol-v2.1-final.json`; prose counts must not supersede it.

## Information and fairness contract

- All retained methods receive the same semantic position observation and same discrete action space.
- No method receives hidden map truth, disturbance flags, change indicator, regime identity, executed-action feedback or evaluator-only state.
- Neural methods may use a deterministic numeric encoding of the same semantic observation; representation implementation does not grant extra information.
- Primary fairness/accounting axis is **actual environment interactions**.
- Identical hyperparameters, optimizer updates, rollout lengths or planning updates are not required across different algorithms.
- Method-specific configurations are frozen from the completed bounded tuning process and must not be altered during final execution.

## Phase-A requirements

- Every method trains independently from its own method-appropriate fresh initialization under the same task semantics and principal interaction budget.
- No method may inherit another method's learned parameters/state.
- Probes are deterministic/no-learning evaluations and must not change learner state, exploration state or scientific RNG streams.
- Exact method-native scientific checkpoints must preserve all state required for later continuation.
- Checkpoint/probe interaction indices must exactly match the final recipe.
- Training failures are retained scientific outcomes; failed roots are not replaced from outcomes.

## Phase-B matched-set requirements

Each Phase-B method/root/layout/condition unit must:

1. restore the exact matching Phase-A checkpoint;
2. advance the frozen one-interaction common nominal no-learning prefix;
3. create one exact matched branch point;
4. fork `FN`, `FD`, `AN`, `AD` atomically from that point;
5. preserve learner/environment/RNG lineage and method-native continuation semantics;
6. execute exactly 256 actual post-boundary interactions per successful branch;
7. retain scientific failures without silently substituting a new root/seed.

Adaptive learning begins only after the matched boundary. Replay buffers, target networks, optimizers, exploration state, policy/rollout state, empirical models, recency counters, schedules and RNG state must not be silently reset.

Episode resets are environment lifecycle events, not learner resets. The persistent multi-episode policy remains the committed authority for continuation through the 256-interaction horizon.

## Temporal evidence for recovery

Protocol-v2.1 requires passive temporal evidence collection that does not insert extra learning/update boundaries.

- Metric: mean reward per actual environment interaction.
- Fixed window width: 32 interactions.
- Horizon: 256 interactions.
- Exact endpoints: 32, 64, 96, 128, 160, 192, 224, 256.
- Windows continue across episode boundaries and are never reset/realigned by an episode reset.
- Every successful Phase-B branch must retain the exact 8 fixed windows in schema-v2 analysis evidence.
- For PPO/DQN and other method-native learners, temporal capture must be observational/passive; execution must not be split into artificial 32-step learning calls that change optimizer/rollout semantics.
- Raw matched-set evidence and standardized branch records must agree on window count, endpoints, widths and finite values.

## Final research estimands

### RQ1 — nominal learning
- Primary: final no-learning probe performance.
- Secondary: predeclared time-average learning-trajectory performance.
- Direct method comparison: root-paired A-minus-B after equal layout reduction.

### RQ2 — resilience/adaptation
- Frozen loss and Adaptive loss are directed according to metric direction.
- Matched adaptation benefit remains `(FN-FD)-(AN-AD)` after direction normalization.
- Primary direct method comparison: adaptation benefit.
- Frozen/Adaptive loss contrasts are secondary.

### RQ3 — recovery
- Primary conditions: persistent `action-remap` family.
- Supporting conditions: action-failure and observation-corruption diagnostics.
- Matched reference: root-level `AN` trajectory versus `AD` trajectory.
- Root-level layouts are equally weighted window-by-window before recovery inference.
- Higher-is-better gap: `AN - AD`.
- Primary tolerance: 0.10 reward/interaction.
- Sensitivity tolerances: 0.05 and 0.20.
- Stable recovery: two consecutive in-tolerance windows.
- Recovery time: endpoint of the first window in the first stable run.
- Confirmation time: endpoint of the final required stability window.
- Non-recovery: right-censored at 256 with `recovery_time=null`.
- A censored root must never be represented as having recovered at 256.
- A separately named restricted fixed-horizon recovery-delay estimand may use 256 for censored roots only for the explicitly labeled fixed-horizon comparison; it is not the recovery time.

## Statistical analysis

Before T-610, the following are frozen:

- independent unit: root;
- layouts/episodes/probes/windows are repeated/nested observations, not independent replicates;
- equal-weight layout reduction inside root before inference;
- direct method contrasts pair common root identities only and use A-minus-B orientation;
- two-sided 95% Student-t pointwise intervals use the predeclared critical value for the **actual** independent-root count `n=2..12`;
- no formal p-value superiority family;
- no multiplicity correction is claimed because no simultaneous hypothesis-testing family is authorized;
- pointwise interval overlap/non-overlap must not be described post hoc as statistical significance;
- scientific failures/missing roots remain visible in denominators;
- recovery censoring/non-recovery remains explicit;
- sensitivity thresholds are fixed before outcomes and cannot replace the primary threshold after inspection;
- no composite resilience score.

If fewer than two common independent roots remain for a specific method contrast, an inferential Student-t contrast is not produced rather than inventing an interval.

## Computational evidence

- Actual environment interactions are the primary fairness/resource accounting quantity.
- Wall-clock seconds and process CPU seconds are secondary descriptive observations.
- Method-native update opportunities/optimizer updates and Dyna planning updates may be reported where their semantics are interpretable.
- These quantities do not redefine the fairness criterion and are not a new primary RQ.
- Final execution remains Windows / Python 3.12 / CPU as committed by the final protocol authority.

## Evidence, provenance and failure retention

At minimum retain:

- immutable Study recipe and SHA-256;
- deterministic plan/job identities;
- resolved run configuration and protocol version;
- exact Phase-A scientific checkpoints and lineage;
- matched Phase-B branch-point fingerprints;
- raw run-bundle artifacts and standardized analysis records;
- temporal reward windows for protocol-v2.1 Phase B;
- explicit resource measurements;
- scientific/infrastructure failure distinction and reasons;
- validation report;
- deterministic analysis package;
- deterministic CSV/JSON evidence handoff plus hashes and result identifiers;
- software/Git/protocol provenance sufficient to regenerate derived tables.

Filesystem evidence remains authoritative. UI/index/database views are derived/read-only and must be rebuildable from stored evidence.

## Result generation and UI boundary

- Thesis tables/figures must be regenerated from validated stored evidence, not manually keyed values.
- The PySide6 application may display validated stored learning, loss, adaptation-benefit, recovery and method-contrast outputs.
- The UI must not choose thresholds, recompute final scientific estimands, exclude roots, replace failures, or become the scientific authority.
- If stored evidence is absent/invalid, the UI must show an explicit unavailable/error state rather than synthesize a result.

## Links to thesis evidence

Every final figure/table must identify or inherit traceable provenance for:

- study/experiment/result identifiers;
- included independent roots and retained failures/exclusions;
- source analysis/evidence artifacts;
- analysis recipe/version;
- protocol recipe SHA-256;
- Git commit and environment/software identity;
- generation timestamp or deterministic artifact metadata;
- caption/claim scope.

## Final-reserve gate

T-533 may run synthetic/non-final mechanics validation only. It must not execute, inspect or tune against final-reserve outcomes. The required separate T-610 authorization and narrow DEC-062 recovery authorization were supplied on 2026-09-02. Final scientific execution must still stop immediately if the committed final-reserve firewall/gate is not satisfied; authorization is supplied only through the accepted backend token and does not change the frozen authority fields. DEC-062 corrects only the missing application of the already accepted zero-interaction DEC-054 deployment-start settlement.
