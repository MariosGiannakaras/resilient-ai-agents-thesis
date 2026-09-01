# resilient-ai-agents-thesis

**Official Greek title:** Σύγκριση και Αξιολόγηση Ανθεκτικών Πρακτόρων Τεχνητής Νοημοσύνης σε Περιβάλλοντα με Αβεβαιότητα  
**Official English title:** Comparison and Evaluation of Resilient AI Agents in Uncertain Environments

Version-controlled repository for the complete thesis lifecycle: research context, bibliography consumption, scientific implementation, controlled experiments, evidence validation, statistical analysis, thesis/defense assets, writing, review and final delivery.

## Project status

The project is currently at the **final scientific-experiment authorization gate**.

| Item | Current state |
|---|---|
| Master progress | **7/8 milestones complete** |
| Scientific/pre-final implementation | **Complete** through protocol-v2.1, Study backend and pre-final readiness |
| Accepted application | **Complete** through T-534, T-535 and T-536 |
| Final repository hygiene | **T-537 COMPLETE** |
| Final read-only preflight | **Complete**; T-537 changed no scientific/execution code |
| Final protocol-v2.1 reserve | **Sealed** — `final_reserve_access=false` |
| Final execution authorization | **Not granted** — `requires-explicit-t610-gate` |
| Current gate | **T-610 BLOCKED only by separate explicit scientific authorization** |
| Final v2.1 outcomes | **Not generated or inspected yet** |
| Thesis writing | **Not authorized yet**; separate pre-WP7 approval is required after accepted final evidence |
| Standalone Windows packaging | Deferred to **T-803** after the thesis deliverable |

All declared implementation/application/hygiene dependencies for T-610 are complete. The active tree has been cleaned of superseded non-scientific residue while historical scientific protocols, configs, evidence, freeze manifests, decisions and reproducibility-critical code remain intact. The next scientific action is therefore not more software development: it is the explicit authorization of the frozen final experiment.

> `docs/context/TASKS.md` is the canonical task/dependency ledger and `docs/context/CURRENT_STATUS.md` is the authoritative compact state. The task table in this README is a human-readable snapshot only; the canonical files win if the project state changes.

## Project principle

The research contribution is the controlled comparison of resilient AI-agent strategies under uncertainty/change. GridWorld is the common controlled testbed and visualization surface; the application supports execution, inspection and presentation but is not the research contribution itself.

> **Polished outside, bounded inside.**

The final tool is local and single-user. Scientific validity, reproducibility and a realistic thesis scope take priority over production-platform complexity.

## Current scientific protocol

DEC-058 / protocol-v2.0 remain immutable historical freeze authority. DEC-060 and `configs/protocols/protocol-v2.1-final.json` are the current frozen pre-execution scientific authority.

Protocol-v2.1 retains:

- five methods: **Q-Learning, SARSA, DQN, PPO and Dyna-Q+**;
- common actual-environment-interaction fairness semantics;
- independent Phase-A nominal learning and exact method/root/layout checkpoints;
- matched Phase-B **FN / FD / AN / AD** branches;
- **12 independent final roots**, **2 held-out final layouts**, **4 Phase-B conditions** and a **256-interaction** Phase-B horizon;
- RQ1 nominal learning evidence;
- RQ2 primary adaptation benefit `(FN-FD)-(AN-AD)` plus Frozen/Adaptive loss views;
- RQ3 passive 32-interaction windows, primary tolerance `0.10`, sensitivity `0.05/0.20`, two-window stable recovery and explicit right-censoring with `recovery_time=null`;
- root as the independent statistical unit, equal layout reduction, root-paired direct method contrasts and predeclared Student-t intervals selected by actual root count.

The read-only final preflight confirms a **603-job** frozen Study plan while keeping final execution blocked. No protocol-v2.1 final-reserve outcome has been generated, inspected or used.

## Current architecture

The active scientific/backend implementation lives in:

```text
src/resilient_agents/
```

The architecture is **study-first**:

```text
immutable Study recipe
        -> deterministic job plan
        -> Phase A independent nominal learning
        -> exact scientific checkpoints
        -> Phase B FN / FD / AN / AD branches
        -> temporal evidence
        -> evidence validation/freeze
        -> root-level statistical analysis
        -> recovery/direct contrasts
        -> deterministic thesis / defense exports
        -> stored-evidence application views
```

A `Run` is a lower-level scientific evidence unit. A `Study` is the authoritative parent lifecycle.

### Scientific core

