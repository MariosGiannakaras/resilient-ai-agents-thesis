# Current Project Status

**Date:** 2026-08-26
**Status:** Authoritative current-state summary

This file is intentionally short. Detailed policy, history, requirements, and design rationale live in the source-of-truth documents routed by `AGENTS.md`; do not grow this file into a second project manual.

## Current execution state

- Canonical concrete ledger: `docs/context/TASKS.md`.
- `T-100` and `T-101` were accepted and squash-merged in PR #55 (`45e04cd`).
- `T-102` was objectively reviewed, CI-validated, and squash-merged in PR #57 (`48f7124`); the accepted snapshot now cites durable merged-main source provenance.
- Current work package: **WP2 — Research framing**.
- `T-200` passed canonical CI and objective diff review, then squash-merged through PR #58 (`67bb423`).
- `T-210` passed canonical CI and objective review, then squash-merged through PR #60 (`ff3b970`).
- DEC-032 completes `T-211` locally on `research/gridworld-implementation-adr`: the selected path is a small project-owned GridWorld using the locked Gymnasium 1.3.0 API through the accepted core contracts; MiniGrid is not a core dependency, and scientific parameters remain unfrozen.
- Current task: **`T-212`**, ready after the `T-211` PR is CI-validated, objectively reviewed, squash-merged, and synchronized to main.
- Exact next action: validate/review the `T-211` decision reconciliation, push/open its PR, complete canonical CI/review/merge, then implement the selected GridWorld in `src/resilient_agents/`.
- No scientific RQ/environment/model/metric/protocol choice was frozen by the hardware baseline.

## Accepted repository / Codex baseline

- Python 3.12 + `uv` + committed lockfile.
- Independent research package: `src/resilient_agents/`.
- Ground-truth/agent-visible information boundary and independent deterministic RNG streams are established.
- Filesystem-first run bundles, provenance/checksums, selective Git LFS, and guarded one-commit/one-push publication per finalized whole experiment are established.
- Run publication fails closed on inconsistent finalization/checksums/index/provenance; analysis exclusion remains separate from the original execution outcome.
- Untracked non-output repository inputs are treated as dirty source provenance; generated `results/**`/`artifacts/**` do not create a false source-dirty state.
- Future Streamlit UI remains a thin layer over the validated headless core after pilots.

Codex uses progressive disclosure: the session-start core is exactly `AGENTS.md`, `TASKS.md`, and this file. The canonical tracked execution bootstrap is `docs/context/CODEX_EXECUTION_PROMPT.md`. Goal mode persists across the canonical lifecycle: routine task completion, PR creation, CI, objective diff review, squash merge, reconciliation, and next-task selection are autonomous execution steps rather than stop conditions when available permissions and repository policy allow them. Only genuinely external/user-only gates pause the goal.

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

The actual target-machine baseline is accepted in `SYSTEM_CAPABILITY_REPORT.md` and the generated schema-v2 snapshot `system-capability.accepted.json` (DEC-031). The machine provides a Ryzen 5 2600X (6 cores/12 threads), about 31.9 GiB usable RAM, a Radeon RX 570 with 8 GiB VRAM, and about 169.4 GiB free on the repository filesystem at collection. The canonical runtime is native Windows CPython 3.12 managed by the locked `uv` environment. CPU execution remains mandatory; NVIDIA/CUDA is absent and no AMD scientific-compute backend is validated, so no accelerator-specific dependency is accepted yet.

## Lifecycle gates

The accepted sequence remains:

> target-machine baseline → research framing/GridWorld → metrics/agent selection → pilots → protocol/statistical-plan freeze → experiment management/dashboard → validated application → final experiment campaign → frozen evidence/statistics → thesis evidence package → Greek thesis/review/freeze → defense presentation → final audit/delivery

The application is complete only after the intended real configure/run/monitor/history/compare/export workflow and the self-explanatory UX/onboarding criteria are validated on the same scientific core. Final experiments then use the frozen protocol through that validated core/workflow. Writing and presentation claims later trace to a frozen evidence package plus citation-ready literature.

## Still intentionally unfrozen

The T-200 construct-level RQ/hypothesis framing is complete but remains explicitly provisional. Final operational RQ/hypotheses, GridWorld scientific parameters, model/agent set, uncertainty severities, seeds/repetitions, budgets, hyperparameters, recovery threshold, experiment matrix, and statistical plan remain evidence/pilot dependent.

Supervisor identity, future corrections, deadlines, example theses, final Word formatting, and exact defense/submission rules are later-stage inputs and do not block current implementation. Current official guidance is rechecked at the explicit writing/defense tasks.

## Repository visibility

The thesis repository may be temporarily public at explicit user direction to use public GitHub Actions. Public CI availability is an operational choice, not approval for permanent public release; privacy, copyright/licensing, source-material, secret, provenance, and final-release checks remain required before any intended public distribution.
