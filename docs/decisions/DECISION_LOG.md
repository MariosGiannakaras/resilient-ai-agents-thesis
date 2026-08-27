# Decision Log

Current project-wide decision index. Detailed dedicated decision files/ADRs control where present; Git history preserves older rationale. Later accepted decisions explicitly supersede conflicting earlier details without rewriting historical evidence.

## Decision index

| ID | Decision | Current status |
|---|---|---|
| DEC-001 | Repository is thesis source of truth with explicit external bibliography boundary. | Accepted; clarified by DEC-017/021. |
| DEC-002 | Official application controls academic identity/titles. | Accepted. |
| DEC-003 | Preserve original application unchanged; public release requires review/redaction. | Accepted. |
| DEC-004 | Scientific/headless core precedes and remains independent from polished UI. | Accepted; still authoritative. |
| DEC-005 | No inherited final scientific matrix from historical chats. | Accepted. |
| DEC-006 | No acceleration assumptions before actual-machine inventory. | Accepted; inventory applied by DEC-031. |
| DEC-007 | Raw chat exports excluded. | Accepted. |
| DEC-008 | Recheck current Department guidance near delivery. | Accepted. |
| DEC-009 | Historical conversation exports are context only. | Accepted. |
| DEC-010 | Fresh GridWorld discovery; no legacy-code dependency. | Accepted; resolved by DEC-032. |
| DEC-011 | Codex/system owns automated capability inventory. | Accepted. |
| DEC-012 | Corrected bootstrap context superseded earlier bootstrap wording. | Historical; current state is TASKS/CURRENT_STATUS. |
| DEC-013 | Thesis-completion-first scope: polished outside, bounded inside. | Accepted. |
| DEC-014 | Lean agent workflow and staged literature refresh. | Accepted; bibliography acquisition portion superseded by DEC-017. |
| DEC-015 | Automated technical execution/review; user is not routine GitHub operator. | Accepted; refined by DEC-028/030 and current branch gate. |
| DEC-016 | Original in-repository bibliography lifecycle. | **Superseded by DEC-017.** |
| DEC-017 | Dedicated canonical `ThesisBibliography` repository. | Accepted. |
| DEC-018 | English technical/operational repo language; preserve required Greek/source-language material. | Accepted. |
| DEC-019 | Early lightweight debug visualization allowed through the same scientific core. | Accepted. |
| DEC-020 | Implementation/evidence priority; writing-stage inputs deferred. | Accepted; reinforced by pre-WP7 gate. |
| DEC-021 | Complete research-corpus consumer with citation-ready formal sublayer. | Accepted/implemented. |
| DEC-022 | Accept immutable full-corpus baseline. | Accepted/implemented; later sync baseline recorded in current context. |
| DEC-023 | Python 3.12 + `uv`, headless core, information/RNG contracts, filesystem bundles, guarded publication. | Core/storage parts accepted/implemented; its Streamlit UI detail is **superseded by DEC-044**. |
| DEC-024 | Material changes require active-document reconciliation in the same PR. | Accepted. |
| DEC-025 | `TASKS.md` is canonical resumable Codex task registry. | Accepted. |
| DEC-026 | End-to-end lifecycle handoffs and complete defense package. | Accepted. |
| DEC-027 | Self-explanatory UI and lightweight onboarding baseline. | Accepted; Streamlit-specific detail **superseded by DEC-044/046**. |
| DEC-028 | Lean Codex bootstrap, persistent goal, bounded dependency-valid execution. | Accepted/implemented. |
| DEC-029 | Risk-based proportional testing. | Accepted; refined by DEC-030. |
| DEC-030 | Quota-efficient fail-fast validation; PR CI canonical full-suite guard. | Accepted. |
| DEC-031 | Native Windows CPU target-machine/runtime baseline. | Accepted. |
| DEC-032 | Project-owned Gymnasium GridWorld implementation. | Accepted/implemented. |
| DEC-033 | Curve-based component resilience estimands; no composite score. | Accepted/implemented; roles refined by DEC-042. |
| DEC-034 | Historical pilot capability set F0/C0/R0. | Accepted for historical pilots; final-current role set **refined by DEC-042**. |
| DEC-035 | Versioned pre-final `pilot-v0.1` protocol. | Historical pilot authority. |
| DEC-036 | One resumable headless scientific execution path. | Accepted/implemented. |
| DEC-037 | Deterministic finalized-bundle pilot analysis. | Accepted/implemented. |
| DEC-038 | Durable-main predeclared pilot campaign execution. | Historical pilot execution decision. |
| DEC-039 | R0 active terminal-observation alias amendment (`pilot-v0.2`). | Historical pilot amendment. |
| DEC-040 | Post-pilot freeze constraints: R0 unchanged unsuitable; recovery threshold sensitivity; preserve full curves/components. | Accepted diagnostic conclusion. |
| DEC-041 | Freeze historical `protocol-v1.0`; remove R0 from v1.0 final comparator. | Accepted/implemented historical baseline; v1.0 evidence immutable. |
| DEC-042 | Pre-WP7 protocol-v1.1 + application refinement: add D0, improve final design/statistics/application before writing. | **Current accepted scientific refinement.** |
| DEC-043 | Reopen UI framework and select React/Vite + FastAPI during web-focused comparison. | **Superseded by DEC-044** after standalone requirement clarified. |
| DEC-044 | Native standalone NiceGUI application, Python-only supported user path, Windows own-window/onedir delivery. | **Current accepted application architecture.** |
| DEC-045 | Plotly stored scientific views + ECharts live telemetry + Mermaid infographics + AG Grid Community tables. | **Current accepted visual-analytics architecture.** |
| DEC-046 | Novice-first modern compact UI, contextual help/tooltips, semantic icons/colors, micro-interactions and purposeful animation. | **Current accepted UX contract.** |

