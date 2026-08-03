# Bibliography Integration Contract

**Status:** active project architecture  
**Canonical bibliography repository:** `MariosGiannakaras/ThesisBibliography`

## Ownership boundary

`ThesisBibliography` owns discovery, intake, original PDFs, content-based duplicate handling, metadata, OCR/conversion, canonical source Markdown, conversion review, scientific analysis, evidence verification, selection status, otherwise-uncovered `MAT-*` material, author notes, corpus generation, and bibliography integrity metadata.

`resilient-ai-agents-thesis` owns the research design, GridWorld, uncertainty mechanisms, agents, experimental protocol, implementation, runs/results, statistics, artifacts, dashboard, thesis, and presentation. There is no submodule, write-back path, or local primary-source processing workflow.

## Imported surface and trust

The consumer installs the complete committed upstream `research-corpus/` byte-for-byte under `research/bibliography/`, plus consumer-owned `IMPORT_INTEGRITY.json`. The corpus exposes sources, analyses, evidence, materials, notes, aggregates, catalogs, and the nested `citation-ready/` package. PDFs, LFS objects/pointers, originals, intake/conversion workspaces, caches, temporary files, and upstream history are forbidden.

Accessibility and citation trust are separate:

- `citation-ready/` is the only automatic formal-citation layer. Final claims using `SRC-*` must resolve in its manifest and use verified evidence with analysis/limitations.
- the full corpus remains searchable for discovery, terminology, comparison, synthesis, drafting, and identifying upstream promotion needs;
- rejected and theory-only sources stay accessible without being promoted;
- `MAT-*` items preserve research material but are not formal citations unless promoted upstream and re-synchronized;
- notes require no bibliographic identity, but claims derived from them require citation-ready support.

Canonical evidence remains in the original source language.

## Provenance

A valid package may be committed later than the source snapshots recorded inside it. The importer therefore records and validates separately:

1. requested immutable tag/full SHA;
2. resolved checkout commit;
3. complete-corpus `SOURCE_COMMIT` and adjacent metadata `source_commit`;
4. citation-ready `SOURCE_COMMIT` and adjacent metadata `source_commit`;
5. ancestry of both source commits to the checkout commit;
6. both upstream SHA-256 manifests and their exact path sets;
7. import timestamp, consumer schema, counts, and metadata/checksum digests.

Checkout commit equality with either package source commit is not required. Generated upstream files are never modified to manufacture equality.

## Synchronization

`.github/workflows/sync-bibliography.yml` accepts only an explicit immutable tag or full SHA. For the initial migration it uses `bibliography-integration-v2`, which resolves to `27e325a74722b8f80643e6d1902e4bf3847036f5`.

The workflow:

1. reads the immutable ref from dispatch input or `.bibliography-sync-trigger`;
2. verifies read-only access to `research-corpus/catalog/package-metadata.json` without exposing the secret;
3. checks out both repositories with full history, bibliography LFS disabled, and bibliography credentials not persisted;
4. proves the ref is a tag/full SHA and records the exact checkout;
5. runs all upstream validators;
6. copies the already committed corpus without regeneration;
7. validates structure, trust semantics, counts, IDs, source-commit ancestry, UTF-8, forbidden artifacts, transactionality, and both checksum manifests;
8. installs only `research/bibliography/`, runs consumer validation/tests, and opens a generated-only PR;
9. never merges directly to `main` and never writes upstream.

The initial baseline acceptance check is 583 canonical sources, 112 citation-ready sources, 19 research materials, 280 indexed original PDFs, and upstream schema version 1. These values are not permanent logic; later imports validate their own metadata dynamically.

## Search and validation

`scripts/search_bibliography.py` provides deterministic local search across source, analysis, evidence, material, note, and aggregate layers with explicit trust labels. Its index is reproducible and ignored.

`scripts/validate_bibliography_usage.py` applies context-sensitive rules: final thesis/frozen scientific documents permit only citation-ready `SRC-*`; internal research documents may reference any canonical `SRC-*` and registered `MAT-*`, but unknown IDs always fail.

Freshness searches and any source/material promotion occur only in `ThesisBibliography`, followed by a new immutable synchronization.
