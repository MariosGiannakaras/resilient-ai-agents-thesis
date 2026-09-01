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
12. PySide6 / Qt application architecture decision and a reusable UI-facing Study/evidence contract foundation.

Historical science and prototype/application history remain auditable; completed work is not rewritten merely to make the current tree visually smaller.

## Current repository preparation

Before the clean UI restart:

- reconcile active context/docs that still describe superseded v1.1/NiceGUI/pre-freeze state;
- keep historical decision records and scientific evidence intact;
- remove merged/stale remote working branches where they contain no unique required work;
- retain `main` and deliberate archive/provenance branches;
- ensure no stale open implementation PR remains;
- start the new UI from one fresh branch off current `main`.

Repository cleanup does not authorize the final scientific experiment.

## Current application rebuild/restart

The active implementation goal is a clean PySide6 presentation rebuild from today's protocol-v2.1/Study contracts.

### Inputs that are authority

- `AGENTS.md`
- `docs/context/TASKS.md`
- `docs/context/CURRENT_STATUS.md`
- DEC-059 application architecture
- DEC-060 protocol-v2.1 amendment
- `configs/protocols/protocol-v2.1-final.json`
- `docs/research/RQ_EVIDENCE_TRACEABILITY.md`
- relevant `docs/architecture/` UX/information-architecture guidance

### Existing code policy

Do not simply continue the paused UI implementation.

Audit `src/resilient_agents/desktop/` first:

- preserve UI-neutral read-model, evidence adapter, provenance, Study-service and execution-policy contracts that are still correct;
- presentation widgets/windows/pages/styles/navigation may be replaced from scratch;
- existing screenshots/layouts are historical reference only and do not constrain the new design;
- no scientific analysis/threshold/RNG/checkpoint/finalization logic moves into Qt.

### Required user experience

The application should be novice-first, modern, compact, self-explanatory and truthful.

The frozen Thesis Study path should clearly expose:

> Study overview/review -> frozen scientific configuration -> final-execution lock/authorization state -> monitor/validate/results/export when legitimately available

The DEVELOPMENT/Exploratory path should support:

> Configure -> Review -> Create -> Run -> Live Monitor -> Results/Compare -> History/Artifacts/Export

The UI must:

- use plain-language primary labels with technical IDs under progressive disclosure;
- explain methods, conditions, metrics, units and consequences in-context;
- provide actionable empty/loading/disabled/warning/error/locked states;
- distinguish DEVELOPMENT/synthetic, live/provisional, finalized run and validated evidence states;
- present stored RQ1/RQ2/RQ3 outputs, including recovery trajectories/status/speed and direct method contrasts when valid evidence exists;
- keep historical schema-v1 evidence truthful without inventing v2.1 recovery semantics;
- never fabricate progress/metrics/trajectory or calculate scientific estimands from raw evidence.

### UI validation

Use DEVELOPMENT/synthetic fixtures only while rebuilding.

Prefer:

- targeted widget/read-model/integration tests for changed contracts;
- representative workflow checks;
- deterministic screenshots/render checks for important views/states;
- repository CI as the canonical full-suite pre-merge guard.

Do not spend model quota on broad redundant screenshot/test proliferation without a concrete regression risk.

### UI completion boundary

The new UI package is complete when the intended end-to-end workflows are coherent and truthful, v2.1 stored evidence is represented correctly, the final-reserve lock is impossible to bypass through UI behavior, affected active docs are reconciled and CI is green.

Final standalone Windows packaging is **not** part of this phase; it remains deferred until after the thesis.

## Final protocol-v2.1 evidence path

The scientific protocol is frozen but execution remains separately gated.

Only after explicit final-scientific-experiment authorization:

1. execute the frozen protocol-v2.1 final Study matrix on the accepted execution path;
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

The project is complete only when the scientific questions are answered with reproducible evidence, the bounded application supports the real Study workflow, and the thesis/defense package communicates the same frozen evidence. Production-platform engineering is not required.
