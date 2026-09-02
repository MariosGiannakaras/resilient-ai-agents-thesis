# User Decisions

This file records explicit **current** user decisions. Historical chats and superseded implementation choices remain context only and do not override later instructions, accepted evidence or repository authority.

## Overall direction

- Primary goal: a correct, scientifically adequate and realistically completable thesis.
- Thesis subject: **comparison/evaluation of resilient AI agents in uncertain/changing environments**.
- GridWorld is the common controlled experimental testbed and visualization surface; it is not the thesis subject.
- The standalone application is an important experiment/control/analysis/demonstration deliverable, but not the main scientific contribution.
- Simplify unnecessary architecture/features, not scientific completeness, usability or visual quality.
- Research/protocol/application/evidence remain the current priority. Thesis Results/Discussion writing remains blocked until the explicit later approval gate.

## Current scientific comparison

The current final scientific authority is protocol-v2.1 under DEC-058 + DEC-060. The retained methods are:

1. **Q-Learning** — tabular off-policy value learning.
2. **SARSA** — tabular on-policy value learning.
3. **DQN** — neural off-policy value approximation.
4. **PPO** — neural on-policy actor-critic/policy-gradient optimization.
5. **Dyna-Q+** — learned-model planning plus recency-based directed re-exploration.

Frozen and Adaptive/Continual are deployment regimes applied to each method in Phase B, not separate algorithms.

Historical F0/C0/D0, R0 and protocol-v1.1 choices remain auditable history only. They are not current final-method guidance.

## Scientific integrity and final reserve

- Protocol-v2.1 owns the selected method-specific configurations, Phase-A interaction budget/probes, final roots, held-out final layouts, Phase-B conditions and 256-interaction horizon.
- The principal fairness budget is actual environment interactions; method-native hyperparameters and update mechanics remain appropriate to each method.
- Phase B uses exact matched FN/FD/AN/AD branching from each method/root/layout unit's own exact Phase-A scientific state.
- RQ1 concerns nominal learning/performance; RQ2 concerns matched resilience/adaptation effects; RQ3 concerns recovery status/speed under the frozen v2.1 temporal contract.
- Recovery uses passive 32-interaction windows, AN versus AD, primary tolerance `0.10`, sensitivity `0.05`/`0.20`, two-window stability and right-censoring at 256 with `recovery_time=null` for non-recovery.
- Multiple roots are independent units; layouts/episodes/probes/windows are not treated as independent replicates.
- Development/tuning/pilot/final evidence remain separated. Failed/cancelled/interrupted/incomplete/invalid/excluded units remain recorded.
- No best-seed selection, outcome-driven root replacement, final-reserve tuning, opaque composite resilience score or post-hoc favorable statistical relabeling.
- Final figures/tables come only from validated stored frozen evidence.
- Agent-visible information and evaluator ground truth remain strictly separated.
- **T-610 final execution, the narrow DEC-062 recovery and T-611 validation/freeze were explicitly authorized and are complete.** `final_reserve_access=false` and the backend token guard remain unchanged. The first 216-job attempt is immutable failed/incomplete history; only the validated/frozen fresh replacement from the corrected merged commit is accepted final evidence. T-612 outcome analysis was not authorized by the T-611 execution.

## Application architecture

- Local single-user application; no authentication, roles, mandatory cloud/public deployment, mobile app or enterprise observability.
- Scientific core and Study backend remain independent under `src/resilient_agents/`; the UI is control/observation/presentation, never a second scientific runner.
- Current application framework: **PySide6 / Qt 6 Widgets** under DEC-059.
- DEC-061 controls the current T-534 experiment-first product/UX model while preserving DEC-059's framework/runtime/scientific-firewall clauses.
- Historical Streamlit/React/NiceGUI implementations are superseded and must not guide the new implementation except as optional historical reference.
- Final standalone Windows packaging is intentionally deferred until after the thesis and will target the finally accepted rebuilt UI.
- Pause/resume/stop/cancel/restart controls appear only when technically safe; unsupported controls are explicit rather than simulated.
- Resource telemetry, if shown, remains lightweight and truthful rather than becoming an observability subsystem.

