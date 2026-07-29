# Source Acquisition Workflow

## Goal

Collect the actual papers used by the project in a lawful, traceable and reproducible way without turning the bibliography folder into an uncurated archive.

## Storage layout

```text
bibliography/original/related-work/   Original lawful PDF copies
bibliography/markdown/                Searchable conversions when needed
bibliography/notes/                   Structured reading notes and evidence extraction
bibliography/source_manifest.json     Download/source/checksum register
```

Do not commit publisher PDFs whose redistribution or local storage is not permitted. The private repository does not remove copyright obligations.

## Acquisition rules

### Automatically downloadable

Codex may download a paper when at least one of the following is true:

- official open-access proceedings provide the PDF,
- arXiv or another author-provided preprint is publicly available,
- the publisher page explicitly marks the paper open access,
- an institutional repository provides a lawful author manuscript.

For every downloaded file record:

- title and authors,
- publication year and venue,
- DOI or stable URL,
- version type: version of record, accepted manuscript or preprint,
- access/license note,
- retrieval date,
- local path,
- SHA-256,
- whether full-text review is complete.

### User-assisted download

When only a paywalled version is available:

1. Record the DOI and official publisher page.
2. Search for a lawful author manuscript or institutional repository copy.
3. If none is found, ask the user to obtain it through the university library, the author or another lawful route.
4. After the user adds the file, calculate SHA-256 and update the manifest.

Do not use Sci-Hub, unofficial mirrors or links whose legality/provenance cannot be established.

## Initial curated acquisition list

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

Run `scripts/download_open_access_bibliography.py` after cloning to acquire the entries with verified direct PDF URLs and generate/update the local manifest.

## Reading-note template

Create one note per decision-driving paper under `bibliography/notes/`:

```markdown
# Citation

## Publication status and source

## Research question

## Environment / data

## Compared methods

## Experimental protocol

## Metrics and statistics

## Main results

## Limitations / threats to validity

## Relevance to this thesis

## Claims safe to cite

## Claims not supported by the paper
```

## Literature refresh gates

### Gate A — Initial research design

Search and acquire papers for:

- GridWorld novelty/non-stationarity,
- action failure or transition stochasticity,
- observation/reward corruption,
- recovery and adaptation metrics,
- fair multi-seed RL comparison,
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
- Extract exact methods, experiment counts, results and limitations.
- Add papers needed to compare the project’s findings with prior results.
- Do not write from abstracts alone.

### Gate D — Before submission

- Check for major recent publications.
- Verify every DOI, author list, year, venue and citation.
- Recheck the official university template and submission instructions.

## Scope control

A paper is added because it supports a concrete research, methodology, validity or discussion need. Do not collect hundreds of loosely related PDFs. A smaller verified evidence base is preferable to a large unread archive.