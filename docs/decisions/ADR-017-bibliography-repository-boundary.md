# ADR-017 — Separate canonical bibliography repository

**Date:** 2026-08-02  
**Status:** Accepted by user

## Context

The thesis repository originally contained an acquisition/archive workflow for papers, PDFs, Markdown conversions, structured notes, and excerpts. During the bibliography work this responsibility moved to the dedicated private `MariosGiannakaras/ThesisBibliography` repository, where the corpus was normalized, reviewed source-by-source, and exported through a verified selection gate.

Keeping both repositories capable of acquiring and curating primary sources would create duplicate sources of truth, divergent identifiers, inconsistent review status, and unnecessary binary/storage duplication.

## Decision

1. `MariosGiannakaras/ThesisBibliography` is the canonical source of truth for the complete bibliography lifecycle.
2. `MariosGiannakaras/resilient-ai-agents-thesis` consumes only the verified generated thesis package under `research/bibliography/`.
3. The repositories keep separate Git histories; no submodule is used.
4. Synchronization is pull-based, pinned to an exact bibliography commit, validated, and delivered through a Pull Request to the thesis repository.
5. The thesis repository has no write path into `ThesisBibliography`; the sync credential is read-only.
6. Primary PDFs, raw source archives, conversion workspaces, unverified analyses, and unverified evidence are not imported into the thesis repository.
7. Canonical source-derived scientific text and citation-ready evidence remain in the original source language. Translation is a thesis-writing operation, not a bibliography transformation.
8. Canonical citation linkage uses the exported `SRC-XXXXXXXXXX` identifiers and exact `SOURCE_COMMIT`.
9. Literature freshness gates remain required, but source discovery/review occurs in `ThesisBibliography` and reaches the thesis repo only through a new verified export.

## Superseded decisions

This ADR supersedes the repository-location and local-acquisition parts of:

- **DEC-001** where “repository as source of truth” previously included the full bibliography lifecycle,
- the bibliography download/acquisition implementation in **DEC-014**,
- **DEC-016 — Original PDF archive with Markdown-first bibliography workflow** as an architecture of the thesis repository.

The scientific principles in those decisions remain valid where applicable: lawful acquisition, original-source preservation, provenance, Markdown/searchability, staged literature refresh, and source verification. Their implementation now belongs to `ThesisBibliography`.

## Consequences

- No new primary bibliography material is added under the thesis repository's legacy `bibliography/` workspace.
- The old downloader is blocked and the old acquisition document is retained only as a historical marker.
- `research/bibliography/` is generated and integrity-checked; manual changes fail validation.
- Research framing, model/metric/GridWorld decisions, writing, and citation checks read the imported verified analyses/evidence rather than an independently curated main-repo bibliography.
- A read-only repository secret or equivalent GitHub App credential is required for automated cross-private-repository synchronization.

## Validation

The integration must verify:

- exact bibliography `SOURCE_COMMIT`,
- manifest/catalog/analysis/evidence set equality,
- absence of PDFs, Git LFS pointers, raw originals, and other forbidden artifacts,
- SHA-256 integrity of every generated imported file,
- every canonical `SRC-*` reference in thesis repository text exists in the imported manifest.

## Related files

- `docs/context/BIBLIOGRAPHY_INTEGRATION.md`
- `bibliography/README.md`
- `scripts/bibliography_import.py`
- `scripts/validate_bibliography_usage.py`
- `.github/workflows/sync-bibliography.yml`
- `.github/workflows/validate-bibliography-import.yml`
