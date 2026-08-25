# DEC-030 — Quota-efficient fail-fast validation

- **Date:** 2026-08-25
- **Status:** Accepted.

## Decision

Implementation and validation must minimize model quota, local repetition, and GitHub Actions waste without weakening scientific or correctness safeguards.

- Codex uses the smallest targeted validators/tests during implementation.
- When GitHub Actions is available, pull-request CI is the canonical full-suite pre-merge verification; Codex does not run the full suite locally merely to duplicate CI.
- Successful CI is treated as a conclusion, not as material for repeated log analysis. Detailed logs are inspected only for failed, cancelled, or ambiguous checks.
- Local full-suite runs are reserved for unavailable CI, CI/test-infrastructure changes where local reproduction is useful, or debugging a specific failure.
- Adjacent dependency-valid tasks may share one coherent branch/PR when no scientific, review, user-decision, external-machine, or protocol-freeze gate separates them.
- CI remains a single bounded job with superseded-run cancellation, a hard timeout, cheap deterministic preflight checks before expensive setup/tests where practical, and compact success output while preserving clear failure diagnostics.
- Pure generated `results/**` / `artifacts/**` pushes may skip the full repository suite; PRs and any push containing source/config/protocol/bibliography/test/active-document changes retain complete validation.
- Required configuration, contracts, schemas, provenance, lifecycle preconditions, and scientific invariants fail closed at clear boundaries before expensive work. Required failures must not be swallowed or converted into defaults/empty results/apparent success.
- Optional probes may report explicit `unavailable` or `unsupported` states only when genuinely non-fatal, and downstream logic must not treat those states as affirmative evidence.
- Finalization is atomic/transactional where practical so partial output cannot masquerade as valid finalized evidence.
- Validation should not be repeated in hot loops when one trusted boundary check is sufficient.
- Codex gives concise user-facing progress updates at meaningful completed/validated checkpoints rather than narrating every command. When an objective finite denominator exists, progress is reported as `X/Y`; otherwise no artificial fraction is invented.
- Progress fractions are derived from real canonical state: top-level/project and work-package/deliverable counts come from `TASKS.md`, while a lower-level active-task fraction is shown only when that task has a real finite substep set. In-progress/failed work never counts as complete.

## Rationale

The thesis needs strong scientific invariants, but model quota and execution time should be spent on implementation, research decisions, and genuine failures rather than duplicated full-suite runs, verbose successful logs, micro-PR overhead, repeated validation of already-trusted state, or noisy low-value status narration. Concise repository-derived progress keeps long Codex sessions understandable without creating a second tracking system.

## Non-goals

This decision does not reduce required scientific-invariant coverage, permit false passes, weaken bibliography integrity checks, replace pilot/final experiment validation with unit tests, or authorize invented progress percentages.