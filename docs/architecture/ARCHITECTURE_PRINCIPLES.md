# Architecture Principles

1. **Core without UI.** Environment, agents, runner, storage and analysis can operate through CLI/programmatic interfaces.
2. **Dashboard as control/presentation layer.** It sends validated commands and reads real state; it does not reimplement scientific logic.
3. **One canonical config path.** CLI and UI resolve the same schema and defaults.
4. **Immutable raw results.** Storage behavior does not depend on UI state.
5. **Explicit lifecycle state machine.** Queue/run/pause/cancel/failure semantics are testable.
6. **Restart and recovery.** Partial state, checkpoints and manifests survive process/application interruption where technically supported.
7. **Stable identifiers and lineage.** Runs, experiments, datasets and artifacts use immutable IDs.
8. **Structured events/logs.** Human-readable views derive from structured backend records.
9. **Version everything that affects results.** Code, config schema, environment, agent, metric and processing versions.
10. **Simple local architecture.** Prefer a modular monolith/process-based design appropriate for one user.
11. **Avoid microservices and Kubernetes.** They add failure modes without current need.
12. **Avoid cloud infrastructure and complex authentication.**
13. **Avoid unnecessary realtime technology.** Polling, local IPC or event streams are chosen by measured need.
14. **Portable CPU-first execution.** Hardware acceleration is optional and isolated behind capability detection.
15. **Dependency restraint.** Add libraries only for clear correctness, reproducibility or usability value.
16. **No hidden notebook state.** Notebooks explore; production code and configurations remain canonical.
17. **Separation of data layers.** Raw, processed, summaries and thesis-frozen artifacts have distinct retention/mutation policies.
18. **Schema validation at boundaries.** Configs, run manifests and result records fail clearly on invalid input.
19. **Scientific errors are first-class.** Invalid config, unreachable map, metric failure and statistical misuse are not generic UI exceptions.
20. **Decision traceability.** Significant architecture/research choices enter the decision log or ADR.
21. **Small, reviewable changes.** Avoid speculative frameworks and future-proofing without evidence.
22. **Security proportional to scope.** Protect secrets and private material without inventing public-service threat models.
