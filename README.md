# resilient-ai-agents-thesis

**Official Greek title:** Σύγκριση και Αξιολόγηση Ανθεκτικών Πρακτόρων Τεχνητής Νοημοσύνης σε Περιβάλλοντα με Αβεβαιότητα  
**Official English title:** Comparison and Evaluation of Resilient AI Agents in Uncertain Environments

Version-controlled repository for the complete thesis lifecycle: research context, bibliography consumption, scientific implementation, controlled experiments, evidence validation, statistical analysis, thesis/defense assets, writing, review and final delivery.

> `docs/context/TASKS.md` is the canonical task/dependency ledger and `docs/context/CURRENT_STATUS.md` is the authoritative compact state. This README is a human-readable overview only.

## Current project state

| Item | Current state |
|---|---|
| Master research/application milestones | **8/8 complete**; tracker #87 closed completed |
| Scientific/pre-final implementation | **Complete** through protocol-v2.1, Study backend and application hardening |
| Accepted application | **Complete** through T-534/T-535/T-536; active tree cleaned by T-537 |
| Final protocol-v2.1 execution | **T-610 COMPLETE** through the formal DEC-062 replacement path |
| Final evidence freeze | **T-611 COMPLETE** |
| Final statistical analysis | **T-612 COMPLETE** |
| Final thesis/appendix/defense assets | **T-613 COMPLETE** |
| Pre-WP7 user approval | **APPROVED** on 2026-09-03 |
| Current academic-guidance pass | **T-700 COMPLETE** |
| Example-thesis structure/style review | **T-701 COMPLETE** |
| Current task | **T-702 READY** — major-writing-gate bibliography freshness review and immutable re-sync |
| Full Greek thesis drafting | **T-710 BLOCKED by T-702** |
| Standalone Windows packaging | Deferred to **T-803** after the thesis deliverable |

The first protocol-v2.1 Study from `7442dcb65674dcb3bc9ce0c71996418289d79061` remains an immutable, unfinalized 216-job failed attempt. It is permanently excluded from accepted downstream evidence.

The DEC-062 replacement `protocol-v2.1-final--t610-recovery-01` completed the unchanged **603/603** plan from clean source commit `86fb01a13fd77b98ea0b8d8fa6d5c5d6e2cbd730`, producing **600 accepted scientific run bundles** with zero recorded infrastructure/scientific failures.

Accepted downstream identities:

- T-611 freeze manifest SHA-256: `20a88bf9eee2ba8c4f60064634004f3746a594460f91fcd2491beae5cb498858`
- T-611 600-record inventory SHA-256: `0c2b352b88045951d32e58ee3479656dce00e35d55899bcdea65dc07604d8045`
- T-612 analysis manifest SHA-256: `dd467d1f282b183ccf767084639b5ad38cc02caa5e3b6ce521128d177bb3ee62`
- T-613 asset manifest SHA-256: `9457275306fb633cb58d9af2e402531ff7d56a0f1f0f5eadc176f4a05726abd8`

T-613 finalized **31 figures, 12 table assets and 117 registered output variants**. The complete 121-file package reproduced twice byte-for-byte. Twenty-eight of thirty planned inventory categories are supported; categories 1 and 6 remain explicitly unavailable because the accepted T-612 package contains no registered probe/checkpoint-series values, and no post-hoc reconstruction is allowed.

## Project principle

The research contribution is the controlled comparison of resilient AI-agent strategies under uncertainty and dynamic change. **GridWorld is the controlled testbed, not the thesis subject.** The desktop application supports experiment execution, inspection, evidence presentation and reproducibility; it is not the source of scientific truth.

## Frozen scientific protocol

DEC-058 / protocol-v2.0 remain immutable historical freeze authority. DEC-060 plus `configs/protocols/protocol-v2.1-final.json` define the accepted final scientific design.

Protocol-v2.1 retains:

- five methods: **Q-Learning, SARSA, DQN, PPO and Dyna-Q+**;
- common actual-environment-interaction fairness;
- independent Phase-A nominal learning and exact checkpoints;
- matched Phase-B **FN / FD / AN / AD** branches;
- **12 independent roots**, **2 held-out final layouts**, **4 Phase-B conditions**, **256 interactions** per Phase-B horizon;
- RQ1 nominal-learning estimands;
- RQ2 primary adaptation benefit `(FN-FD)-(AN-AD)` plus distinct Frozen/Adaptive loss views;
- RQ3 passive 32-interaction windows, primary tolerance `0.10`, sensitivity `0.05/0.20`, two-window stable recovery and explicit right-censoring with `recovery_time=null`;
- root as the independent statistical unit, equal layout reduction, root-paired direct method contrasts and Student-t intervals using actual root count;
- no formal p-value superiority family and no composite global ranking.

