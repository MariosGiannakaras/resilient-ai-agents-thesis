# resilient-ai-agents-thesis

**Official Greek title:** Σύγκριση και Αξιολόγηση Ανθεκτικών Πρακτόρων Τεχνητής Νοημοσύνης σε Περιβάλλοντα με Αβεβαιότητα  
**Official English title:** Comparison and Evaluation of Resilient AI Agents in Uncertain Environments

Version-controlled repository for the complete thesis lifecycle: research framing, bibliography governance, scientific implementation, controlled experiments, frozen evidence, statistical analysis, thesis/defense assets, writing, review, final submission and standalone application delivery.

> `docs/context/TASKS.md` is the canonical task/dependency ledger. `docs/context/CURRENT_STATUS.md` is the compact current state. This README is the human-readable entry point.

## Current state

The scientific experiment/evidence chain is complete and frozen. The active academic task is **T-716**, a full-content thesis reconstruction/expansion after the T-715 reader-scoped version was rejected as too compressed. T-715 remains an auditable completed composition milestone, but **is not the final thesis**.

| Area | State |
|---|---|
| Scientific implementation / protocol-v2.1 | COMPLETE |
| Final execution T-610 | COMPLETE — accepted replacement 603/603 jobs, 600 scientific bundles |
| Evidence freeze T-611 | COMPLETE |
| Statistical analysis T-612 | COMPLETE |
| Thesis/appendix/defense assets T-613 | COMPLETE |
| T-710 Greek manuscript | COMPLETE |
| T-711/T-714 Word composition and full-content baseline | COMPLETE / archived |
| T-715 reader-scope + audit hardening | COMPLETE as bounded task; superseded as final-thesis candidate |
| **T-716 full-content evidence-aware thesis** | **IN_PROGRESS — stage-3 full-content milestone archived; final evidence/citation audit remains** |
| T-712 supervisor/reviewer corrections | DEFERRED until real feedback exists |
| T-713 final thesis freeze | DEFERRED until T-716 acceptance + T-712 + official finalization inputs |
| Defense T-720/T-721/T-722 | DEFERRED downstream work |
| Final audits/delivery T-800/T-801/T-802 | DEFERRED downstream work |
| Standalone Windows package T-803 | DEFERRED post-thesis deliverable |

The archived T-714 run #66 is the current full-content baseline (about 20.9k whole-document words). T-716 must restore and improve that coverage, integrate all validated T-715 scientific corrections, use the user-restored older drafts where still correct, and strengthen source support without filler or scientific recomputation.

## Complete downstream lifecycle

The project does **not** end when a review-ready thesis DOCX exists. The retained sequence is:

1. **T-716 — Full-content thesis reconstruction and evidence-aware rewrite.** Reconcile T-714, useful older-draft material, T-715 corrections, frozen project evidence and the multi-source claim/evidence map. Produce and archive the exact reviewed DOCX + QA identity.
2. **T-712 — Supervisor/reviewer corrections.** Starts only from actual external feedback; internal audits are not relabelled as supervisor feedback.
3. **T-713 — Final thesis freeze.** Resolve official student/person/declaration metadata, final Word fields/cross-references/TOC/lists, final PDF/submission candidate and final thesis identity.
4. **T-720 — Defense narrative and evidence map.** Recheck current defense-specific rules; derive the defense story strictly from the accepted final thesis/evidence.
5. **T-721 — Final PowerPoint + speaker material.** Build slides, notes/script and evidence links from frozen thesis/results/application assets.
6. **T-722 — Rehearsal and defense validation.** Validate duration, readability, media, demo/static fallback and thesis/slide consistency.
7. **T-800 — Final bibliography/citation/official-guidance audit.** Recheck every final citation and current submission/defense requirement.
8. **T-801 — Reproducibility/privacy/licensing consistency audit.** Check repository, thesis, defense, application assets and distribution boundaries together.
9. **T-802 — Academic delivery readiness.** Final file set, administrative/deposit requirements and submission checklist.
10. **T-803 — Clean standalone Windows application package.** Produce the final distributable application only after the academic deliverable is stable.

See `docs/context/TASKS.md` and `docs/thesis/WP7_WP8_TOOL_WORKFLOW.md` for the canonical dependency details.

