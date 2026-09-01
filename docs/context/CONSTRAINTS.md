# Constraints

## Compute and hardware

- Accepted actual-machine inventory is `SYSTEM_CAPABILITY_REPORT.md` plus `system-capability.accepted.json`; regenerate after material host/runtime changes.
- CPU execution is the required supported scientific baseline. The observed Radeon RX 570 is not a validated scientific-compute backend; do not assume CUDA/ROCm/DirectML.
- The experiment matrix must remain practical on measured hardware or an explicitly approved alternative.

## Accepted technical baseline

- Python 3.12; dependency/environment management uses `uv`, `pyproject.toml`, `.python-version`, committed `uv.lock`.
- Scientific logic lives in `src/resilient_agents/` and works independently from the UI.
- Evaluator ground truth is separated from agent-visible information; scientific randomness uses independently derived deterministic streams.
- Filesystem run bundles are the evidence source of truth; indexes/databases are rebuildable caches only.
- A run ID is one whole experiment and may contain many seeds/episodes; a finalized whole experiment uses at most one guarded automatic Git commit/push.
- Historical Streamlit/React frontend directions are superseded. DEC-044 selects **NiceGUI 3.16 native mode** over the same Python core/runtime service boundary.

## Application execution and delivery

- Local, single-user operation; no required cloud/public deployment/mobile/multi-user authentication/distributed orchestration.
- Normal research workflows should work offline after required dependencies/project assets are installed.
- The user should not need routine code/console/manual Git for supported application workflows.
- Root `run_app.bat` is the one-click launcher for a repository checkout.
- Final thesis delivery includes a cleaned Windows NiceGUI/PyInstaller **onedir + windowed** application folder that opens in its own desktop window without requiring recipient-installed Python/Node or browser interaction.
- Native packaging must use safe writable run/output locations and must not rely on temporary PyInstaller extraction paths.

## Testing and validation budget

- Testing is risk-based/proportional to changed behavior and scientific/reliability impact.
- Use targeted tests during implementation; PR CI is the canonical full-suite guard when available.
- There is no coverage-percentage target. Broad fuzz/property/mutation/exhaustive matrices/snapshot proliferation/large E2E suites require a concrete risk justification.
- CI uses tiny deterministic fixtures, known-answer cases, contracts and representative smoke/integration paths; pilot/final experiment matrices are never tests.
- On CI failure inspect the narrowest failed step; do not repeatedly reanalyse successful CI.
- Required config/schema/provenance/lifecycle conditions fail closed. Optional unavailability remains explicit.

## UI/UX complexity

- DEC-046 is authoritative: normal use must be understandable to a non-programmer with no prior RL/model/configuration/repository knowledge.
- Use plain-language primary labels, technical IDs as secondary detail, helper text, visible units/ranges/consequences, info icons/tooltips, contextual explanations and progressive disclosure.
- Tooltips/help must stay synchronized with scientific definitions and implemented behavior; required workflow information cannot exist only in a tooltip.
- Status meaning uses text + consistent symbols/icons + accessible semantic visual treatment; color alone never carries essential meaning.
- Pre-run review exposes readable resolved configuration, protocol/stage, agent(s), condition/layout, seeds/repetitions, episode budgets, relevant parameters, run count and blocking issues.
- Empty/loading/disabled/warning/error/unavailable states are actionable.
- First-run onboarding is short, skippable, replayable and locally stateful; do not introduce accounts or a second heavyweight tour/frontend subsystem.
- UI is modern and compact rather than sparse/oversized. Consistent icons, restrained hover/focus/selection micro-interactions and purposeful status/chart/GridWorld animations are allowed when they improve comprehension.
- Animation/interpolation must never fabricate progress/trajectory/data or alter scientific timing/actions/RNG; essential state remains understandable with reduced motion where practical.

## Research scope

