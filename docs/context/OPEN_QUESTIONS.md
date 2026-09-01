# Open Questions

This file contains only issues that are genuinely unresolved after current repository evidence and accepted decisions. Superseded historical questions are listed as resolved rather than silently carried forward.

## Resolved since earlier versions

The following are **not open questions anymore**:

- bibliography ownership/import/authentication/provenance baseline;
- Python 3.12 + `uv`, filesystem run bundles, information boundary, deterministic RNG and guarded whole-experiment publication;
- actual target-machine CPU/RAM/storage/GPU/runtime baseline;
- project-owned Gymnasium GridWorld implementation strategy;
- historical F0/C0/R0 pilot diagnosis and the decision **not** to freeze the accepted R0 construction unchanged;
- current comparator direction: F0 frozen Q-learning, C0 continual Q-learning and D0 Dyna-Q+ as three scientifically distinct resilience/adaptation roles for candidate v1.1;
- validated common F0/C0 alpha `0.5`, gamma `0.96875`, epsilon `0.125`, 512 training episodes/layout, 16 pre-change, 32 post-change, horizon 48 and 32 paired final roots;
- seven single-factor condition structure and the new structural remap naming direction;
- primary metric direction: cumulative deficit, immediate degradation and terminal performance/gap; recovery is secondary/sensitivity rather than the sole headline outcome;
- need for paired effects/95% confidence intervals and explicit sample counts in v1.1 analysis;
- application framework: NiceGUI 3.16 native mode, not Streamlit/React/Vite;
- standalone own-window/cleaned Windows application-folder delivery target;
- Plotly/ECharts/Mermaid/AG Grid visual roles;
- novice-first self-explanatory UI contract, contextual tooltips/help, compact modern design, semantic icons/colors, micro-interactions and purposeful animation;
- canonical resumable Codex task/checkpoint workflow and one active implementation branch/PR;
- overall application -> final experiments -> evidence -> thesis/review -> defense -> delivery lifecycle.

Historical pilot/v1.0 evidence remains immutable; resolving a question for v1.1 never relabels old evidence.

## Current open questions

| ID | Open issue | Why open | Needed by | Blocks? | Resolver / safe rule |
|---|---|---|---|---|---|
| OQ-ACA-001 | Are supervisor-specific corrections introduced later? | None currently exist. | When feedback arrives. | No. | User/supervisor; record as explicit change when received. |
| OQ-ACA-002 | What is the eventual submission/presentation schedule? | No verified date provided. | Delivery planning. | No. | User/Department; never invent dates. |
| OQ-ACA-003 | Is there a current official Word template/submission package? | Not needed for current implementation. | WP7/final QA. | No. | Recheck official sources near writing/submission. |
| OQ-ACA-004 | What are the exact current defense duration/language/file/template/live-demo/submission rules? | May change and have not been verified for final delivery. | Defense freeze. | No now. | Recheck official guidance near WP7/defense; do not invent slide count/duration. |
| OQ-V11-001 | Which bounded D0 `planning_steps` and `kappa` values should be selected? | D0 integration is validated, but D0-only tuning must use predeclared non-final evidence. | T-521/T-522. | Yes for v1.1 freeze. | Define a small search in T-521; select only from development/tuning/non-final evidence in T-522. |
| OQ-V11-002 | What exact four fresh held-out final layouts and final seed values are frozen for v1.1? | Counts/constraints are decided, exact reserve values must be generated/precommitted before inspection. | T-521. | Yes for v1.1 final. | Generate/validate/freeze before any v1.1 final execution; never choose from observed final outcomes. |
| OQ-V11-003 | What exact paired interval/effect implementation is frozen? | Paired 95% CI requirement is accepted; implementation details/aggregation must be encoded before final evidence. | T-521/T-522. | Yes for final analysis. | Use paired seed/layout structure, explicit n and predeclared deterministic/statistically justified CI procedure; no post-hoc favorable method. |
| OQ-V11-004 | Does the candidate v1.1 pass non-final tuning/pilot acceptance without further amendment? | Cannot be known before T-522 evidence. | T-522. | Yes for freeze. | Freeze, amend or reject based on predeclared non-final criteria; retain failures/non-recovery. |
| OQ-RUNTIME-001 | Which lifecycle controls are actually safe in the active-run service? | Stop/cancel/restart are desired where safe; pause/resume may not be. | T-530. | Yes for corresponding UI controls. | Capability-based service; unsupported actions remain visibly unsupported. |
| OQ-PKG-001 | Does the NiceGUI/pywebview/PyInstaller `onedir + windowed` build pass on the actual Windows thesis machine? | CI/browser validation cannot substitute for native target-machine packaging behavior. | T-532. | Yes for final application delivery. | Validate native launch/close/restart, WebView2/runtime assets and writable paths on Windows; document any prerequisite that cannot be bundled. |
| OQ-UI-001 | Which optional advanced controls survive after the real v1.1/runtime workflow is integrated? | Core UX is confirmed; speculative advanced controls remain unnecessary until real workflow proves value. | T-531. | No now. | Implement required novice-first workflow first; add only evidence-backed low-risk controls. |
| OQ-AI-001 | Is any optional AI feature useful in the application? | No demonstrated need. | Late UI only. | No. | Do not integrate unless measurable value appears. |
| OQ-PRIV-001 | What must be redacted/licensed differently before deliberate public distribution? | Temporary CI visibility is not a public-release decision. | Final release. | No now. | Run final privacy/secret/copyright/licensing audit. |

## Current authority

Concrete status/dependencies are in `TASKS.md`; the immediate work is `T-521`. Questions resolved by an accepted task/decision must be removed from the open table in the same reconciliation checkpoint rather than remaining as stale uncertainty.
