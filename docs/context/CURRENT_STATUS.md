# Current Project Status

**Date:** 2026-08-25
**Status:** Authoritative current-state summary

This file is intentionally short. Detailed policy, history, requirements, and design rationale live in the source-of-truth documents routed by `AGENTS.md`; do not grow this file into a second project manual.

## Current execution state

- Canonical concrete ledger: `docs/context/TASKS.md`.
- Current work package: **WP1 — Target-machine baseline**.
- Current tasks: **`T-100`** and **`T-101`** complete on branch `feat/target-machine-baseline` in PR #55.
- Current state: review/merge gate after accepting the actual-machine capability and runtime baseline.
- Exact next action: review and squash-merge PR #55, then start the first dependency-valid task, `T-200`; `T-210` is also ready but remains later in canonical task order.
- No scientific RQ/environment/model/metric/protocol choice was frozen by the hardware baseline.

## Accepted repository / Codex baseline

- Python 3.12 + `uv` + committed lockfile.
- Independent research package: `src/resilient_agents/`.
- Ground-truth/agent-visible information boundary and independent deterministic RNG streams are established.
- Filesystem-first run bundles, provenance/checksums, selective Git LFS, and guarded one-commit/one-push publication per finalized whole experiment are established.
- Run publication fails closed on inconsistent finalization/checksums/index/provenance; analysis exclusion remains separate from the original execution outcome.
- Untracked non-output repository inputs are treated as dirty source provenance; generated `results/**`/`artifacts/**` do not create a false source-dirty state.
- Future Streamlit UI remains a thin layer over the validated headless core after pilots.

Codex uses a progressive-disclosure bootstrap: the session-start core is exactly `AGENTS.md`, `TASKS.md`, and this file. `AGENTS.md` is a compact routing/control file; task-specific specifications are opened only when needed. The canonical tracked execution bootstrap is `docs/context/CODEX_EXECUTION_PROMPT.md`, and Goal mode is the long-horizon wrapper that continues across successive dependency-valid bounded scopes until a genuine gate requires input or no valid work remains before that gate.

Testing is risk-based and proportional: targeted local checks while implementing, PR CI as the canonical full-suite pre-merge guard when available, no duplicate full-suite runs for reassurance, and no arbitrary coverage/mutation/fuzz/property/combinatorial expansion without a concrete risk.

Codex reports objective `X/Y` progress only from real denominators in `TASKS.md` and preserves recoverable `IN_PROGRESS`/branch checkpoints across interruptions.

## Bibliography baseline

`MariosGiannakaras/ThesisBibliography` remains the canonical bibliography source of truth and is currently private. The accepted immutable thesis import is `bibliography-integration-v3`:

- resolved checkout: `71995373ae0da64149583cae8d7a2c17e5ab1a0a`
- complete-corpus source: `e46693d4201cf47c118eb61c216243f3c5798e28`
- citation-ready source: `822891fb585c98dbe4464602e97998704d1609c5`
- 585 canonical sources; 113 citation-ready; 19 research materials
- 281 indexed original PDFs as metadata only; 1,568 integrity-covered consumer files

`research/bibliography/citation-ready/` is the strict automatic formal-citation layer. Upstream promotion/refresh occurs in `ThesisBibliography`, followed by a new immutable synchronization; primary bibliography originals/PDFs/LFS objects are not copied here.

## Target-machine baseline

The actual target-machine baseline is accepted in `SYSTEM_CAPABILITY_REPORT.md`
and the generated schema-v2 snapshot `system-capability.accepted.json` (DEC-031).
The machine provides a Ryzen 5 2600X (6 cores/12 threads), about 31.9 GiB usable
RAM, a Radeon RX 570 with 8 GiB VRAM, and about 169.4 GiB free on the repository
filesystem at collection. The canonical runtime is native Windows CPython 3.12
managed by the locked `uv` environment. CPU execution remains mandatory;
NVIDIA/CUDA is absent and no AMD scientific-compute backend is validated, so no
accelerator-specific dependency is accepted yet.

## Lifecycle gates

The accepted sequence remains:

> target-machine baseline → research framing/GridWorld → metrics/agent selection → pilots → protocol/statistical-plan freeze → experiment management/dashboard → validated application → final experiment campaign → frozen evidence/statistics → thesis evidence package → Greek thesis/review/freeze → defense presentation → final audit/delivery

The application is complete only after the intended real configure/run/monitor/history/compare/export workflow and the self-explanatory UX/onboarding criteria are validated on the same scientific core. Final experiments then use the frozen protocol through that validated core/workflow. Writing and presentation claims later trace to a frozen evidence package plus citation-ready literature.

## Still intentionally unfrozen

Final RQ/hypotheses, GridWorld scientific parameters, model/agent set, uncertainty severities, seeds/repetitions, budgets, hyperparameters, recovery threshold, experiment matrix, and statistical plan remain evidence/pilot dependent.

Supervisor identity, future corrections, deadlines, example theses, final Word formatting, and exact defense/submission rules are later-stage inputs and do not block current implementation. Current official guidance is rechecked at the explicit writing/defense tasks.

## Repository visibility

The thesis repository may be temporarily public at explicit user direction to use public GitHub Actions. Public CI availability is an operational choice, not approval for permanent public release; privacy, copyright/licensing, source-material, secret, provenance, and final-release checks remain required before any intended public distribution.
