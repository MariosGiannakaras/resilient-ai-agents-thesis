# Implementation Roadmap

`TASKS.md` is the concrete task/status/dependency registry and always wins on exact current state. This roadmap summarizes the current high-level path without reopening completed scientific decisions.

## Completed foundation

The following are implemented and remain reusable:

1. project/bibliography ownership boundary and immutable generated bibliography consumer;
2. actual-machine capability inventory and Python 3.12 + locked `uv` research environment;
3. project-owned Gymnasium GridWorld, deterministic RNG and evaluator/agent information boundary;
4. immutable historical protocol-v1.0/v1.1/pilot evidence and reproducible history;
5. protocol-v2 multimethod scientific execution foundation for Q-Learning, SARSA, DQN, PPO and Dyna-Q+;
6. exact method-native scientific checkpoints/continuation and matched FN/FD/AN/AD Phase-B execution;
7. Study-first backend with immutable recipe/plan/store/lifecycle/artifact lineage and restart-safe service;
8. protocol-v2 feasibility, fair tuning/sizing and DEC-058 protocol-v2.0 scientific freeze;
9. DEC-060 protocol-v2.1 recovery/direct-comparison amendment with schema-v2 temporal evidence, right-censored recovery semantics, root-paired direct comparisons and actual-root Student-t intervals;
10. deterministic validation/analysis/export handoff and concise RQ → evidence → estimand → output traceability;
11. deny-by-default final Study execution guard, read-only final preflight and DEVELOPMENT-only end-to-end synthetic scientific-pipeline smoke;
12. PySide6 / Qt application framework/runtime decision plus reusable UI-facing Study/evidence/live-observer contracts;
13. DEC-061 experiment-first T-534 product/UX contract.

Historical science and prototype/application history remain auditable; completed work is not rewritten merely to make the current tree visually smaller.

## Current repository preparation

Pre-implementation repository preparation has reconciled active context, preserved historical evidence/decisions, removed stale working branches, retained deliberate provenance refs and established T-534 as the active application task.

Repository/UI preparation does not authorize the final scientific experiment.

## Current application rebuild/restart

The active implementation goal is a clean PySide6 presentation rebuild from today's protocol-v2.1/Study/evidence contracts under DEC-059 + DEC-061.

### Inputs that are authority

- `AGENTS.md`
- `docs/context/TASKS.md`
- `docs/context/CURRENT_STATUS.md`
- DEC-059 application framework/runtime architecture
- DEC-060 protocol-v2.1 scientific amendment
- DEC-061 experiment-first application UX
- `configs/protocols/protocol-v2.1-final.json`
- `docs/research/RQ_EVIDENCE_TRACEABILITY.md`
- `docs/architecture/UI_INFORMATION_ARCHITECTURE.md`

### Existing code policy

Do not simply continue the historical/pre-v2.1 presentation.

Audit `src/resilient_agents/desktop/` first:

- preserve still-correct UI-neutral Study/results/evidence read models, provenance adapters, execution supervision/policy and live-observer/event contracts;
- reuse Qt-native GridWorld drawing primitives where useful;
- presentation widgets/windows/pages/styles/navigation/copy may be replaced from scratch;
- historical screenshots/layouts are reference only and do not constrain the new design;
- remove active protocol-v2.0/DEC-058-only/T-528 presentation assumptions;
- no scientific analysis/threshold/RNG/checkpoint/finalization logic moves into Qt.

### Product architecture

The application is **experiment-first**, not StudyStore/job/artifact-first.

Primary navigation:

> **Experiment → Run → Results → Evidence**

Help/onboarding and technical/provenance detail are contextual/secondary rather than additional primary destinations.

#### Experiment

The Frozen Thesis experiment should explain the scientific flow in user terms:

> five fixed methods → Phase-A nominal learning → exact checkpoint → matched Phase B → disturbance → Frozen vs Adaptive → RQ1/RQ2/RQ3

All five final methods are fixed by the protocol and cannot be deselected. Frozen and Adaptive are matched deployment regimes of the same method, never algorithm choices.

DEVELOPMENT/Exploratory configuration remains inside Experiment and may support backend-approved method/scope selection through:

> **Configure → Review → Create**

DEVELOPMENT remains visibly non-confirmatory and does not use final-reserve identities/outcomes.

#### Run

The GridWorld is the dominant scientific visualization:

- Phase A: one large nominal GridWorld for the current method;
- Phase B: two large exact-matched side-by-side panels, **Frozen — learning off** and **Adaptive — learning continues**;
- compact method status shows pending/running/complete/failed state without ranking;
- primary live facts are method, phase, condition, interaction, intended action → executed action and reward;
- roots/layouts/true state/delivered observation/branch IDs/flags/change events/hashes are technical detail.

