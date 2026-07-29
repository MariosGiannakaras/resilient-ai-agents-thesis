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
- **Consequences:** Earlier “Master's thesis” wording is superseded.
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
- **Decision:** Do not treat historical model/metric lists as candidates. Build the shortlist from scratch after fresh literature, environment definition, automated hardware inventory, feasibility prototypes and pilots.
- **Rationale:** Prevent arbitrary or obsolete experimental design.
- **Alternatives:** Reuse or lightly filter historical lists.
- **Consequences:** Historical names may be rediscovered independently, but only fresh evidence can place them in the shortlist. Main implementation is blocked until research decisions are made.
- **Related requirements:** REQ-RES-005, REQ-RES-007, REQ-EXP-007.
- **Files:** `MODEL_CANDIDATES.md`, `METRICS_CANDIDATES.md`, `OPEN_QUESTIONS.md`.

## DEC-006 — No acceleration assumptions before automated inventory
- **Date:** 2026-07-29
- **Status:** Accepted
- **Context:** Historical hardware reports may be stale; Codex will access the actual execution system.
- **Decision:** Codex automatically records hardware/software capabilities before compute-dependent choices. No NVIDIA/CUDA/ROCm assumption is permitted; CPU-compatible execution is the safe temporary baseline.
- **Rationale:** Direct system evidence is more reliable than chat history or manual transcription.
- **Alternatives:** Assume specific hardware/acceleration from old messages; manual questionnaire.
- **Consequences:** Model and batch decisions use measured capabilities and benchmark evidence.
- **Related requirements:** REQ-TECH-001, REQ-TECH-002.
- **Files:** `CONSTRAINTS.md`, `AGENTS.md`, `CODEX_BOOTSTRAP_PROMPT.md`.

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
- **Rationale:** Separates verified available official evidence from unresolved formatting-delivery details.
- **Alternatives:** Assume historical examples define the format.
- **Consequences:** Word styling remains adaptable.
- **Related requirements:** REQ-ACA-005, REQ-THESIS-002.
- **Files:** `docs/university/`, `THESIS_REQUIREMENTS.md`.

## DEC-009 — Conversation exports are context only
- **Date:** 2026-07-29
- **Status:** Accepted by user
- **Context:** Bootstrap synthesis initially treated historical mentions as candidate lists and reconstructed preferences.
- **Decision:** Old conversations are examples and context only. They do not establish selected models, metrics, GridWorld rules, stack, hyperparameters or user preferences. All such decisions are made anew.
- **Rationale:** Historical chats contain exploratory AI suggestions and may be obsolete or incorrect.
- **Alternatives:** Use recency/frequency to infer preferred choices.
- **Consequences:** Candidate workspaces were reset and source hierarchy updated.
- **Related requirements:** REQ-RES-005, REQ-RES-007.
- **Files:** `AGENTS.md`, `SOURCE_AUDIT.md`, `MODEL_CANDIDATES.md`, `METRICS_CANDIDATES.md`, `GRIDWORLD_SPEC.md`.

## DEC-010 — Fresh GridWorld discovery; no legacy-code dependency
- **Date:** 2026-07-29
- **Status:** Accepted by user
- **Context:** The project will be developed anew. Earlier bootstrap text incorrectly asked for an existing GridWorld repository/path or legacy folder.
- **Decision:** Codex performs a current landscape review, compares reuse/adapt/custom, prototypes the strongest options and only then downloads/integrates a suitable library or implements a minimal custom environment.
- **Rationale:** Prevents locking the thesis to an old or unsuitable repository.
- **Alternatives:** Require recovery of old code; preselect a historical public repository.
- **Consequences:** Legacy-source blockers and repository-specific preferences are removed.
- **Related requirements:** REQ-RES-008.
- **Files:** `GRIDWORLD_SPEC.md`, `OPEN_QUESTIONS.md`, `CODEX_BOOTSTRAP_PROMPT.md`, `IMPLEMENTATION_ROADMAP.md`.

## DEC-011 — Codex owns system inventory
- **Date:** 2026-07-29
- **Status:** Accepted by user
- **Context:** Codex will run on and have access to the actual system.
- **Decision:** Codex automatically collects CPU, RAM, GPU/VRAM, OS, drivers, runtimes and storage. The user is not asked to manually supply data that can be inspected reliably.
- **Rationale:** Reduces errors and stale information.
- **Alternatives:** Manual hardware questionnaire.
- **Consequences:** Hardware remains a Codex phase task, not a user-provided repository prerequisite.
- **Related requirements:** REQ-TECH-001, REQ-TECH-002.
- **Files:** `CONSTRAINTS.md`, `OPEN_QUESTIONS.md`, `AGENTS.md`, `CODEX_BOOTSTRAP_PROMPT.md`.

## DEC-012 — Final bootstrap re-audit governs the next phase
- **Date:** 2026-07-29
- **Status:** Accepted
- **Context:** Tool operations were interrupted and the first synthesis contained the three interpretation errors documented in `FINAL_BOOTSTRAP_AUDIT.md`.
- **Decision:** The corrected context files and final audit supersede inconsistent bootstrap wording. Research discovery and system inspection may begin, but implementation remains phase-gated.
- **Rationale:** Prevent stale or partially generated documentation from steering Codex.
- **Alternatives:** Preserve initial files and explain corrections only in chat.
- **Consequences:** Codex must read the final audit and corrected bootstrap prompt before work.
- **Files:** `FINAL_BOOTSTRAP_AUDIT.md`, `CHANGELOG_CONTEXT.md`, `CODEX_BOOTSTRAP_PROMPT.md`.

## Pending decisions

Future entries are required for:

- final research questions/hypotheses,
- GridWorld reuse/adapt/custom decision after fresh landscape review,
- uncertainty taxonomy,
- selected models/baselines,
- primary metrics and statistical plan,
- seeds/repetitions/budgets,
- application stack/storage/runner,
- optional AI,
- citation style and final Word template.
