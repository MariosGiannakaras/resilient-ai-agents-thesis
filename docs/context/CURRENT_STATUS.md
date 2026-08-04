# Current Project Status

**Date:** 2026-08-04  
**Status:** Authoritative current-state summary

Active repository files must agree with this state. Historical records may preserve earlier states only when explicitly marked historical. Documentation synchronization is governed by `docs/context/DOCUMENTATION_GOVERNANCE.md`.

## Bibliography integration

The first complete immutable bibliography import is finished.

- Requested ref: `bibliography-integration-v2`
- Resolved checkout: `27e325a74722b8f80643e6d1902e4bf3847036f5`
- Complete-corpus source commit: `ca511a0ff91388e7798e011642cc6b5608b336d8`
- Citation-ready source commit: `ef44fe3c30e6648f591ad9d3546ffc336fce4287`
- Canonical sources: 583
- Citation-ready selected sources: 112
- Research materials: 19
- Indexed original PDFs: 280, metadata only
- Consumer-recorded corpus files: 1561

The private read credential succeeded. All upstream validators, both upstream checksum manifests, consumer integrity, contextual source-reference validation, and repository checks passed for the imported baseline. The former HTTP 401 and incomplete-import blockers are resolved. No bibliography PDF or bibliography LFS object entered this repository.

## Research implementation architecture

DEC-023 establishes the implementation baseline:

- Python 3.12 + `uv` + committed lockfile;
- independent package at `src/resilient_agents/`;
- evaluator-ground-truth versus agent-visible information boundary;
- deterministic independent RNG streams;
- explicit scenario/experiment/protocol contracts without hidden scientific defaults;
- filesystem-first run bundles with provenance, capability snapshot, checksums, events/traces, and summary;
- one guarded automatic Git commit and push per finalized whole experiment, never per seed;
- selective Git LFS for large thesis-produced artifacts;
- useful large result artifacts retained by default while storage permits;
- future Streamlit dashboard as a thin layer only after core/pilot validation.

The actual target-machine inventory is still required before compute-dependent dependency/model/budget choices. The current base core remains CPU-compatible.

## Documentation and Codex execution

The obsolete pre-import `CODEX_BOOTSTRAP_PROMPT.md` has been retired. `docs/context/CODEX_EXECUTION_PROMPT.md` is the only tracked current Codex prompt template and is intentionally state-driven from this file and the roadmap.

For local use, copy the canonical prompt to git-ignored root `CODEX_TASK.md`; the local copy can be deleted after Codex reads it without affecting Git history.

Every material change must reconcile all affected active docs/prompts/status/decision/workflow files in the same PR. Useful historical records are marked historical rather than left as ambiguous current guidance. CI includes a documentation-consistency validator for mechanically detectable stale states.

## Trust model

`research/bibliography/citation-ready/` is the strict formal-citation layer. The complete corpus remains searchable for internal research, terminology, synthesis, rejected/theory-only context, `MAT-*` material, and notes without silent promotion. Promotion is performed only upstream in `ThesisBibliography`, followed by a new immutable synchronization.

## Active bounded work

1. Run and accept the target-system inventory on the actual experiment machine.
2. Complete source-traceable model/agent-family comparison.
3. Complete bounded GridWorld prototype/ADR work and promote the selected environment into `src/resilient_agents/`.
4. Define versioned scenario/change/disturbance schemas and known-answer environment fixtures.
5. Validate metric estimands with synthetic fixtures before complex agent implementation.
6. Define the pilot protocol and implement only the small agent set justified by the research roles.
7. Run pilots before any polished dashboard implementation or final protocol freeze.

The final research question, hypotheses, model set, GridWorld scientific parameters, uncertainty severities, seeds, budgets, hyperparameters, recovery threshold, and statistical plan remain unfrozen.

## Deferred, non-blocking inputs

Supervisor identity, future supervisor corrections, final deadlines, example theses, and Word formatting remain later-stage inputs and do not block current research or implementation.
