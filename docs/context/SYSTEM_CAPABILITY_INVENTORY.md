# System Capability Inventory

**Status:** schema-v2 collector and target-system baseline accepted under `T-100`/`T-101`.

## Purpose

The thesis must base feasibility decisions on the actual machine used for development and final experiments, not on assumptions, a GitHub Actions runner, ChatGPT infrastructure, or an unrelated development host.

`scripts/system_inventory.py` provides a small standard-library-only collector for that purpose.

## Privacy boundary

The collector intentionally does **not** record:

- username or account name,
- hostname,
- IP/MAC/network configuration,
- home-directory paths,
- environment-variable dumps,
- machine/installation identifiers,
- serial numbers.

The report contains only capability-relevant information: OS, architecture, Python runtime, logical CPU count/model when available, total RAM, filesystem capacity, selected tool/package versions, repository commit/cleanliness, and NVIDIA GPU/VRAM/driver data when `nvidia-smi` is available and succeeds.

Schema version 2 enumerates Windows display adapters from the display-class registry in addition to the NVIDIA `nvidia-smi` probe. It prefers the full-width `HardwareInformation.qwMemorySize` value because legacy `AdapterRAM`/`HardwareInformation.MemorySize` values may saturate near 4 GiB. Non-Windows non-NVIDIA GPU families are not enumerated; their absence is therefore **not evidence that no accelerator exists**.

## Run on the target machine

From a clean checkout of this repository:

```bash
python scripts/system_inventory.py --output docs/context/system-capability.local.json
```

The local file is gitignored by design. It is an inspection artifact until reviewed.

The collector can also print the JSON directly:

```bash
python scripts/system_inventory.py
```

## Acceptance procedure

The report becomes project evidence only after all of the following are true:

1. It was generated on the machine that will actually run the thesis development/pilot/final experiments, or the report explicitly records a later approved target machine.
2. The repository commit in the report is known and the collector itself is present at that commit.
3. The values are inspected for obvious probe failures or misleading omissions.
4. GPU conclusions respect the supported-probe boundary; an empty NVIDIA device list is not generalized to all accelerator families.
5. The reviewed capability summary is recorded in project context/decision documentation and used to bound prototype/model/experiment choices.
6. If a raw JSON snapshot is committed later, it is added deliberately under a stable reviewed filename rather than by unignoring the local scratch file.

## Current decision impact

The accepted target-system report is
`docs/context/SYSTEM_CAPABILITY_REPORT.md`, backed by the stable generated JSON
snapshot `docs/context/system-capability.accepted.json`. DEC-030 applies its
runtime/dependency implications.

The accepted baseline requires:

- CPU-compatible GridWorld and model prototypes;
- no CUDA/NVIDIA or AMD scientific-compute assumption;
- no model selection merely because a display adapter exists;
- no GitHub Actions runner hardware recorded as thesis hardware;
- no frozen training budgets or runtime feasibility claims before prototypes and pilots.

## Schema summary

The JSON top-level fields are:

- `schema_version`
- `collected_at_utc`
- `privacy_policy`
- `system`
- `cpu`
- `memory`
- `storage`
- `accelerators`
- `tools`
- `python_packages`
- `repository`

The collector uses atomic file replacement when `--output` is provided. Missing optional probes are represented by `null`, an empty device list, or an explicit unsupported-probe note instead of invented values.
