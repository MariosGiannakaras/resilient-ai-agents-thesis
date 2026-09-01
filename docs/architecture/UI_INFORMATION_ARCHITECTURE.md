# UI Information Architecture

**Status:** current application information/interaction contract for T-534 under DEC-059 + DEC-061.  
**Scientific authority:** DEC-058 historical freeze, DEC-060 amendment, `configs/protocols/protocol-v2.1-final.json`.  
**Application framework:** PySide6 / Qt 6 Widgets.

The application is an **experiment-first thin client** over the framework-neutral Study/evidence backend. The user-facing hierarchy explains the scientific experiment; the backend continues to own recipes, jobs, roots, checkpoints, branch construction, validation, aggregation, recovery semantics, analysis, evidence finalization and authorization.

## Clean-rebuild rule

The historical/pre-v2.1 PySide6 presentation is reference only. Start T-534 from fresh current `main` and classify existing `src/resilient_agents/desktop/` code before editing:

- preserve still-correct UI-neutral Study/evidence read models, execution supervision, live-observer boundaries and provenance adapters;
- reuse Qt drawing primitives when they remain truthful and useful;
- windows/pages/navigation/layout/theme/copy may be rebuilt from scratch;
- old screenshots are historical visual evidence, not layout authority;
- remove active protocol-v2.0/T-528 presentation assumptions;
- never move scientific configuration, RNG, checkpoint identity, root/layout reduction, estimand calculation, recovery decisions or evidence finalization into Qt state.

## Primary navigation

Use four primary destinations only:

1. **Experiment** — understand/review the experiment; configure DEVELOPMENT work where permitted.
2. **Run** — execute/observe supported work with the GridWorld as the dominant live surface.
3. **Results** — inspect validated stored outputs organized explicitly by RQ1/RQ2/RQ3.
4. **Evidence** — inspect validation/export/readiness state and reproducibility details.

Help/onboarding is available from the header and contextually within these surfaces. Study history, artifacts, provenance and technical identifiers are secondary/drill-down content rather than extra primary navigation destinations.

## Global shell

Keep the shell visually restrained:

- compact app identity and current evidence/mode state;
- four-item navigation;
- contextual Help/onboarding affordance;
- concise final-experiment lock indication when relevant;
- no permanent large sidebar blocks for protocol IDs, task IDs or administrative state.

The shell should remain usable at 1366×768 and comfortable at 1440×900. Important status combines text + icon/symbol + accessible semantic treatment; color alone is insufficient.

## Experiment

### Purpose

Explain **what is being tested and why** before exposing orchestration details.

The scientific story should be understandable without StudyStore/job terminology:

> five methods learn nominally → exact learned state enters matched Phase B → disturbances are applied → Frozen and Adaptive deployments are compared → RQ1/RQ2/RQ3 are answered from validated stored evidence.

### Frozen Thesis experiment

The final Thesis experiment is read-only. It must clearly show:

- protocol-v2.1 identity and final-execution lock;
- all five fixed methods: Q-Learning, SARSA, DQN, PPO, Dyna-Q+;
- concise accurate method explanations;
- Phase A as independent nominal learning with a common actual-environment-interaction fairness budget;
- exact checkpoint handoff into matched Phase B;
- disturbance/condition families at a human-readable level;
- Frozen = learning off and Adaptive = learning continues;
- Frozen and Adaptive as **paired deployment regimes of each method**, never algorithm choices;
- an understandable FN/FD/AN/AD explanation;
- how the experiment maps to RQ1 Learning, RQ2 Resilience/Adaptation and RQ3 Recovery;
- the fact that scientific settings are frozen and cannot be edited from the UI.

The user cannot deselect any of the five methods in the final Thesis experiment.

Exact root IDs, layout IDs, config IDs, checkpoint hashes, recipe hashes and authorization strings belong under **Technical details** unless they are needed to explain an error.

### DEVELOPMENT / Exploratory experiment

DEVELOPMENT configuration is a sub-flow inside Experiment:

> **Configure → Review → Create**

Only settings explicitly supported by the backend are editable. Method selection may be offered here when supported. DEVELOPMENT scope must never expose final-reserve roots/layouts/outcomes and must remain visibly non-confirmatory.

### Pre-run review

Before creation or supported execution, show a readable resolved summary of purpose/evidence class, methods, phases/conditions, locked versus selected settings, validation blockers and DEVELOPMENT/non-confirmatory status. For the final Thesis experiment, show the final-execution lock rather than an editable authorization control. Backend job counts and exact identities are secondary detail.

## Run

### Purpose

Make the scientific process visible without allowing the visualization to influence it.

The hierarchy is:

1. current method / phase / condition and truthful execution state;
2. large GridWorld visualization;
3. primary live transition facts;
4. compact progress for all five methods;
5. technical/backend detail on demand.

Study history tables, artifact inventories and raw job metadata do not occupy the main Run workspace.

### Five-method status strip

Show a compact persistent status for the five retained methods when the current experiment contains them. Each method can be Pending / Running / Complete / Failed (or the truthful backend equivalent), with text/icon semantics. The status strip is navigation/context, not a scientific ranking.

For DEVELOPMENT studies containing a subset, show only the actual configured methods while retaining a clear DEVELOPMENT label.

### Phase A — Nominal learning

For the current method:

- show one **large nominal GridWorld** as the dominant surface;
- label `Phase A — Nominal learning`;
- show truthful interaction/job progress from backend counters only;
- primary transition fields: method, phase, interaction, intended action → executed action, reward;
- condition is omitted/nominal where not applicable.

Episode, environment step, root/layout identity, true state, delivered observation, flags and IDs are secondary technical detail.

