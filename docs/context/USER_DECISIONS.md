# User Decisions

This file records explicit current user decisions. Historical chats provide context but do not override later instructions, accepted evidence or repository decisions.

## Overall direction

- Primary goal: a correct, scientifically adequate, realistically completable thesis.
- The application is an important deliverable and demonstration/analysis surface, but not the main scientific contribution.
- Simplify unnecessary architecture/features, not scientific completeness, usability or visual quality.
- Repository covers the full thesis lifecycle; `ThesisBibliography` remains the explicit bibliography-lifecycle exception.
- Current priority remains research/protocol/application/evidence; normal thesis writing/formatting stays blocked until the explicit pre-WP7 approval gate.

## Research and experiments

- Use a simple controlled GridWorld and a small scientifically justified set of distinct agent roles/uncertainty mechanisms.
- Current candidate-v1.1 comparator direction is:
  - **F0:** frozen tabular Q-learning baseline;
  - **C0:** continual tabular Q-learning adaptation;
  - **D0:** Dyna-Q+ model-learning/planning/re-exploration role.
- Historical R0 pilot evidence is retained, but the accepted R0 construction is not reinstated unchanged after severe nominal truncation.
- Do not add deep/advanced RL merely to increase model count.
- Preserve validated F0/C0 alpha `0.5`, gamma `0.96875`, epsilon `0.125`, 512 training episodes/layout, 16 pre-change episodes, 32 post-change episodes, horizon 48 and 32 paired final roots.
- Candidate v1.1 keeps seven single-factor conditions, uses structural remap names `action-remap-2-swap` / `action-remap-4-cycle`, four fresh held-out final layouts and a fresh precommitted final seed bank.
- D0-specific planning parameters are selected only through a small predeclared non-final tuning search.
- Single-run comparison is forbidden; use paired/multiple seeds and preserve development/tuning/pilot/final separation.
- Failed/cancelled/interrupted/incomplete/invalid/excluded runs remain recorded.
- Primary v1.1 reporting: cumulative deficit, immediate degradation, terminal performance/gap. Recovery is secondary/sensitivity; do not choose a post-hoc favorable threshold or create an opaque composite resilience score.
- Paired effects, 95% confidence intervals, explicit n and layout-aware interpretation are required for v1.1 final analysis.
- Final figures/tables come only from real stored data and frozen accepted evidence.

## Scientific integrity and execution

- Agent-visible information and evaluator ground truth remain strictly separated.
- GridWorld/live visualization never changes scientific execution, actions, timing or RNG.
- Resolved parameters/provenance are stored per whole experiment.
- A run ID is one whole experiment, possibly containing many seeds/episodes.
- Finalized whole experiments produce at most one guarded automatic result commit/push; never one permanent commit per seed/episode.
- Useful thesis-produced artifacts are retained when storage permits; configured large formats may use Git LFS.
- A final campaign begins only after its protocol is frozen and the intended application workflow is accepted; any headless fallback uses the identical scientific core/configuration path.

## Application architecture

- Local, single-user application; no authentication, roles, multi-user system, mandatory cloud/public deployment, mobile app or enterprise observability.
- Scientific core remains independent under `src/resilient_agents/`; UI is a control/observation/analysis layer, never a second runner.
- **DEC-044 current framework:** NiceGUI 3.16 native mode (`pywebview`) over the Python runtime/scientific services.
- Historical Streamlit implementation and temporary React/Vite exploration are superseded; no active second frontend stack is retained.
- Root `run_app.bat` stays the normal one-click launcher from a repository checkout.
- Final thesis delivery also includes a cleaned Windows NiceGUI/PyInstaller **onedir + windowed** application folder that opens in its own desktop window without requiring recipient-installed Python/Node or browser/terminal interaction.
- Pause/resume/stop/cancel/restart appear only where technically safe; unsupported capabilities are explicit rather than simulated.
- Resource telemetry is a lightweight truthful current CPU/RAM/disk/supported-GPU snapshot, not an observability subsystem.

## Required application journey

The user must be able to complete the real workflow without code/console/manual routine Git:

