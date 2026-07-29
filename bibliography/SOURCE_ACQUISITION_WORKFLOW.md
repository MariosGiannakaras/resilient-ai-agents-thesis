# Source Acquisition Workflow

## Goal

Collect the actual papers and comparable theses used by the project in a lawful, traceable and reproducible way without turning the bibliography folder into an uncurated archive.

The authoritative storage, naming, classification and reading policy is in `bibliography/README.md`.

## Source hierarchy

```text
bibliography/original/related-work/   Immutable lawful paper/report PDFs
bibliography/original/theses/         Immutable lawful thesis/dissertation PDFs
bibliography/markdown/related-work/   Complete searchable paper Markdown copies
bibliography/markdown/theses/         Complete searchable thesis Markdown copies
bibliography/notes/                   Source-centric structured analysis
bibliography/excerpts/                Topic-centric useful evidence
bibliography/source_manifest.json     Acquired PDF/version/checksum register
```

The working hierarchy is:

> thematic excerpts → structured note → complete Markdown → original PDF only for verification

Original PDFs are retained as archival backups when storage rights and repository limits permit. They are not part of routine agent reading.

## Acquisition rules

### Automatically downloadable

Codex may download a source when at least one of the following is true:

- official open-access proceedings provide the PDF,
- arXiv or another author-provided preprint is publicly available,
- the publisher page explicitly marks the source open access,
- an institutional repository provides a lawful author manuscript or thesis.

**Access is not the same as redistribution permission.** Until an applicable license or repository policy is verified, downloaded files are treated as local-research-use-only and are not committed or redistributed.

For every acquired PDF, the acquisition manifest records:

- stable source ID,
- title and complete verified author list,
- publication year and venue/institution,
- DOI, handle or stable official URL,
- version type: version of record, accepted manuscript, preprint or thesis,
- access provenance,
- separate rights/license status, including `unknown/local-use-only` when not verified,
- retrieval date,
- local PDF path,
- PDF SHA-256,
- full-text review status for that exact PDF revision.

The manifest is updated atomically. Existing user-acquired records are preserved. A full-text review flag is retained only when the PDF checksum is unchanged.

Markdown path/checksum, conversion status, semantic topics, note path and excerpt usage are stored in the structured note/front matter rather than in downloader-managed manifest fields. This prevents later acquisition refreshes from silently discarding analysis metadata.

### User-assisted or NotebookLM-discovered sources

When the user uploads PDFs, Markdown exports, citation lists or NotebookLM-discovered material:

1. Inspect the actual content rather than trusting the uploaded filename.
2. Resolve canonical title, complete authors, year, DOI/URL and version status.
3. Detect duplicates, alternate versions and superseded revisions.
4. Identify which research topics are covered and which evidence gaps remain.
5. Rename and classify files immediately according to `bibliography/README.md`.
6. Preserve the original PDF unchanged and compute SHA-256.
7. Update the acquisition manifest with the exact PDF archive record.
8. Preserve the complete Markdown as a separate searchable archive copy with the same basename.
9. Link the Markdown to the PDF checksum in the structured note/front matter.
10. Validate page markers, headings, tables, figures, equations, references and reported values.
11. Create/update the structured note and thematic excerpts.
12. Update the related-work matrix and coverage/gap analysis where relevant.

NotebookLM may help discover sources, summarize relationships and reveal missing coverage, but it is not treated as the primary evidence source. Claims are verified against the acquired full text.

### Paywalled or non-direct sources

When only a paywalled or non-direct version is available:

1. Record the DOI/handle and official publisher or institutional page.
2. Search for a lawful author manuscript or institutional repository copy.
3. If none is found or direct automated download is unreliable, ask the user to obtain it through the university library, official repository, author or another lawful route.
4. After the user adds the file, calculate SHA-256, record rights status and complete the normal intake workflow.

Do not use Sci-Hub, unofficial mirrors or links whose legality/provenance cannot be established.

## Naming and classification

PDF and complete Markdown use the same lowercase `snake_case` basename:

```text
<first_author>_<year>_<short_descriptive_title>.pdf
<first_author>_<year>_<short_descriptive_title>.md
```

Physical archive folders separate papers/reports from theses/dissertations. Content classification uses multiple `topics` in the structured note, because a source may support several areas such as models, uncertainty, metrics and GridWorld design.

Do not create duplicate source files for multiple topics.

## Complete Markdown conversion

The complete Markdown is the default searchable full-text copy, not a summary.

Required properties:

- exact link to the PDF path and checksum,
- title, authors and section order preserved,
- page markers where reliable,
- tables/equations/captions/references preserved or clearly marked when conversion is incomplete,
- explicit OCR/extraction warnings,
- conversion tool/version/date,
- Markdown SHA-256,
- conversion state `generated-unverified` or `verified`.

Before marking a conversion verified, compare representative sections and every figure/table/equation/result that may be used in the thesis against the PDF.

## Notes and useful excerpts

Create one source-centric note under `bibliography/notes/` for every decision-driving or citation-relevant source.

Create topic-centric evidence files under `bibliography/excerpts/` only when verified useful content exists. Each entry includes source ID, page/section/table/figure location, evidence type, intended use and necessary caveats.

Do not copy the entire source or note into excerpts. Keep the active evidence set small and relevant.

## Initial curated paper acquisition list

These sources are relevant enough to download and read during the first research phase. Inclusion here does **not** make their methods mandatory.

