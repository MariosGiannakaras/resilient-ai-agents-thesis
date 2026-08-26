# Current Project Status

**Date:** 2026-08-26
**Status:** Authoritative current-state summary

This file is intentionally short. Detailed policy, history, requirements, and design rationale live in the source-of-truth documents routed by `AGENTS.md`; do not grow this file into a second project manual.

## Current execution state

- Canonical concrete ledger: `docs/context/TASKS.md`.
- `T-100` and `T-101` were accepted and squash-merged in PR #55 (`45e04cd`).
- `T-102` was objectively reviewed, CI-validated, and squash-merged in PR #57 (`48f7124`); the accepted snapshot now cites durable merged-main source provenance.
- Current work package: **WP4 — Pilot protocol and headless experiment system**.
- `T-200` passed canonical CI and objective diff review, then squash-merged through PR #58 (`67bb423`).
- `T-210` passed canonical CI and objective review, then squash-merged through PR #60 (`ff3b970`).
- DEC-032 completed `T-211`, passed canonical CI/review, and squash-merged through PR #61 (`9df6787`).
- `T-212`/`T-213` passed canonical CI/review and squash-merged through PR #62 (`e7352d5`).
- `T-300`/`T-301` passed canonical CI/review and squash-merged through PR #63 (`25f67bb`).
- `T-310`/`T-311` passed canonical CI/review and squash-merged through PR #64 (`e7d97a5`).
- `T-312` passed canonical CI/review and squash-merged through PR #65 (`6f596a3`).
- `T-400` passed canonical CI/review and squash-merged through PR #66 (`1502bfd`).
- `T-401` passed canonical CI/review and squash-merged through PR #67 (`8ddfcc2`).
- `T-402` passed canonical CI/review and squash-merged through PR #68 (`34ca10b`).
- `T-410` completed the bounded pilot lifecycle. PR #71 (`1b94ebb`) merged the v0.2 amendment; all 14 PV02 children are published and the validated analysis contains 336 units plus 18,144 sensitivity records with no v0.2 failure/exclusion. The retained v0.1 failure and superseded attempts remain explicit.
- Pilot evidence confirms CPU/runtime/storage feasibility but makes two final-freeze constraints mandatory: R0's current configuration has approximately 96% nominal truncation and recovery classification varies across metric settings in 33/42 agent-condition-layout cells. No final claim or favorable threshold/model selection is allowed from these diagnostics.
- `T-411` freshness review completed in canonical `ThesisBibliography`; no new evidence required protocol change.
- `T-412` completed; protocol is objectively frozen with deterministic seeds and statistical analysis plan.
- `T-500` corrective audit completed: experiment_manager uses canonical FINALIZATION_MARKER from run_bundle.py, full integrity validation (checksums, marker-manifest agreement, run-id identity), tests use real RunBundle finalization semantics.
- `T-510` corrective repair completed: Compare/Artifacts pages operate on real data, lifecycle gate protects final reserve, protocol eligibility is validated, and resource telemetry uses the actual schema.
- `T-511` completed: post-execution UI validation verified and explicitly logged.
- `T-600` completed: 14 execution commits preserved durably in `archive/final-campaign-execution`.
- `T-601` completed: freeze manifest validates exact file bytes and provenance reachability.
- `T-602` completed: reproducible analysis generated exactly 896 valid units.
- `T-603` completed: generated artifacts and primary metric figures.
- `T-604` completed: evidence package constructed with claim-to-result mapping.
- Current work package: **WP7 — Thesis writing, review, and defense presentation** (DEFERRED).
- Current task: **`T-700`**, deferred. Exact next action: Hand off to the human user for thesis drafting.
- All autonomous execution work is completed.

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
