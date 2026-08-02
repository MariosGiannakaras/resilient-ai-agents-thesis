# Contradictions and Superseded Context

Old conversations are not a set of decisions to merge. They are historical context. When they contain conflicting proposals, the correct resolution is not to choose the newest or most frequent proposal; it is to perform current research and make a new evidence-backed decision.

| ID | Older / mistaken interpretation | Current authoritative rule | Resolution | Confirmation needed? |
|---|---|---|---|---|
| CON-001 | Old responses described the work as a “Master's thesis”. | The official application defines it as a thesis of the Department of Informatics and Computer Engineering. | Official application prevails. | No. |
| CON-002 | Different thesis titles appeared historically. | Use the exact titles from the official application until a formal change. | Superseded. | No. |
| CON-003 | Old conversations were treated as a source of user preferences and candidate shortlists. | They were provided only as examples/context; current decisions are made from fresh evidence. | Historical content removed from decision authority and selection workspaces. | No. |
| CON-004 | Different chats “locked” different model sets. | No model shortlist exists. | Fresh bibliography/environment/feasibility/pilot selection required. | Later as a formal research decision. |
| CON-005 | A particular LLM/ReAct or another advanced model was presented as the central agent. | No model has priority because it was mentioned historically. | Re-evaluate from zero. | Later. |
| CON-006 | FastAPI/React, Tauri/React/Python, or another stack was presented as final. | Stack selection follows core requirements and prototypes. | No preferred stack. | Later through an ADR. |
| CON-007 | Old responses proposed fixed seeds, run counts, budgets, and hyperparameters. | These are selected from verified literature, pilots, desired precision, and measured resources. | Historical values discarded as defaults/candidates. | Later. |
| CON-008 | The project was assumed to require recovery of an old folder or user-owned GridWorld code. | The application is built afresh and old code is not required. | Remove legacy-code blocker. | No. |
| CON-009 | A specific public GridWorld repository appeared as a historical candidate. | Codex performs a fresh landscape search and integrates only a currently suitable option after review. | Remove repository-specific preference from the current plan. | No. |
| CON-010 | Hardware was treated as information the user must manually provide. | Codex inspects the actual system automatically. | Owner changed to Codex automated inventory. | No. |
| CON-011 | Some flows were dashboard-first. | Scientific core is independent; a lightweight debug surface may assist validation, while the polished final dashboard follows validated core and pilot evidence. | Core-first scientific architecture remains mandatory without blocking useful early visualization. | No. |
| CON-012 | Mock/proxy metrics were treated as useful final-demo data. | The final application must not show fake progress/logs/metrics. | Mocks only in isolated, clearly labelled tests/dev fixtures. | No. |
| CON-013 | GPU-heavy approaches were proposed without system inspection. | Do not assume NVIDIA/CUDA; capability decisions follow automated inventory/benchmarks. | Hardware-aware selection. | After inventory. |
| CON-014 | This thesis repository was previously designed to acquire, archive, convert, note, and excerpt bibliography sources directly under `bibliography/`. | `MariosGiannakaras/ThesisBibliography` now owns the complete bibliography lifecycle; this repository imports only verified generated evidence under `research/bibliography/`. | Local acquisition/archive instructions are retired compatibility markers and must not be reactivated. | No. |