# T-526 Physical Windows Feasibility Runbook

**Status:** one-time Phase-A and DEC-053 recovery immutable; DEC-054 zero-interaction boundary settlement and fresh Phase-B v0.3 are implemented and await reviewed physical validation
**Plan:** `configs/protocols/protocol-v2-feasibility-v0.1.json`  
**Entrypoint:** `scripts/run_protocol_v2_feasibility_windows.ps1`
**Recovery amendment:** `configs/protocols/protocol-v2-t526-recovery-phase-b-v0.1.json`
**Recovery/Phase-B entrypoint:** `scripts/run_protocol_v2_t526_recovery_phase_b_windows.ps1`
**DEC-053 amendment:** `configs/protocols/protocol-v2-t526-recovery-phase-b-v0.2.json`
**DEC-053 entrypoint:** `scripts/run_protocol_v2_t526_recovery_phase_b_v02_windows.ps1`
**DEC-054 config:** `configs/protocols/protocol-v2-t526-boundary-settlement-phase-b-v0.3.json`
**DEC-054 entrypoint:** `scripts/run_protocol_v2_t526_boundary_settlement_phase_b_v03_windows.ps1`

## Purpose

This runbook executes the first physical-machine portion of T-526 on the accepted thesis host. Hosted CI is intentionally insufficient for this gate because CPU runtime, memory/artifact behavior and method feasibility are part of the evidence being measured.

The first physical pass performs only:

1. dependency/runtime preflight;
2. the complete focused protocol-v2 conformance suite;
3. ordered GridWorld Phase-A discrimination;
4. bounded Q-Learning / SARSA / DQN / PPO / Dyna-Q+ nominal-learning feasibility;
5. actual interaction, probe, wall/CPU-time and checkpoint-size recording;
6. selection of the first non-degenerate GridWorld level using the committed rule.

It does **not** perform final tuning, final experiments, final-reserve access, final statistical inference, UI work or thesis writing.

The Phase-B action-remap/action-failure/observation-corruption calibration candidates are already committed in the same plan but are not executed until the Phase-A physical result identifies a usable GridWorld level and the retained artifacts are reviewed.

## Preconditions

- Run in native Windows PowerShell on the accepted thesis machine.
- Use branch `feat/pre-wp7-protocol-v1.1-ui-rebuild` at the reviewed PR #92 head.
- Working tree must be clean before execution.
- Do not manually edit the committed feasibility JSON.
- Do not create or inspect any v2 final-reserve artifact.
- The output directory must not contain prior retained pilot evidence.

## Command

