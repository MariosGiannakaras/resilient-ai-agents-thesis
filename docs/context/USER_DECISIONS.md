# User Decisions

This file records explicit current user decisions. Historical chats provide context but do not override later instructions, accepted evidence or repository decisions.

## Overall direction

- Primary goal: a correct, scientifically adequate and realistically completable thesis.
- Thesis subject: **comparison/evaluation of resilient AI agent strategies in uncertain/changing environments**.
- GridWorld is the common controlled experimental testbed and visualization surface; it is not the thesis subject.
- The standalone application is an important experiment/control/analysis/demonstration deliverable, but not the main scientific contribution.
- Simplify unnecessary architecture/features, not scientific completeness, usability or visual quality.
- Research/protocol/application/evidence remain current priority. Normal thesis writing stays blocked until the explicit pre-WP7 approval gate.

## Current scientific strategy set

DEC-047 is the current agent-selection direction. Candidate v1.1 targets five main strategies, subject to implementation/non-final validation/freeze:

1. **Fixed Q-Learning** — uses the learned nominal policy but does not learn during evaluation; historical technical identity `F0`.
2. **Adaptive Q-Learning** — continues ordinary off-policy Q-learning online; historical technical identity `C0`.
3. **SARSA** — on-policy continual model-free adaptation.
4. **Dyna-Q** — continual learning plus an empirical learned model and planning, without recency bonus.
5. **Dyna-Q+** — Dyna-Q-style planning plus directed re-exploration of long-untried actions; historical technical identity `D0`.

The set is mechanism-driven: no adaptation → off-policy model-free adaptation → on-policy model-free adaptation → model-based planning → planning plus explicit re-exploration.

- Historical R0 robust-planner pilot evidence is retained, but unchanged R0 is not reinstated after severe nominal truncation.
- A redesigned Robust Planner may become a conditional sixth main comparator only if a small predeclared non-final nominal-viability/fairness/runtime gate passes.
- **Random Agent** may be used as a clearly labelled non-ranked lower/reference fixture.
- A nominal/fully-informed planner may be used only as a clearly privileged scale/debug reference, never in a fair ranking.
- Expected SARSA and extra tabular variants remain deferred unless a distinct non-final scientific need appears.
- Do not add DQN/PPO/SAC/deep/meta-learning merely to increase model count; reopen deep methods only if the accepted RQ/representation actually requires function approximation.

## Scientific settings and experimental integrity

- Preserve validated Fixed/Adaptive Q-Learning alpha `0.5`, gamma `0.96875`, epsilon `0.125`, 512 training episodes/layout, 16 pre-change episodes, 32 post-change episodes, horizon 48 and current target 32 paired final roots unless explicit evidence-backed amendment changes them.
- SARSA may receive only a small predeclared fairness-relevant non-final tuning surface.
- Dyna-Q and Dyna-Q+ should share learned-model/planning machinery and matched planning-step budgets where appropriate; Dyna-Q has explicit no-recency-bonus semantics.
- Candidate v1.1 keeps seven single-factor conditions, structural remap names `action-remap-2-swap` / `action-remap-4-cycle`, four fresh held-out final layouts and a fresh precommitted final seed bank.
- Multiple settings mean **protocol-approved resolved configurations**, not an unrestricted hyperparameter playground.
- Every compared configuration has stable identity/hash/provenance and multiple predefined roots/repetitions. Single-run ranking, best-seed selection, best-final switching and post-hoc favorable parameter selection are forbidden.
- Development/tuning/pilot/exploratory/final evidence remain separated. Failed/cancelled/interrupted/incomplete/invalid/excluded runs remain recorded.
- Primary v1.1 reporting: cumulative deficit, immediate degradation and terminal performance/gap. Recovery remains secondary/sensitivity; no opaque composite resilience score.
- Paired effects, 95% confidence intervals, explicit `n` and layout-aware interpretation are required for v1.1 final analysis.
- Final figures/tables come only from real stored frozen evidence.
- Agent-visible information and evaluator ground truth remain strictly separated. No scientific agent receives true state, executed-action truth, changepoint/regime identity or disturbance flags unless a future protocol explicitly changes the information question.

## User-facing model naming

- Ordinary users must not be expected to understand `F0`, `C0`, `D0`, method schema IDs or config hashes.
- Primary UI concept is **Agent strategy**.
- Use the five full human-readable strategy names above in New Experiment, Runs, Compare, charts, legends, screenshots and thesis/presentation-facing exports.
- Each strategy has a plain one-sentence explanation plus useful mechanism badges such as `Does not adapt`, `Model-free`, `On-policy`, `Off-policy`, `Uses planning`, `Re-explores for change`.
- Historical/internal IDs, schema names and hashes remain available only under **Technical details / Reproducibility**.
- The thesis may introduce stable abbreviations after the full names, but must not rely on unexplained repository IDs.

## Application architecture and execution

- Local single-user application; no authentication, roles, mandatory cloud/public deployment, mobile app or enterprise observability.
- Scientific core remains independent under `src/resilient_agents/`; UI is a control/observation/analysis layer, never a second scientific runner.
- Current framework: **NiceGUI 3.16 native mode (`pywebview`)** over Python runtime/scientific services.
- Historical Streamlit and temporary React/Vite implementations are superseded; no active second frontend stack.
- Root `run_app.bat` remains one-click repository-checkout launcher.
- Final delivery also contains a cleaned Windows NiceGUI/PyInstaller `onedir + windowed` application folder opening in its own desktop window without recipient-installed Python/Node or browser/terminal interaction.
- Pause/resume/stop/cancel/restart appear only when technically safe; unsupported controls are explicit rather than simulated.
- Resource telemetry is a lightweight truthful CPU/RAM/disk/supported-GPU snapshot, not an observability subsystem.