## Scientific boundary

The research contribution is the controlled comparison of resilient AI-agent strategies under uncertainty and dynamic change. **GridWorld is the controlled testbed, not the thesis subject.** The desktop application supports experiment execution, inspection and evidence presentation; it is not the source of scientific truth.

The accepted scientific design is defined by DEC-060 plus `configs/protocols/protocol-v2.1-final.json`, with DEC-058/protocol-v2.0 retained as immutable historical freeze authority. The final design includes:

- Q-Learning, SARSA, DQN, PPO and Dyna-Q+;
- common actual-environment-interaction fairness;
- Phase-A nominal learning and exact checkpoints;
- matched Phase-B **FN / FD / AN / AD** branches;
- 12 independent roots, two held-out layouts and four Phase-B conditions;
- RQ1 nominal-learning estimands;
- RQ2 adaptation benefit `(FN-FD)-(AN-AD)` with Frozen/Adaptive losses kept distinct;
- RQ3 passive 32-interaction windows, primary tolerance `0.10`, two consecutive qualifying windows and explicit right-censoring at 256 interactions;
- root as the independent statistical unit, equal layout reduction and declared root-paired comparisons;
- no formal p-value superiority family and no composite global ranking.

T-612 is the authority for final statistical interpretation. Writing may explain those results but must not redefine, recompute or selectively replace them.

## Accepted implementation architecture

The active implementation lives under `src/resilient_agents/` and follows a study-first lifecycle:

```text
immutable Study recipe
        -> deterministic job plan
        -> Phase A nominal learning
        -> exact scientific checkpoints
        -> Phase B FN / FD / AN / AD
        -> temporal evidence
        -> evidence validation/freeze
        -> root-level statistical analysis
        -> recovery/direct contrasts
        -> deterministic thesis/defense assets
        -> stored-evidence application views
```

The accepted frontend is native **PySide6 / Qt 6 Widgets** under `src/resilient_agents/desktop/` with the information architecture:

> **Experiment → Run → Results → Evidence**

Historical Streamlit, React/Vite and NiceGUI directions are retained only where they document implementation history and superseded decisions. They are not the current application architecture.

## Bibliography and claim-evidence policy

`MariosGiannakaras/ThesisBibliography` owns the bibliography lifecycle. This repository consumes an immutable synchronized snapshot under `research/bibliography/`.

Formal thesis citations must resolve to the validated citation-ready layer:

```text
research/bibliography/citation-ready/
```

A citation-ready source is **not automatically a source of truth**. T-716 uses a claim-centred evidence model:

- each literature claim has a stable claim ID;
- all relevant sources are attached to that claim, not only the first convenient source;
- primary papers, independent replications/surveys and contradictory/limiting evidence are compared explicitly;
- exact equations, algorithms and empirical findings prefer primary sources;
- scientific quality, relevance, methodological strength and primary/foundational value outrank blind recency;
- when materially comparable sources cover the same claim, the more recent source is preferred by default;
- an older authoritative/foundational source may outrank a newer but weaker, derivative, informal or student source, with the reason kept explicit;
- surveys/talks may guide synthesis/discovery but do not override primary evidence;
- protocol-specific decisions are labelled as project decisions even when literature motivates them;
- project/result claims point to frozen repository authorities, not to external papers;
- conflicting sources remain visible and the final wording is bounded to the strongest common support.

The complete source-ranking rule is `docs/thesis/BIBLIOGRAPHY_SOURCE_SELECTION_POLICY.md`. The human-readable claim mapping lives in `docs/thesis/CLAIM_EVIDENCE_TREE.md`; the machine-readable registry lives in `docs/thesis/claim-evidence-map.json`. Both the registry and the selection-policy contract are validated before T-716 can be accepted. The synchronized `research/bibliography/` directory remains immutable and contains only the governed ThesisBibliography import.

## Repository map