From the repository root:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_protocol_v2_feasibility_windows.ps1
```

The script itself performs the lock/dependency/test preflight. No manual hyperparameter, seed or environment selection is required.

## Expected retained outputs

The committed plan requires the following under:

`results/pilots/protocol-v2-feasibility-v0.1/`

- `manifest.json`
- `system-capability.json`
- `phase-a-runs.jsonl`
- `level-summary.json`
- `failures.jsonl`

A successful process exit does not imply that every method scientifically succeeded. Failed/unstable method units are retained in `failures.jsonl` and remain part of the feasibility evidence.

`level-summary.json` may legitimately report no selected level. In that case the correct next step is protocol review/amendment, not manual selection of the visually most attractive method ranking.

## Ordered discrimination rule

Levels are evaluated in the committed order:

1. `gw-l1` — 7×7
2. `gw-l2` — 10×10
3. `gw-l3` — 14×14

The runner stops at the first complete level for which both conditions are false:

- **universal final floor:** every core method has median final-probe success ≤ 0.10 across the root-layout units;
- **universal early ceiling:** every core method has median success ≥ 0.90 at interaction 512.

This rule asks only whether the testbed discriminates at a useful difficulty. It never selects a level because a preferred algorithm ranks first.

## Evidence handling after execution

Do not rerun, delete, rename or hand-edit the generated pilot output. Inspect `git status`, retain the entire output directory, and provide/commit those artifacts for review. The next T-526 step will use the selected level and the already-predeclared Phase-B calibration candidates.

The final frontend remains blocked until T-526 and T-527 are complete. T-527 must freeze the retained methods, budgets, hyperparameters, Phase-B episode/reset lifecycle, severities, roots/statistics and machine-readable protocol before T-528 chooses a different framework from NiceGUI and rebuilds the UI.

## Retained physical Phase-A checkpoint (2026-08-29)

The clean physical Windows checkout executed the committed entrypoint exactly once from reviewed source commit `5198dbe077119b7caa4e9a101b55b115a979c22e`.

- Selected level: `gw-l1` (7×7), the first level in the declared ladder. It was neither a universal final floor nor a universal early ceiling.
- Completed units: 30/30 (five core methods × three roots × two layouts).
- Failures: zero scientific failures and zero infrastructure/runtime-guardrail failures.
- Interactions: 61,440 training and 28,524 isolated probe interactions.
- Runtime: 129.344 summed unit wall-seconds and 459.469 summed unit process-CPU-seconds.
- Checkpoint measurement: 4,680,026 aggregate serialized bytes; every unit remained below the warning threshold.
- Retained file bundle: 40,488 bytes under `results/pilots/protocol-v2-feasibility-v0.1/`.
- Validation: exact required file set, declared plan SHA-256, source commit, complete unique unit matrix, interaction/probe budgets, runtime/checkpoint guardrails and copied accepted capability snapshot all passed; `failures.jsonl` is empty.

Do not rerun, delete, rename, replace or hand-edit this evidence.

## Phase-B recovery blocker

The committed Phase-A runner materialized each exact final checkpoint in memory only long enough to record its SHA-256 identity and serialized size. It did not retain checkpoint payload files. The repository also has no committed Phase-B severity-calibration entrypoint or fully specified execution handoff that can consume the one-time trained states.

Consequently, Phase-B cannot proceed faithfully from this retained bundle. Regenerating Phase A would violate the explicit one-time execution boundary, while inventing a new post-outcome handoff/lifecycle would be a protocol amendment. `T-526A` therefore requires explicit scientific review/authority for a non-outcome-driven recovery path that preserves this bundle unchanged, retains only the already-predeclared candidate set and does not access final reserve.

## DEC-052 recovery authorization and lifecycle

DEC-052 supplies that explicit narrow authority. It does not reopen Phase A. The new runner verifies the five original file hashes and requires the declared Phase-A-affecting paths to have no Git diff from source commit `5198dbe077119b7caa4e9a101b55b115a979c22e`. It materializes only the 30 already-selected `gw-l1` checkpoint payloads and compares every scientifically deterministic row field, checkpoint SHA-256 and learner-state SHA-256 exactly. A single mismatch is retained as recovery/infrastructure failure and blocks Phase B.

The amendment freezes the T-526 calibration-only Phase-B lifecycle before execution:

- selected level `gw-l1`, five core methods, three roots and both layouts;
- the two original categorical action remaps, three action-failure probabilities and three observation-corruption probabilities;
- exactly one common nominal no-learning prefix interaction;
- FN/FD/AN/AD forks from the exact same branch point;
- exactly ten actual post-boundary interactions per branch;
- no episode reset.

Both selected layouts have shortest-path length 12, so `1 + 10 = 11 < 12`. None of the declared disturbances can shorten the physical transition graph. This removes reset/terminal ambiguity without freezing the later final lifecycle owned by T-527.

Adaptive PPO begins native rollout collection at the first post-boundary interaction. Its native update quantum remains 128, so the ten-interaction pilot segment performs no premature optimizer update; its exact transient rollout state is hash-retained and is not promoted as a restorable checkpoint.

## Recovery command and reviewed-head gate

Do not run recovery from uncommitted implementation. First commit/push the amendment implementation, wait for green `Repository checks` and `Protocol-v2 pilot checks`, confirm PR #92 points to that commit, and confirm native-Windows Git is clean. Then run from the repository root:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_protocol_v2_t526_recovery_phase_b_windows.ps1
```

The script enforces the physical Windows/branch/clean/current-remote/current-draft-PR/green-check preflight. It creates only:

- `results/pilots/protocol-v2-feasibility-v0.1-recovery/`;
- `results/pilots/protocol-v2-feasibility-phase-b-v0.1/`.

