# DEC-022 — Accept the Immutable Full-Corpus Baseline

**Status:** Accepted  
**Date:** 2026-08-04

## Decision

Accept `bibliography-integration-v2` at checkout `27e325a74722b8f80643e6d1902e4bf3847036f5` as the first complete immutable bibliography consumer baseline.

The complete-corpus source commit is `ca511a0ff91388e7798e011642cc6b5608b336d8`. The nested strict citation-ready source commit is `ef44fe3c30e6648f591ad9d3546ffc336fce4287`.

## Rationale

The import passed private read verification, all upstream validators, ancestry validation, both SHA-256 manifests, consumer integrity, contextual source-reference validation, and supported-Python CI. It contains complete searchable text while preserving `citation-ready/` as the only formal-citation surface.

## Boundary

This decision implements DEC-021 and preserves DEC-017. It does not promote rejected, theory-only, `MAT-*`, or note content. It does not freeze any research question, model, GridWorld implementation, metric, severity, seed count, budget, hyperparameter, threshold, or final protocol.