The accepted T-612 interpretation is recorded in `docs/research/T612_FINAL_STATISTICAL_ANALYSIS.md`. Later writing may explain those results but must not redefine or recompute them.

## Architecture

The active scientific/backend implementation lives under:

```text
src/resilient_agents/
```

The research lifecycle is study-first:

```text
immutable Study recipe
        -> deterministic job plan
        -> Phase A independent nominal learning
        -> exact scientific checkpoints
        -> Phase B FN / FD / AN / AD
        -> temporal evidence
        -> evidence validation/freeze
        -> root-level statistical analysis
        -> recovery/direct contrasts
        -> deterministic thesis/defense assets
        -> stored-evidence application views
```

`src/resilient_agents/evidence_v2/` owns the protocol-v2.1 validation/analysis/export path. Filesystem evidence is authoritative; indexes/databases are rebuildable caches.

## Accepted desktop application

The accepted frontend is native **PySide6 / Qt 6 Widgets** under `src/resilient_agents/desktop/`. It consumes the Study backend directly and does not reimplement protocol or statistical logic.

The final information architecture is:

> **Experiment → Run → Results → Evidence**

Key boundaries:

- the Thesis experiment is immutable/read-only in the application;
- DEVELOPMENT configuration uses backend-constrained paths;
- live GridWorld/telemetry are presentation-only and cannot alter actions, RNG, checkpoints, metrics or evidence;
- Results display validated stored RQ1/RQ2/RQ3 evidence;
- right-censored recovery stays `recovery_time=null`;
- Evidence surfaces registered lineage/provenance rather than arbitrary filesystem browsing;
- application screenshots may illustrate workflow, but **never replace T-613 quantitative figures/tables for scientific claims**.

The source application remains launchable from the validated Windows checkout. Standalone packaging is intentionally deferred to T-803.

## WP7 writing state

The user explicitly approved entry into WP7 after T-613 completion.

### T-700 — complete

Current public Department/University guidance was rechecked on 2026-09-03 and recorded in:

`docs/thesis/OFFICIAL_GUIDANCE_SNAPSHOT_2026-09-03.md`

The current working Word contract remains A4, Times New Roman 11 pt main text, 1.5 line spacing, numbered Heading styles, 14 pt chapter headings, 12 pt subheadings, automatic TOC, figure/table captions and controlled front/final matter.

No current public ICE-specific rule was found that fixes defense duration, slide count, PowerPoint template or mandatory live demo. Those items are intentionally rechecked near T-720/T-722 rather than inferred from another department.

IEEE numeric citations are the WP7 project default because the Department permits multiple consistent styles and the technically closest contextual examples predominantly use numeric references. This is **not represented as an ICE mandate**; any later explicit supervisor/Department instruction supersedes it.

### T-701 — complete

The user supplied 22 example-thesis files. Integrity review identified **21 unique completed theses**, because `example-theses 1.pdf` and `example-theses 10.pdf` are byte-identical.

The examples were reviewed comparatively for structure/presentation only. They were not added to the bibliography and are not scientific sources.

The canonical derived guide is:

`docs/thesis/THESIS_STRUCTURE_AND_STYLE_GUIDE.md`

The final research-first manuscript architecture is:

1. **Εισαγωγή**
2. **Θεωρητικό Υπόβαθρο και Σχετική Βιβλιογραφία**
3. **Μεθοδολογία και Πειραματικός Σχεδιασμός**
4. **Αρχιτεκτονική και Υλοποίηση του Ερευνητικού Συστήματος**
5. **Πειραματικά Αποτελέσματα**
6. **Συζήτηση**
7. **Συμπεράσματα και Μελλοντική Εργασία**

Results and Discussion are intentionally separate. This project has three distinct RQs/estimands, paired contrasts, uncertainty intervals, sensitivity analysis and right-censoring; merging interpretation into a generic “Evaluation/Conclusions” chapter would weaken the scientific argument.

### T-702 — next and READY

The currently consumed bibliography snapshot is still pinned to upstream `MariosGiannakaras/ThesisBibliography` SHA:

`f10afcc41e3e1bd877d884cf7a5ae6b5284046f5`

It remains a valid immutable prior snapshot, but REQ-RES-012 requires a **new dated literature freshness review at the major writing gate**.

T-702 therefore must:

