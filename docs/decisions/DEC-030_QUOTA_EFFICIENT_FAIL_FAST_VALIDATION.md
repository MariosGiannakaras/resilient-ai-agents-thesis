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
- Pure `main` pushes containing only finalized `results/**` and/or generated `artifacts/**` do not rerun the full code/bibliography suite. Pull requests remain fully checked, and any mixed push containing a non-ignored path still triggers the complete repository workflow. Result validity remains protected by the guarded publisher/run-bundle contracts and the later explicit evidence-validation/freeze gates; this optimization must never be extended to source, config, protocol, bibliography, test, or active documentation paths.
- Required configuration, contracts, schemas, provenance, lifecycle preconditions, and scientific invariants fail closed at clear boundaries before expensive work. Required failures must not be swallowed or converted into defaults/empty results/apparent success.
- Optional probes may report explicit `unavailable` or `unsupported` states only when genuinely non-fatal, and downstream logic must not treat those states as affirmative evidence.
- Finalization is atomic/transactional where practical so partial output cannot masquerade as valid finalized evidence.
- Validation should not be repeated in hot loops when one trusted boundary check is sufficient.

## Rationale

The thesis needs strong scientific invariants, but model quota and execution time should be spent on implementation, research decisions, and genuine failures rather than duplicated full-suite runs, verbose successful logs, micro-PR overhead, repeated validation of already-trusted state, or full code-suite runs triggered by data-only experiment publication.

## Non-goals

This decision does not reduce required scientific-invariant coverage, permit false passes, weaken bibliography integrity checks, or replace pilot/final experiment validation with unit tests.
