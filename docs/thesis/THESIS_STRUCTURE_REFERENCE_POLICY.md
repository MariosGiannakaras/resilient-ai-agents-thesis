# Thesis Structure and Authoring Reference Policy

**Status:** Active WP7 reference policy. The explicit pre-WP7 user approval gate was satisfied on 2026-09-03; T-700 and T-701 are complete. This policy controls how official guidance and contextual example theses may influence the manuscript without becoming scientific evidence.

## Purpose

Define how official Department/University guidance, supervisor instructions and completed example theses are used for **structure, presentation, formatting, academic register and document conventions**. These materials do not supply scientific evidence for the resilient-agent research claims.

## Authority order

When sources disagree, use this order:

1. current official Department/University requirements verified at T-700 and rechecked later where required;
2. explicit current supervisor instructions supplied by the user;
3. `docs/thesis/THESIS_REQUIREMENTS.md`;
4. `docs/thesis/THESIS_STRUCTURE_AND_STYLE_GUIDE.md`, derived by T-701 from contextual examples and project scientific needs;
5. individual example-thesis conventions.

Example theses never override official requirements and never become scientific sources merely because their format is useful.

## T-700 official-reference disposition

The known ICE references were re-verified on 2026-09-03. The dated result is:

`docs/thesis/OFFICIAL_GUIDANCE_SNAPSHOT_2026-09-03.md`

The principal current public references remain:

### ICE-THESIS-GUIDE — Department thesis-writing instructions

- Role: primary Department structural/format reference.
- URL: `https://ice.uniwa.gr/wp-content/uploads/2022/06/%CE%9220_04_03_%CE%9F%CE%94%CE%97%CE%93%CE%99%CE%95%CE%A3-%CE%A3%CE%A5%CE%93%CE%93%CE%A1%CE%91%CE%A6%CE%97%CE%A3-%CE%94%CE%99%CE%A0%CE%9B%CE%A9%CE%9C%CE%91%CE%A4%CE%99%CE%9A%CE%97%CE%A3-%CE%95%CE%A1%CE%93%CE%91%CE%A3%CE%99%CE%91%CE%A3_%CE%A4%CE%9C%CE%A0%CE%A5.pdf`
- T-700 result: no newer public ICE document was found that supersedes it for the checked thesis-writing requirements.

### ICE-PPS-REGULATION — Internal undergraduate-programme regulation

- Role: institutional definition and obligations of the Diploma Thesis.
- URL: `https://ice.uniwa.gr/wp-content/uploads/2022/12/%CE%95%CF%83%CF%89%CF%84%CE%B5%CF%81%CE%B9%CE%BA%CF%8C%CF%82-%CE%9A%CE%B1%CE%BD%CE%BF%CE%BD%CE%B9%CF%83%CE%BC%CF%8C%CF%82-%CE%9B%CE%B5%CE%B9%CF%84%CE%BF%CF%85%CF%81%CE%B3%CE%AF%CE%B1%CF%82-%CF%84%CE%BF%CF%85-%CE%A0%CE%A0%CE%A3-%CE%A4%CE%9C%CE%A0%CE%A5.pdf`
- Relevant authority: Article 28; individual thesis, 30 ECTS, scientific/systematic character, plagiarism/author-declaration and examination obligations.

### ICE-PPS — Five-year programme of studies

- Role: programme context/formal position of the Diploma Thesis.
- Known public URL: `https://ice.uniwa.gr/wp-content/uploads/2022/01/%CE%A4%CE%9C%CE%97%CE%9C%CE%91-%CE%9C%CE%97%CE%A7%CE%91%CE%9D%CE%99%CE%9A%CE%A9%CE%9D-%CE%A0%CE%9B%CE%97%CE%A1%CE%9F%CE%A6%CE%9F%CE%A1%CE%99%CE%9A%CE%97%CE%A3-%CE%9A%CE%91%CE%99-%CE%A5%CE%A0%CE%9F%CE%9B%CE%9F%CE%93%CE%99%CE%A3%CE%A4%CE%A9%CE%9D-%CE%A0%CE%91%CE%94%CE%91_%CE%A0%CE%A0%CE%A3.pdf`
- Known content places the Diploma Thesis in the tenth semester with 30 ECTS.

