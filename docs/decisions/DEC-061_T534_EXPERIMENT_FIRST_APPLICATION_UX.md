# DEC-061 — T-534 experiment-first application UX

**Date:** 2026-09-01  
**Status:** Accepted  
**Task:** T-534 — Clean protocol-v2.1 PySide6 UI rebuild

## Context

DEC-059 correctly selected **PySide6 / Qt 6 Widgets** as the final application framework and correctly established a thin presentation boundary over the framework-neutral Study backend. Its framework/runtime/scientific-firewall clauses remain current.

The protocol-v2.1 amendment and pre-final readiness work now make the scientific story more explicit than the historical T-528 presentation. The previous application shell was organized primarily around Study lifecycle/storage concepts (`Study / Runs / Results / Artifacts`) and still contains protocol-v2.0/T-528 presentation assumptions. That is useful implementation history but it is not the product model for the clean T-534 rebuild.

The intended user must understand the **experiment** before internal orchestration. StudyStore jobs, artifact IDs, roots, hashes and lineage remain important reproducibility details, but they are implementation/evidence mechanics rather than the primary information architecture.

## Decision

T-534 uses an **experiment-first** product model while preserving the Study backend as the execution/evidence authority.

The primary application navigation is deliberately small:

1. **Experiment**
2. **Run**
3. **Results**
4. **Evidence**

Help, onboarding, settings that are actually needed, and technical/reproducibility details are contextual or secondary surfaces rather than additional primary workspaces.

This decision supersedes only the product-model/navigation/presentation clauses of DEC-059 that describe a recipe-first `Study / Runs / Results / Artifacts` interface or protocol-v2.0-specific UI identity. It does **not** supersede DEC-059's PySide6 selection, direct Python application boundary, Qt-thread/process rules, read-only scientific visualization boundary, final-reserve firewall, or packaging deferral.

DEC-058 remains immutable historical scientific authority. DEC-060 plus `configs/protocols/protocol-v2.1-final.json` remain the current scientific authority. This decision changes no scientific method, estimand, threshold, root/layout rule, experiment identity or execution gate.

## Product mental model

The application should explain the scientific sequence in the same order the thesis experiment is understood:

> **Five methods learn nominally → the trained state is deployed under matched nominal/disturbed conditions → Frozen and Adaptive regimes are compared → validated outputs answer RQ1/RQ2/RQ3 → evidence/export preserves reproducibility.**

The five final methods are fixed by the frozen protocol:

- Q-Learning
- SARSA
- DQN
- PPO
- Dyna-Q+

The final Thesis experiment never offers algorithm removal/reselection. Method selection is a DEVELOPMENT/Exploratory convenience only where the backend recipe explicitly permits it.

**Frozen and Adaptive are not algorithms and are not mutually exclusive choices.** They are matched Phase-B deployment regimes of the same method. The UI must never present a `Frozen OR Adaptive` selection for the scientific comparison.

## Primary surface: Experiment

Purpose: explain and review what will be tested before exposing execution mechanics.

### Frozen Thesis experiment

The frozen Thesis experiment is read-only and protocol-v2.1 aware. It should show, in human-readable form:

- the scientific purpose and current final-execution lock;
- the five fixed methods and short accurate descriptions;
- Phase A as independent nominal learning under a common actual-interaction fairness budget;
- the transition from each method's exact Phase-A checkpoint into matched Phase B;
- the disturbance families/conditions at an understandable level;
- Frozen (`learning off`) and Adaptive (`learning continues`) as paired regimes;
- a concise visual explanation of FN/FD/AN/AD and how RQ1/RQ2/RQ3 use the stored evidence;
- fixed protocol scope and important units without making roots/job counts the central story;
- technical IDs, exact roots/layouts/checkpoint/config hashes and similar provenance only under progressive disclosure.

The final experiment remains visibly locked while the separate authorization gate is closed. No UI action can synthesize, request, persist or pass the authorization token.

### DEVELOPMENT / Exploratory experiment

DEVELOPMENT configuration lives inside **Experiment**, not as a separate primary navigation area. It may support:

> Configure → Review → Create

where the backend permits selected methods/scope. Every such experiment is prominently non-confirmatory and cannot use final-reserve identities/outcomes or later masquerade as thesis evidence.