> Dashboard → configure approved experiment → understand/validate resolved configuration → launch → monitor truthful active state/live GridWorld/live charts → inspect history/detail → compare compatible agents/settings/results → inspect/export artifacts.

Application completion means this journey works end to end on the scientific core; successful page rendering alone is not completion.

## Novice-first UI and onboarding

- UI must be understandable by someone with no coding, RL, model, experiment-setting or repository knowledge.
- Use plain-language primary labels; technical IDs remain secondary reproducibility detail.
- Explain agents, uncertainty conditions, settings, metrics, units, ranges and consequences with concise helper text, info icons/tooltips and contextual/expandable help.
- Tooltips are supplemental; information required to make a safe decision must remain visible or otherwise directly accessible.
- Use progressive disclosure for genuinely advanced/model-specific settings rather than exposing internal switches by default.
- Before launch, show a readable resolved configuration including agents, layout, condition/severity, seeds/repetitions, budgets, relevant hyperparameters, protocol/stage, run count/retention/evidence classification and blocking validation.
- Status/validation meaning uses stable understandable text + icons/symbols + semantic accessible colors; color alone never carries essential meaning.
- Empty/loading/disabled/warning/error/unavailable states explain what happened/why and the useful next action.
- Confirm only destructive/high-impact actions; routine navigation/configuration remains friction-light.
- A short first-run onboarding is added after screen structure stabilizes: Previous/Next/Skip/Finish, skippable/non-blocking and replayable from Help/Getting Started using lightweight local state.
- Every page must remain understandable if onboarding is skipped.

## Visual design and interaction

- Final UI is **modern and compact**: information-dense without becoming cryptic, oversized or decoration-heavy.
- Use consistent iconography, spacing, typography, cards, tables, filters and semantic status treatments.
- Purposeful colors support comprehension/accessibility and agent identity; no color-only meaning.
- Use restrained hover/focus/selection micro-interactions and smooth transitions where they improve affordance/state comprehension.
- Smooth GridWorld/chart/status animations are desired, but animation/interpolation must never fabricate scientific progress/trajectory/data or affect execution timing/RNG/actions.
- Essential state remains understandable with reduced motion where practical.
- Desktop/laptop responsive layout is required; mobile parity is not.

## Visual analytics and thesis/presentation screenshots

- Application should expose enough clear analytical information that appropriate real-data views can be directly screenshot for the thesis and defense presentation.
- **Plotly:** stored scientific comparison figures (distributions, grouped comparisons, heatmaps, paired effects/CIs where available).
- **ECharts:** real live/provisional telemetry and compatible multi-agent/settings overlays during runs.
- **Mermaid:** explanatory F0/C0/D0 and experiment/information-flow infographics.
- **AG Grid Community:** filterable/sortable/selectable analytical run/result/artifact tables.
- Historical v1.0 error bars must remain truthfully labelled as SD until real paired CI artifacts exist.
- Clearly distinguish `LIVE / PROVISIONAL`, finalized-run and versioned analysis/evidence data; live values do not become final thesis evidence automatically.

## Screenshots and packaging

- Root `ui-screenshots/` will contain stable accepted UI review screenshots; CI may use browser mode for deterministic captures of the same NiceGUI pages.
- Diagnostic fixtures/screenshots are not scientific evidence and must be labelled accordingly.
- Final UI screenshots are shown to the user for review before application acceptance.
- Native Windows launch/close/restart and packaged onedir behavior must be validated before delivery.

## Scope restraint

- Do not implement microservices, Kubernetes, distributed workers, complex permission systems, enterprise observability, plugin ecosystems or remote-execution platform features without a demonstrated thesis need.
- Queue priorities, advanced orchestration/checkpoint UX and optional AI assistance remain deferred unless real workflow evidence justifies them.
- Every feature maps to research, reproducibility, usability or thesis-delivery value.

## Codex continuity, progress and quota interruption

