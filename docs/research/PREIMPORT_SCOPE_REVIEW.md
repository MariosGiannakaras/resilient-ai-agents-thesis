# Pre-Import Research Scope Review

**Status:** `PROPOSED / PRE-IMPORT / NON-BINDING`  
**Date:** 2026-08-03  
**Depends on:** `PREIMPORT_RESEARCH_FRAMING.md`

## Purpose

This review tests whether all three official uncertainty examples should become full resilience/recovery dimensions in the final experiment matrix.

The current answer is **no**. The canonical bibliography supports a more bounded and scientifically cleaner hierarchy:

- **Primary resilience/recovery axis:** persistent environment/rule/dynamics change.
- **Supporting robustness diagnostics:** observation disturbance and action-execution disturbance.

This is a provisional scope recommendation. It is not frozen until the controlled bibliography import, system capability report, environment prototypes, and agent feasibility checks are complete.

## Why the three disturbance channels should not be treated symmetrically

The official application names examples such as observation/data noise, changing rules, and failed action execution. Those examples establish the intended uncertainty scope, but they do not require every uncertainty mechanism to answer exactly the same research question or receive an identical adaptation protocol.

The selected canonical literature shows different scientific roles for the channels.

### Environment/rule/dynamics change

The strongest non-stationary RL studies explicitly examine agents that continue operating while transitions or rewards change at unknown times. Their methods separate change detection from adaptation, reuse prior contexts, and evaluate post-change reward trajectories, detection delay, or repeated-context recovery.

This channel therefore supports the thesis requirement to evaluate:

- adaptation;
- resilience as a temporal process;
- recovery speed;
- novel versus recurring change where feasible;
- degradation and recovery trajectories after a hidden change point.

It is the most direct primary axis for the thesis research question.

### Observation disturbance

The selected observation-robust literature models corrupted, missing, or noisy observations and asks whether a policy can preserve utility despite imperfect sensing. The strongest evidence emphasizes clean-versus-disturbed utility, robustness regret, belief inference, or invariance under observation kernels.

These methods generally do **not** define recovery after an environmental changepoint. Robust execution under persistent observation noise is therefore valuable evidence, but it should not automatically be labelled adaptation or recovery.

### Action-execution disturbance

The selected action-robust literature models the difference between intended and executed action, for example stochastic action replacement, no-op failure, or adversarial action perturbation. It provides a natural severity parameter and a clean robustness-versus-nominal-performance trade-off.

Again, the primary construct is resistance to execution uncertainty rather than learning a new environment after a changepoint.

## Recommended scientific hierarchy

### Tier 1 — primary recovery experiment

Use one clearly defined environment/rule/dynamics change family as the main non-stationary experiment.

Candidate forms for later prototype comparison include:

- obstacle/topology rule change;
- transition-success or movement-dynamics change;
- movement-cost/reward-rule change.

Only the smallest scientifically sufficient form should survive the environment-specification gate.

The change should be:

- introduced at a known experimental time but hidden from the agent;
- persistent for a predefined post-change horizon;
- serializable and reproducible;
- parameterized by a small severity axis;
- observable in the ground-truth trace without exposing its identity to agents that are not entitled to that information.

Primary outcomes can then include immediate degradation, failure magnitude, recovery time/profile, end-window performance, and clean-performance trade-offs.

### Tier 2 — supporting observation robustness diagnostic

Use a bounded observation-corruption mechanism as a targeted diagnostic rather than a full independent resilience study.

Candidate questions:

- How much does performance degrade as observation corruption increases?
- Does a robustness-oriented mechanism preserve disturbed performance at an unacceptable nominal cost?
- Are failures gradual or catastrophic at particular severity ranges?

Do not claim online recovery unless an included agent actually updates after the observation regime changes and the protocol was designed to measure that capability.

### Tier 3 — supporting action-failure robustness diagnostic

Use a simple discrete action-execution model, such as no-op or random valid-action replacement with controlled probability.

Required trace fields later include intended action, executed action, and disturbance event.

Candidate questions:

- How much performance is retained as action-failure probability increases?
- Does robustness training or another selected capability improve stressed performance without excessive clean-performance loss?
- Which failure patterns emerge as severity increases?

Again, do not call the result recovery if the policy is frozen and no adaptation occurs.

## Consequence for the candidate research questions

The provisional main question should be interpreted primarily around **persistent environmental change**, because that is where recovery speed is scientifically identifiable.