## Primary surface: Run

Purpose: make the actual learning/deployment process understandable while keeping execution truthful and scientifically passive.

### Overall hierarchy

The Run workspace prioritizes the **current method, phase and GridWorld**. Administrative Study history/tables must not dominate the screen.

A compact five-method status strip remains visible enough to answer which methods are pending, running, complete or failed. Root/layout/job identity is secondary technical detail.

### Phase A — nominal learning

For the currently executing method:

- one **large** GridWorld is the dominant visual surface;
- clearly label the current method and `Phase A — Nominal learning`;
- show truthful progress from backend counters only;
- primary live facts are method, phase, interaction, intended/executed action and reward, plus condition when applicable;
- episode/root/layout/state/observation/IDs/flags/checkpoint details remain secondary unless needed to explain an exceptional event.

### Phase B — matched deployment

When matched disturbed deployment is observable, show **two large side-by-side GridWorld panels simultaneously**:

- **Frozen — learning off**
- **Adaptive — learning continues**

The pair must refer to the same matched method/root/layout/interaction context. The current presentation event boundary may drop frames, but it must never invent synchronization. If an exact pair is unavailable, the UI says so rather than pairing unrelated frames.

The current condition/disturbance is prominent. The user should be able to understand what changed and why the two regimes are being compared without reading job IDs.

The primary live transition information is:

- method;
- phase;
- condition;
- interaction;
- intended action → executed action;
- reward.

True state, delivered observation, branch IDs, root/layout IDs, disturbance flags, change-event IDs and hashes are available through a compact **Technical details** disclosure. They do not occupy the main visualization area.

Live visualization remains presentation-only, lossy and non-blocking. It cannot change actions, observations delivered to the learner, RNG, checkpoint state, scientific timing, metrics, evidence or execution order.

## Primary surface: Results

Purpose: answer the research questions from validated stored outputs rather than expose generic analysis artifacts.

The top-level Results organization is exactly:

1. **RQ1 — Learning**
2. **RQ2 — Resilience / Adaptation**
3. **RQ3 — Recovery**

No surface declares a `winner`, `best algorithm`, formal statistical superiority or significance claim that is not part of the frozen analysis contract.

### RQ1 — Learning

Where validated stored Phase-A probe outputs support it, the preferred primary visualization is a real interaction-axis **learning curve**. The UI may project already-stored probe/root/summary values but must not perform a new scientific root/layout reduction merely to draw the chart.

Also expose the stored:

- final nominal performance;
- pointwise interval/denominator information;
- trajectory/time-average summary;
- root distributions where available;
- direct root-paired method contrasts;
- secondary computational evidence separately from policy quality.

If no chart-ready validated trajectory summary exists, show the truthful stored probe/root evidence without inventing an aggregate curve.

### RQ2 — Resilience / Adaptation

The primary comparison is stored adaptation benefit:

`(FN-FD) - (AN-AD)`

Supporting views separately show:

- Frozen disturbance loss `FN-FD`;
- Adaptive disturbance loss `AN-AD`;
- condition filtering/family context;
- stored intervals and root denominators;
- stored direct method contrasts.

Frozen/Adaptive remain regimes of each method, never algorithm choices.

### RQ3 — Recovery

For schema-v2 protocol-v2.1 evidence, present stored:

- AN-vs-AD 32-interaction recovery trajectories;
- recovered/non-recovered status;
- observed recovery time **conditional on recovery**;
- separately named restricted fixed-horizon recovery delay;
- right-censored non-recovery;
- primary action-remap axis plus supporting condition diagnostics;
- stored sensitivity outputs where available;
- stored direct method contrasts.

A right-censored root at horizon 256 always keeps `recovery_time=null`. The UI must never display `256` as an observed recovery time when recovery did not occur.

Historical schema-v1 evidence remains historical and receives no synthetic v2.1 recovery semantics.

## Primary surface: Evidence

Purpose: make validated outputs and reproducibility usable without turning the application into an artifact browser.

Primary content should answer:

- what evidence exists and whether it is DEVELOPMENT, provisional, finalized or validated;
- which result/export packages are available;
- which thesis-ready tables/figures/exports exist when legitimately produced;
- whether validation/analysis/export stages are complete or blocked;
- what the user can inspect/export next.