- `docs/context/TASKS.md` is the single canonical resumable task registry with stable IDs/checklists/dependencies.
- Every Codex session reads the three-file session-start core and inspects Git/branch/PR/CI state before work.
- Continue the long-running goal autonomously through dependency-valid work; routine Git, PR, CI, objective diff review, fixes and task reconciliation are execution work rather than user gates.
- Preserve exact unfinished state (branch/PR, last validation, changed files, tests, blocker, next action) before a quota/session interruption can lose it.
- Newly discovered required work is added durably to TASKS/issues/decisions/status rather than remaining only in chat.
- One active implementation branch/PR is used for the current pre-WP7 refinement package.
- Use X/Y only from objective canonical denominators; in-progress/failed work never counts as complete.
- Do not submit an APPROVE review on own PR. Current package explicitly defers merge until integrated user-facing acceptance even if normal workflow could otherwise squash-merge a green own PR.

## Testing effort

- Testing is risk-based/proportional and must not consume more quota/time than justified by material risk.
- Prefer a few strong known-answer/contract/invariant/representative integration tests over near-duplicate coverage expansion.
- No arbitrary coverage target, broad fuzz/property/mutation testing, exhaustive parameter combinations, snapshot proliferation or final/pilot matrices in CI without a concrete need.
- Run targeted tests during implementation; PR CI is the full-suite guard when available. Successful CI is recorded without repeated log analysis.

## End-to-end lifecycle

- Project continues beyond the application through v1.1 final runs, frozen analysis/evidence, Greek Word thesis/review/final freeze, PowerPoint defense package and final audits.
- Thesis/presentation consume a frozen evidence package rather than reconstructing claims from memory/raw runs.
- WP7 writing/defense work remains blocked until scientific/application refinement is satisfactory, T-511 human acceptance passes, and the user explicitly approves starting WP7.

## Thesis writing/review

- Thesis main language is Greek and final thesis deliverable is Microsoft Word unless official guidance changes.
- Current official instructions override historical examples.
- Normal chapter drafting/final styling are deferred until accepted evidence exists.
- Later supplied completed theses are contextual examples only, not scientific/official formatting authority.
- Supervisor/reviewer corrections received later enter an explicit revision/revalidation cycle.

## Defense presentation

- After thesis stability, produce a PowerPoint `.pptx`, embedded speaker notes and a separate full spoken Greek script, all traceable to final thesis/citation-ready sources/frozen evidence.
- Validate rendering, legibility, factual/numerical consistency, timing and demo/screenshot fallback before presentation freeze.
- Recheck current official defense duration/content/file/template/live-demo rules near defense; do not invent them now.
- Microsoft PowerPoint is the final inspection/rehearsal surface; optional Canva/design tooling never becomes scientific source of truth.

## GridWorld, hardware and tooling

- Project-owned GridWorld is the accepted core path; legacy code recovery is not required.
- Third-party code/dependencies require current license/maintenance/compatibility/suitability review.
- Codex/system inventory collects inspectable hardware/software/storage; user does not manually transcribe available machine information.
- CPU is validated scientific baseline; NVIDIA/CUDA is not assumed.

## Bibliography and language

- `MariosGiannakaras/ThesisBibliography` owns source discovery/originals/OCR/conversion/scientific analysis/evidence/source selection.
- Thesis repo consumes verified generated corpus under `research/bibliography/`; nested citation-ready layer is formal citation surface.
- Source-derived scientific evidence remains in the original source language.
- Repository-authored operational/technical material is English; exact official Greek text stays exact; thesis/expected defense-language materials remain Greek unless official rules change.

## Documentation consistency and repository

- Material research/architecture/status/UI/workflow/task decisions require affected active docs/issues/prompts/tests/workflows to be reconciled in the same PR.
- Delete obsolete active files; keep useful older decisions only when clearly historical/superseded.
- Repository is source of truth for thesis code/context/experiments/results/writing/presentation/final deliverables except bibliography ownership.
- Secrets/credentials/raw chat exports remain forbidden.
- Temporary public visibility for CI is not a permanent public-release decision; deliberate distribution still requires privacy/copyright/licensing audit.
- Fabricated citations, data, results, progress or conclusions are forbidden.

## Optional AI

- Add an AI feature only if measurable practical value is demonstrated; it cannot alter experimental evidence, replace statistics or present hypotheses as facts.