- Official topic uses a simple controlled environment and compares resilient decision agents under uncertainty/dynamic change.
- Current candidate-v1.1 direction is F0 frozen Q-learning, C0 continual Q-learning and D0 Dyna-Q+; historical R0 pilot evidence remains but the accepted R0 construction is not reinstated unchanged.
- Preserve validated F0/C0 alpha `0.5`, gamma `0.96875`, epsilon `0.125`, 512 training episodes/layout, 16 pre-change, 32 post-change, horizon 48 and 32 paired final roots.
- Candidate v1.1 uses seven single-factor conditions, four fresh held-out final layouts, fresh precommitted final seeds and bounded D0-only tuning. Exact D0 planning parameters and final reserve values remain unfrozen until T-521/T-522.
- Primary reporting is cumulative deficit, immediate degradation and terminal performance/gap; recovery is secondary/sensitivity. Paired effects/95% CIs and explicit n are required.
- No composite resilience score, post-hoc favorable threshold or deep-RL expansion merely to increase model count.

## GridWorld and third-party code

- There is no requirement to recover an old codebase.
- Third-party code requires source/license/maintenance/security/API/testability/determinism/suitability review and pinned versions where applicable.
- DEC-032 selects the project-owned schema-v1 GridWorld using Gymnasium 1.3.0; MiniGrid/Pygame remain prototype-only.
- Environment and agents use shared core contracts rather than a second scientific execution interface.

## Reproducibility, results, and large files

- Every experiment stores resolved config, seeds, source Git commit, runtime/capability/provenance metadata.
- Finalized raw results are immutable/checksummed; failures/cancellations/interruptions/invalid/excluded runs are retained with reasons.
- Final figures/tables are generated only by version-controlled processing from real stored data.
- Useful thesis-produced outputs are retained when storage permits; configured large formats use Git LFS. Bibliography PDFs/LFS objects remain upstream.

## Live application truthfulness

- T-530 provides the UI-independent Python runtime service; NiceGUI never becomes a second scientific runner.
- Live GridWorld is read-only observer state and live charts consume real runtime DTOs only.
- Live/provisional values, finalized run values and versioned analysis/evidence are visibly distinct; provisional values are never automatically promoted into thesis evidence.
- Historical runs lacking retained step trace explicitly show replay unavailable; never synthesize a plausible path.
- Lifecycle controls are capability-based. Unsupported pause/resume/stop/cancel/restart operations are not simulated.

## Lifecycle and evidence handoffs

- The v1.1 final campaign waits for candidate protocol non-final validation/freeze and intended application acceptance according to `TASKS.md`.
- Thesis/presentation writing remains blocked until the explicit pre-WP7 user approval gate.
- After final analysis, a frozen evidence package maps RQs, methods, source IDs, runs, figures/tables/captions and planned claims.
- Supervisor/reviewer corrections affecting evidence or claims require corresponding revalidation.

## Documentation/source-of-truth consistency

- A material change is incomplete until affected active docs/prompts/tasks/issues/decisions/status/tests/workflows are reconciled in the same PR.
- Obsolete active files are deleted; useful historical decisions are explicitly marked superseded.
- Generated bibliography content is never manually edited. Follow `DOCUMENTATION_GOVERNANCE.md`.

## Privacy and repository

- Temporary public repository visibility for CI is operational, not a permanent public-release decision.
- Secrets/credentials/raw conversation exports are forbidden in tracked content.
- Deliberate public release requires final privacy/license/copyright audit and redaction/exclusion where necessary.

## Academic delivery and defense

- No final deadline or verified defense schedule is currently known; do not invent them.
- Current Word template/submission rules and exact defense duration/content/file/live-demo rules are rechecked near delivery.
- Planned defense output is PowerPoint `.pptx` plus embedded speaker notes and separate full spoken Greek script, subject to current official requirements.
- Microsoft PowerPoint remains final rendering/rehearsal target; later supervisor-specific instructions are recorded as explicit changes.