Detailed provenance remains available under progressive disclosure:

- artifact IDs;
- registered paths;
- SHA-256 values;
- source job IDs;
- source artifact IDs;
- recipe/checkpoint/result identities;
- full lineage and manifest detail.

The old standalone Artifacts/provenance workspace is therefore a reusable data source/pattern, not the new primary product surface.

## Reuse boundary for the existing desktop package

T-534 must audit rather than wholesale-delete `src/resilient_agents/desktop/`.

### Preserve or adapt when still correct

Strong candidates for reuse are:

- `study_read_model.py` — safe read-only facade over durable Study state;
- `results_read_model.py` — strict verified projection of stored v1/v2/v2.1 analysis;
- `execution_supervisor.py` — non-blocking QProcess worker supervision;
- `live_events.py` — lossy presentation-only event stream and exact FD/AD pairing;
- `live_instrumentation.py` — runtime-only observer boundary, provided current tests reconfirm no scientific feedback;
- evidence/provenance adapters and safe DEVELOPMENT creation/execution contracts;
- the Qt-native GridWorld drawing primitives after presentation/sizing refactoring.

### Redesign rather than inherit

The following historical presentation is not design authority:

- `main_window.py` navigation/sidebar/header;
- `study_flow.py` / `study_page.py` page composition and protocol-v2.0 copy;
- `runs_page.py` Study-history-first layout and small live visualization hierarchy;
- `results_page.py` generic tab naming/layout where it obscures explicit RQ organization;
- `artifacts_page.py` as a primary navigation destination;
- current theme/card/banner density where it produces clutter;
- old onboarding/help copy and protocol-v2.0/T-528 labels.

## Protocol-v2.1 presentation cleanup

T-534 must remove active presentation dependence on protocol-v2.0/T-528 wording. In particular, current desktop code contains v2.0-specific root discovery/protocol loading, DEC-058-only display identity, and T-528 execution/help messages. Those are migration targets, not current authority.

The rebuilt UI should load/display the current self-contained protocol-v2.1 final configuration while preserving the backend's deny-by-default final execution guard. The desktop layer may keep a defense-in-depth DEVELOPMENT guard, but it must not implement an alternate final-authorization contract that can drift from `StudyService`.

## UX invariants

The final interface is:

- modern and compact;
- information-dense without administrative clutter;
- understandable to a non-programmer/non-RL user;
- designed for ordinary thesis laptop/desktop sizes;
- accessible by text/icon/state semantics rather than color alone;
- keyboard/focus usable;
- progressively disclosive for technical detail;
- explicit about loading/empty/error/locked/unavailable states;
- restrained in banners/cards/help copy;
- truthful about live versus stored/validated evidence.

Tooltips supplement the interface; required workflow/scientific meaning never exists only in a tooltip.

## Scientific invariants

The UI must not:

- alter retained final methods or method configurations;
- reinterpret Frozen/Adaptive as algorithms;
- calculate or choose scientific thresholds;
- reduce layouts/roots into new estimands;
- decide recovery status/time;
- calculate statistical intervals or direct method contrasts from raw evidence;
- replace failed roots/seeds;
- access/tune from final-reserve identities/outcomes during T-534;
- control scientific RNG/checkpoints/actions/observations/timing;
- finalize evidence independently of the backend;
- authorize the final experiment;
- create unsupported `winner`, `best`, significance or superiority claims.

## Validation consequence

T-534 implementation and screenshots use DEVELOPMENT/synthetic fixtures only. Validation should be risk-based: targeted read-model/policy/widget tests, representative Experiment/Run/Results/Evidence workflows, bounded deterministic screenshots at laptop/desktop sizes, launcher checks when affected, then canonical repository CI on the exact PR head.

The Run validation set must explicitly cover Phase-A single-GridWorld presentation and Phase-B exact matched Frozen/Adaptive side-by-side presentation. Results validation must explicitly cover RQ1/RQ2/RQ3 and a right-censored recovery case.

## Gate boundary

Nothing in this decision authorizes T-610. `final_reserve_access=false` remains sealed, no final-v2.1 outcome may be inspected during T-534, and thesis Results/Discussion writing remains separately gated.