### Phase B — Frozen vs Adaptive

When exact matched presentation frames exist, show two **large side-by-side** panels simultaneously:

- **Frozen — learning off**
- **Adaptive — learning continues**

They must share the authoritative matched method/root/layout/**condition**/interaction identity. Condition is part of the presentation-pair identity because two otherwise matching frames from different disturbance conditions are not a valid scientific comparison. Never display unrelated frames as a pair. If exact pairing is temporarily unavailable because the lossy presentation stream dropped frames, show an explicit unavailable/waiting state rather than fabricate synchronization.

Primary Phase-B context:

- method;
- `Phase B — Disturbance / resilience`;
- condition/disturbance;
- interaction;
- Frozen intended → executed action and reward;
- Adaptive intended → executed action and reward.

Technical disclosure may additionally show true states, delivered observations, branch identifiers, root/layout IDs, regime IDs, disturbance flags, change-event IDs and presentation sequence.

### Live-science boundary

Live events are transient, lossy and presentation-only. They may drop frames and may be rendered/interpolated only for visual continuity where that cannot imply fabricated scientific transitions. They never:

- select or modify actions;
- alter observations delivered to learners;
- change RNG/checkpoints/method state;
- block/backpressure scientific execution;
- alter interaction counts or timing;
- become scientific evidence;
- change validation/analysis outcomes.

If historical evidence lacks live/replay data, say so. Do not synthesize replay.

## Results

### Purpose

Answer the research questions from **validated stored backend outputs**. The Results page never recomputes scientific estimands from raw evidence.

The top-level organization is:

1. **RQ1 — Learning**
2. **RQ2 — Resilience / Adaptation**
3. **RQ3 — Recovery**

A compact selected-evidence control may switch between compatible validated Studies/packages. Provenance details should not visually precede the research result.

### RQ1 — Learning

Primary intent: show how methods learned under the common interaction budget and how their nominal performance compares.

Where validated stored Phase-A probes allow it, prefer an interaction-axis **learning curve**. The visualization may directly project stored probe/root/summary outputs; it must not perform a new root/layout aggregation in the UI. If the backend does not emit an aggregate trajectory suitable for a mean curve, show stored root-level trajectories/points or a truthful non-aggregated representation instead of inventing a curve.

Also expose stored:

- final standardized nominal value;
- pointwise interval and included/planned root denominator;
- trajectory/time-average summary;
- root-level distribution/detail where available;
- direct root-paired method contrasts;
- computational/resource evidence separately from policy quality.

Do not label the highest visual value as a winner.

### RQ2 — Resilience / Adaptation

Primary effect:

`(FN-FD) - (AN-AD)`

Present stored adaptation benefit as the primary chart/table. Supporting views separately show:

- Frozen disturbance loss `FN-FD`;
- Adaptive disturbance loss `AN-AD`;
- condition/family filtering;
- intervals and root denominators;
- stored direct method contrasts;
- branch-level FN/FD/AN/AD detail under progressive disclosure when useful.

Frozen and Adaptive remain matched regimes, not selectable algorithms.

### RQ3 — Recovery

For protocol-v2.1 schema-v2 evidence present stored:

- AN-vs-AD recovery trajectory over 32-interaction windows;
- recovered versus non-recovered status;
- observed recovery time **conditional on recovery**;
- separately named restricted fixed-horizon recovery delay;
- right-censored roots;
- primary action-remap condition family plus supporting diagnostics;
- sensitivity outputs when stored;
- direct method contrasts emitted by analysis.

Right-censored roots retain `recovery_time=null`; **256 is the observation horizon, never an invented observed recovery time**.

Historical schema-v1 packages remain truthful historical evidence and do not acquire synthetic v2.1 recovery status/trajectory semantics.

### Result-interpretation rules

- Compare only compatible protocol/evidence definitions.
- Higher reward is better where declared by stored metadata.
- Show effect sizes/intervals only as emitted by validated analysis.
- Never relabel SD as CI or pointwise intervals as formal superiority tests.
- Never create `winner`, `best algorithm`, p-value/significance or unsupported statistical-superiority claims.
- Explain incomplete/common-root blocks and retained failures rather than silently dropping them.

## Evidence

### Purpose

Give the user a clear handoff/readiness view first and reproducibility internals second.

Primary sections should communicate:

- evidence class/state: DEVELOPMENT, provisional, finalized, validated/derived as applicable;
- validation/analysis/export readiness;
- available result/export packages;
- thesis-ready figures/tables/exports when they legitimately exist;
- useful next action when evidence is incomplete or unavailable.

Evidence may include study history and artifact drill-down, but the default view should not begin with hashes or producer job IDs.

### Technical details

Progressive disclosure can expose:

- Study/recipe/protocol/result identifiers;
- artifact IDs and registered paths;
- SHA-256 checksums;
- source job IDs / source artifact IDs;
- checkpoint lineage;
- result index and integrity manifest;
- complete evidence lineage.

Only backend-registered evidence is shown. The UI does not browse arbitrary filesystem content and whatever happens to be visible on screen is never the authoritative export source.

## Self-explanatory UX contract

The application must remain understandable without programming, RL, repository or StudyStore knowledge. Use human-readable primary labels, concise visible explanations of methods/regimes/RQs, progressive disclosure for technical identifiers, and actionable loading/empty/warning/error/disabled/unavailable/locked states. Required workflow or scientific meaning cannot exist only in tooltips. Status uses text plus stable icon/symbol and accessible semantic treatment rather than color alone. Avoid unnecessary confirmations and excessive permanent cards, banners or help paragraphs.