The validated scientific layer includes:

- project-owned Gymnasium-compatible GridWorld;
- strict separation of evaluator ground truth from agent-visible information;
- independent scoped RNG streams;
- actual environment-interaction accounting;
- Q-Learning, SARSA, DQN, PPO and Dyna-Q+ implementations;
- isolated no-learning evaluation probes;
- exact method-specific scientific checkpoint/restore semantics;
- matched Frozen nominal / Frozen disturbed / Adaptive nominal / Adaptive disturbed Phase-B execution;
- fail-closed information, checkpoint and branch invariants.

### Study orchestration

`src/resilient_agents/study/` owns framework-neutral orchestration:

- immutable content-addressed `StudyRecipe`;
- evidence classes separating development/tuning/confirmatory/derived/history;
- deterministic recipe-to-job DAG materialization;
- scientific-vs-infrastructure failure semantics;
- restart-safe study persistence and artifact lineage;
- sequential stage barriers;
- executor registry/scheduler;
- framework-neutral `StudyService` facade;
- deny-by-default protocol-v2.1 final execution unless the separate T-610 authorization path supplies the required authorization.

### Protocol-v2.1 evidence and analysis

`src/resilient_agents/evidence_v2/` owns the v2-only evidence/analysis path, kept separate from historical v1.x analysis so finalized historical evidence remains reproducible.

It covers:

- planned-vs-produced evidence validation;
- exact Phase-A checkpoint → Phase-B lineage;
- standardized heterogeneous-method analysis records;
- passive Phase-B temporal evidence;
- right-censored recovery analysis;
- root/layout reduction and declared method contrasts;
- deterministic analysis and evidence-handoff exports with provenance.

## Accepted desktop application

The accepted frontend is a native **PySide6 / Qt 6 Widgets** application under `src/resilient_agents/desktop/`. It consumes the Study backend directly and does not reimplement scientific protocol logic.

The final information architecture is:

> **Experiment → Run → Results → Evidence**

Current accepted UI behavior includes:

- **Locked Thesis experiment** with all five protocol methods fixed and read-only;
- separate backend-constrained DEVELOPMENT Configure → Review → Create workflow;
- truthful durable Run state plus presentation-only live GridWorld frames;
- one dominant Phase-A GridWorld and simultaneous exact matched **Frozen vs Adaptive** Phase-B views;
- explicit `Method N of 5 · Name` orientation and compact five-method lifecycle strip;
- larger RQ1/RQ2 charts and stored-evidence RQ3 recovery trajectories with correct right-censor presentation;
- RQ-local direct comparisons, progressive provenance disclosure and actionable Evidence readiness;
- deterministic 1366×768 and 1440×900 review coverage without final scientific execution.

The application uses **Frozen** only for the scientific regime. The overall read-only Thesis state is named **Locked Thesis experiment** to avoid ambiguity.

Generated UI review screenshots are CI/local QA artifacts and are not committed as active scientific evidence. Superseded historical T-528 screenshot copies remain auditable through Git history and their exact-head Actions artifact.

From PowerShell on the validated Windows thesis machine, the source application can be launched with:

```powershell
& "$env:USERPROFILE\.local\bin\uv.exe" sync --locked --group gridworld-prototype --group protocol-v2-pilot --no-progress
& "$env:USERPROFILE\.local\bin\uv.exe" pip install --python .venv\Scripts\python.exe --requirement requirements\application-ui.txt
.\.venv\Scripts\python.exe -m resilient_agents.desktop
```

Standalone Windows packaging is intentionally deferred to T-803.

## What remains from here

The remaining path is sequential and evidence-gated:

1. **Authorize T-610 separately.** This is the only current pre-run gate. Authorization must be explicit; cleanup/README/CI/UI/preflight completion does not grant it.
2. **T-610 — Execute the frozen protocol-v2.1 final matrix.** No outcome-driven protocol changes are allowed.
3. **T-611 — Validate and freeze final evidence.** Check completeness, integrity, provenance and scientific validity before accepting evidence for analysis.
4. **T-612 — Run the predeclared statistical analysis.** Produce RQ1/RQ2/RQ3 estimands, sensitivity diagnostics and direct method contrasts from the frozen evidence.
5. **T-613 — Produce the final figure/table/export package.** Generate the rich reproducible thesis + appendix + defense assets defined in `docs/research/T-613_THESIS_FIGURE_INVENTORY.md`.
6. **Explicit pre-WP7 user approval.** Even accepted final evidence does not automatically authorize thesis writing.
7. **WP7 — Thesis and defense.** Recheck current university rules, review example theses, draft the Greek thesis, create the review-ready Word document, apply corrections, freeze the thesis, and prepare/rehearse the defense deck.
8. **WP8 — Final audit/delivery.** Bibliography/citation audit, reproducibility/privacy/licensing/delivery audit, final academic readiness and eventually the standalone Windows application package.

