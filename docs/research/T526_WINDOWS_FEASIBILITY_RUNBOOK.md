# T-526 Physical Windows Feasibility Runbook

**Status:** one-time Phase-A complete; Phase-B blocked on explicit checkpoint-handoff recovery review
**Plan:** `configs/protocols/protocol-v2-feasibility-v0.1.json`  
**Entrypoint:** `scripts/run_protocol_v2_feasibility_windows.ps1`

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