| ID | Suggested filename | Official/open source | Acquisition |
|---|---|---|---|
| SRC-RW-001 | `balloch_2022_novgrid.pdf` | `https://arxiv.org/pdf/2203.12117` | Auto-download open preprint |
| SRC-RW-002 | `leike_2017_ai_safety_gridworlds.pdf` | `https://arxiv.org/pdf/1711.09883` | Auto-download open preprint |
| SRC-RW-003 | `benjamins_2021_carl.pdf` | `https://arxiv.org/pdf/2110.02102` | Auto-download open preprint |
| SRC-RW-004 | `sutton_1990_dyna.pdf` | `https://papers.nips.cc/paper_files/paper/1990/file/d9fc5b73a8d78fad3d6dffe419384e70-Paper.pdf` | Auto-download official proceedings PDF |
| SRC-RW-005 | `steinparz_2022_reactive_exploration.pdf` | `https://proceedings.mlr.press/v199/steinparz22a/steinparz22a.pdf` | Auto-download official PMLR PDF |
| SRC-RW-006 | `cheung_2020_nonstationary_mdp.pdf` | `https://proceedings.mlr.press/v119/cheung20a/cheung20a.pdf` | Auto-download official PMLR PDF |
| SRC-RW-007 | `wei_luo_2021_nonstationary_blackbox.pdf` | `https://proceedings.mlr.press/v134/wei21b/wei21b.pdf` | Auto-download official PMLR PDF |
| SRC-RW-008 | `de_la_rosa_2025_morphin.pdf` | `https://arxiv.org/pdf/2601.20714` | Auto-download author preprint; record conference status |
| SRC-RW-009 | `luo_2022_escp.pdf` | `https://doi.org/10.1609/aaai.v36i7.20730` | Prefer official AAAI PDF; if automated retrieval fails, ask user to download from the official page |
| SRC-RW-010 | `alami_2023_change_point_detection.pdf` | `https://proceedings.mlr.press/v232/alami23a/alami23a.pdf` | Auto-download official PMLR PDF |
| SRC-RW-011 | `tessler_2019_action_robust_rl.pdf` | `https://arxiv.org/pdf/1901.09184` | Auto-download open preprint |
| SRC-RW-012 | `zhang_2020_state_adversarial_mdp.pdf` | `https://arxiv.org/pdf/2003.08938` | Auto-download open preprint |
| SRC-RW-013 | `peng_2024_complexity_nonstationary_rl.pdf` | `https://proceedings.mlr.press/v237/peng24a/peng24a.pdf` | Auto-download official PMLR PDF |

## Comparable thesis/dissertation acquisition list

| ID | Suggested filename | Official/open source | Acquisition |
|---|---|---|---|
| SRC-THESIS-001 | `balloch_2024_sudden_environmental_change_dissertation.pdf` | `https://arxiv.org/pdf/2505.10330` | Auto-download open manuscript; verify against Georgia Tech record `https://hdl.handle.net/1853/76967` |
| SRC-THESIS-002 | `liu_2024_nonstationary_rl_thesis.pdf` | `https://opus.lib.uts.edu.au/bitstream/10453/186408/1/thesis.pdf` | Auto-download official open institutional thesis |
| SRC-THESIS-003 | `nasereddin_2020_gridworld_variability_dissertation.pdf` | `https://doi.org/10.31390/gradschool_dissertations.5431` | Official LSU repository; user/Codex follows the official download page if direct retrieval is unavailable |
| SRC-THESIS-004 | `grooten_2026_adaptive_rl_dissertation.pdf` | Official TU/e research portal record | User/Codex follows the official open-access document link and records license/version |

## Running the downloader

Python 3.9 or newer is required and verified in GitHub Actions.

```bash
python scripts/download_open_access_bibliography.py
```

The script acquires entries with verified direct PDF URLs into `bibliography/original/`, validates them and generates or safely refreshes the local acquisition manifest. A mismatched/untracked cached PDF is quarantined before a fresh authoritative download is attempted.

The downloader does not convert PDFs to Markdown, assign semantic topics or mark a source as fully reviewed without checksum-bound evidence.

## Literature refresh gates

### Gate A — Initial research design

Search and acquire sources for:

- GridWorld novelty/non-stationarity,
- action failure or transition stochasticity,
- observation/reward corruption,
- recovery and adaptation metrics,
- fair multi-seed RL comparison,
- specific candidate models/baselines,
- comparable dissertations/theses for structure and reporting,
- simple local research dashboards only as implementation examples.

### Gate B — Before pilot/final protocol freeze

Search again for recent primary studies that could change:

- the uncertainty taxonomy,
- the minimal model/baseline set,
- primary outcomes,
- seed/repetition/statistical choices,
- GridWorld framework decision.

### Gate C — Before writing Related Work, Methodology and Discussion

- Fully read all decision-driving papers.
- Inspect comparable theses for chapter structure, experimental tables, limitation reporting and how results are connected to research questions.
- Extract exact methods, experiment counts, results and limitations.
- Add sources needed to compare the project's findings with prior results.
- Use NotebookLM gap/correlation suggestions only as discovery input and verify them against source text.
- Do not write from abstracts alone.

### Gate D — Before submission

- Check for major recent publications and theses.
- Verify every DOI/handle, author list, year, venue/institution and citation.
- Recheck source checksums and claims used in final text/slides.
- Recheck the official university template and submission instructions.

## Scope control

A source is added because it supports a concrete research, methodology, validity, writing-structure, result-comparison or presentation need. Do not collect hundreds of loosely related PDFs.

Keep complete valid source archives, but keep the active notes/excerpts evidence base small, verified and directly useful.