There is **no additional implementation/application/hygiene package required before T-610**. The repository is intentionally stopped at the scientific authorization boundary.

## Thesis/defense result assets

T-613 is the canonical final v2.1 figure/table/export task after T-612. Its pre-execution contract is `docs/research/T-613_THESIS_FIGURE_INVENTORY.md`.

The final package is designed to be substantially richer than application screenshots. It covers roughly **30 figure/asset categories plus tables**, including:

- RQ1 learning progression, final/time-average comparisons, root-level distributions and direct contrasts;
- RQ2 adaptation benefit, Frozen-vs-Adaptive losses, condition panels, paired diagnostics, heatmaps and direct contrasts;
- RQ3 recovery trajectories, recovered proportion, restricted delay, conditional observed recovery time, right-censor composition, tolerance sensitivity, root-level diagnostics and direct contrasts;
- experiment-flow, RQ/evidence and provenance-lineage diagrams;
- main-thesis, appendix and defense-specific variants.

Expected outputs are vector-first `SVG`/`PDF` where appropriate, high-resolution `PNG` for Word/PowerPoint compatibility, and machine-readable tables such as `CSV`. Every quantitative asset must remain traceable to validated stored evidence, source artifact IDs/hashes, the analysis package and the generator Git commit.

Application screenshots are suitable for illustrating the software workflow; they are **not** the quantitative source for thesis claims.

## Task registry snapshot

Status legend: **Complete** = accepted task finished; **Superseded** = historical task intentionally replaced and must not execute; **Blocked** = dependency/approval gate not satisfied; **Deferred** = intentionally scheduled for a later lifecycle stage.

