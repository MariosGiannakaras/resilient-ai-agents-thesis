# T-719A Targeted Final Pass

**Status:** IN_PROGRESS — bounded internal author-directed refinement after accepted T-719  
**Base authority:** `thesis/archive/T719_final_authority_audited_review_ready.docx`  
**Base SHA-256:** `1529f2b8a69594f164050544a54e1de115acb40a5a0eb6291156d3ecccf1afb9`

T-719A exists only because the author supplied a new, narrowly scoped post-T-719 pass. It is not supervisor/reviewer feedback and does not reopen T-712. It must not alter any frozen scientific decision, result, estimand, threshold, horizon, root, layout, seed, budget, method configuration or T-613 registered quantitative asset.

## Confirmed changes

Only these three reader-facing clarifications are accepted for implementation:

1. **Glossary / Recovery** — replace the remaining symmetric-sounding “stable approach” wording with an explicit directed AN−AD stable-criterion definition. Mathematical thresholds and the two-window rule remain unchanged.
2. **Fairness boundary** — add one sentence in §3.3 stating that the common Phase-A actual-environment-interaction budget provides resource/budget matching, not equality of attained nominal competence at the Phase-B boundary.
3. **RQ1 / −0.100 interpretation** — add one short sentence after the first §5.2.1 result paragraph explaining that, with both final layouts having shortest-path length 12 and the frozen reward contract, −0.100 is the return of a shortest-path solution: eleven ordinary −0.1 rewards followed by the terminal +1.0 goal reward. Do not call this a “global optimum”.

## Authority for the three changes

- Directed RQ3 recovery: `docs/decisions/DEC-060_PROTOCOL_V2_1_RECOVERY_AND_COMPARISON_AMENDMENT.md` and `configs/protocols/protocol-v2.1-final.json`.
- Phase-A fairness boundary: the same protocol authority plus §3.3/§3.4 methodology and accepted RQ1 evidence. The budget is 8,192 actual environment interactions for every method; the final attained nominal means are not constrained to be equal.
- −0.100 interpretation: `configs/protocols/protocol-v2.1-final.json` fixes `shortest_path_length=12` for both final layouts, `step=-0.1`, and `goal=1.0`; `src/resilient_agents/gridworld.py` applies `goal_reward` on the terminal transition instead of `step_reward`.

## Explicitly unchanged / unresolved

- **Chacon-Chamorro bibliography identity:** do not patch the manuscript. The synchronized citation-ready catalog/manifest identify the 2025 IEEE TAI DOI `10.1109/TAI.2025.3567371`, while the citation-ready checked analysis still explicitly describes the verified 2024 arXiv `2409.13187` version. This remains an upstream `MariosGiannakaras/ThesisBibliography` reconciliation item.
- **Appendix B.3 pagination:** no manual blank lines, brittle page breaks, caption splitting, registered-asset changes or unjustified figure shrinking. Leave unchanged unless natural reflow from the accepted edits demonstrably fixes it without collateral damage.
- **Front matter:** do not invent student identity, committee/date data or declaration text. Exact declaration wording remains gated by authoritative Department/University input.
- **Cover page number:** current official Department guidance does not establish a rule requiring the visible cover number to be suppressed. Do not hide it by convention; keep this as a downstream formatting item unless stronger authority is found.

## Acceptance / QA

The final candidate must:

1. start from the exact T-719 base hash;
2. contain exactly the three accepted semantic edits;
3. preserve the same 32 bibliography entries and citation sequence;
4. preserve all 25 embedded media byte-for-byte;
5. preserve all frozen results/protocol values and registered quantitative assets;
6. preserve header/footer/section numbering configuration unless authority explicitly requires otherwise;
7. export to PDF and receive focused semantic, pagination, caption/image and visual QA on that exported PDF;
8. keep T-712 DEFERRED after merge and leave final personal/declaration/submission gates for T-713.
