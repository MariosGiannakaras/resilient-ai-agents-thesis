# Decision Log

Use this file for project-wide research and architecture decisions. Detailed alternatives may use separate ADRs.

## DEC-001 — Private repository as source of truth
- **Date:** 2026-07-29
- **Status:** Accepted
- **Context:** Codex/other agents do not have access to the original ChatGPT conversations.
- **Decision:** `MariosGiannakaras/resilient-ai-agents-thesis` is the permanent version-controlled source of truth.
- **Rationale:** Decisions and evidence must remain available independently of chat history.
- **Alternatives:** Large bootstrap prompts; raw chat archive in repo.
- **Consequences:** Context files must be maintained; raw chats remain excluded.
- **Related requirements:** REQ-REPO-001, REQ-REPO-003.
- **Files:** `README.md`, `AGENTS.md`, `docs/context/`.

## DEC-002 — Official application controls academic identity
- **Date:** 2026-07-29
- **Status:** Accepted
- **Context:** Old chats used inconsistent degree labels and title variants.
- **Decision:** Use the exact institution and titles from the official application.
- **Rationale:** It is the primary approved source.
- **Alternatives:** Historical title variants.
- **Consequences:** Earlier “Master’s thesis” wording is superseded.
- **Related requirements:** REQ-ACA-001..003.
- **Files:** `thesis/source-material/`, `docs/context/CONTRADICTIONS.md`.

## DEC-003 — Original application retained unchanged in private repository
- **Date:** 2026-07-29
- **Status:** Accepted by user
- **Context:** The scanned application contains personal contact/student data.
- **Decision:** Store the original unchanged in the private repository.
- **Rationale:** Preserve the authoritative source; user explicitly approved.
- **Alternatives:** Redacted copy only; metadata extraction only.
- **Consequences:** Repository must remain private; redact/remove before any public release.
- **Related requirements:** REQ-REPO-002.
- **Files:** `thesis/source-material/SOURCE_MANIFEST.md`.

## DEC-004 — Research core precedes dashboard
- **Date:** 2026-07-29
- **Status:** Accepted
- **Context:** Historical work sometimes prioritized UI scaffolding.
- **Decision:** Validate independent core/CLI and pilot runs before dashboard implementation.
- **Rationale:** Scientific correctness and reproducibility have higher priority than presentation.
- **Alternatives:** Dashboard-first vertical prototype.
- **Consequences:** UI work is phase-gated.
- **Related requirements:** REQ-ARCH-001, REQ-ARCH-002.
- **Files:** `AGENTS.md`, `IMPLEMENTATION_ROADMAP.md`.

## DEC-005 — No final model, metric or experimental matrix yet
- **Date:** 2026-07-29
- **Status:** Accepted
- **Context:** Old chats contain incompatible “final” model lists, seeds and budgets.
- **Decision:** Treat them as candidates; select after literature, GridWorld audit, hardware inventory and pilots.
- **Rationale:** Prevent arbitrary/obsolete experimental design.
- **Alternatives:** Reuse the most recent historical list.
- **Consequences:** Main implementation is blocked until research decisions are made.
- **Related requirements:** REQ-RES-005, REQ-EXP-007.
- **Files:** `MODEL_CANDIDATES.md`, `METRICS_CANDIDATES.md`, `OPEN_QUESTIONS.md`.

## DEC-006 — CPU-first compute strategy
- **Date:** 2026-07-29
- **Status:** Accepted pending hardware verification
- **Context:** Approximate hardware is Ryzen 5 2600X and Radeon RX 570 8 GB; no NVIDIA/CUDA.
- **Decision:** Every required workflow must run on CPU; acceleration is optional after a supported proof.
- **Rationale:** Avoid architecture/model choices that cannot run on the actual machine.
- **Alternatives:** Assume ROCm or CUDA-equivalent GPU training.
- **Consequences:** Large neural/world-model candidates face a high inclusion threshold.
- **Related requirements:** REQ-TECH-001, REQ-TECH-002.
- **Files:** `CONSTRAINTS.md`, `MODEL_CANDIDATES.md`.

## DEC-007 — Raw chat exports excluded
- **Date:** 2026-07-29
- **Status:** Accepted
- **Context:** Exports contain repetition, obsolete AI proposals, personal context and unrelated text.
- **Decision:** Commit only verified synthesis, not `OldConvo.zip` or extracted transcripts.
- **Rationale:** Privacy, clarity and source governance.
- **Alternatives:** Archive all conversations under `docs/raw/`.
- **Consequences:** Source audit records filenames and limitations.
- **Related requirements:** REQ-REPO-003.
- **Files:** `SOURCE_AUDIT.md`, `.gitignore`.

## DEC-008 — Official department guidance snapshot, not frozen final template
- **Date:** 2026-07-29
- **Status:** Accepted
- **Context:** A department writing-guidelines PDF was verified, but a current Word template was not.
- **Decision:** Record the guidance now; recheck current template/submission rules near finalization.
- **Rationale:** Separates verified current evidence from unresolved formatting delivery details.
- **Alternatives:** Assume historical examples define the format.
- **Consequences:** Word styling remains adaptable.
- **Related requirements:** REQ-ACA-005, REQ-THESIS-002.
- **Files:** `docs/university/`, `THESIS_REQUIREMENTS.md`.

## Pending decisions

Future entries are required for:
- final research questions/hypotheses,
- existing GridWorld reuse or replacement,
- uncertainty taxonomy,
- selected models/baselines,
- primary metrics and statistical plan,
- seeds/repetitions/budgets,
- application stack/storage/runner,
- optional AI,
- citation style and final Word template.