| WP | Task | Status | Scope |
|---|---|---|---|
| WP0 | T-001 | ✅ Complete | Repository/project identity and controlled Git/PR workflow |
| WP0 | T-002 | ✅ Complete | Immutable ThesisBibliography integration/provenance |
| WP0 | T-003 | ✅ Complete | Python 3.12 + locked `uv` environment/importable core |
| WP0 | T-004 | ✅ Complete | Information/RNG/scenario/experiment/stage contracts |
| WP0 | T-005 | ✅ Complete | Run bundles/provenance/checksums/metrics/publication safeguards |
| WP0 | T-006 | ✅ Complete | Documentation reconciliation/canonical execution prompt |
| WP0 | T-007 | ✅ Complete | End-to-end lifecycle/user/Codex/defense handoffs |
| WP0 | T-008 | ✅ Complete | Lean session-start core and resumable execution |
| WP0 | T-009 | ✅ Complete | Project-scoped developer-documentation configuration |
| WP1 | T-100 | ✅ Complete | Target-machine hardware/software/storage inventory |
| WP1 | T-101 | ✅ Complete | Compute-dependent dependency/runtime constraints |
| WP1 | T-102 | ✅ Complete | Durable capability-provenance reconciliation |
| WP2 | T-200 | ✅ Complete | Source-traceable historical RQ/hypothesis framing |
| WP2 | T-210 | ✅ Complete | GridWorld implementation comparison |
| WP2 | T-211 | ✅ Complete | GridWorld ADR |
| WP2 | T-212 | ✅ Complete | Project-owned Gymnasium GridWorld |
| WP2 | T-213 | ✅ Complete | Known-answer/determinism/disturbance/information tests |
| WP3/4 | T-300 | ✅ Complete | Resilience/degradation/recovery estimands |
| WP3/4 | T-301 | ✅ Complete | Known-answer metric validation |
| WP3/4 | T-310 | ✅ Complete | Historical bounded agent-role comparison |
| WP3/4 | T-311 | ✅ Complete | Robust-MDP citation decision |
| WP3/4 | T-312 | ✅ Complete | Historical F0/C0/R0-capable implementation |
| WP3/4 | T-400 | ✅ Complete | Historical partitions/pilot protocol |
| WP3/4 | T-401 | ✅ Complete | Headless runner/orchestration |
| WP3/4 | T-402 | ✅ Complete | Reproducible analysis pipeline |
| WP3/4 | T-410 | ✅ Complete | Pilot diagnostics/R0 amendment evidence |
| WP3/4 | T-411 | ✅ Complete | Pre-freeze bibliography freshness review |
| WP3/4 | T-412 | ✅ Complete | Immutable protocol-v1.0 freeze/statistical plan |
| WP5 | T-500 | ✅ Complete · historical | Experiment-manager baseline |
| WP5 | T-510 | ✅ Complete · historical | Streamlit dashboard baseline |
| WP5 | T-511 | ✅ Complete · historical acceptance | Intended-user application workflow/self-explanatory UX acceptance |
| WP5 | T-512 | ✅ Complete · historical | Self-explanatory UX/onboarding pass |
| WP5 | T-513 | ✅ Complete | Refinement governance/single branch/PR/handoff |
| WP5 | T-520 | ✅ Complete | Information-limited deterministic Dyna-Q+ integration |
| WP5 | T-521 | ✅ Complete · non-final history | Candidate protocol-v1.1/config identity/paired-statistics infrastructure |
| WP5 | T-522 | ⛔ Superseded | Historical v1.1 tuning/freeze gate; do not execute |
| WP5 | T-523 | ✅ Complete | SARSA + Dyna-Q + broader mechanism implementation foundation |
| WP5 | T-524 | ✅ Complete | Source-backed protocol-v2 research contract freeze |
| WP5 | T-525 | ✅ Complete | Framework-neutral multimethod training/checkpoint/deployment foundation |
| WP5 | T-526 | ✅ Complete | Environment discrimination + method/severity/CPU feasibility pilots |
| WP5 | T-526A | ✅ Complete | DEC-054 boundary settlement and Phase-B v0.3 validation |
| WP5 | T-527 | ✅ Complete | Fair tuning, precision/runtime sizing and statistical freeze |
| WP5 | T-528 | ✅ Complete · historical | Historical PySide6 final-application/frontend baseline |
| WP5 | T-529 | ✅ Complete | Study-first protocol-v2 backend from recipe through evidence/export |
| WP5 | T-530 | ✅ Complete · historical/superseded | UI-independent runtime service/read-only observer foundation |
| WP5 | T-531 | ✅ Complete · prototype history | Functional NiceGUI prototype |
| WP5 | T-532 | ✅ Complete · prototype history | Prototype screenshot/packaging feasibility work |
| WP5 | T-533 | ✅ Complete | Protocol-v2.1 recovery/direct-comparison amendment |
| WP5 | T-534 | ✅ Complete | Clean protocol-v2.1 experiment-first PySide6 UI rebuild |
| WP5 | T-535 | ✅ Complete | Pre-T610 intended-user workflow/UX hardening |
| WP5 | T-536 | ✅ Complete | Final visual polish and richer in-app result visualization |
| WP5 | T-537 | ✅ Complete | Final pre-T610 repository hygiene and active-tree cleanup |
| WP6 | T-600 | ✅ Complete · historical | Frozen protocol-v1.0 final matrix |
| WP6 | T-601 | ✅ Complete · historical | v1.0 evidence validation/freeze |
| WP6 | T-602 | ✅ Complete · historical | v1.0 statistical analysis |
| WP6 | T-603 | ✅ Complete · historical | v1.0 figures/tables/artifacts |
| WP6 | T-604 | ✅ Complete · historical | v1.0 evidence package |
| WP6 | T-610 | 🔒 Blocked — authorization only | Execute frozen protocol-v2.1 final matrix |
| WP6 | T-611 | 🔒 Blocked by T-610 | Validate/freeze protocol-v2.1 final evidence |
| WP6 | T-612 | 🔒 Blocked by T-611 | Predeclared v2.1 RQ1/RQ2/RQ3 statistical analysis |
| WP6 | T-613 | 🔒 Blocked by T-612 | Final v2.1 figures/tables/exports + thesis/defense evidence package |
| WP7 | T-700 | 🔒 Blocked | Recheck current Department/University submission/formatting/defense rules; also requires explicit pre-WP7 approval |
| WP7 | T-701 | ⏸ Deferred | Review completed example theses and derive structure/style guide |
| WP7 | T-710 | ⏸ Deferred | Draft complete Greek thesis from accepted evidence |
| WP7 | T-711 | ⏸ Deferred | Produce review-ready Word thesis + ASSET placement register |
| WP7 | T-712 | ⏸ Deferred | Incorporate supervisor/reviewer corrections and revalidate |
| WP7 | T-713 | ⏸ Deferred | Freeze final thesis deliverable |
| WP7 | T-720 | ⏸ Deferred | Defense narrative/slide outline/evidence map |
| WP7 | T-721 | ⏸ Deferred | Final PowerPoint + speaker material |
| WP7 | T-722 | ⏸ Deferred | Validate/rehearse defense package/demo fallback |
| WP8 | T-800 | ⏸ Deferred | Final bibliography/citation/official-guidance audit |
| WP8 | T-801 | ⏸ Deferred | Final reproducibility/privacy/licensing/docs/thesis/defense/application-asset audit |
| WP8 | T-802 | ⏸ Deferred | Final academic delivery readiness |
| WP8 | T-803 | ⏸ Deferred | Final cleaned Windows standalone application package |

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
results/runs/                          Lower-level whole-run bundles
results/studies/                       Study-level parent lifecycle/evidence bundles
results/thesis-final/                  Historical/frozen thesis evidence namespaces; v2.1 final only after authorization
artifacts/                             Reproducible generated figures/tables/exports