It never writes the original Phase-A directory. Do not rerun, delete, replace or hand-edit generated recovery/Phase-B evidence. Execute all eight candidates; do not select a final severity or preferred remap inside T-526.

## Retained DEC-052 physical recovery attempt (2026-08-29)

The clean physical Windows checkout executed the new entrypoint once from reviewed PR #92 head `5e784d31729ad09c40f2633f3d1682896e624317` after Repository and Protocol-v2 pilot checks were green.

- Original five-file bundle integrity: passed before and after the attempt.
- Phase-A source compatibility with `5198dbe...`: passed for all declared paths.
- Q-Learning / `t526-r01` / `gw-l1-a`: exact checkpoint and learner match.
- SARSA / `t526-r01` / `gw-l1-a`: exact checkpoint and learner match.
- DQN / `t526-r01` / `gw-l1-a`: learner-state SHA exactly matched `bee1cce1...`; canonical checkpoint byte size exactly matched `460571`; reconstructed checkpoint-envelope SHA `7b385564...` did not equal authoritative `f2da03f3...`.
- Barrier result: failed at 2/30 exact matches with one retained infrastructure/recovery failure.
- Phase B: not started; 0/240 matched sets and zero branch interactions.
- Runtime: 16.648 seconds for the retained recovery attempt.
- Recovery artifacts: 499,535 hash-covered bytes under `results/pilots/protocol-v2-feasibility-v0.1-recovery/`; independent failed-attempt integrity/lineage validation passes.

Do not rerun the DEC-052 attempt, alter its evidence or reinterpret the matching learner digest as satisfying DEC-052. At the conclusion of that attempt a new explicit scientific/recovery decision was required. DEC-053 now supplies a separate, versioned authority without rewriting this historical result. The original Phase-A bundle remains authoritative and unchanged.

## DEC-053 SB3 identity correction and v0.2 authority

The technical audit in `T526_SB3_SCIENTIFIC_CONTINUATION_IDENTITY_AUDIT.md` inspected the retained reconstructed DQN archive and SB3 2.9.0 save/load/learn implementation. `_canonicalize_zip()` normalizes the outer ZIP only. The inner SB3 `data` member retains `start_time`, which comes from `time.time_ns()` and affects elapsed-time/FPS logging only. Original Phase A and DEC-052 executed at different times, so that field necessarily differs. SB3 also emits human-readable class fields containing process memory addresses; the loader ignores those display values and restores the separate cloudpickle payload.

Focused tests prove all of the following without a scientific rerun:

- changing only `start_time` changes the raw archive and no other archive field;
- both archives retain and restore the exact same historical learner SHA and DEC-053 derived continuation SHA;
- perturbing online parameters, DQN target parameters, optimizer state, replay contents/cursor/full state, counters or RNG changes/fails the scientific identity;
- changing a schedule definition not directly represented in the historical hash fails the derived invariant barrier;
- DQN `_n_calls` is uniquely determined as `num_timesteps` under the frozen fresh-start, single-environment, one-step callback path and is rejected if unequal;
- PPO policy/value/optimizer/counters/RNG are historically hashed, schedules are explicitly audited, and checkpoints remain restricted to legal completed rollout/update boundaries whose consumed buffer is reset before future collection.

DEC-053 therefore treats raw SB3 archive hashes as retained transport/audit identities, never byte-identical states. Acceptance still requires the exact physically recorded historical learner SHA, exact accounting/probes/configuration/source/provenance, successful restore and post-restore SHA, all explicit continuation invariants and an exact derived round trip. Q-Learning, SARSA and Dyna-Q+ retain the stronger raw-envelope equality requirement.

