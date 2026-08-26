# Reproducible Experiment Analysis

`src/resilient_agents/analysis.py` is the version-controlled, UI-independent path from finalized run bundles to pilot diagnostics. It never repairs or rewrites a run, and it derives scientific records only from execution status `completed`. Failed, cancelled, and invalid runs remain explicit inventory and operational-diagnostic inputs with zero scientific units.

## Invocation

```text
uv run python scripts/analyze_experiments.py \
  --repo-root <repository-root> \
  --analysis-id <new-analysis-id> \
  --run-id <finalized-run-id> [--run-id <another-run-id> ...]
```

Run IDs are explicit, unique, and sorted deterministically. Every input must pass the existing finalization marker, manifest, file checksum, and unique run-index validation. Pilot analysis additionally requires a clean committed analysis source. An existing analysis ID is immutable and cannot be overwritten.

## Scientific derivation

For each completed runner bundle, analysis reconstructs and validates the stored `pilot-v0.1` protocol and exact headless request. It verifies summary identity, requested root and agent order, training-curve lengths, common Q-checkpoint integrity, matched pre-change curves, state digests, and frozen-F0 state invariance. Primary schema-v1 metrics are recomputed from the stored reference/disrupted curves and must exactly equal the stored runner metrics.

One scientific unit is one `(run, layout, condition, root seed, agent role)` record. Units retain their curves, primary metrics, starting-state provenance where applicable, and reference/disrupted final-state digests. Aggregates group only valid completed units by layout, condition, and agent, report unit identities/counts, explicit recovery-status counts, metric means, and sample standard deviations. Recovery delay is averaged only among genuinely recovered units; non-recovery remains categorical and is never replaced by the horizon.

The complete predeclared `pilot-v0.1` metric-sensitivity grid is recomputed per unit and retained both as unit records and diagnostic aggregates. These outputs are descriptive pilot diagnostics only. They do not freeze a statistical model, support final claims, or permit post-outcome tuning of final evidence.

## Operational diagnostics and outputs

Operational event attempts remain separate from the atomic completed-root scientific units, so interrupted/retried work cannot become an extra observation. Per-run diagnostics include execution status, event/episode attempt counts, phase/outcome counts, root start/completion counts, wall-clock duration, bundle bytes, and manifest/summary digests. Later exclusion decisions never overwrite original execution status.

```text
results/summaries/<analysis-id>/
  analysis.json
  units.jsonl
  sensitivity.jsonl
  manifest.json
  checksums.sha256
  FINALIZED
```

Files are written under a temporary identity, checksummed, atomically renamed, and marked `FINALIZED` last. `validate_analysis()` rejects missing/extra/symlinked artifacts, malformed/non-finite JSON, identity or record-count drift, and checksum/size corruption. The output records the exact input run IDs and analysis-source Git commit and remains reproducible from the immutable bundles and version-controlled code.