Never fabricate synchronization when the lossy presentation stream lacks an exact matched pair.

#### Results

Organize explicitly around the research questions:

> **RQ1 — Learning / RQ2 — Resilience & Adaptation / RQ3 — Recovery**

- RQ1: real stored interaction-axis learning/probe trajectory where scientifically supported, plus final/time-average/interval/denominator/direct-contrast evidence; no UI-invented aggregation.
- RQ2: primary `(FN-FD)-(AN-AD)` with Frozen `FN-FD` and Adaptive `AN-AD` losses as separate supporting views, condition filtering and stored contrasts.
- RQ3: stored AN-vs-AD trajectory, recovery/non-recovery status, observed recovery time conditional on recovery, separately named restricted fixed-horizon delay, right-censoring, sensitivity/direct contrasts where available. A censored horizon 256 is never an observed recovery time.

No winner/best-algorithm/significance/superiority language is introduced beyond what the frozen analysis contract supports.

#### Evidence

Lead with user-facing evidence readiness:

- evidence/validation/analysis/export state;
- available results/exports;
- thesis-ready outputs when legitimately produced;
- useful next action when incomplete.

Study history, artifact IDs/paths/checksums, producer jobs, recipe/checkpoint/result IDs and lineage remain available under progressive technical disclosure.

### UX requirements

The application should be novice-first, modern, compact, self-explanatory and truthful:

- plain-language primary labels with technical IDs under progressive disclosure;
- contextual help/tooltips that supplement, rather than hide, required information;
- accessible text/icon/state cues and clear keyboard/focus behavior;
- actionable empty/loading/disabled/warning/error/locked states;
- strong GridWorld/chart hierarchy and restraint in permanent cards/banners/help paragraphs;
- clear separation of DEVELOPMENT/synthetic, live/provisional, finalized and validated evidence states;
- no fabricated progress/metrics/trajectory/replay.

### UI validation

Use DEVELOPMENT/synthetic fixtures only while rebuilding.

Prefer:

- targeted read-model/policy/widget/integration tests for changed contracts;
- representative Experiment/Run/Results/Evidence workflow checks;
- deterministic screenshots including Phase-A large GridWorld, exact matched Phase-B Frozen/Adaptive side-by-side, RQ1/RQ2/RQ3 results and a right-censored RQ3 case;
- launcher checks when affected;
- repository CI as the canonical full-suite pre-merge guard.

Do not spend model quota on broad redundant screenshot/test proliferation without a concrete regression risk.

### UI completion boundary

The new UI package is complete when the four-surface experiment-first workflow is coherent and truthful, v2.1 stored evidence is represented correctly, the final-reserve lock is impossible to bypass through UI behavior, active protocol-v2.0/T-528 presentation assumptions are gone, affected active docs are reconciled and CI is green.

Final standalone Windows packaging is **not** part of this phase; it remains deferred until after the thesis.

## Final protocol-v2.1 evidence path

The scientific protocol is frozen. Separate T-610 execution and DEC-062 recovery authorization are satisfied; the backend guard remains mandatory.

Under the authorized DEC-062 recovery path:

1. preserve the first 216-job attempt as immutable failed/incomplete history, merge the bounded DEC-054 Study-boundary correction, pass the clean preflight and execute the unchanged 603-job matrix from zero as a distinct replacement instance;
2. validate/freeze complete final evidence and integrity;
3. execute the predeclared root-level RQ1/RQ2/RQ3 analysis and sensitivity diagnostics;
4. render final figures/tables/data and freeze evidence/result/claim identifiers;
5. create the thesis/defense evidence handoff.

Failed/cancelled/invalid/scientific-failure outcomes remain visible and attributable. Final figures/tables derive only from frozen real evidence.

## Mandatory writing approval

Completing repository cleanup, UI implementation or final evidence processing does **not** automatically authorize thesis Results/Discussion writing. The later explicit user approval gate remains mandatory.

## Downstream thesis/defense path

After explicit approval:

- recheck current official thesis/Word/submission/defense requirements;
- review any user-supplied completed theses only as contextual examples;
- draft/review/freeze the Greek Word thesis from citation-ready bibliography plus frozen scientific evidence;
- incorporate supervisor/reviewer corrections with affected-evidence revalidation;
- build the PowerPoint defense narrative/deck/evidence map, embedded speaker notes and separate Greek spoken script;
- validate PowerPoint rendering, factual consistency, rehearsal timing and demo/static fallback;
- run final bibliography/reproducibility/privacy/licensing/delivery audits;
- build the final post-thesis standalone Windows application package under issue #94.

## Completion rule

The project is complete only when the scientific questions are answered with reproducible evidence, the bounded application makes the real experiment understandable and operable, and the thesis/defense package communicates the same frozen evidence. Production-platform engineering is not required.
