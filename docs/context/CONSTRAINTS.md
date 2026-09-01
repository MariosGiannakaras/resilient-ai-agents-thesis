# Constraints

## Compute and environment

- Accepted actual-machine inventory is `SYSTEM_CAPABILITY_REPORT.md` plus `system-capability.accepted.json`; regenerate after material host/runtime changes.
- CPU execution is the required supported scientific baseline. Do not assume CUDA/ROCm/DirectML.
- Python is 3.12 and repository dependency management uses `uv`, `pyproject.toml`, `.python-version` and committed `uv.lock`.
- The root locked environment is part of the historical/reproducible research surface. The active PySide6 application dependency overlay is `requirements/application-ui.txt`; do not infer the current UI framework from superseded packages that may still exist in the historical root lock.

## Scientific authority

- Scientific logic lives under `src/resilient_agents/` and remains usable without importing or launching the UI.
- DEC-058 and `configs/protocols/protocol-v2.0-final.json` are immutable historical protocol-v2.0 freeze authority.
- DEC-060 and `configs/protocols/protocol-v2.1-final.json` are the current pre-execution scientific authority.
- The retained comparison methods are Q-Learning, SARSA, DQN, PPO and Dyna-Q+.
- Final Phase-A and Phase-B dimensions, selected method-specific hyperparameters, roots, held-out layouts, conditions and budgets are frozen by protocol-v2.1 and are not UI choices.
- Actual environment interactions are the principal fairness budget. Method-native hyperparameters/update mechanics remain method-appropriate.
- Evaluator ground truth is separated from agent-visible information. Scientific randomness uses independently derived deterministic streams.
- Final roots/layouts/seeds are not tuning inputs and must not be selected or replaced from observed outcomes.
- Scientific failures/cancellations/invalid units remain recorded; favorable replacement roots/seeds are forbidden.

## Final-reserve execution gate

- `final_reserve_access=false` and `execution_authorization=requires-explicit-t610-gate` remain mandatory until a separate explicit final-scientific-experiment authorization is given.
- The generic Study backend denies confirmatory/final execution by default without the separate authorization token.
- UI work, tests, screenshots, synthetic smoke runs, documentation changes and repository cleanup never constitute final-experiment authorization.
- Do not inspect or execute final-reserve outcomes, begin the final matrix, or start Results/Discussion writing before the separate authorization gate.

## Evidence and analysis

- Durable filesystem Study/run bundles and registered artifacts are the evidence source of truth; indexes/databases/read models are rebuildable or presentation-oriented views.
- Finalized raw evidence is immutable/checksummed and provenance must remain deterministic.
- Root is the independent statistical unit. Layouts, episodes, probes and recovery windows are repeated/nested observations.
- RQ1 uses Phase-A nominal-learning evidence; RQ2 uses matched FN/FD/AN/AD effects; RQ3 uses the frozen AN-vs-AD recovery contract.
- Protocol-v2.1 recovery uses passive 32-interaction windows over the 256-interaction Phase-B horizon. Windows cross episode boundaries without reset/realignment.
- Primary recovery tolerance is `AN - AD <= 0.10`, with frozen sensitivities `0.05` and `0.20`; stable recovery requires two consecutive in-tolerance windows.
- Non-recovery is right-censored at 256 with `recovery_time=null`; 256 is never fabricated as an observed recovery time.
- Direct method contrasts are root-paired A-minus-B after equal layout reduction and use common independent roots when failures create asymmetry.
- Two-sided 95% Student-t pointwise intervals use the predeclared critical value for the actual independent-root count. No formal p-value superiority family or post-hoc significance relabeling is authorized.
- Final figures/tables must be generated only from validated stored evidence. See `docs/research/RQ_EVIDENCE_TRACEABILITY.md`.

## Application architecture

