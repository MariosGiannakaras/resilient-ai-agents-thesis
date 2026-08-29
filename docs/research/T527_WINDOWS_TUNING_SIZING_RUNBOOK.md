# T-527 Physical Windows Tuning and Sizing Runbook

**Status:** DEC-055 pre-outcome implementation; physical validation pending  
**Decision:** `docs/decisions/DEC-055_PROTOCOL_V2_FAIR_TUNING_AND_SIZING_AUTHORITY.md`  
**Plan:** `configs/protocols/protocol-v2-t527-tuning-sizing-v0.1.json`  
**Entrypoint:** `scripts/run_protocol_v2_t527_tuning_sizing_windows.ps1`

## Purpose and boundary

This runbook executes the single reviewed T-527 non-final development program on the authoritative native Windows thesis PC. It performs fair six-candidate tuning for each of Q-Learning, SARSA, DQN, PPO and Dyna-Q+, selects one configuration per method mechanically, selects the common Phase-A budget from the declared 4,096/8,192 rule, and performs fresh 24-root precision/runtime sizing on the two development layouts and two primary action remaps.

It never executes T-526 again, never accesses final reserve, never creates final layouts/roots, and never generates confirmatory outcomes. Tuning and sizing evidence are not final thesis evidence.

## Reviewed-head gate

Before execution, the committed entrypoint requires:

- native Windows CPython 3.12 and the locked CPU-only protocol-v2 environment;
- branch `feat/pre-wp7-protocol-v1.1-ui-rebuild`;
- a clean native-Windows worktree;
- local HEAD equal to the fetched remote branch and draft PR #92 head;
- both `Repository checks / sanity` and `Protocol-v2 pilot checks / focused-conformance` green on that exact head;
- successful integrity/lineage validation of every immutable T-526 evidence package;
- the committed deterministic input-diagnostics package;
- absent/empty new tuning and sizing output directories.

## Command

From the repository root in native Windows PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_protocol_v2_t527_tuning_sizing_windows.ps1
```

The entrypoint may execute once. Do not resume or rerun a partial/failed package. A failure is retained and requires explicit scientific or infrastructure review without seed/config replacement.

## Expected evidence

- `results/pilots/protocol-v2-t527-input-diagnostics-v0.1/` — deterministic descriptive T-526 input audit;
- `results/pilots/protocol-v2-t527-tuning-v0.1/` — 180 candidate units, selection scores, runtimes, failures and integrity;
- `results/pilots/protocol-v2-t527-sizing-v0.1/` — 240 selected-config Phase-A sizing units, 480 action-remap matched sets evaluated at both 256 and 512 interactions, deployment-start checkpoints, root precision, runtime and integrity.

Only after these packages validate may DEC-056 freeze the final held-out layouts, final root reserve, final statistics, retained configurations/budgets/conditions and the machine-readable protocol-v2.0 firewall. DEC-056 does not execute that reserve.