## Clean UI restart — current explicit direction

- The previously paused UI implementation is considered incomplete/non-authoritative for continuation.
- Restart implementation from a **fresh current `main`**, not from the paused branch/worktree or pre-v2.1 assumptions.
- Before implementing, read `AGENTS.md`, `TASKS.md`, `CURRENT_STATUS.md`, DEC-059, DEC-060, DEC-061, `configs/protocols/protocol-v2.1-final.json` and `docs/research/RQ_EVIDENCE_TRACEABILITY.md`.
- Rebuild the presentation layer from today's protocol-v2.1 and Study/evidence contracts.
- Existing PySide6 presentation code may be replaced from scratch where useful. First classify `src/resilient_agents/desktop/` so UI-neutral read-model, evidence adapter, provenance and execution-policy contracts are preserved.
- The UI must never calculate recovery thresholds, root reductions, estimands or final scientific conclusions from raw evidence. It presents validated stored evidence/read models.
- UI implementation/testing uses DEVELOPMENT/synthetic fixtures only unless and until separately authorized real evidence exists.
- No UI path may bypass the backend final-experiment authorization guard.
- Everything user-facing should be self-explanatory through appropriate wording, hierarchy, symbols/icons, semantic visual treatment, help/tooltips and actionable states.

## Experiment-first T-534 product model

- The application is organized around the **scientific experiment**, not around StudyStore/jobs/artifacts.
- Primary navigation is deliberately limited to **Experiment / Run / Results / Evidence**. Help/onboarding and technical details are contextual/secondary.
- The final Thesis experiment always contains all five frozen methods. The user cannot deselect methods from the final experiment.
- Method selection is permitted only in DEVELOPMENT/Exploratory configuration where the backend explicitly supports it.
- Frozen and Adaptive are matched Phase-B deployment regimes of the same method. They are never shown as algorithms or a mutually exclusive `Frozen OR Adaptive` choice.
- Experiment should explain the complete scientific story: nominal learning → exact checkpoint → matched Phase B → disturbances → Frozen vs Adaptive → RQ1/RQ2/RQ3.
- Study history, job counts, artifact IDs, hashes and lineage remain available but are secondary reproducibility/technical detail rather than the main user journey.

## Run / live presentation

- The GridWorld is a major Run-screen surface, not a small widget below administrative tables.
- During Phase A, show one large nominal GridWorld for the current method.
- During Phase B, show **Frozen — learning off** and **Adaptive — learning continues** simultaneously as two large side-by-side GridWorlds when an exact matched interaction pair is available.
- A compact status strip shows progress/state across the five methods without implying ranking.
- Primary live information is method, phase, condition, interaction, intended/executed action and reward.
- Root/layout identity, episode/environment-step detail, true state, delivered observation, branch/regime IDs, disturbance flags, change-event IDs and hashes belong under progressive technical disclosure unless needed to explain an error.
- Live visualization is presentation-only, lossy and non-blocking; missing matched frames are shown as unavailable/waiting rather than fabricated.

## Novice-first UI and interaction

- UI must be understandable by someone with no coding, RL, experiment-setting or repository knowledge.
- Plain-language primary labels; technical identifiers secondary under reproducibility/technical details.
- Explain methods, disturbance conditions, settings, metrics, units, ranges and consequences with concise helper text, contextual help and progressive disclosure.
- Required workflow information must not exist only in tooltips.
- Pre-run/review views show readable resolved configuration and blocking issues without exposing dangerous editability for frozen scientific choices.
- Status uses stable text plus icons/symbols and accessible semantic visual treatment; color is never the sole meaning.
- Empty/loading/disabled/warning/error/unavailable states explain what happened and the useful next action.
- Confirm destructive/high-impact actions only; ordinary use remains friction-light.
- The UI should be modern, compact and information-dense rather than sparse/oversized.
- Avoid excessive permanent cards, banners and help paragraphs; preserve a clear visual hierarchy.
- Purposeful hover/focus/selection transitions and GridWorld/chart/status animation are allowed, but must never fabricate progress/trajectory/data or alter scientific execution/RNG/timing.
- Desktop/laptop usability is required; mobile parity is not.