A tighter future formulation may become:

> How do agents with different robustness and online-adaptation capabilities differ in immediate degradation and recovery after an unannounced persistent change in GridWorld dynamics or rules?

Observation and action disturbances can then support one secondary diagnostic question:

> How robust are the same selected agents to controlled observation and action-execution disturbances when evaluated under a clearly declared frozen or adaptive regime?

This structure is preferable to a full `agents × 3 disturbance families × severities × timing patterns × adaptation regimes` factorial design unless later pilots demonstrate that the larger matrix is both necessary and feasible.

## Matrix-size control

The final experiment count can grow multiplicatively through:

- agent count;
- disturbance family;
- severity;
- scenario/layout;
- frozen versus adaptive regime;
- novel versus recurring context;
- independent repetitions.

The thesis should therefore spend experimental budget on replication and interpretable effect estimates rather than adding many weakly motivated cells.

The default scope-control rule is:

1. keep one primary dynamic-change family for the full recovery protocol;
2. use observation and action uncertainty as smaller diagnostic suites;
3. keep recurring-context recall conditional;
4. do not add compound disturbances before single-factor behavior is understood;
5. prefer severity curves within a small number of factors over many unrelated perturbation types;
6. preserve enough independent runs for uncertainty-aware comparison.

## Implications for agent selection

This hierarchy also prevents model selection from becoming a catalogue exercise.

The final agent set should be chosen so that each agent has a distinct scientific role in the **primary dynamic-change experiment**. Supporting observation/action diagnostics reuse the same selected agents where semantically valid; they should not require extra algorithms solely to make those diagnostics look competitive.

Likely capability roles remain:

- ordinary nominal learner/reference;
- robustness-oriented comparator where feasible;
- online adaptive comparator;
- optional context-memory/recall capability only if it answers a retained secondary question.

The exact algorithms remain open.

## Implications for metrics

### Primary dynamic-change suite

Prioritize:

- nominal reference performance;
- immediate post-change degradation;
- failure depth/duration;
- recovery time with a predeclared threshold and stabilization rule;
- integrated recovery performance;
- end-window post-change performance;
- non-recovery/censoring;
- independent-run uncertainty.

### Observation/action diagnostics

Prioritize:

- clean performance;
- disturbed performance by severity;
- absolute/relative degradation;
- failure/success rate where task semantics permit;
- worst-window or risk-sensitive summaries if justified;
- independent-run uncertainty.

Recovery metrics are added only if online updates and a meaningful persistent regime are explicitly part of that diagnostic.

## GridWorld prototype implication

The prototype comparison should now emphasize whether the candidate implementation can represent the primary change cleanly while still exposing observation/action disturbance hooks.

For a custom Gymnasium prototype, test:

- an explicit persistent transition/rule change at an exact step;
- separate observation transformation;
- intended-versus-executed action transformation;
- event trace parity and deterministic replay.

For a MiniGrid prototype, test whether the same semantics can be added through thin project-owned wrappers/subclassing without inheriting confounding orientation, action, observation, reward, or mission semantics.

## Explicit exclusions at this stage

Do not add to the initial protocol:

- separate reward-noise family;
- adversarial observation attacks;
- multiple simultaneous changes;
- safety/CMDP constraints as another experimental axis;
- multi-agent effects;
- visual-domain shifts;
- continuous-control physics perturbations;
- a new algorithm for each uncertainty family.

These remain possible future extensions only if a later research gap or supervisor requirement makes them necessary.

## Promotion gate

This scope review can become part of the final research design only after:

1. the verified bibliography package is imported and the claims above are mapped to canonical source IDs/evidence;
2. the target-system inventory bounds feasible agent and run budgets;
3. GridWorld prototypes confirm clean implementation of the proposed disturbance hierarchy;
4. agent prototypes establish a fair and feasible comparison;
5. pilot results confirm that the proposed metrics behave sensibly;
6. the required pre-freeze literature refresh finds no evidence that materially changes the design.

## Current recommendation

Use **persistent rule/dynamics change as the thesis's primary resilience/recovery experiment**. Keep **observation noise and action-execution failure as supporting robustness diagnostics** using the same selected agent set where scientifically valid.

This is currently the smallest design that covers the official uncertainty examples while keeping “resilience” tied to an actual degradation–adaptation–recovery process and preserving enough experimental budget for reliable repetitions.
