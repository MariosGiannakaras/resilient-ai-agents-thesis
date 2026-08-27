# DEC-042 — Pre-WP7 protocol v1.1 and application refinement

**Date:** 2026-08-27  
**Status:** Accepted user-directed refinement; implementation in progress

## Context

The user has not accepted the existing application, agent set, experiment design, runs/results, or UI as the final thesis state. `protocol-v1.0`, the `FINAL-*` run bundles, and the existing thesis-final evidence package are real, finalized historical evidence and must remain immutable, but they do not satisfy the current pre-WP7 product/scientific acceptance gate.

A review of the repository and current RL methodology identified two material refinements:

1. the final `protocol-v1.0` comparison is scientifically controlled but narrow because F0 and C0 are two deployment regimes of the same tabular Q-learning implementation; and
2. the current Streamlit pages do not implement the intended configure → launch → live GridWorld → inspect → compare → export workflow, while the headless scientific core itself is reusable and should remain UI-independent.

The historical R0 robust-value-iteration role remains useful pilot evidence but is not suitable for unchanged reinstatement because its accepted pilot configuration exhibited approximately 96% nominal truncation.

## Decision

### Evidence preservation and versioning

- Preserve `protocol-v1.0`, every finalized historical run, and existing frozen analysis/artifacts byte-for-byte.
- Any revised primary experiment uses a new protocol version, new run identities, fresh held-out final layouts, and a fresh precommitted final seed bank.
- `protocol-v1.1` begins as **candidate**, not frozen. It may become frozen only after D0 implementation, bounded non-final tuning/pilot validation, protocol validation, and pre-final acceptance criteria are satisfied. No final-v1.1 run is launched merely to complete CI or UI work.

### Agent set

Retain:

- **F0 — Frozen Q-learning:** common nominal checkpoint, no post-change updates.
- **C0 — Continual Q-learning:** same common checkpoint/base configuration, online post-change Q-learning updates.

Add:

- **D0 — Dyna-Q+:** tabular model-based planning built on the same information-limited interaction surface. It learns its transition/reward model only from observations legitimately available to the agent, performs bounded planning updates, and uses the Dyna-Q+ recency bonus to support re-exploration in a changing environment.

D0 must be deterministic under the established RNG/seed contracts and serializable/resumable where the common agent contract requires it. D0-specific planning parameters are selected only through a small predeclared development/tuning search; no D0 parameter is chosen from final evidence.

Do not add deep RL merely to increase model count. Do not reinstate R0 unchanged.

### Candidate protocol v1.1

Preserve the accepted F0/C0 base Q-learning configuration selected by existing tuning evidence:

- learning rate `0.5`;
- discount factor `0.96875`;
- exploration epsilon `0.125`;
- `512` nominal training episodes per layout;
- `16` pre-change episodes;
- `32` post-change episodes;
- `48`-step evaluation horizon;
- `32` paired final root seeds.

Retain seven single-factor conditions, but use structural names in the new version:

1. `nominal`;
2. `action-remap-2-swap`;
3. `action-remap-4-cycle`;
4. `action-failure-1of8`;
5. `action-failure-1of4`;
6. `observation-corruption-1of8`;
7. `observation-corruption-1of4`.

Use four fresh held-out final layouts under the same GridWorld scale/structural constraints. Do not reuse already-inspected v1.0 final layouts as the new primary held-out set.

### Statistical roles

Primary outcome reporting emphasizes separate component estimands rather than a composite score:

- cumulative deficit;
- immediate degradation;
- terminal gap/performance.

Recovery remains an explicit secondary/sensitivity outcome because accepted pilot evidence showed material threshold/stability sensitivity. Preserve `NO_DEGRADATION`, `RECOVERED`, and `NOT_RECOVERED`; never encode non-recovery as an artificial horizon recovery time.

Add paired agent-effect reporting and 95% confidence intervals using the paired root/layout design, with explicit `n`, per-layout views, and aggregate views. Do not select favorable thresholds or metrics after inspecting outcomes.

### Application architecture and UI

Keep the Python/Gymnasium scientific core headless. Add an application-facing runtime/service layer between Streamlit and the runner for truthful active-run state, progress/events, read-only live GridWorld observation, history, and capability-based lifecycle controls. Unsupported controls must be shown as unsupported rather than simulated.

Rebuild the Streamlit application around the accepted information architecture:

- Dashboard;
- New Experiment;
- Runs / live GridWorld workspace;
- Compare;
- Artifacts.

The UI may significantly replace the existing `src/app/*` page implementation. It must not duplicate scientific execution logic or fabricate status, metrics, logs, progress, or historical replay. Existing finalized runs that lack a retained step trace explicitly show replay unavailable.

Visualization speed controls affect presentation cadence only, never scientific execution timing or RNG.

### UI review artifacts

Create a repository-root `ui-screenshots/` directory. Stable CI-rendered application screenshots are committed there as review artifacts once the relevant UI milestone is stable. CI may also upload diagnostic screenshot artifacts, but screenshots are not scientific evidence. Deterministic UI fixtures may render chrome/empty/error states; they must never be presented as real experiment results.

### Work branch and tracking

All work governed by this decision uses the single implementation branch:

`feat/pre-wp7-protocol-v1.1-ui-rebuild`

Master tracker: GitHub issue #87. Component trackers: #88–#91. Do not create a parallel implementation branch for this work package. Keep the canonical repository task/status handoff synchronized so a new Codex session can resume without chat history.

### Testing and completion

Testing remains risk-based and proportional. Focus on scientific/information-boundary/determinism/configuration/runtime-truthfulness regressions plus small representative UI/render checks. Never run pilot/final matrices as CI tests and do not expand into an arbitrary coverage project.

Automated UI rendering or screenshots do not satisfy `T-511`. The application remains `USER_VALIDATION_REQUIRED` until the user performs/accepts the intended end-to-end workflow.

WP7/WP8 remain blocked. Technical completion of this branch does not imply permission to begin thesis writing; explicit user approval is still required after pre-WP7 refinement and human UI review.
