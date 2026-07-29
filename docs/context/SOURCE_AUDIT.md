# Source Audit

## Source hierarchy

1. Newer explicit user instruction.
2. Official approved application or formal thesis description.
3. Current official University/Department guidance.
4. User decisions reconstructed from conversation exports, ordered by recency/specificity.
5. Real bibliography and primary technical documentation.
6. AI-generated historical suggestions, only as non-binding candidates.

## Sources reviewed for bootstrap

| Source | Type | Use | Trust / limitations | Repository treatment |
|---|---|---|---|---|
| `GiannakarasMariosThesisApplication.pdf` | Official primary document | Academic identity, exact titles, official broad objective and examples | High trust for visible content; scanned one-page document | Stored unchanged in `thesis/source-material/` with SHA-256 |
| `Pasted text(15).txt` | User task specification | Repository structure, required files, definition of done | High trust as current explicit instruction | Synthesized; original task file not committed |
| `OldConvo.zip` containing 10 Markdown conversation exports | Historical conversational source | Prior ideas, user preferences, contradictions and legacy references | Mixed trust; contains AI proposals, repetition and obsolete decisions | Not committed; only verified synthesis retained |
| Official Department writing-guidelines PDF | Official institutional source | Structure, methodology, formatting, citations | Authoritative unless superseded by newer official guidance | Source URL and dated snapshot recorded |
| Connected GitHub inventory | Direct system source | New repository verification and search for existing user repos | High trust for accessible account state; may not include local/unconnected code | Results summarized; no unsupported inference |
| Public `prasenjit52282/GridWorld` repository | Third-party technical reference | Possible historical repository candidate/reference | Not confirmed as the user's existing code; license and commit must be reviewed before reuse | URL recorded only; no code copied |
| AMD ROCm compatibility documentation | Primary vendor documentation | Hardware feasibility check | Version/platform-specific; must be rechecked at implementation time | Used only for CPU-first constraint rationale |

## Conversation export inventory

The following files were inspected from the private export and were not committed:

- `_AI.md`
- `_Resilient_AI_Agents.md`
- `AI_agent_resilience_topics.md`
- `AI_Model_Comparison_Tools.md`
- `THESIS_-_AI.md`
- `THESIS_-_Bibliography_on_AI_resilience.md`
- `THESIS_-_Resilient_AI_Agents.md`
- `THESIS_-_Resilient_AI_Agents-1.md`
- `THESIS_-_Translate_to_Greek_AI_agents.md`
- `Thesis_Experimental_Design.md`

## Provenance caveats

- A statement repeated by an assistant is not automatically a user decision.
- “Locked”, “final” or “completed” wording in an old AI response has no authority without user confirmation or observable artifact.
- Repository/code claims remain unverified until the exact URL/path and commit are inspected.
- Literature references from old chats must be verified against the original publication before use.
- Current official guidance must be rechecked near submission.
