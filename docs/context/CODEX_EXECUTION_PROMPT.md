# Codex Execution Prompt

## User entrypoint

Give Codex only:

> `/goal Read docs/context/CODEX_EXECUTION_PROMPT.md and execute it completely. Execute T-534, the clean protocol-v2.1 PySide6 UI rebuild, from a fresh branch created from latest current main. Implement DEC-061 with primary surfaces Experiment / Run / Results / Evidence. Preserve scientific methodology and the separate BLOCKED T-610 final-experiment authorization gate. Perform routine Git, PR creation, CI, objective review, corrections, documentation reconciliation and own-PR squash merge when policy permits.`

The repository's persistent execution invariant is **Complete the canonical project task registry autonomously**, but only through dependency-valid, non-gated work. For this run the active bounded package is specifically T-534; stop before T-610.

## Startup / resume

1. Inspect Git status, branch, recent commits, upstream state, open PR and CI. Resume work marked `IN_PROGRESS` only when it belongs to the current T-534 package.
2. Read only the session-start core:
   - `AGENTS.md`
   - `docs/context/TASKS.md`
   - `docs/context/CURRENT_STATUS.md`
3. Confirm T-534 remains the active application task. Start from latest `main`; do not continue a paused/pre-v2.1 UI branch/worktree.
4. Then read DEC-059, DEC-060, DEC-061, `configs/protocols/protocol-v2.1-final.json`, `docs/research/RQ_EVIDENCE_TRACEABILITY.md` and `docs/architecture/UI_INFORMATION_ARCHITECTURE.md`.
5. Work on **one bounded scope** at a time inside one coherent T-534 branch/PR.

Repository/Git/GitHub/evidence state beats stale memory or prose.

## T-534 target

PySide6 / Qt 6 Widgets remains the framework. Study/evidence backend remains scientific authority. Audit `src/resilient_agents/desktop/` before replacing presentation code.

Preserve still-correct UI-neutral Study/results/evidence read models, execution supervision/policy, live-observer/event boundaries, provenance adapters and useful Qt GridWorld drawing primitives. Windows/pages/navigation/layout/theme/copy may be rebuilt. Remove active protocol-v2.0/DEC-058-only/T-528 presentation assumptions.

Implement four primary surfaces:

- **Experiment** — explain five fixed methods → Phase-A nominal learning → exact checkpoint → matched Phase B → disturbances → Frozen versus Adaptive → RQ1/RQ2/RQ3. Final Thesis experiment always contains Q-Learning, SARSA, DQN, PPO and Dyna-Q+ with no method deselection. DEVELOPMENT method/scope selection is allowed only where backend-supported. Frozen/Adaptive are matched regimes, not algorithms or alternatives.
- **Run** — GridWorld is dominant. Phase A: one large nominal GridWorld. Phase B: two large simultaneous **Frozen — learning off / Adaptive — learning continues** panels only from an exact matched interaction pair. Never fabricate pairing. Keep compact method status. Primary live fields: method, phase, condition, interaction, intended action → executed action, reward; roots/layouts/states/observations/IDs/flags/hashes are technical details.
- **Results** — exactly **RQ1 — Learning / RQ2 — Resilience & Adaptation / RQ3 — Recovery**. RQ1 uses real stored Phase-A trajectory/probe evidence where supported plus stored final/time-average/interval/denominator/direct contrasts. RQ2 keeps primary `(FN-FD)-(AN-AD)` separate from Frozen `FN-FD` and Adaptive `AN-AD`. RQ3 shows stored AN-vs-AD trajectory, recovery status, observed recovery time conditional on recovery, separately named restricted fixed-horizon delay, censoring and stored sensitivities/contrasts. Never show censored 256 as observed recovery time.
- **Evidence** — lead with validation/evidence/analysis/export readiness and user-facing outputs; keep Study history, IDs, paths, checksums and lineage under progressive technical disclosure.

Help/onboarding and reproducibility detail are contextual/secondary. Do not rebuild a StudyStore/job/artifact-first administrative console.

## Scientific and UX boundaries

Qt consumes validated stored outputs. It must not calculate thresholds, root/layout reductions, estimands, recovery status/time, intervals, direct method contrasts or scientific conclusions from raw evidence. It must not alter actions, observations, RNG, checkpoints, timing, interaction counts, execution order or evidence. Historical schema-v1 stays truthful. Never invent winner/best-algorithm/significance/superiority claims.

Final reserve remains sealed. UI work/tests/screenshots/synthetic smoke never authorize T-610. Do not access final roots/layouts/outcomes, run the final matrix, tune from final identities or begin Results/Discussion.

Make the app novice-first, modern, compact, information-dense without clutter, laptop/desktop friendly, keyboard/focus usable and accessible without color-only meaning. Use plain-language labels, progressive disclosure, lightweight onboarding and actionable loading/empty/warning/error/disabled/unavailable/locked states. Required meaning cannot exist only in tooltips. Avoid excessive permanent cards/banners/help text.

## Validation and Git

Use DEVELOPMENT/synthetic fixtures only. Prefer targeted contract/read-model/widget/integration tests, representative Experiment/Run/Results/Evidence workflows, bounded deterministic screenshots and affected launcher checks. Include Phase-A large GridWorld, exact matched Phase-B pair, RQ1/RQ2/RQ3 and a right-censored RQ3 case. Repository CI is the canonical full-suite guard; avoid redundant test proliferation.

Inspect the diff and reconcile affected active docs/tests/workflows. Do not submit an `APPROVE` review on your own PR. When exact-head CI is green and policy permits, squash-merge the coherent T-534 PR.

Report `Project: X/Y` only from a real canonical finite denominator in `TASKS.md`. **In-progress/failed work never counts as complete**.

## Stop conditions

Complete T-534 through implementation, targeted validation, PR/CI correction, reconciliation and permitted merge. Stop before T-610 unless separate explicit scientific authorization is supplied.
