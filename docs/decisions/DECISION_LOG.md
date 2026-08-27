# Decision Log

This is the current decision index. Dedicated decision files control where present; older decisions remain auditable but later explicit supersession wins.

## DEC-001 — Repository source of truth
Accepted. This repository owns thesis context, implementation, experiments, results, writing and deliverables; `ThesisBibliography` is the explicit bibliography-lifecycle exception.

## DEC-002 — Official application controls academic identity
Accepted. Institution and exact Greek/English titles come from the approved application until formally changed.

## DEC-003 — Original application retained
Accepted. Preserve the original application; deliberate public release requires privacy/redaction review.

## DEC-004 — Scientific core precedes polished UI
Accepted. Headless scientific execution remains independent; polished user-facing workflow is validated later on the same core.

## DEC-005 — No inherited final scientific matrix
Accepted. Final models/settings/seeds/budgets/protocol come from evidence/prototypes/pilots, not historical chat suggestions.

## DEC-006 — No acceleration assumptions before inventory
Accepted and satisfied. Validated native Windows CPU execution remains the required scientific baseline unless explicitly amended.

## DEC-007 — Raw chat exports excluded
Accepted.

## DEC-008 — Current Department guidance rechecked near delivery
Accepted. Historical guidance is a snapshot only.

## DEC-009 — Historical conversations are context, not authority
Accepted.

## DEC-010 — Fresh GridWorld decision; no legacy code requirement
Accepted and later implemented through DEC-032.

## DEC-011 — Automated system inventory
Accepted.

## DEC-012 — Historical bootstrap wording superseded by current state files
Accepted/historical.

## DEC-013 — Thesis-completion-first scope
Accepted: polished outside, bounded inside.

## DEC-014 — Lean reading/research workflow
Accepted; bibliography acquisition clause later superseded by DEC-017.

## DEC-015 — Automated technical execution/review
Accepted. Codex handles routine bounded Git/PR/CI/objective review/corrections where permitted; user is reserved for genuine subjective/external gates.

## DEC-016 — Original in-repository bibliography lifecycle
**SUPERSEDED by DEC-017.**

## DEC-017 — Dedicated canonical ThesisBibliography repository
Accepted. `MariosGiannakaras/ThesisBibliography` owns source/original/OCR/analysis/evidence lifecycle; this repository consumes immutable generated output only.

## DEC-018 — English technical/operational repository language
Accepted; exact official Greek/original-language scientific evidence remain unchanged where required; final thesis remains Greek.

## DEC-019 — Early debug visualization allowed
Accepted when it uses the same core interfaces and does not alter experiments.

## DEC-020 — Implementation/evidence first; writing-stage inputs deferred
Accepted. Missing supervisor details/deadlines/templates do not block research/application work.

## DEC-021 — Complete research-corpus import with strict citation sublayer
Accepted/implemented. `citation-ready/` is the formal automatic citation surface.

## DEC-022 — Immutable full-corpus baseline
Accepted/implemented; later synchronized baseline advanced to `bibliography-integration-v3` without changing trust architecture.

## DEC-023 — Research core, reproducible runs and guarded publication
Accepted/implemented as infrastructure: Python 3.12 + `uv`, `src/resilient_agents/`, information boundary, deterministic RNG, filesystem bundles, one guarded result publication per whole experiment, selective LFS. Its historical Streamlit UI clause is superseded by DEC-044.

## DEC-024 — Active-document reconciliation is part of material change
Accepted. A change is incomplete while related active source-of-truth files contradict it.

## DEC-025 — Canonical resumable Codex task registry
Accepted. `docs/context/TASKS.md` is the concrete task/resume ledger; interrupted work must remain recoverable across sessions/quota windows.

## DEC-026 — End-to-end lifecycle and defense package
Accepted. Application -> final experiments -> frozen evidence -> thesis/review -> defense -> audit/delivery handoffs are explicit; final presentation includes `.pptx`, embedded notes and separate full spoken Greek script.

## DEC-027 — Self-explanatory UI/onboarding baseline
Accepted historically and extended/superseded in framework/presentation detail by DEC-044/046. Core principle remains: understandable labels/help/status/actionable states and lightweight onboarding.

## DEC-028 — Lean Codex bootstrap and persistent bounded Goal execution
Accepted/implemented. Session-start core is exactly AGENTS/TASKS/CURRENT_STATUS; task/PR/CI boundaries do not require repeated “continue”.

## DEC-029 — Risk-based proportional testing
Accepted. No arbitrary coverage or test-expansion project.

## DEC-030 — Quota-efficient fail-fast validation
Accepted. Targeted checks during work; PR CI is the canonical full-suite guard; no repeated successful-log analysis or pilot/final matrices as tests.

## DEC-031 — Target-machine runtime baseline
Accepted. Native Windows CPython 3.12 via locked `uv`, CPU-compatible scientific execution, no assumed validated GPU scientific backend.

## DEC-032 — Project-owned Gymnasium GridWorld
Accepted/implemented. Small project-owned Gymnasium-compatible environment; MiniGrid/Pygame remain non-core prototype context.

## DEC-033 — Curve-based resilience component estimands
Accepted/implemented. Separate immediate/worst/terminal gaps, cumulative deficit and explicit recovery states; no composite resilience score.

