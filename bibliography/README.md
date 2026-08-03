# Bibliography integration

`MariosGiannakaras/ThesisBibliography` is the sole source of truth for bibliography intake, originals, duplicate detection, metadata, OCR/conversion, source Markdown, scientific analysis, evidence verification, selection decisions, `MAT-*` research materials, author notes, corpus generation, and bibliography integrity metadata.

This thesis repository owns research questions, GridWorld and uncertainty design, agent comparison, protocol, implementation, runs, analysis, artifacts, dashboard, thesis text, and presentation. It has no bibliography write-back path and must not download, ingest, OCR, convert, deduplicate, classify, or promote primary sources locally.

## Generated consumer surface

The complete committed upstream `research-corpus/` is installed read-only as `research/bibliography/`. It contains all searchable canonical source Markdown, analyses, available evidence, research materials, notes, aggregates, and catalogs. Original PDFs and Git LFS objects are never copied; `catalog/originals-index.csv` retains their hashes, relationships, paths, and immutable URLs.

`research/bibliography/citation-ready/` is the strict formal-citation layer. A final scientific claim using `SRC-XXXXXXXXXX` must resolve in its manifest and use the corresponding verified evidence with the recorded analysis and limitations. Other canonical sources remain available for internal research but are not silently promoted. `MAT-*` material and metadata-free notes are searchable for discovery and drafting; formal claims still require citation-ready support.

The imported evidence remains in each source's original language. Translation occurs only in thesis writing and never replaces canonical evidence.

## Synchronization

Synchronization uses `.github/workflows/sync-bibliography.yml` with an explicit immutable tag or full SHA. The workflow uses the read-only `BIBLIOGRAPHY_SYNC_TOKEN`, validates the already committed upstream corpus without regenerating it, checks source-commit ancestry and both upstream checksum manifests, installs transactionally, runs consumer tests, and opens a generated-only Pull Request. It never writes to `ThesisBibliography` and never merges directly to `main`.

The consumer-owned `IMPORT_INTEGRITY.json` records requested ref, resolved checkout commit, complete-corpus and citation-ready source commits, timestamp, schema versions, counts, and relevant digests. It supplements rather than replaces the upstream checksum manifests. Manual changes under `research/bibliography/` are rejected.

## Search and references

Use `python scripts/search_bibliography.py QUERY` for deterministic trust-aware local search. Useful filters include `--citation-ready`, `--include-rejected`, `--layer`, `--id`, and `--topic`. The reproducible index is stored only in ignored `.cache/bibliography/`.

`scripts/validate_bibliography_usage.py` distinguishes source identity, internal research references, and formal citations. Internal research documents may reference canonical rejected/theory-only sources and valid `MAT-*` items with explicit trust labels; final/frozen scientific documents may cite only citation-ready `SRC-*` entries and may not use `MAT-*` as formal citations.

## User-provided bibliography material

User-provided PDFs, Markdown files, NotebookLM exports, source lists, and related bibliography inputs are processed in `ThesisBibliography`. They enter this repository only through a later validated immutable synchronization.

Legacy files under `bibliography/` are historical compatibility markers, not an active intake workflow.