- DEC-059 is the current application architecture authority: Python-native PySide6 / Qt 6 Widgets over the framework-neutral Study backend.
- Historical Streamlit/React/NiceGUI application implementations are superseded history, not current implementation guidance.
- The current UI restart must begin from fresh `main` and may replace the presentation layer from scratch. Existing pre-restart widgets/layouts/styles/screenshots are reference/history only, not design authority.
- Preserve UI-neutral Study backend, evidence read-model, execution-policy and provenance contracts unless a concrete defect requires a bounded backend fix.
- Qt presentation state never owns scientific identity, RNG, checkpoint state, experiment configuration, evidence reduction, recovery thresholds or finalization.
- The UI presents validated stored evidence; it does not recompute scientific estimands from raw evidence.
- Local single-user operation; no required cloud/public deployment, authentication, mobile app or distributed orchestration.
- Root `run_app.bat` remains the repository-checkout launcher unless the accepted UI rebuild deliberately replaces it with an equivalent supported launcher.
- Final standalone Windows packaging is deferred until after the thesis and is not a pre-UI or pre-final-experiment gate.

## UI/UX contract

- Normal use must be understandable to a non-programmer with no prior RL/model/configuration/repository knowledge.
- Use plain-language primary labels, technical IDs as secondary detail, concise helper text, visible units/ranges/consequences, tooltips/contextual help and progressive disclosure.
- Required workflow information cannot exist only in a tooltip.
- Status meaning uses text plus consistent symbols/icons and accessible semantic visual treatment; color alone never carries essential meaning.
- Empty/loading/disabled/warning/error/unavailable states are actionable and self-explanatory.
- The interface should be modern, compact and information-dense without becoming visually noisy.
- Animation/interpolation must never fabricate progress, trajectories or data and must never alter scientific timing/actions/RNG.
- Development/synthetic/test data must be clearly labelled and never visually promoted as thesis evidence.

## Testing and validation budget

- Testing is risk-based and proportional to changed behavior and scientific/reliability impact.
- Use targeted tests during implementation; repository CI is the canonical full-suite guard when available.
- There is no coverage-percentage target. Broad fuzz/property/mutation/exhaustive matrices/snapshot proliferation/large E2E suites require a concrete risk justification.
- CI uses tiny deterministic fixtures, known-answer cases, contracts and representative smoke/integration paths; pilot/final experiment matrices are never tests.
- Required config/schema/provenance/lifecycle conditions fail closed. Optional unavailability remains explicit.

## GridWorld and third-party code

- GridWorld is the controlled experimental testbed and visualization environment, not the thesis subject.
- DEC-032 selects the project-owned Gymnasium GridWorld using Gymnasium 1.3.0; MiniGrid/Pygame remain prototype-only.
- Environment and agents use shared scientific contracts rather than a second UI-specific execution interface.
- Third-party code requires source/license/maintenance/security/API/testability/determinism/suitability review and pinned versions where scientifically or operationally required.

## Documentation and repository hygiene

- `TASKS.md` is the canonical dependency/task ledger and `CURRENT_STATUS.md` is the compact current-state summary.
- A material change is incomplete until affected active docs/prompts/tasks/issues/decisions/status/tests/workflows are reconciled in the same PR.
- Historical decisions remain auditable and are marked superseded rather than rewritten.
- Repository cleanup must not delete historical scientific evidence, canonical decisions, final protocol authority, thesis source material or unique unmerged work.
- Generated bibliography content is never manually edited. `MariosGiannakaras/ThesisBibliography` owns the bibliography lifecycle; this repo consumes its generated snapshot read-only.
- The repository remains public by explicit user decision. Secrets, credentials and raw conversation exports are forbidden in tracked content.

## Academic delivery

- Thesis main language is Greek and the final academic document is Microsoft Word unless later official guidance changes this.
- No final deadline, defense schedule, exact defense duration or current official submission package is known; never invent them.
- Current Word/template/submission and defense requirements are rechecked near delivery.
- Thesis/presentation writing remains blocked until the evidence and explicit pre-WP7 approval gates are satisfied.
