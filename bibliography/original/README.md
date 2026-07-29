# Original Bibliography Sources

Αυτός ο φάκελος είναι το immutable archive των αρχικών πηγών.

## Περιεχόμενο

```text
original/related-work/   Papers, reports, standards and official documentation
original/theses/         Comparable theses and dissertations
```

Τα αρχεία διατηρούνται ως archival backup και verification source. Δεν αποτελούν το καθημερινό working format των agents.

## Κανόνες

- Preserve every accepted PDF unchanged after acquisition.
- Use collision-safe lowercase filenames: `<first_author>_<year>_<short_title>[__<version_token>].pdf`.
- A version token is required when multiple preprint/revision/publication forms of the same work are retained.
- Never overwrite a retained PDF with another revision. Use tokens such as `arxiv-v2`, `accepted`, `vor` or `rev-YYYYMMDD` and keep each version separately traceable.
- Record official URL/DOI/handle, retrieval date, version, access provenance, rights/license status and SHA-256.
- Commit only lawfully acquired files whose repository storage is permitted.
- Review file size and GitHub/Git LFS limits before committing large theses or collections.
- Store the complete searchable conversion under `../markdown/` with the exact same version-specific basename.
- Store source analysis under `../notes/` and active thematic evidence under `../excerpts/`.

## Usage policy

The normal reading order is:

> excerpts → structured note → complete Markdown → original PDF only when verification is required

Open the PDF only for:

- exact page or quotation verification,
- tables, figures, equations or captions that did not convert correctly,
- checking a suspicious extraction,
- resolving differences between source revisions.

Do not include this folder in routine whole-bibliography agent reading.

## Retention

Keep valid source PDFs even when only part of their content is useful. Delete only documented duplicates, corrupted files or wrong sources. A newer legitimate revision does not automatically replace or delete an earlier retained version.

The authoritative bibliography policy is in `../README.md` and acquisition details are in `../SOURCE_ACQUISITION_WORKFLOW.md`.