1. execute the writing-gate freshness review in canonical `MariosGiannakaras/ThesisBibliography`;
2. process any genuinely relevant new sources through its normal intake/analysis/evidence/selection lifecycle;
3. create a new immutable consumer identity even if the citation-ready selected set is unchanged;
4. synchronize that accepted snapshot into `research/bibliography/` through the controlled consumer workflow;
5. verify citation-ready integrity/provenance.

**T-710 remains blocked until T-702 is complete.**

## Planned drafting sequence after T-702

The final document order is not the drafting order. The evidence-driven sequence is:

1. Chapter 3 — Methodology and Experimental Design
2. Chapter 4 — Architecture and Implementation
3. Chapter 5 — Results
4. Chapter 6 — Discussion / validity / limitations
5. Chapter 7 — Conclusions
6. Chapter 2 — Background and Related Work
7. Chapter 1 — Introduction
8. Greek summary / English abstract near review-ready freeze

This reduces rewriting and prevents early prose from dictating the final scientific story.

## Bibliography boundary

`MariosGiannakaras/ThesisBibliography` is the canonical bibliography lifecycle repository. This repository consumes an immutable generated snapshot read-only. Formal automatic citation trust is limited to:

```text
research/bibliography/citation-ready/
```

No primary bibliography source is independently ingested or promoted here.

## Repository map

```text
src/resilient_agents/                  Scientific core + study backend
src/resilient_agents/study/            Study recipe/DAG/store/scheduler/service
src/resilient_agents/evidence_v2/      Protocol-v2.1 validation/analysis/export
src/resilient_agents/desktop/          Accepted PySide6 research application

configs/                               Version-controlled protocol/scenario inputs
scripts/                               Reproducibility and maintenance utilities
tests/                                 Risk-based scientific/backend/UI regression tests

research/bibliography/                 Immutable consumed bibliography corpus
results/runs/                          Lower-level scientific run bundles
results/studies/                       Study-level lifecycle/evidence bundles
results/final-evidence/                Accepted frozen final evidence
results/analysis/                      Final statistical analysis
results/thesis-assets/                 Final T-613 thesis/appendix/defense assets

docs/context/                          Current status/tasks/workflow
docs/research/                         Methodology, RQ evidence and scientific reports
docs/experiments/                      Experiment/provenance rules
docs/architecture/                     Backend/frontend architecture
docs/thesis/                           Thesis/defense requirements and workflows
docs/decisions/                        Decisions and ADRs
```

## Current authority files

Always start with:

1. `AGENTS.md`
2. `docs/context/TASKS.md`
3. `docs/context/CURRENT_STATUS.md`

Important supporting authorities now include:

- `configs/protocols/protocol-v2.1-final.json`
- `docs/decisions/DEC-060_PROTOCOL_V2_1_RECOVERY_AND_DIRECT_COMPARISONS.md`
- `docs/decisions/DEC-062_T610_FAILED_ATTEMPT_RECOVERY.md`
- `docs/research/T612_FINAL_STATISTICAL_ANALYSIS.md`
- `docs/research/T-613_THESIS_FIGURE_INVENTORY.md`
- `results/final-evidence/protocol-v2.1-final/`
- `results/analysis/protocol-v2.1-final/`
- `results/thesis-assets/protocol-v2.1-final/`
- `docs/thesis/OFFICIAL_GUIDANCE_SNAPSHOT_2026-09-03.md`
- `docs/thesis/THESIS_STRUCTURE_AND_STYLE_GUIDE.md`
- `docs/thesis/WP7_WP8_TOOL_WORKFLOW.md`

## Evidence and integrity principles

- Finalized evidence is immutable and checksum/provenance protected.
- Scientific failures are retained; they are not replaced by favorable roots.
- Infrastructure retries preserve the same scientific identity.
- Historical failed T-610 evidence remains excluded from final thesis claims.
- Phase-B evidence traces to exact Phase-A checkpoint lineage.
- Non-recovery remains explicit; the horizon is never substituted as fake observed recovery time.
- Final figures/tables/results come from frozen accepted evidence, not UI transcription.
- T-612 estimands/statistics are not redesigned during writing.
- WP7 approval is satisfied, but declared downstream dependencies still apply; specifically, T-710 waits for T-702.

## End-to-end lifecycle

> methodology/bibliography → feasibility/pilots → protocol freeze → validated Study backend/application → final protocol-v2.1 execution → evidence validation/freeze → predeclared RQ1/RQ2/RQ3 analysis → reproducible thesis/appendix/defense assets → **WP7 approval (satisfied)** → official-guidance/example review → **writing-gate bibliography freshness/re-sync (T-702)** → Greek thesis/review → defense presentation → final audit/delivery
