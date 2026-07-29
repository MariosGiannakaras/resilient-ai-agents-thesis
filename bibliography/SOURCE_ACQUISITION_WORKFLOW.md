# Source Acquisition Workflow

## Goal

Collect the actual papers and comparable theses used by the project in a lawful, traceable and reproducible way without turning the bibliography folder into an uncurated archive.

## Storage layout

```text
bibliography/original/related-work/   Original lawful paper PDF copies
bibliography/original/theses/         Comparable lawful thesis/dissertation PDFs
bibliography/markdown/                Searchable conversions when needed
bibliography/notes/                   Structured reading notes and evidence extraction
bibliography/source_manifest.json     Download/source/checksum register
```

Do not commit publisher PDFs whose redistribution or local storage is not permitted. The private repository does not remove copyright obligations.

Large theses may be downloaded locally for review, but before committing them inspect file size, license and repository policy. Use Git LFS or keep a source record without the binary when appropriate.

## Acquisition rules

### Automatically downloadable

Codex may download a source when at least one of the following is true:

- official open-access proceedings provide the PDF,
- arXiv or another author-provided preprint is publicly available,
- the publisher page explicitly marks the source open access,
- an institutional repository provides a lawful author manuscript or thesis.

For every downloaded file record:

- title and authors,
- publication year and venue/institution,
- DOI, handle or stable URL,
- version type: version of record, accepted manuscript, preprint or thesis,
- access/license note,
- retrieval date,
- local path,
- SHA-256,
- whether full-text review is complete.

### User-assisted download

When only a paywalled or non-direct version is available:

1. Record the DOI/handle and official publisher or institutional page.
2. Search for a lawful author manuscript or institutional repository copy.
3. If none is found or direct automated download is unreliable, ask the user to obtain it through the university library, official repository, author or another lawful route.
4. After the user adds the file, calculate SHA-256 and update the manifest.

Do not use Sci-Hub, unofficial mirrors or links whose legality/provenance cannot be established.

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

Run `scripts/download_open_access_bibliography.py` after cloning to acquire entries with verified direct PDF URLs and generate/update the local manifest.

## Reading-note template

Create one note per decision-driving paper or thesis under `bibliography/notes/`:

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

## Structural lessons for writing (theses only)

## Claims safe to cite

## Claims not supported by the source
```

## Literature refresh gates

### Gate A — Initial research design

Search and acquire sources for:

- GridWorld novelty/non-stationarity,
- action failure or transition stochasticity,
- observation/reward corruption,
- recovery and adaptation metrics,
- fair multi-seed RL comparison,
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
- Add sources needed to compare the project’s findings with prior results.
- Do not write from abstracts alone.

### Gate D — Before submission

- Check for major recent publications and theses.
- Verify every DOI/handle, author list, year, venue/institution and citation.
- Recheck the official university template and submission instructions.

## Scope control

A source is added because it supports a concrete research, methodology, validity, writing-structure or discussion need. Do not collect hundreds of loosely related PDFs. A smaller verified evidence base is preferable to a large unread archive.