# Definition of Done

This file defines project-level completion conditions. It is **not** the operational task tracker. Concrete task IDs, dependencies, in-progress resume state, and next actions are maintained only in `docs/context/TASKS.md`. Phase order and major handoffs are covered by `IMPLEMENTATION_ROADMAP.md` and `EXECUTION_WORKFLOW.md`.

## Foundation and bibliography

- [x] Official application examined and exact titles recorded.
- [x] Old conversation exports classified as historical context only.
- [x] Confirmed requirements, decisions, constraints, contradictions, and open questions documented.
- [x] Official application stored and integrity-pinned.
- [x] Raw chat exports excluded.
- [x] Canonical `ThesisBibliography` ownership boundary established.
- [x] Complete immutable research-corpus consumer implemented.
- [x] First full-corpus baseline imported and validated.
- [x] Private bibliography authentication/read access verified.
- [x] Citation-ready formal-evidence boundary enforced.

## Research infrastructure

- [x] Python 3.12 + `uv` + committed lockfile established.
- [x] Independent importable `src/resilient_agents/` package established.
- [x] Ground-truth/agent-information boundary implemented and tested.
- [x] Independent deterministic RNG streams implemented and tested.
- [x] Scenario/experiment/change/protocol contracts established without hidden scientific defaults.
- [x] Filesystem-first run bundles/provenance/checksums established.
- [x] Guarded one-commit/one-push publication per finalized whole experiment implemented and tested.
- [x] Selective Git LFS policy for large thesis-produced artifacts established.
- [x] Development/tuning/pilot/final separation infrastructure established.
- [x] Documentation governance and stale-state validation established.
- [x] Canonical resumable Codex task registry and interruption-recovery workflow established.
- [x] End-to-end lifecycle/user handoffs and defense-presentation workflow defined.

## Current research/environment phase

- [x] Actual target-machine inventory run and accepted.
- [x] Bounded GridWorld prototype comparison completed and ADR accepted.
- [x] Selected GridWorld implementation and uncertainty schema validated with known-answer/reference-trace tests.
- [ ] Main research question and minimal secondary questions/hypotheses approved.
- [ ] Final model/baseline set justified by citation-ready evidence, environment fit, feasibility, and pilots.
- [x] Resilience/recovery metric estimands operationalized and validated on known-answer fixtures; final protocol roles/parameters remain a later freeze gate.
- [ ] Seeds, budgets, severities, tuning rules, and statistical plan justified for pilots/final protocol.
- [ ] Full headless experiment completes with real selected environment/agents and auditable outputs.
- [ ] Pilot report supports protocol freeze decisions.

## Application completion phase

- [ ] `protocol-v1.0` and analysis plan frozen before final result inspection.
- [ ] Real pilot/headless workflow establishes the required UI feature budget.
- [ ] Thin local Streamlit dashboard uses the same core/configuration/result interfaces.
- [ ] Essential workflows validated: configure, run/monitor, history, compare, detailed analysis, artifacts/export.
- [ ] A real approved multi-seed experiment can be executed end to end through the user-facing application.
- [ ] Primary controls and scientific concepts are self-explanatory through clear labels, helper text, visible units and accurate contextual explanations/tooltips.
- [ ] Pre-run review shows the resolved experiment configuration, protocol, run count and blocking validation before execution.
- [ ] Status/loading/empty/warning/error states use consistent understandable text plus symbols/icons/semantic visual treatment and actionable guidance; color is never the sole essential signal.
- [ ] Destructive/high-impact actions use proportionate confirmation; harmless navigation/configuration is not burdened by unnecessary confirmation steps.
- [ ] A short first-run onboarding/tutorial supports Previous/Next/Skip/Finish, can be replayed from Help/Getting Started, and uses lightweight local state rather than a new account/persistence subsystem.
- [ ] Onboarding/contextual-help implementation remains lightweight; no custom JavaScript/DOM tour framework is added without demonstrated necessity.
- [ ] No scientific logic is duplicated in UI callbacks and no fake progress/metrics/logs exist.
- [ ] Screenshots/views are polished, readable, consistently styled and based on real data/state.

## Final experimental and evidence phase

- [ ] Required final runs complete or transparently accounted for after application/protocol validation.
- [ ] Finalized raw results immutable and checksummed.
- [ ] Failures/cancellations/invalid/excluded runs retained with reasons.
- [ ] Statistical analysis reproducible from frozen evidence.
- [ ] `results/thesis-final/` frozen from the validated final run set.
- [ ] Every thesis figure/table has machine-readable provenance.
- [ ] A versioned thesis/defense evidence package maps RQs, protocol/methods, source IDs, result/run IDs, figures/tables, captions, and planned claims.

## Final thesis phase

- [ ] Official current thesis/template/submission/defense rules reverified.
- [ ] Required bibliography freshness/full-evidence checks completed and synchronized.
- [ ] Complete Greek thesis drafted from citation-ready bibliography and frozen evidence package.
- [ ] Review-ready Word document complete with required bilingual front matter and validated figures/tables/cross-references.
- [ ] Supervisor/reviewer feedback incorporated when received and affected evidence/citations revalidated.
- [ ] Citations/bibliography audited against citation-ready evidence.
- [ ] Claims trace to source IDs or result/artifact IDs.
- [ ] Final thesis `.docx` and any officially required exports frozen/versioned.

## Defense presentation phase

- [ ] Current official defense duration/content/file requirements reverified.
- [ ] Slide narrative and slide-to-thesis/result/source evidence map complete.
- [ ] Final PowerPoint `.pptx` generated from the final thesis/frozen evidence.
- [ ] Embedded speaker notes are synchronized with slide order.
- [ ] Separate full spoken Greek script is complete and suitable for rehearsal/following/reading during preparation.
- [ ] Real application screenshots/demo assets are validated and a non-live fallback exists where needed.
- [ ] PowerPoint rendering, legibility, media, factual consistency, and timing rehearsal pass.

## Final repository/delivery phase

- [ ] Privacy/secret/license scan passed.
- [ ] Reproduction guide validated on a clean environment.
- [ ] Thesis, presentation, speaker material, application, and frozen evidence agree.
- [ ] Required delivery files are present and validated.
- [ ] Final release/commit and thesis result set frozen.