The versioned reviewed-head command is:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_protocol_v2_t526_recovery_phase_b_v02_windows.ps1
```

It may execute exactly once, only after the implementation/configuration/docs are committed and pushed, both PR #92 checks are green on that exact commit, PR #92 points to it and native Windows Git is clean. It reconstructs all 30 units from unit one and creates only:

- `results/pilots/protocol-v2-feasibility-v0.1-recovery-v0.2/`;
- after 30/30 only, `results/pilots/protocol-v2-feasibility-phase-b-v0.2/`.

Any scientific identity failure is retained and stops the attempt. Phase B remains the unchanged eight-condition, 240-set, 960-branch, 9,600-post-boundary-interaction calibration and cannot begin before 30/30. No additional retry/relaxation, T-527 decision, A2C addition or final-reserve access is authorized.

## Retained DEC-053 physical attempt (2026-08-29)

The clean physical Windows checkout executed the v0.2 entrypoint once from reviewed PR #92 head `167d012a6eb1b0a2a5638836dea73d799128375f` after Repository and Protocol-v2 pilot checks were green.

- Recovery: 30/30 accepted scientific continuation states, zero historical learner-fingerprint mismatches, zero recovery failures and exact serialized byte sizes. Q-Learning, SARSA and Dyna-Q+ retained exact raw-envelope identity. All six DQN and six PPO units retained distinct original/reconstructed raw transport hashes while passing exact learner, restore, round-trip and derived-invariant barriers.
- Recovery runtime/artifacts: 132.519 wall-seconds; 33 hash-covered files and 4,760,652 bytes under `results/pilots/protocol-v2-feasibility-v0.1-recovery-v0.2/`. Independent validation reports `valid-complete`.
- Phase B: all eight Q-Learning conditions for `t526-r01/gw-l1-a` completed, totaling 8/240 matched sets, 32/960 branches, eight common-prefix interactions and 320/9,600 post-boundary interactions.
- Failure: the next planned set, SARSA `t526-r01/gw-l1-a` / `action-remap-swap-right-down`, failed before its prefix. The exact checkpoint retains a deferred on-policy update for state `[1,5]`, action `down`, reward `-0.1`, next state `[1,6]`. The frozen common prefix requires a quiescent no-learning state. Discarding the update would alter the exact continuation state; resolving it would select the next on-policy action and apply learning without an authorized boundary rule.
- Phase-B runtime/artifacts: 1.355 wall-seconds; 3 hash-covered files and 24,957 bytes under `results/pilots/protocol-v2-feasibility-phase-b-v0.2/`. Independent validation reports `valid-failed`, with zero scientific failures and one infrastructure/lifecycle failure at the next contiguous planned set.

Do not rerun, resume, replace or hand-edit either v0.2 evidence directory. T-526A, T-526 and T-527 remain blocked pending a new explicit scientific/lifecycle decision for the SARSA deferred-update boundary. DEC-053 does not authorize silently discarding or resolving that update.

## DEC-054 boundary settlement and fresh Phase-B v0.3 authority

The lifecycle audit in `T526_PHASE_A_BOUNDARY_SETTLEMENT_AUDIT.md` proves that the exact fixed-budget cutoff is an administrative algorithm boundary. Five of six retained SARSA checkpoints contain one deferred nonterminal backup for the already-counted interaction 2,048; all other retained states and one SARSA state are quiescent. Existing SARSA bootstrapped-truncation semantics already select a behavior-policy action solely for the continuation estimate and discard it without execution.

DEC-054 therefore derives a distinct deployment-start state with zero environment interactions. It verifies exact DEC-053 source identity/counters, uses the restored Phase-A epsilon/action order/RNG and deferred `next_state`, applies the one-step SARSA backup once, clears deferred state, retains the advanced exploration RNG and leaves no deployment pending action. Q-Learning, DQN, PPO, Dyna-Q+ and quiescent SARSA are explicit verified no-ops.

After commit/push, green checks on the exact PR #92 head and a clean native Windows worktree, run exactly once:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_protocol_v2_t526_boundary_settlement_phase_b_v03_windows.ps1
```

The entrypoint validates the original Phase-A, DEC-052, DEC-053 recovery v0.2 and failed Phase-B v0.2 trees. It does not execute Phase A or recovery. It creates only:

- `results/pilots/protocol-v2-feasibility-boundary-settlement-v0.1/`;
- after a 30/30 settlement barrier, `results/pilots/protocol-v2-feasibility-phase-b-v0.3/`.

Phase-B v0.3 starts from matched set one and keeps the existing 240-set/960-branch/240-prefix/9,600-post-boundary design exactly. Do not copy v0.2 rows, rerun/resume either attempt, access final reserve or start T-527 before complete validated evidence.
