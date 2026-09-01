# T-613 Thesis/Defense Figure and Table Inventory

**Status:** pre-execution output contract; no final outcomes are present or inspected here.  
**Authority boundary:** T-613 executes only after T-610 final execution, T-611 evidence validation/freeze, and T-612 predeclared final analysis are complete. The application is an inspection surface; final thesis figures/tables are generated reproducibly from validated stored outputs rather than screenshots.

## Output principles

- Preserve the exact RQ1/RQ2/RQ3 definitions, estimands, denominators, right-censoring semantics, condition identities and method order already frozen by protocol-v2.1.
- Generate deterministic publication assets with source-artifact lineage and a manifest tying every figure/table to the validated analysis/evidence package.
- Produce vector-first outputs (`SVG` and/or `PDF`) plus high-resolution `PNG` for Word/PowerPoint compatibility and machine-readable tables (`CSV` plus Markdown/other thesis-consumption form where useful).
- Use one consistent, colorblind-safe visual grammar with redundant markers/line styles so interpretation never depends on color alone.
- Main-text figures emphasize the primary claims; appendix/supplementary assets expose root-level variability, condition detail and diagnostics without overwhelming the thesis narrative.
- Do not infer rankings, significance claims or recovery times that are not present in the validated stored analysis.

## RQ1 — nominal learning

### Main-text figures

1. **RQ1 learning progression / probe curves by method** — interaction/probe axis, stored method summaries and stored intervals where available.
2. **RQ1 final nominal performance** — five-method point/range or bar-with-interval comparison using the registered final-value summary.
3. **RQ1 interaction-axis time-average** — separate five-method summary so final-probe and across-training behavior are not conflated.

### Appendix / diagnostic figures

4. **RQ1 final-value root distribution** — root-level values by method from validated root records.
5. **RQ1 time-average root distribution** — matching root-level diagnostic.
6. **RQ1 checkpoint/probe heatmap or compact matrix** where validated stored probe data support it.
7. **RQ1 direct method contrasts** — root-paired A-minus-B contrasts with stored intervals, explicitly labeled as predeclared direct comparisons.

### Tables

- five-method final-value summary with denominators and intervals;
- five-method time-average summary with denominators and intervals;
- complete RQ1 direct-contrast table;
- appendix root-level RQ1 table where size remains practical.

## RQ2 — resilience / adaptation

### Main-text figures

8. **Adaptation benefit by method for each condition** — primary RQ2 effect with stored intervals.
9. **Frozen vs Adaptive disturbance-associated loss** — paired/grouped view, kept distinct from adaptation benefit.
10. **Condition small multiples** — one panel per frozen protocol condition with consistent scales where scientifically appropriate.

### Appendix / diagnostic figures

11. **Frozen→Adaptive paired/dumbbell plot by method and condition** from validated stored summaries/root records.
12. **Root-level adaptation-benefit distributions** by method and condition.
13. **Method × condition heatmap** for stored adaptation benefit, accompanied by numeric values and clear directionality.
14. **RQ2 direct method contrasts** by condition and estimand with stored intervals.
15. **Root-level Frozen/Adaptive paired diagnostics** where useful for auditability and explanation.

### Tables

- complete method × condition Frozen loss / Adaptive loss / adaptation-benefit summary;
- primary RQ2 effect table with denominators and intervals;
- complete RQ2 direct-contrast table;
- appendix root-level RQ2 values.

## RQ3 — recovery

### Main-text figures

16. **Recovery directed-gap trajectories** over the frozen 32-interaction windows, showing baseline gap, primary tolerance, observation horizon and backend-classified recovery/non-recovery.
17. **Recovered proportion by method** for the primary recovery condition family, with right-censored counts visible.
18. **Restricted recovery delay through horizon** by method/condition with stored intervals.
19. **Observed recovery time conditional on recovery** only where recovery exists; right-censored cases remain unavailable rather than receiving the horizon as a fake recovery time.

### Appendix / diagnostic figures

20. **Per-condition RQ3 small multiples** across all supported recovery conditions.
21. **Per-root recovery trajectories** for detailed audit/appendix inspection.
22. **Recovered vs right-censored composition** by method/condition.
23. **Primary tolerance sensitivity comparison** for the frozen 0.05 / 0.10 / 0.20 sensitivity contract.
24. **RQ3 direct method contrasts** for recovery-status indicator and restricted recovery delay with stored intervals.
25. **Recovery-time / confirmation-time diagnostic timeline** where the validated root-level recovery records provide those stored values.

### Tables

- recovery summary by method/condition with recovered/censored roots, recovered proportion, conditional recovery time and restricted delay;
- primary/sensitivity recovery table;
- complete RQ3 direct-contrast table;
- appendix root-level recovery status/time/censoring table;
- appendix trajectory table keyed by method/root/condition/window.

## Cross-RQ / methodology / defense assets

26. **Experiment flow schematic** — Phase A → exact checkpoint → matched FN/FD/AN/AD → validation/analysis/export.
27. **RQ-to-evidence map** — RQ1/RQ2/RQ3 → stored estimands → registered tables/figures.
28. **Evidence lineage schematic** — frozen recipe → jobs → validation → analysis package → T-613 figures/tables.
29. **Compact all-method/all-RQ summary graphic** for defense use only when it can remain descriptive and not collapse distinct estimands into a composite score.
30. **Defense-optimized variants** of selected main figures with larger labels and the same underlying data/provenance.

## T-613 deliverable manifest

T-613 must record for each generated asset:

- stable asset ID and filename;
- RQ / estimand / condition scope;
- source registered artifact IDs and SHA-256 values;
- source final evidence/analysis package identity;
- generator version / source Git commit;
- deterministic generation parameters that affect presentation only;
- intended use (`main-thesis`, `appendix`, `defense`, or multiple);
- vector/raster/table variants generated;
- explicit note that application screenshots are illustrative UI assets, not the quantitative source for thesis claims.
