# Constraints

## Compute and hardware

- Actual hardware/software inventory is not a user-supplied blocker. Codex must collect it automatically from the execution system.
- Until inventory and capability benchmarks are complete, the safe baseline is CPU-compatible execution.
- Do not assume NVIDIA, CUDA, usable ROCm, or an unlimited compute budget.
- Old references to a specific CPU/GPU are historical hints only and must not drive decisions until verified on the real system.
- The final experiment matrix must remain practically executable on the actual hardware or on an explicitly approved alternative environment.

## Execution and deployment

- Local, single-user operation.
- No required public deployment, cloud infrastructure, mobile client, multi-user authentication, or distributed orchestration.
- Normal research workflows must work offline after dependencies and required project inputs are installed.

## Research scope

- The official topic requires a simple simulated environment, comparison under uncertainty/dynamic change, resilience, and recovery speed.
- Exact operationalization, GridWorld implementation, model set, metrics, and protocol are not frozen.
- Old conversations are not used as a shortlist or defaults.
- Every selection requires current bibliography/technical evidence and a documented decision.

## GridWorld and third-party code

- There is no requirement to recover an old codebase.
- Third-party code is downloaded/integrated only after source, license, maintenance, security, API, testability, determinism, and suitability review.
- Every dependency or copied/adapted component requires a pinned version/commit and attribution.
- A custom implementation remains an equal option and is preferred when it reduces total complexity without sacrificing scientific validity.

## Reproducibility and data

- Every run requires seed/config/version/hardware/software provenance.
- Raw results are immutable.
- Failures, cancellations, interruptions, and exclusions are retained.
- Final figures/tables are generated only through version-controlled processing from real data.
- Large files require a documented retention/LFS/external-storage policy before large batches are committed.

## Privacy and repository

- The repository remains private while it contains the unredacted official application and personal information.
- Tokens, passwords, API keys, credentials, and local secrets are forbidden.
- Raw conversation exports are not stored in the repository.
- Any public release requires a privacy/license audit and redaction first.

## Academic delivery

- No final deadline is currently known.
- The current Word template and submission package remain unverified.
- Supervisor-specific instructions, when provided, are recorded and override generic conventions where applicable.