## Dedicated current decision files

- `DEC-041_PROTOCOL_V1_0_FREEZE.md` — immutable historical v1.0 freeze/R0 removal.
- `DEC-042_PRE_WP7_PROTOCOL_V1_1_AND_APPLICATION_REFINEMENT.md` — current scientific/application refinement.
- `DEC-043_APPLICATION_FRAMEWORK_REOPENING.md` — historical React/Vite exploration; superseded.
- `DEC-044_NATIVE_STANDALONE_NICEGUI_APPLICATION.md` — current native application architecture.
- `DEC-045_VISUAL_ANALYTICS_STACK.md` — current analytical/infographic/live-chart roles.
- `DEC-046_NOVICE_FIRST_UI_AND_PRESENTATION_UX.md` — current self-explanatory UX/presentation contract.

## Current consequences

### Scientific

- Historical v1.0/final evidence remains immutable.
- T-520 validated D0 Dyna-Q+ beside F0/C0 without weakening historical protocol semantics.
- T-521 owns candidate-v1.1 schema, bounded D0-only tuning design, four fresh held-out layouts, fresh seed bank, structural remap IDs and paired 95% CI support.
- Primary current reporting direction: cumulative deficit, immediate degradation, terminal performance/gap; recovery secondary/sensitivity.
- No deep-RL expansion merely for model count; no opaque composite resilience score/post-hoc favorable threshold.

### Application

- No active Streamlit or React/Vite frontend remains in the current implementation path.
- NiceGUI 3.16 native mode opens the local app in its own desktop window over the same Python core/runtime services.
- Root `run_app.bat` remains the repository-checkout launcher; final delivery additionally requires a cleaned NiceGUI/PyInstaller `onedir + windowed` Windows folder.
- Live GridWorld and ECharts graphs consume truthful T-530 observer/runtime state only; provisional values remain distinct from final evidence.
- Plotly figures are designed for honest thesis/presentation screenshots, with uncertainty labels matching the underlying artifact (e.g. v1.0 SD is not called CI).

### UX

- A user with no code/RL/model/configuration knowledge must understand the normal workflow without a separate manual.
- Plain-language labels, tooltips/info icons, contextual explanations, units/ranges/consequences, progressive disclosure and readable resolved-config review are required.
- Modern compact design uses consistent icons/semantic colors, actionable states, restrained micro-interactions and purposeful animations; color/animation never carries or fabricates scientific meaning alone.
- Onboarding is short/skippable/replayable and lightweight; pages remain understandable without it.

### Governance

- Current package remains one branch `feat/pre-wp7-protocol-v1.1-ui-rebuild` and draft PR #92 through integrated human-facing acceptance.
- `TASKS.md` is canonical for completion/dependencies; master tracker #87 mirrors major progress.
- WP7 writing remains blocked until T-511 human application acceptance plus explicit user approval.

## Still pending decisions/gates

These are not forgotten; they are explicit task/open-question gates:

- exact bounded D0 `planning_steps`/`kappa` search and selection;
- exact four fresh final-layout definitions and fresh final seed values;
- candidate-v1.1 freeze/amend/reject decision after non-final evidence;
- exact paired CI implementation/aggregation details predeclared before final evidence;
- safe runtime lifecycle capability set discovered in T-530;
- target-Windows native/onedir packaging validation;
- later supervisor corrections/deadlines/official Word and defense specifics;
- optional AI only if measurable value is ever demonstrated.
