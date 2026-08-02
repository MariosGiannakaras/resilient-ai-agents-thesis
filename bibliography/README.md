# Bibliography integration

The bibliography is no longer acquired, cleaned, converted, analysed, or curated in this repository.

## Source of truth

`MariosGiannakaras/ThesisBibliography` is the independent canonical repository for:

- source discovery and metadata,
- original PDF preservation,
- Markdown conversion and OCR status,
- source-by-source scientific analysis,
- verified citation-ready evidence,
- inclusion/exclusion decisions,
- the controlled thesis export package.

Scientific source text and citation-ready evidence remain in the language of the original source. This repository must not create translated canonical copies.

## What this repository consumes

The thesis repository consumes only the generated, verified package under:

```text
research/bibliography/
```

The import contains only the package produced by the `ThesisBibliography` exporter, plus a generated integrity manifest. It must include an exact `SOURCE_COMMIT`, `manifest.csv`, the selected catalog rows, verified analyses, and verified evidence. It must not contain PDFs, Git LFS objects, raw originals, unverified analyses, or unverified evidence.

The generated directory is replaced only by `scripts/bibliography_import.py` through the PR-based `.github/workflows/sync-bibliography.yml` workflow. Manual edits are rejected by hash validation.

## Writing and citations

Use canonical `SRC-XXXXXXXXXX` identifiers from the imported manifest when connecting thesis claims to evidence. Before using a claim, read the corresponding imported evidence and analysis; open the canonical source in `ThesisBibliography` only when additional source context or primary-text verification is required.

The normal reading order in this repository is:

> imported evidence → imported analysis → canonical source in `ThesisBibliography` when needed

Every canonical `SRC-*` identifier referenced by repository text must exist in the imported manifest.

## Synchronization

Synchronization is pull-based and reviewable:

1. Run **Sync verified thesis bibliography** with an explicit branch, tag, or commit of `ThesisBibliography`.
2. The workflow checks out the private bibliography repository using read-only secret `BIBLIOGRAPHY_SYNC_TOKEN`.
3. The bibliography exporter builds a fresh verified package from that exact commit.
4. The thesis repository validates and transactionally replaces only `research/bibliography/`.
5. The workflow opens a Pull Request; it does not merge directly to `main`.
6. CI validates package integrity and canonical source references before merge.

Do not use a submodule and do not grant this repository write access to `ThesisBibliography`.

## Legacy material

`bibliography/SOURCE_ACQUISITION_WORKFLOW.md` and `scripts/download_open_access_bibliography.py` are retained only as migration/history markers and explicitly block the obsolete local-acquisition workflow. They are not valid bibliography procedures.
