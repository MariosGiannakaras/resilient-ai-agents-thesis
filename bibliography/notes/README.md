# Bibliography Notes

Create one structured note per source that is relevant enough to evaluate or cite.

A note is not the full source. It is the controlled analysis layer that explains what the source actually did, what it found and how it relates to this thesis.

## Naming

```text
<src-id-lowercase>__<source-basename>.md
```

Example:

```text
src-rw-001__balloch_2022_novgrid.md
```

## Required front matter

```yaml
source_id:
citation_key:
title:
authors:
year:
venue_or_institution:
doi_or_url:
publication_version:
rights_status:
pdf_path:
pdf_sha256:
markdown_path:
markdown_sha256:
conversion_status: pending  # pending | generated-unverified | verified
review_status: not-read     # not-read | partial | full-text
topics: []
decision_relevance: []
last_verified_utc:
```

Use multiple `topics` rather than copying the same source into multiple physical folders.

Suggested topics include:

- `gridworld-environments`
- `nonstationarity-adaptation`
- `models-baselines`
- `uncertainty-disturbances`
- `metrics-statistics`
- `experimental-protocol`
- `robustness-resilience`
- `thesis-writing-structure`
- `presentation-visuals`

## Note sections

1. **Verified citation and acquired version.**
2. **Review status and conversion quality.**
3. **Research question.**
4. **Method and assumptions.**
5. **Environment/data and experimental design.**
6. **Models/baselines.**
7. **Metrics and statistical treatment.**
8. **Main findings.**
9. **Limitations and threats to validity.**
10. **Relationship to this thesis.**
11. **Possible effect on research scope, model choice or protocol.**
12. **Useful sections/pages/tables/figures.**
13. **Claims this source can support.**
14. **Claims this source does not support.**
15. **Follow-up sources, contradictions or evidence gaps.**
16. **Structural lessons for writing/presentation, when applicable.**

## Rules

- Do not mark `full-text` unless the complete acquired version was actually reviewed.
- Do not preserve a `full-text` status after the PDF or Markdown checksum changes without revalidation.
- Numerical findings must include experimental context, compared baselines and limitations.
- Short quotations require exact page references and verification against the PDF.
- Paraphrases must preserve the source's meaning and caveats.
- NotebookLM or another AI tool may suggest relationships and missing topics, but claims must be checked against the full Markdown/PDF.
- Do not fabricate DOI, venue, page, quotation, metric or result data.

## Relationship to excerpts

A note is source-centric. `../excerpts/` is topic-centric.

After a note is verified, move only the genuinely useful evidence into the appropriate thematic excerpt file with source ID and location. Do not copy the whole note.
