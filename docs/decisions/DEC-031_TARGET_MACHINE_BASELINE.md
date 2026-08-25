# DEC-031 — Target-Machine Runtime and Acceleration Baseline

**Status:** Accepted

**Date:** 2026-08-25

## Decision

Accept `docs/context/system-capability.accepted.json` and
`docs/context/SYSTEM_CAPABILITY_REPORT.md` as the target-machine capability
baseline.

Use native Windows CPython 3.12 managed by the locked `uv` environment as the
canonical experiment runtime. Preserve CPU execution as the required supported
baseline. Do not add accelerator-specific or deep-learning dependencies merely
because an AMD Radeon RX 570 display adapter with 8 GiB VRAM is present: no
scientific-compute backend for it has been validated, and NVIDIA/CUDA tooling is
absent.

Use Windows Git/Git LFS for LFS-sensitive artifact operations unless the active
shell has a compatible Git LFS installation. Do not mix the Windows virtual
environment with WSL's incompatible system Python.

## Rationale

This baseline is generated from the actual experiment machine and separates
observed hardware from supported compute capability. CPU-first bounded
GridWorld/tabular work fits the measured 6-core/12-thread CPU, approximately
31.9 GiB usable RAM, and current storage while avoiding an unjustified GPU stack.

## Boundaries

This decision unlocks hardware-dependent prototypes and research framing. It
does not freeze the research question, environment choice, agents, metrics,
scenario matrix, seeds, budgets, tuning rules, statistics, or final protocol.
Those remain evidence- and pilot-dependent.

## Reopening conditions

Reopen if the target machine or canonical runtime changes, or if a bounded
prototype demonstrates that a specific acceleration backend is necessary and
compatible enough to reduce overall thesis risk.