Required workflow without code/console/routine manual Git:

> Dashboard → configure approved experiment/strategy/settings → understand resolved configuration → launch → monitor truthful live state/GridWorld/charts → history/detail → compare compatible strategies/configurations → inspect/export artifacts.

After application acceptance, approved/frozen experiments run directly from the desktop application on the validated thesis machine. Codex/console is not required merely to execute them; Codex remains for code/protocol/debugging changes. Backend owns resolved config, seeds, execution, persistence/provenance, finalization and guarded Git publication.

## Novice-first UI and interaction

- UI must be understandable by someone with no coding, RL, model, experiment-setting or repository knowledge.
- Plain-language primary labels; technical identifiers secondary.
- Explain strategies, uncertainty conditions, settings, metrics, units, ranges and consequences with concise helper text, info icons/tooltips and contextual/expandable help.
- Tooltips supplement rather than hide information required for safe decisions.
- Use progressive disclosure for advanced/model-specific settings.
- Pre-run review shows readable strategy/layout/condition/seeds/repetitions/budgets/hyperparameters/protocol/stage/run count/retention/evidence classification and blocking validation.
- Status uses stable text + icons/symbols + accessible semantic colors; color is never the sole meaning.
- Empty/loading/disabled/warning/error/unavailable states explain what happened and the useful next action.
- Confirm destructive/high-impact actions only; ordinary use remains friction-light.
- Short first-run onboarding is skippable/replayable; every page remains understandable without it.
- Modern compact information-dense UI with consistent iconography/spacing/typography/cards/tables/filters.
- Restrained hover/focus/selection micro-interactions and smooth purposeful GridWorld/chart/status animations are desired, but animation must never fabricate progress/trajectory/data or affect execution/RNG/timing.
- Desktop/laptop responsiveness required; mobile parity is not.

## Visual analytics and screenshots

- **Plotly:** stored scientific/thesis/presentation-ready comparisons, distributions, heatmaps, paired effects/CIs where available.
- **ECharts:** real live/provisional telemetry and compatible multi-strategy/configuration overlays.
- **Mermaid:** explanatory strategy/experiment/information-flow infographics using human-readable names.
- **AG Grid Community:** filterable/sortable/selectable analytical run/result/artifact tables.
- Historical v1.0 error bars remain truthfully labelled SD until real paired CI artifacts exist.
- `LIVE / PROVISIONAL`, finalized-run and versioned analysis/evidence are visibly distinct.
- Root `ui-screenshots/` contains stable accepted UI review screenshots; diagnostic fixture captures are clearly non-scientific.
- User will capture useful real screenshots/GIF/video for thesis/defense when instructed. Later each receives an `ASSET-*` record with exact state/run/config, crop, target section/slide, caption, placement/size, evidence identity and static fallback.

## Repository, continuity and testing

- One active implementation branch/PR for the current pre-WP7 package.
- `TASKS.md` is the canonical resumable ledger; every Codex session reads AGENTS/TASKS/CURRENT_STATUS and inspects actual Git/PR/CI state.
- Newly discovered work/decisions go into durable tasks/issues/decisions/status so chat/quota changes do not lose them.
- Use X/Y only from objective canonical denominators; in-progress/failed work never counts complete.
- Material changes reconcile related active docs/issues/prompts/tests/workflows in the same PR.
- Testing is risk-based/proportional: strong known-answer/contract/invariant/representative integration tests, no arbitrary coverage/fuzz/mutation/snapshot project and no pilot/final matrices in CI.
- PR CI is the canonical full-suite guard.
- Historical finalized evidence is immutable; no fabricated citations/data/results/progress/conclusions.

## Thesis, review and defense

- Project continues through v1.1 final evidence, Greek Word thesis, review/revision, final freeze, PowerPoint defense and final audits.
- WP7 remains blocked until scientific/application refinement, T-511 human acceptance and explicit user approval.
- Thesis main language is Greek and final thesis deliverable is Microsoft Word unless official guidance changes.
- Current official instructions override historical examples; later supplied theses are contextual examples only.
- ChatGPT is preferred for later Greek drafting/review/narrative/placement guidance; Codex/repository automation owns reproducible evidence/assets/technical checks.
- Microsoft Word is final `.docx` composition/inspection surface; Microsoft PowerPoint is final `.pptx` inspection/rehearsal surface; Canva is optional polish only.
- Final defense package includes `.pptx`, embedded speaker notes, separate full spoken Greek script and tested live-demo/static fallback.

## Bibliography and language

- `MariosGiannakaras/ThesisBibliography` owns source discovery/originals/OCR/conversion/scientific analysis/evidence/source selection.
- Thesis repo consumes verified generated corpus; `citation-ready/` is the formal citation surface.
- Source-derived evidence remains in original source language.
- Repository-authored operational/technical material is English; exact official Greek text remains exact; thesis/expected defense materials remain Greek unless rules change.
