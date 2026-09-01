# Codex Execution Prompt

## User entrypoint

Give Codex only:

> `/goal Read docs/context/CODEX_EXECUTION_PROMPT.md and execute it completely. Execute T-534, the clean protocol-v2.1 PySide6 UI rebuild, from a fresh branch created from the latest current main. Implement DEC-061 with primary surfaces Experiment / Run / Results / Evidence. Preserve the scientific methodology and the separate BLOCKED T-610 final-experiment authorization gate. Complete routine Git, PR, CI, objective review, correction, documentation reconciliation and own-PR squash merge when repository policy permits.`

The active goal is specifically `T-534`. Repository/Git/GitHub/evidence state beats stale session memory or prose.

## Start correctly

1. Inspect Git status, branch, recent commits, upstream state, open PR and CI. Resume unfinished work only if it belongs to the current T-534 package.
2. Read first: `AGENTS.md`, `docs/context/TASKS.md`, `docs/context/CURRENT_STATUS.md`.
3. Confirm T-534 remains the active application task and start one fresh implementation branch from latest `main`. Do not continue a paused/pre-v2.1 UI branch/worktree.
4. Then read DEC-059, DEC-060, DEC-061, `configs/protocols/protocol-v2.1-final.json`, `docs/research/RQ_EVIDENCE_TRACEABILITY.md` and `docs/architecture/UI_INFORMATION_ARCHITECTURE.md`.

## Implementation target

PySide6 / Qt 6 Widgets remains the framework. The Study/evidence backend remains scientific authority. Audit `src/resilient_agents/desktop/` before replacing presentation code.

Preserve still-correct UI-neutral Study/results/evidence read models, execution supervision/policy, live-observer/event boundaries, provenance adapters and useful Qt GridWorld drawing primitives. Windows/pages/navigation/layout/theme/copy may be rebuilt. Remove active protocol-v2.0/DEC-058-only/T-528 presentation assumptions.

Implement four primary surfaces:

- **Experiment** — explain the scientific flow: five fixed methods → Phase-A nominal learning → exact checkpoint → matched Phase B → disturbances → Frozen versus Adaptive → RQ1/RQ2/RQ3. The final Thesis experiment always contains Q-Learning, SARSA, DQN, PPO and Dyna-Q+ and offers no method deselection. DEVELOPMENT method/scope selection is allowed only where backend-supported. Frozen and Adaptive are matched regimes of each method, not algorithms or mutually exclusive choices.
- **Run** — make GridWorld dominant. Phase A uses one large nominal GridWorld. Phase B uses two large simultaneous **Frozen — learning off / Adaptive — learning continues** panels only from an exact matched interaction pair. Never fabricate pairing. Keep compact method status. Primary live fields are method, phase, condition, interaction, intended action → executed action and reward; roots/layouts/states/observations/IDs/flags/hashes are technical details.
- **Results** — organize exactly as **RQ1 — Learning / RQ2 — Resilience & Adaptation / RQ3 — Recovery**. RQ1 uses real stored Phase-A trajectories/probes where scientifically supported, plus stored final/time-average/interval/denominator/direct-contrast evidence. RQ2 keeps primary `(FN-FD)-(AN-AD)` separate from Frozen `FN-FD` and Adaptive `AN-AD` losses. RQ3 shows stored AN-vs-AD trajectory, recovery status, observed recovery time conditional on recovery, separately named restricted fixed-horizon delay, right-censoring, sensitivities/direct contrasts where available. Never show censored horizon 256 as observed recovery time.
- **Evidence** — lead with validation/evidence/analysis/export readiness and available user-facing outputs. Keep Study history, artifact IDs/paths/checksums, producer jobs, recipe/checkpoint/result IDs and lineage under progressive technical disclosure.

Help/onboarding and reproducibility detail are contextual/secondary. Do not rebuild a StudyStore/job/artifact-first administrative console.

## Non-negotiable boundaries

Qt presentation consumes validated stored outputs. It must not calculate thresholds, root/layout reductions, estimands, recovery status/time, statistical intervals, direct method contrasts or scientific conclusions from raw evidence. It must not alter actions, observations, RNG, checkpoints, timing, interaction counts, execution order or evidence. Historical schema-v1 remains truthful and gains no synthetic v2.1 recovery semantics. Never invent winner/best-algorithm/significance/superiority claims.

The final reserve remains sealed. UI work, tests, screenshots and synthetic smoke never authorize T-610. Do not access final roots/layouts/outcomes, run the final matrix, tune from final identities or begin Results/Discussion.

## UX and validation

Make the application novice-first, modern, compact, information-dense without clutter, laptop/desktop friendly, keyboard/focus usable and accessible without color-only meaning. Use plain-language labels, progressive disclosure, lightweight onboarding and actionable loading/empty/warning/error/disabled/unavailable/locked states. Required scientific/workflow meaning cannot exist only in tooltips. Avoid excessive permanent cards/banners/help text.

Use DEVELOPMENT/synthetic fixtures only for implementation testing/screenshots. Prefer targeted contract/read-model/widget/integration tests, representative Experiment/Run/Results/Evidence workflows, bounded deterministic screenshots and affected launcher checks. Include Phase-A large GridWorld, exact matched Phase-B Frozen/Adaptive, RQ1/RQ2/RQ3 and a right-censored RQ3 state. Use repository CI as the canonical full-suite guard; avoid redundant test proliferation.

When T-534 is coherent, inspect the diff, reconcile affected active docs/tests/workflows, obtain green exact-head CI and squash-merge the single coherent PR when permitted. Stop before T-610 unless separate explicit scientific authorization is supplied.
