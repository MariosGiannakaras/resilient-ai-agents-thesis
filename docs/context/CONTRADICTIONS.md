# Contradictions and Superseded Context

Old conversations and historical decisions are not active guidance when a later explicit user instruction or accepted decision supersedes them. Current explicit user instructions, accepted decisions, verified evidence and actual repository state control.

| ID | Older / mistaken interpretation | Current authoritative rule | Resolution | Confirmation needed? |
|---|---|---|---|---|
| CON-001 | Old responses described the work as a “Master's thesis”. | Official application defines the Department thesis. | Official application prevails. | No. |
| CON-002 | Different thesis titles appeared historically. | Use exact official Greek/English titles until formal change. | Superseded. | No. |
| CON-003 | Old chats were treated as preferences/shortlists. | Historical chats are context only; current evidence/decisions control. | Superseded. | No. |
| CON-004 | Different chats “locked” different model sets. | Current candidate-v1.1 roles are F0/C0/D0 under DEC-042/T-520/T-521; historical sets are not active. | Reopened through evidence, then superseded. | No for current candidate direction; v1.1 freeze still gated. |
| CON-005 | A particular LLM/ReAct/deep agent was central because it appeared historically. | No advanced/deep model is added merely for model count; every role needs distinct RQ value. | Superseded. | No. |
| CON-006 | FastAPI/React, Tauri/React/Python, Streamlit, or the temporary React/Vite exploration was the final application stack. | DEC-044 selects **NiceGUI 3.16 native mode** over the Python scientific/runtime core; DEC-043 remains historical only. | All older frontend-stack choices are superseded. | No. |
| CON-007 | Historical fixed seeds/budgets/hyperparameters were defaults. | Current validated F0/C0 values and candidate-v1.1 budgets are evidence-backed; exact unfrozen D0/final-reserve values follow T-521/T-522. | Historical arbitrary defaults discarded. | No. |
| CON-008 | Old folder/user GridWorld code had to be recovered. | Project-owned GridWorld is implemented; legacy code is not required. | Closed. | No. |
| CON-009 | A specific public GridWorld repository had historical priority. | DEC-032 project-owned Gymnasium path is accepted. | Superseded. | No. |
| CON-010 | User must manually provide hardware. | Codex/system inventory inspects actual machine. | Closed. | No. |
| CON-011 | Dashboard-first workflow. | Scientific core remains independent; UI is control/presentation over the core. | Core-first invariant. | No. |
| CON-012 | Mock/proxy metrics were useful final-demo data. | No fake progress/logs/metrics/trajectories/results; fixtures are labelled tests only. | Superseded. | No. |
| CON-013 | GPU-heavy approach assumed CUDA. | CPU is validated scientific baseline; no CUDA/ROCm assumption. | Closed. | No. |
| CON-014 | Thesis repo directly owns bibliography ingestion/OCR/archive. | `ThesisBibliography` owns bibliography lifecycle; this repo consumes verified generated corpus. | Superseded. | No. |
| CON-015 | Bibliography consumer remained citation-only/incomplete. | Complete immutable corpus import is established. | Closed. | No. |
| CON-016 | Results were ignored/manual-commit only. | Whole-experiment outputs/provenance are tracked; guarded automatic publication is implemented. | Superseded. | No. |
| CON-017 | Many small permanent commits expected. | Prefer coherent squash merge; finalized whole experiment at most one result publication commit. | Superseded. | No. |
| CON-018 | Old Codex bootstrap prompt controls work. | `CODEX_EXECUTION_PROMPT.md` + three-file session core + `TASKS.md` control. | Superseded. | No. |
| CON-019 | A current-state overlay was enough while dependent docs stayed stale. | Material changes require affected active source-of-truth reconciliation in the same PR. | Governance/CI controls. | No. |
| CON-020 | Future tasks could be READY despite incomplete dependencies. | READY means task dependencies are complete. | Registry/CI enforce. | No. |
| CON-021 | Final experiments could start immediately after protocol freeze regardless of application acceptance. | Normal v1.1 final execution follows T-522 + T-511 gates and identical scientific core path. | Reconciled in `TASKS.md`. | No. |
| CON-022 | Defense was a generic presentation task. | Deferred defense package includes `.pptx`, embedded notes, full Greek spoken script, evidence map and validation/rehearsal. | Reconciled. | Exact official rules later. |
| CON-023 | 2026-08-26 launcher decision said a standalone executable/package was not required. | Later explicit 2026-08-27 direction requires the final program to run in its own window and be delivered as a cleaned standalone application folder, while `run_app.bat` remains the repository-checkout launcher. | Later instruction supersedes the “not required” clause; DEC-044/T-532 govern packaging. | No. |
| CON-024 | R0 remained the likely third final comparator after the historical pilot. | Accepted R0 construction showed severe nominal truncation; current candidate uses D0 Dyna-Q+ as the third distinct agent, while R0 evidence is retained as a negative/exploratory result. | DEC-042/T-520 supersede unchanged-R0 freeze. | No. |
| CON-025 | Two final layouts and historical v1.0 seed reserve were sufficient for the new refinement after outcomes were inspected. | Candidate v1.1 requires four fresh held-out final layouts and a fresh precommitted seed bank. | Prevents post-outcome design leakage. | Exact values in T-521. |
| CON-026 | Recovery binary classification should remain the headline resilience outcome. | Primary v1.1 outcomes are cumulative deficit, immediate degradation and terminal performance/gap; recovery is secondary/sensitivity because pilot classification was threshold-sensitive. | DEC-042/T-521. | No. |
| CON-027 | UI was primarily for the author/technical operator. | DEC-046 requires a novice-first, compact, self-explanatory UI usable by a non-programmer/non-RL user with tooltips/contextual help, semantic icons/colors and purposeful micro-interactions/animation. | Later explicit user direction supersedes technical-only assumptions. | No. |
