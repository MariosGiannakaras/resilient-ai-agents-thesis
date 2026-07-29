# Source Audit

## Source hierarchy

1. Newer explicit user instruction.
2. Official approved application or formal thesis description.
3. Current official University/Department/supervisor guidance.
4. Verified primary scientific literature.
5. Official technical documentation, source code, release history, license and reproducible benchmarks.
6. Actual system inventory and pilot measurements.
7. Conversation exports only as historical context and examples of questions previously discussed; they do not establish decisions, preferences or candidate shortlists.

## Sources reviewed for bootstrap

| Source | Type | Use | Trust / limitations | Repository treatment |
|---|---|---|---|---|
| `GiannakarasMariosThesisApplication.pdf` | Official primary document | Academic identity, exact titles, official broad objective and examples | High trust for visible content; scanned one-page document | Approved for unchanged private storage; local SHA-256 recorded; GitHub binary upload pending verification |
| `Pasted text(15).txt` | Current user task specification | Repository structure, explicit confirmed constraints, required files and definition of done | High trust as explicit current instruction | Synthesized; original task file not committed |
| Current clarification dated 2026-07-29 | Explicit user instruction | Old chats are examples only; decisions from scratch; no legacy-code requirement; Codex inspects hardware | Highest priority for these issues | Incorporated across context/research/Codex files |
| `OldConvo.zip` containing 10 Markdown exports | Historical conversational context | Understand prior explorations and detect possible topics/risks to re-check | Not authoritative; includes AI proposals, repetition, obsolete assumptions and apparent “final” language | Not committed; not used as shortlist or decision source |
| Official Department writing-guidelines PDF | Official institutional source | Structure, methodology, formatting and citation guidance | Official available document; must still be checked for a newer revision near submission | URL and dated snapshot recorded |
| Department/OpenArchives thesis metadata | Supporting public metadata | Verify that recent Department theses exist and identify examples | Not formatting authority; metadata is not full-methodology review | Exact verified titles/URLs recorded |
| Connected GitHub repository inventory | Direct system source | Repository privacy/access and content operations | High trust for accessible account state | Repository metadata and commits verified |
| Public GridWorld ecosystem search | Discovery input | Demonstrates that multiple current alternatives exist and a fresh comparison is required | Not a selection decision | No specific library is frozen or copied |

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

## Provenance rules

- A statement or recommendation in a chat is not a user decision unless independently confirmed in the current task/context.
- “Locked”, “final” or “completed” wording in an old AI response has no authority.
- No historical model, metric, stack, GridWorld repository, budget or hyperparameter is carried into the new design merely because it appeared in an export.
- Literature references from chats must be rediscovered and verified against original publications.
- Repository/package claims require direct inspection of current source, license, releases and code.
- Hardware claims require automated inspection of the actual execution system.
- Current official guidance must be rechecked near submission.