## Results and evidence presentation

- Results are organized explicitly as **RQ1 — Learning / RQ2 — Resilience & Adaptation / RQ3 — Recovery**.
- RQ1 should use a real interaction-axis learning curve where validated stored Phase-A probe outputs support one. The UI must not invent a new aggregate/root reduction merely to draw a curve.
- RQ1 also exposes final nominal performance, stored intervals/denominators, trajectory/time-average evidence and stored direct method comparisons where available.
- RQ2 keeps primary adaptation benefit `(FN-FD)-(AN-AD)` separate from supporting Frozen loss `FN-FD` and Adaptive loss `AN-AD`, with condition filtering and stored direct contrasts.
- RQ3 exposes stored AN-vs-AD recovery trajectory, recovery/non-recovery status, observed recovery time conditional on recovery, separately named restricted fixed-horizon delay, right-censoring and stored sensitivities/contrasts where available.
- A right-censored non-recovery at horizon 256 is never displayed as `recovery time = 256`; observed recovery time remains missing/null.
- The interface must not declare a winner, best algorithm, significance or statistical superiority unsupported by the frozen analysis contract.
- Clearly distinguish DEVELOPMENT/synthetic fixtures, live/provisional state, finalized run state and validated versioned evidence.
- Historical schema-v1 evidence remains truthful historical evidence and must not be silently upgraded to v2.1 recovery semantics.
- Evidence is user-friendly first: validation/evidence state, results/exports and thesis-ready outputs when legitimate. Provenance/IDs/hashes/lineage remain available under progressive disclosure rather than dominating the primary interface.
- Existing screenshots are historical review assets/reference only; the clean rebuild is not required to preserve their layout or styling.

## Repository and continuity

- `TASKS.md` is the canonical resumable ledger; each implementation session starts by reading current repository authority and inspecting actual Git/PR/CI state.
- Use one active implementation branch/PR for the clean UI rebuild.
- Old merged/stale remote working branches may be deleted after confirming they contain no unique required work. Deliberate archive/provenance branches may remain.
- Repository cleanup must not delete scientific evidence, accepted decisions, final protocol authority, thesis source material or unique unmerged work.
- Material changes reconcile related active docs/issues/prompts/tests/workflows in the same PR.
- Testing stays risk-based/proportional; representative contracts/integration/UI checks are preferred over quota-consuming exhaustive test expansion.
- Historical finalized evidence is immutable; no fabricated citations/data/results/progress/conclusions.

## Thesis, review and defense

- Thesis main language is Greek and final thesis deliverable is Microsoft Word unless official guidance changes.
- No verified final deadline or defense schedule is currently known.
- Supervisor-specific corrections will be recorded only when actually received.
- Official submission/template and defense requirements will be rechecked near delivery rather than invented now.
- ChatGPT is preferred for later Greek drafting/review/narrative/placement guidance; repository/Codex work owns reproducible technical evidence/assets/checks.
- Final defense deliverables remain later evidence-gated work.

## Bibliography and repository visibility

- `MariosGiannakaras/ThesisBibliography` owns source discovery/originals/OCR/conversion/scientific analysis/evidence/source selection.
- This thesis repo consumes the verified generated corpus; `citation-ready/` is the formal citation surface.
- Generated bibliography content is not manually edited here.
- Repository-authored operational/technical material is English; exact official Greek text remains exact; thesis/expected defense materials remain Greek unless rules change.
- The repository remains **public** by explicit user decision; secrets/credentials/raw conversation exports remain forbidden in tracked content.