thesis/                                Source material and later thesis deliverables
presentation/                          Later defense sources/assets/final deck

docs/context/                          Current status/tasks/workflow
docs/research/                         Methodology, RQ evidence and figure contracts
docs/experiments/                      Experiment/provenance rules
docs/architecture/                     Backend/frontend architecture
docs/thesis/                           Thesis/defense workflows
docs/decisions/                        Decisions and ADRs
```

## Bibliography boundary

`MariosGiannakaras/ThesisBibliography` is the canonical bibliography lifecycle repository. This repository consumes only an immutable generated snapshot. Formal automatic citation trust is limited to `research/bibliography/citation-ready/`.

The current protocol-v2 consumer snapshot is pinned to upstream SHA:

`f10afcc41e3e1bd877d884cf7a5ae6b5284046f5`

with 597 canonical sources, 121 citation-ready sources and 19 research materials.

## Current control files

Always use these as current authority, in this order:

1. `AGENTS.md`
2. `docs/context/TASKS.md`
3. `docs/context/CURRENT_STATUS.md`

Important current supporting specifications include:

- `configs/protocols/protocol-v2.1-final.json`
- `docs/decisions/DEC-058_PROTOCOL_V2_FINAL_FREEZE.md`
- `docs/decisions/DEC-060_PROTOCOL_V2_1_RECOVERY_AND_DIRECT_COMPARISONS.md`
- `docs/decisions/DEC-061_T534_EXPERIMENT_FIRST_APPLICATION_UX.md`
- `docs/architecture/STUDY_BACKEND_REDESIGN.md`
- `docs/architecture/UI_INFORMATION_ARCHITECTURE.md`
- `docs/research/RQ_EVIDENCE_TRACEABILITY.md`
- `docs/research/T-613_THESIS_FIGURE_INVENTORY.md`

Historical bootstrap, UI and candidate-protocol documentation is context only where explicitly marked historical/superseded. Superseded presentation artifacts need not remain duplicated in the active tree when Git history and recorded CI artifacts preserve the audit trail.

## Evidence and integrity principles

- Filesystem evidence is authoritative; indexes/databases are rebuildable caches.
- Finalized evidence is immutable and checksum/provenance protected.
- Scientific failures remain outcomes and are not replaced by favorable roots.
- Infrastructure failures are distinct and may retry only under the same scientific identity/provenance rules.
- Development/tuning/custom outputs cannot silently become confirmatory evidence.
- Phase-B results must trace to the exact Phase-A scientific checkpoint that generated them.
- Non-recovery remains explicit; the horizon is never substituted as fake observed recovery time.
- Final figures/tables/results are regenerated from frozen validated evidence, not transcribed from the UI.
- No final reserve is accessed before the explicit T-610 scientific authorization gate.
- No thesis writing starts before the later explicit pre-WP7 user approval gate.

## End-to-end lifecycle

The intended project chain is:

> methodology/bibliography → feasibility/pilots → protocol freeze → validated Study backend/application → completed active-tree hygiene → **explicit T-610 authorization** → frozen protocol-v2.1 final Study → evidence validation/freeze → predeclared RQ1/RQ2/RQ3 analysis → rich thesis/appendix/defense evidence package → **explicit pre-WP7 approval** → Greek thesis/review → defense presentation → final audit/delivery

The application is a client and presentation surface of the research backend, not the source of scientific truth.
