# DEC-023 — Research Core, Reproducible Runs, and Automatic Publication

**Status:** Accepted  
**Date:** 2026-08-04

## Decision

Adopt:

- Python 3.12 as the project execution baseline;
- `uv`, `pyproject.toml`, `.python-version`, and committed `uv.lock` for reproducible environment management;
- `src/resilient_agents/` as the independent importable research package;
- strict evaluator-ground-truth versus agent-visible information separation;
- independently derived deterministic RNG streams;
- explicit scenario/experiment/protocol contracts with no hidden scientific defaults;
- filesystem-first self-contained experiment bundles;
- one automatic Git commit and push per finalized whole experiment, never per seed;
- selective Git LFS for large thesis-produced artifacts;
- a thin Streamlit dashboard only after the headless core and pilots establish the real workflow.

## Rationale

The architecture maximizes reproducibility and auditability while keeping the application a bounded local research tool. Automatic result publication removes routine manual Git work without allowing unrelated changes or ambiguous provenance into experiment commits.

## Boundaries

This decision does not freeze the research questions, final model set, GridWorld scientific parameters, uncertainty severities, seed count, budgets, hyperparameters, recovery threshold, statistical plan, or final protocol.

DEC-031 satisfies the actual thesis-machine inventory gate and keeps CPU execution as the required supported baseline. Dependency additions beyond the zero-runtime-dependency core still require relevant prototypes and must not assume an unvalidated accelerator backend.
