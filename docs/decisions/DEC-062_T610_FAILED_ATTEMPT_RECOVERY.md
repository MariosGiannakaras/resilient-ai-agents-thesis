# DEC-062 — T-610 failed-attempt recovery

**Status:** Accepted on 2026-09-02
**Scope:** Infrastructure-only correction and complete replacement execution of the unchanged frozen protocol-v2.1 recipe

## Decision

The first authorized `protocol-v2.1-final` execution is an immutable failed/incomplete historical attempt. It remains auditable at source commit `7442dcb65674dcb3bc9ce0c71996418289d79061`, recipe SHA-256 `8f21075ad2bc7a7944dbac4ba2ee2f3255ec0157706b94f99174b6d9ef99b154` and plan SHA-256 `073779d18f45caeab2ab725e7dce6b54b70394102d45de81e1974c7efaece0f4`. Its durable state is 216 completed jobs, one infrastructure failure and 386 pending jobs. It is not eligible for T-611, T-612, T-613, thesis results or any final scientific conclusion. None of its completed runs or Phase-A checkpoints may be copied, resumed or mixed into replacement evidence.

The recorded failure is a deterministic Study implementation defect at the Phase-A to Phase-B checkpoint boundary. The generic Study Phase-A executor persisted the raw final-budget learner checkpoint without applying the deployment-start settlement already required by DEC-054. SARSA can therefore retain a valid deferred final-budget transition that the Phase-B quiescence guard correctly rejects.

DEC-054 was accepted and its five-method, zero-environment-interaction settlement behavior was physically validated before final outcomes existed. The recovery applies that existing rule at the missing Study boundary. It is implementation conformance, not outcome-driven scientific tuning. For SARSA, the exact DEC-054 behavior-policy bootstrap update settles a valid deferred transition; it consumes zero additional environment interactions and leaves the learner quiescent. Q-Learning, DQN, PPO and Dyna-Q+ retain their already quiescent no-op semantics. Unknown or inconsistent unfinished state continues to fail closed.

## Replacement execution identity

Scientific identity and execution-attempt identity are distinct. The immutable scientific recipe remains `protocol-v2.1-final`, and its deterministic plan remains unchanged. The replacement execution instance is:

- execution instance: `protocol-v2.1-final--t610-recovery-01`;
- scientific recipe: `protocol-v2.1-final`;
- predecessor execution instance: `protocol-v2.1-final`;
- recovery decision: `DEC-062`;
- corrected source commit: recorded from the clean merged commit when the replacement is created.

The Study manifest records this lineage. The execution-instance identifier controls only the storage/run namespace; it does not enter or alter the scientific recipe, plan, statistical identity, roots, layouts, seeds, methods, configurations, budgets, conditions, horizons, estimands or evidence definitions. Existing Study manifests without an explicit execution-identity block remain loadable only as their original same-name initial instance.

## Recovery procedure

1. Commit the first attempt exactly as preserved, including its unfinalized lifecycle, failure event, 216 finalized run bundles and run-index records.
2. Merge the minimal boundary correction, execution-instance provenance support and focused regression tests through the normal PR/CI/review path.
3. Synchronize the Windows execution checkout to clean merged `main`.
4. Run the complete read-only T-610 preflight. It must verify the historical attempt byte-for-byte, reproduce the same recipe and canonical 603-job plan, confirm the replacement does not yet exist and prove the final authorization guard remains deny-by-default.
5. Create the replacement instance from that single clean corrected commit, using `PROTOCOL_V21_FINAL_EXECUTION_AUTHORIZATION` without weakening the guard.
6. Execute all replacement jobs from the beginning. Do not import any artifact or checkpoint from the predecessor. Apply only the existing restart-safe infrastructure-retry contract to the replacement instance.
7. Stop fail-closed if any frozen scientific invariant changes or another scientific-integrity contradiction appears.

T-610 completes only when the replacement Study reaches its objective allowed terminal state with all 603 planned jobs accounted for, coherent provenance and durable finalization. T-611 is then the next dependency-valid task. This decision does not authorize T-611, T-612, T-613, WP7, outcome interpretation, or Results/Discussion writing.
