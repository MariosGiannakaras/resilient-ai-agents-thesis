# Accepted Target-Machine Capability Report

**Status:** Accepted target-machine baseline

**Collected:** 2026-08-25 19:44:21 UTC

**Tasks:** `T-100`, `T-101`

## Evidence and provenance

The automatically generated, privacy-reviewed source snapshot is
`docs/context/system-capability.accepted.json` (schema version 2).

- Collector/source commit: `a4d349e838c8900d3b1885b7f962a4248f20209b`
- Snapshot SHA-256: `26e006d1c36651d961404e8e0a11a710664a4fd516c9149b2e15c00a2eaa458d`
- Repository state at collection: clean (`tracked_changes_present: false`)
- Privacy policy: no user, host, network, machine, installation, path, or serial identifiers

The report was generated with the committed collector on the Windows host that
will be used for thesis development, pilots, and final experiments. The local
scratch snapshot remains ignored; the stable accepted JSON is committed
deliberately as project evidence.

## Measured capability

| Area | Accepted observation |
|---|---|
| Host OS | Windows 10, build `10.0.19045`, AMD64 |
| CPU | AMD Ryzen 5 2600X, 6 physical cores / 12 logical processors |
| RAM | 34,276,913,152 bytes (about 31.9 GiB usable) |
| Repository filesystem | 1,000,186,310,656 bytes total; 181,834,334,208 bytes (about 169.4 GiB) free at collection |
| Display adapter | Radeon RX 570 Series, 8 GiB VRAM from the full-width registry value, driver `31.0.21923.11000` |
| NVIDIA/CUDA | `nvidia-smi` absent; no NVIDIA device reported; `nvcc` absent |
| Project runtime | CPython 3.12.13 managed by `uv` 0.10.10 |
| Repository tooling | Git 2.55.0 for Windows; Git LFS 3.7.1 available; Node 24.7.0 present but not part of the headless-core baseline |
| Optional scientific packages | NumPy, SciPy, pandas, PyTorch, Gymnasium, and MiniGrid are not yet installed in the locked project environment |

## Privacy and probe review

The stable JSON was inspected directly and searched for forbidden names,
hostnames, network identifiers, home/user paths, machine IDs, serial numbers,
and environment dumps. None are present. The only matching privacy terms occur
in the explicit privacy-policy value.

The legacy Windows `AdapterRAM` probe reported approximately 4 GiB for the
display adapter, while the driver registry's full-width
`HardwareInformation.qwMemorySize` reports 8 GiB. Schema v2 records the latter
and its source, avoiding the known 32-bit saturation problem. The exact CPU
description and physical-core count were also verified against read-only
Windows system probes.

## Accepted runtime and dependency constraints (`T-101`)

1. The canonical experiment runtime is native Windows CPython 3.12 managed from
   the committed `uv.lock`. Reproducible commands use `uv sync --frozen` and
   `uv run --frozen ...` from a Windows-capable shell. WSL's system Python 3.10
   is not a compatible project runtime and must not share this Windows virtual
   environment.
2. CPU execution remains the required supported baseline for the custom versus
   reuse GridWorld prototypes, agent prototypes, tests, and pilots. The measured
   CPU/RAM/storage are adequate to begin bounded tabular/CPU-compatible work;
   they do not determine final matrix size, seeds, budgets, or methods before
   prototypes and pilots.
3. The Radeon adapter is accepted hardware evidence, not evidence of a usable
   scientific-compute backend. No CUDA toolchain exists, and no AMD/DirectML
   backend has been installed or validated for this project. Therefore no
   CUDA-, ROCm-, DirectML-, PyTorch-, or deep-learning runtime dependency is
   added at this gate.
4. Windows Git LFS is available for future configured large artifacts. Git/LFS
   operations involving LFS-managed files must use a shell where the matching
   Git LFS executable is available; the current WSL Git emits a missing-LFS
   hook warning and is not the accepted path for LFS-sensitive publication.
5. Storage is sufficient for the next bounded phases but is not an unlimited
   retention guarantee. Run bundles retain useful evidence under the existing
   policy, and free space is rechecked before pilots/final campaigns.

These decisions resolve only compute-dependent runtime/tooling constraints.
They do not freeze the RQ, GridWorld implementation, agent set, metrics,
severities, seeds, budgets, hyperparameters, statistical plan, or protocol.

## Reopening conditions

Regenerate and review the inventory if the experiment host, OS, CPU/RAM/GPU,
storage target, Python/toolchain, or intended acceleration backend materially
changes. Any future accelerator-specific dependency requires a bounded
compatibility prototype and explicit evidence that it reduces thesis risk or
runtime enough to justify its portability and maintenance cost.

## Validation performed

- focused inventory unit tests: 7 passed;
- live schema-v2 collector probe: passed;
- clean-commit/provenance, schema, VRAM, and JSON invariants: passed;
- forbidden-identifier privacy scan and manual review: passed;
- documentation consistency validator: passed before the collector checkpoint;
- full repository checks passed after final documentation reconciliation (51 tests passed, 1 platform-specific symlink test skipped; bibliography/integrity/JSON checks passed).