### ICE-TECHNICAL-WRITING — Technical Writing course specification

- Role: supplementary Department-level writing-quality reference, not a thesis regulation.
- Known public URL: `https://ice.uniwa.gr/wp-content/uploads/2019/07/14072019-%CE%9C%CE%97%CE%A7_%CE%A0%CE%9B%CE%97%CE%A1_%CE%A5%CE%A0%CE%9B-%CE%A0%CE%A3-5-%CE%95%CE%A4%CE%95%CE%A3-%CE%A0%CE%95%CE%A1%CE%99%CE%93%CE%A1%CE%91%CE%9C%CE%9C%CE%91%CE%A4%CE%91.pdf`
- Role remains supplementary only.

## Example-thesis input policy and actual T-701 corpus

Example theses may be supplied through a local ignored folder or directly to the analysis conversation/tooling. In either case, the originals remain **out of the thesis repository** unless redistribution is explicitly requested and appropriate.

The T-701 review used 22 user-supplied files provided as conversation sources rather than committed repository files. Integrity review established that two files (`example-theses 1.pdf` and `example-theses 10.pdf`) are byte-identical, so the comparative corpus contains **21 unique completed theses**.

The originals:

- are not copied into `ThesisBibliography`;
- are not committed to this repository;
- are not citation-ready scientific sources;
- are not used for subject-matter claims, figures, data or results.

Additional example theses independently discovered later may be used only under the scope restrictions then in force; current official/supervisor requirements continue to outrank them.

## T-701 comparative-review result

T-701 reviewed the supplied examples across:

- front-matter order and declarations;
- chapter/subchapter hierarchy and balance;
- introduction/problem/contribution framing;
- theoretical background and related-work organization;
- methodology versus implementation separation;
- experimental design, Results, Discussion, conclusions and future work;
- technical depth and explanatory pacing;
- figure/table/chart/screenshot density and role;
- caption/numbering/cross-reference conventions;
- equation/code/pseudocode treatment;
- bibliography/reference presentation;
- glossary/acronym/index conventions;
- appendix use;
- limitations/validity treatment;
- academic register and recurring document/layout conventions;
- patterns that conflict with current official guidance or do not fit this research-first project.

The output is:

`docs/thesis/THESIS_STRUCTURE_AND_STYLE_GUIDE.md`

Its principal project decision is a seven-chapter research-first structure:

1. Introduction;
2. Background and Related Work;
3. Methodology and Experimental Design;
4. Research-System Architecture and Implementation;
5. Results;
6. Discussion;
7. Conclusions and Future Work.

A separate Discussion chapter is deliberately stricter than common historical example practice because the accepted T-612 analysis contains three distinct RQs/estimands, paired method contrasts, uncertainty intervals, recovery sensitivity and explicit right-censoring.

## Citation-style boundary

Current ICE guidance permits multiple consistent citation systems rather than mandating a single one. T-700/T-701 select IEEE numeric referencing as this project’s WP7 default because it fits the engineering/AI literature and is the dominant convention among the technically closest contextual examples reviewed.

This is a **project writing decision**, not an official ICE mandate. A later explicit supervisor or Department instruction supersedes it and triggers a controlled citation/reference conversion and audit.

## Copyright / privacy boundary

Do not copy prose, figures, results, datasets, source code or scientific claims from example theses merely because they were supplied as references. The derived guide records only abstracted structural/style observations. Do not publish third-party thesis files to GitHub by default.

## Later revision rule

This policy and the derived style guide may change only when:

- newer official Department/University guidance is verified;
- the supervisor supplies an explicit instruction;
- a concrete Word/composition problem demonstrates that a bounded presentation adjustment is needed.

Such changes may alter document presentation but cannot alter frozen protocol-v2.1 science, accepted final evidence, T-612 estimands/results or T-613 quantitative assets.