## DEC-034 — Historical bounded F0/C0/R0 pilot capability set
Accepted for historical pilot implementation only. Later R0 nominal-censoring evidence and DEC-041/042 supersede current retention.

## DEC-035 — Historical versioned pre-final pilot protocol
Accepted/implemented historical pilot authority.

## DEC-036 — One resumable headless scientific execution path
Accepted/implemented.

## DEC-037 — Deterministic finalized-bundle analysis
Accepted/implemented.

## DEC-038 — Durable predeclared pilot campaign execution
Accepted/implemented historical pilot workflow.

## DEC-039 — R0 terminal-observation alias amendment
Accepted/implemented for historical amended pilot evidence.

## DEC-040 — Post-pilot freeze constraints
Accepted historical diagnostic conclusion: do not freeze unchanged R0; do not choose favorable recovery thresholds post hoc.

## DEC-041 — Protocol v1.0 freeze and R0 removal
Accepted historical final-v1.0 authority. `protocol-v1.0` and its final evidence remain immutable.

## DEC-042 — Pre-WP7 protocol-v1.1 and application refinement
**CURRENT scientific refinement authority.**

- Preserve v1.0/final evidence immutably.
- Candidate v1.1 uses F0 frozen Q-learning, C0 continual Q-learning and D0 Dyna-Q+.
- R0 remains historical pilot evidence; do not reinstate unchanged.
- Preserve accepted F0/C0 base values; tune only bounded D0 planning settings through predeclared non-final evidence.
- Support multiple protocol-approved resolved development/tuning configurations with repeated roots, stable identities/provenance and no best-run cherry-picking; final retained settings freeze before final outcomes.
- Four fresh held-out final layouts, fresh seed bank, structural remap IDs, paired effects/95% CIs and component outcomes required.
- Application-framework clauses are superseded by DEC-044/045/046.

File: `DEC-042_PRE_WP7_PROTOCOL_V1_1_AND_APPLICATION_REFINEMENT.md`.

## DEC-043 — Application framework reopening / React-Vite exploration
**SUPERSEDED by DEC-044.** Retained only to explain the intermediate evaluation.

## DEC-044 — Native standalone NiceGUI application
**CURRENT application architecture authority.**

- NiceGUI 3.16 native mode/pywebview, Python-only UI surface.
- UI-independent runtime/scientific services.
- No active Streamlit/React/Vite/Node frontend stack.
- `run_app.bat` repository launcher + validated Windows PyInstaller/NiceGUI `onedir + windowed` delivery.
- Ordinary approved experiments execute from the finished application on the validated thesis machine; Codex is not required just to launch a frozen configuration.
- GitHub remains source of truth/CI/evidence coordination; GitHub-hosted CI is not automatically the validated final scientific machine. Self-hosted thesis-machine runner is optional, not required.

File: `DEC-044_NATIVE_STANDALONE_NICEGUI_APPLICATION.md`.

## DEC-045 — Visual analytics stack
**CURRENT.** Plotly = stored/final scientific figures; ECharts = real live/provisional telemetry; Mermaid = explanatory diagrams; AG Grid Community = analytical tables. Live/provisional/final evidence classes remain distinct.

File: `DEC-045_VISUAL_ANALYTICS_STACK.md`.

## DEC-046 — Novice-first compact UI and presentation UX
**CURRENT.** UI must be understandable without code/RL/configuration knowledge; plain-language labels, secondary technical IDs, tooltips/help, progressive disclosure, semantic icon+text+color states, compact modern design, purposeful micro-interactions/animations and static/reduced-motion-safe meaning.

File: `DEC-046_NOVICE_FIRST_UI_AND_PRESENTATION_UX.md`.

## Current downstream tool/workflow policy

This is a workflow specification rather than a new scientific decision: `docs/thesis/WP7_WP8_TOOL_WORKFLOW.md` records how T-700+ will use Codex/repository automation, ChatGPT, Microsoft Word, PowerPoint, optional Canva and user-captured application screenshots/GIF/video after the explicit WP7 approval gate.

Key constraints:

- Word remains the authoritative final `.docx` composition/inspection surface.
- PowerPoint remains the authoritative final `.pptx` inspection/rehearsal surface.
- Canva is optional polish only and never scientific source of truth.
- ChatGPT is preferred for Greek drafting/review/narrative/placement instructions once WP7 is authorized.
- Every user-captured application asset receives an exact `ASSET-*` placement/provenance record and an essential static fallback.
- Planning this workflow does not unlock T-700+.

## Pending current decisions

Only genuinely unresolved future items remain pending:

- exact T-521 D0 `planning_steps`/`kappa` bounded search values;
- exact four fresh v1.1 final layouts and fresh final seed values;
- exact paired-effect/95% CI implementation/aggregation encoded before final evidence;
- T-522 freeze/amend/reject outcome and final retained D0 settings;
- actual T-530 lifecycle-control capabilities;
- native NiceGUI/PyInstaller target-machine package behavior;
- current official Word/citation/submission/defense rules at T-700;
- later supervisor/reviewer corrections and final delivery specifics.

Current scientific/application/tooling baselines are not pending merely because older documents once described alternatives.