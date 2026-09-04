# Thesis text review and provenance pack

## Purpose

This is a student-facing review aid for the current reader-facing Word thesis. It is not a scientific source and it does not change the manuscript, frozen results, bibliography or evidence.

The pack is generated from the exact review DOCX plus its QA report with:

```bash
python scripts/export_thesis_text_review_pack.py \
  --docx artifacts/t711/resilient-ai-agents-thesis-review-ready.docx \
  --qa artifacts/t711/qa-report.json \
  --output artifacts/thesis-text-review-pack
```

It separates the complete reader-visible thesis into manageable files and records the provenance of each paragraph/table block.

## Generated structure

- `chapters/` — complete text separated into front matter, Chapters 1–7, bibliography and appendices.
- `categories/` — the same complete blocks regrouped by provenance category.
- `sources/` — one file for each formal IEEE reference, including its `SRC-*` identity, reader-visible bibliography entry and the thesis blocks that cite it.
- `sources/SOURCE_INDEX.md` — citation-number ↔ `SRC-*` ↔ thesis-block map.
- `sources/ONLINE_AND_OFFICIAL_WEB_GUIDANCE.md` — distinguishes verified scientific bibliography from official web/compliance guidance and example-thesis structure evidence.
- `data/paragraph_ledger.csv` — machine-readable block-level ledger.
- `FULL_THESIS_TEXT_FOR_REVIEW.md` — complete plain reader-visible text in one file for search/checking.

## Provenance labels

The labels are deliberately descriptive rather than claims of literal authorship of individual sentences:

- `AI-assisted synthesis` — prose composed/synthesized for the thesis; not a verbatim translation from a single source.
- `externally supported` — the block contains one or more formal bibliography citations.
- `project methodology/protocol fact` — grounded in the frozen study protocol/project records.
- `project implementation fact` — grounded in the implemented GridWorld/backend/PySide6 system.
- `frozen experiment result` — grounded in accepted T-611/T-612/T-613 evidence.
- `derived from frozen results` — interpretation/conclusion based on accepted results.
- `project provenance/traceability fact` — evidence/repository lineage rather than literature.

A block can carry more than one label.

## External-source originals

The pack does not duplicate entire copyrighted publications. Each source file points to:

- `research/bibliography/citation-ready/evidence/SRC-*.md`;
- `research/bibliography/citation-ready/analyses/SRC-*.md`;
- the verified original/DOI/arXiv/URL recorded there.

The canonical bibliography repository remains `MariosGiannakaras/ThesisBibliography`. The thesis repository consumes that evidence read-only.

## Citations and bibliography

The Word thesis uses IEEE-style numeric in-text citations such as `[1]`, `[5]`, etc. Those are the **παραπομπές / citations**. The complete formatted entries appear in the final **Βιβλιογραφία / references** section. The QA build requires all visible formal citations to resolve to the immutable citation-ready bibliography layer.

## Intended use

Use this pack to understand and verify every paragraph, read the underlying sources where appropriate, and rewrite the thesis in the student's own genuine wording while preserving factual meaning, numerical results and citations. It is not intended to remove or disguise source attribution, and rewritten literature-backed claims must retain the appropriate citations.
