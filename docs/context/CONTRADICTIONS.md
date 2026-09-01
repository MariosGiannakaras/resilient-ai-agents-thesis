# Contradictions and Superseded Context

Old conversations and historical decisions are not active guidance when a later explicit user instruction, accepted decision, validated evidence or current repository state supersedes them. This file records the current resolution of recurring historical contradictions.

| ID | Older / mistaken interpretation | Current authoritative rule | Resolution | Confirmation needed? |
|---|---|---|---|---|
| CON-001 | Old responses described the work as a “Master's thesis”. | Use the official Department thesis identity and approved titles. | Official application prevails. | No. |
| CON-002 | Different thesis titles appeared historically. | Use the exact official Greek/English titles until a formal change is supplied. | Superseded. | No. |
| CON-003 | Old chats were treated as locked requirements. | Historical chats are context only; current explicit instructions, accepted decisions, evidence and repository authority control. | Superseded. | No. |
| CON-004 | Earlier model sets such as F0/C0/D0 or v1.1 comparator lists remained current. | Protocol-v2.1 retains Q-Learning, SARSA, DQN, PPO and Dyna-Q+ with frozen selected configurations. | DEC-058/060 supersede candidate-v1.1 model-set guidance for future final evidence. | No. |
| CON-005 | A particular LLM/ReAct/deep agent was central because it appeared historically. | Methods are selected for distinct scientific value under the frozen protocol; no extra agent is added merely for model count. | Superseded. | No. |
| CON-006 | Streamlit/React/NiceGUI or the temporary React/Vite exploration was the final application stack. | DEC-059 selects **PySide6 / Qt 6 Widgets** over the framework-neutral Study backend. Historical frontend implementations are prototype/history only. | Superseded by DEC-059. | No. |
| CON-007 | Historical seeds/budgets/hyperparameters or v1.1 reserve values remained current defaults. | Protocol-v2.1 owns the current final roots, held-out layouts, budgets and selected method-specific configurations. They are frozen and not UI choices. | Superseded by DEC-058/060. | No. |
| CON-008 | Old folder/user GridWorld code had to be recovered. | The project-owned Gymnasium GridWorld is the accepted experimental environment. | Closed. | No. |
| CON-009 | A specific public GridWorld repository had priority. | DEC-032 project-owned Gymnasium path is accepted. | Superseded. | No. |
| CON-010 | The user must manually provide hardware details. | Repository/system inventory records the actual thesis-machine baseline. | Closed. | No. |
| CON-011 | Dashboard/UI should own experiment logic. | Scientific core and Study backend remain UI-independent; Qt is control/observation/presentation only. | Core-first invariant. | No. |
| CON-012 | Mock/proxy metrics were acceptable final-demo data. | No fake progress/logs/metrics/trajectories/results; DEVELOPMENT/synthetic fixtures are labelled tests/demo data only. | Superseded. | No. |
| CON-013 | GPU-heavy execution assumed CUDA. | CPU is the validated scientific baseline; no CUDA/ROCm assumption. | Closed. | No. |
| CON-014 | Thesis repo directly owns bibliography ingestion/OCR/archive. | `ThesisBibliography` owns bibliography lifecycle; this repo consumes its generated verified snapshot read-only. | Superseded. | No. |
| CON-015 | Bibliography consumer remained citation-only/incomplete. | A complete generated consumer snapshot is established; citation-ready remains the formal citation surface. | Closed. | No. |
| CON-016 | Results were ignored/manual-commit only. | Study/run evidence and provenance are durable, checksummed and explicitly registered; final publication remains guarded. | Superseded. | No. |
| CON-017 | Many small permanent implementation commits are preferred. | Prefer one coherent working branch/PR and squash merge for bounded implementation packages. | Superseded. | No. |
| CON-018 | An old Codex bootstrap prompt controls work. | `AGENTS.md`, `TASKS.md`, `CURRENT_STATUS.md` and current task-specific authorities control. | Superseded. | No. |
| CON-019 | A current-state overlay is sufficient while dependent active docs stay stale. | Material changes require affected active source-of-truth reconciliation in the same PR. | Governance/CI control. | No. |
| CON-020 | Future tasks can be READY despite incomplete dependencies. | READY requires objective dependency completion; explicit authorization gates remain separate. | Registry/governance control. | No. |
| CON-021 | Final experiments can start automatically after protocol freeze or UI completion. | The protocol is frozen, but final-reserve execution remains blocked by a **separate explicit scientific authorization gate**. UI work/CI/smoke/cleanup never grants it. | Reconciled by DEC-060 and backend guard. | Explicit authorization required only when the user chooses to start the final experiment. |
| CON-022 | Defense is a generic presentation task. | Defense remains later, evidence-gated work with current official requirements rechecked near delivery. | Reconciled. | Exact official rules later. |
| CON-023 | A standalone executable/package is required before the current scientific/UI work can continue. | Final standalone Windows packaging is intentionally deferred until after the thesis and will target the finally accepted rebuilt UI. | Superseded/deferred under issue #94. | No. |
| CON-024 | Historical R0 or candidate-v1.1 Dyna-only framing controls the final comparison. | Historical R0/v1.1 remain auditable research history; protocol-v2.1 five-method comparison is current. | Superseded by protocol-v2. | No. |
| CON-025 | Historical v1.0/v1.1 final layouts/seeds may be reused or selected from inspected outcomes. | Protocol-v2.1 uses its own predeclared held-out final reserve; no outcome-driven replacement or reuse for tuning. | Scientific leakage guard. | No. |
| CON-026 | Recovery should be a single binary headline or old v1.1 deficit metrics remain primary. | RQ3 uses the frozen v2.1 AN-vs-AD recovery trajectory/status/speed contract; RQ1/RQ2 have their separately frozen estimands. | DEC-060 controls. | No. |
| CON-027 | UI is primarily for a technical operator. | The application remains novice-first, self-explanatory and compact, with technical details progressively disclosed. | Current UX contract. | No. |
| CON-028 | The paused/pre-v2.1 UI implementation should simply be continued. | Restart the UI from current `main`; re-read v2.1 contracts and rebuild presentation from today's state. Existing presentation code/screenshots are replaceable reference, not authority. | Latest explicit user direction. | No. |
| CON-029 | Repository cleanup should delete scientific history/evidence to appear clean. | Cleanup targets stale branches and misleading active guidance; historical decisions/evidence/provenance remain auditable and are not rewritten. | Repository hygiene rule. | No. |
