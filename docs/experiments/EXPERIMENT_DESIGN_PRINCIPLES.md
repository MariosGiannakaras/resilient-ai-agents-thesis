# Experiment Design Principles

1. **Start from the research question.** A run exists to estimate or validate something, not because a model/library is fashionable.
2. **No single-run comparisons.** Report distributions across independent repetitions.
3. **No arbitrary hyperparameters.** Values and ranges come from literature, validated defaults, pilots or explicit resource trade-offs.
4. **Separate tuning from final evaluation.** Final scenarios cannot be repeatedly inspected to improve a model.
5. **Keep conditions comparable.** Shared environment/scenarios/metrics and explicit information access.
6. **Report unequal resources honestly.** Equal interactions, wall-clock and internal planning are different budgets.
7. **Use multiple seeds.** Derive and record RNG streams; never hide seed sensitivity.
8. **Do not cherry-pick.** The run registry includes failures, cancellations and poor outcomes.
9. **Predefine exclusions.** Exclusions need objective rules and remain visible.
10. **Separate pilot, exploratory and final evidence.**
11. **Freeze the protocol.** Material changes after freeze create a new protocol version and amendment.
12. **Preserve raw results.** Never edit them to repair analysis.
13. **Record outliers, do not silently delete them.** Analyze causes and run sensitivity checks.
14. **Check statistical assumptions.** Prefer robust estimates when distributions violate simple assumptions.
15. **Report effect sizes and uncertainty.** P-values alone are insufficient.
16. **Handle censored recovery explicitly.** A run that does not recover within the horizon is not assigned an invented recovery time.
17. **Account for dependence.** Episodes nested in the same seed/run are not independent replicates.
18. **Control multiple comparisons where inferential claims require it.**
19. **Use negative and unexpected results.** They are evidence, not defects to hide.
20. **Make computation reproducible.** Config, code, versions, hardware and command accompany every run.
21. **Validate metrics with known-answer fixtures.**
22. **Avoid test leakage.** Held-out layouts/disturbances stay held out.
23. **Do not conflate training performance with evaluation resilience.**
24. **Declare adaptation regime.** Frozen policy, online learning and replanning answer different questions.
25. **Keep the UI out of the scientific loop.** Dashboard actions produce the same validated configs/runner behavior as CLI.