```text
src/resilient_agents/                  Scientific core + Study backend
src/resilient_agents/study/            Study recipe/DAG/store/scheduler/service
src/resilient_agents/evidence_v2/      Protocol-v2.1 validation/analysis/export
src/resilient_agents/desktop/          Accepted PySide6 research application

configs/                               Version-controlled protocol/scenario inputs
scripts/                               Reproducibility, QA and maintenance utilities
tests/                                 Scientific/backend/UI regression tests

research/bibliography/                 Immutable consumed bibliography corpus
results/runs/                          Lower-level scientific run bundles
results/studies/                       Study-level lifecycle/evidence bundles
results/final-evidence/                Accepted frozen final evidence
results/analysis/                      Final statistical analysis
results/thesis-assets/                 Final T-613 thesis/appendix/defense assets

thesis/archive/                        Historical and review milestone DOCX/QA artifacts
thesis/drafts/                         User-restored and working historical thesis drafts
thesis/final/                          Reserved for a genuinely accepted T-713 submission candidate

docs/context/                          Current status/tasks/workflow
docs/research/                         Methodology, RQ evidence and scientific reports
docs/experiments/                      Experiment/provenance rules
docs/architecture/                     Backend/frontend architecture
docs/thesis/                           Thesis/defense requirements, audits and workflows
docs/decisions/                        Decisions and ADRs
```

Generic placeholder-only `data/raw`, `data/processed`, `data/external` and obsolete generic `artifacts/{figures,tables,exports}` scaffolds are not part of the active scientific data model and are removed when they have no consumer. The active `results/`, `research/`, `thesis/archive/`, documentation and provenance history are retained.

## Current authority files

Start with:

1. `AGENTS.md`
2. `docs/context/TASKS.md`
3. `docs/context/CURRENT_STATUS.md`

Then consult, as relevant:

- `configs/protocols/protocol-v2.1-final.json`
- `docs/decisions/DEC-060_PROTOCOL_V2_1_RECOVERY_AND_COMPARISON_AMENDMENT.md`
- `docs/decisions/DEC-062_T610_FAILED_ATTEMPT_RECOVERY.md`
- `docs/research/T612_FINAL_STATISTICAL_ANALYSIS.md`
- `docs/research/T-613_THESIS_FIGURE_INVENTORY.md`
- `results/final-evidence/protocol-v2.1-final/`
- `results/analysis/protocol-v2.1-final/`
- `results/thesis-assets/protocol-v2.1-final/`
- `docs/thesis/T716_REWRITE_PLAN.md`
- `docs/thesis/BIBLIOGRAPHY_SOURCE_SELECTION_POLICY.md`
- `docs/thesis/CLAIM_EVIDENCE_TREE.md`
- `docs/thesis/claim-evidence-map.json`
- `docs/thesis/OFFICIAL_GUIDANCE_SNAPSHOT_2026-09-03.md`
- `docs/thesis/THESIS_STRUCTURE_AND_STYLE_GUIDE.md`
- `docs/thesis/WP7_WP8_TOOL_WORKFLOW.md`

## Evidence and integrity rules

- Finalized scientific evidence is immutable and checksum/provenance protected.
- Scientific failures remain recorded; favorable roots are never substituted for failed evidence.
- Infrastructure retries preserve scientific identity.
- The historical failed 216-job T-610 attempt remains excluded from accepted final evidence.
- Phase-B evidence traces to exact Phase-A checkpoint lineage.
- Non-recovery remains explicit; the 256-interaction horizon is never substituted as a fake observed recovery time.
- Quantitative thesis figures/tables come from frozen T-613 assets, not UI transcription.
- Scientific values/estimands are not redesigned during thesis writing.
- Meaningful user-facing deliverables are committed under `thesis/archive/` before handoff; transient local or CI files are not treated as permanent deliverables.
- Repository cleanup is conservative: docs, results, evidence, decisions, archived thesis milestones and useful implementation history are preserved.

## End-to-end lifecycle

> research/bibliography → feasibility/pilots → protocol freeze → Study backend/application → final protocol-v2.1 execution → evidence freeze → predeclared RQ1/RQ2/RQ3 analysis → reproducible thesis assets → manuscript → Word milestones → **T-716 full-content evidence-aware thesis** → actual supervisor corrections → final thesis freeze → defense narrative/deck/rehearsal → final bibliography/reproducibility/delivery audits → academic submission → standalone Windows package
