# DEC-021 — Complete research-corpus import with strict citation sublayer

- **Date:** 2026-08-04
- **Status:** Accepted
- **Supersedes:** the citation-only imported-surface assumption within DEC-017; DEC-017's repository ownership boundary remains accepted.

## Context

The canonical bibliography repository now publishes a complete committed `research-corpus/` containing all canonical source text, analyses, available evidence, otherwise-uncovered `MAT-*` materials, notes, aggregates, catalogs, and a nested verified citation package. Restricting the thesis repository to only selected citation-ready sources would hide useful research context and conflate accessibility with formal-citation trust.

The package's source snapshots may precede the later repository commit or tag that commits the generated corpus. Requiring package `SOURCE_COMMIT` equality with checkout commit is therefore incorrect.

## Decision

- Import the complete committed upstream `research-corpus/` read-only under `research/bibliography/`.
- Preserve `citation-ready/` as the only automatic formal-citation layer.
- Keep rejected, theory-only, non-citation evidence, `MAT-*` material, and metadata-free notes searchable without silent promotion.
- Require upstream promotion and a new synchronization before non-citation material becomes formal evidence.
- Record requested immutable ref, resolved checkout, complete-corpus source commit, citation-ready source commit, counts, timestamp, consumer schema, and integrity digests separately.
- Validate both source commits as ancestors of the checkout, rather than requiring equality.
- Preserve both authoritative upstream SHA-256 manifests; consumer integrity supplements them and detects manual post-import changes.
- Synchronize only from an immutable tag/full SHA through a read-only, PR-based workflow. Do not regenerate upstream content, import PDFs/LFS objects, merge automatically, or create any write path upstream.
- Provide deterministic trust-aware local search and context-sensitive `SRC-*`/`MAT-*` reference validation.

## Consequences

The complete corpus is available for research and drafting without lowering citation standards. Generated imports are larger but remain text-only, reproducible, integrity-checked, and marked as generated. Source ingestion and promotion remain exclusively upstream. Historical pre-import research documents stay historical and are not rewritten as though they originally carried source-ID traceability.

## Alternatives rejected

- citation-only consumer surface;
- treating every accessible source as citation-ready;
- deleting rejected/theory-only sources or unidentified materials;
- package source commit equals checkout commit;
- mutable `main` synchronization;
- regenerating the corpus in the thesis workflow;
- copying PDFs/LFS objects;
- embeddings, vector databases, cloud retrieval, or opaque committed indexes.
