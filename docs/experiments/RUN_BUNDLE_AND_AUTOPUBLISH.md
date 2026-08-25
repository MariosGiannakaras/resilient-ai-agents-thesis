# Run Bundle and Automatic Git Publication

A `run_id` represents one whole experiment execution and may contain many seeds and episodes. Intermediate seed completion never creates a Git commit.

When the whole experiment reaches an execution-final state (`completed`, `failed`, `cancelled`, or `invalid`), its bundle is finalized once. If automatic publication is enabled, exactly one result commit is created and pushed. `excluded` is not an execution-final state: it is a later analysis/inclusion decision layered over the retained original execution outcome, so exclusion must never overwrite whether the run actually completed, failed, was cancelled, or was invalid.

## Bundle

```text
results/runs/<run-id>/
  manifest.json
  resolved-config.json
  system-capability.json
  events.jsonl
  trace.jsonl
  summary.json
  checksums.sha256
  FINALIZED
```

`results/run-index.jsonl` is updated once per finalized run. The manifest records protocol version/stage, timestamps, source Git commit, Python/platform provenance, final status, retention policy, file sizes, and SHA-256 digests. Source provenance separately records tracked modifications and whether untracked **non-output** files were present when the run started. Untracked files under `results/**` and `artifacts/**` are treated as generated/local output and do not by themselves make the scientific source tree dirty; untracked code, config, data, scripts, or other repository inputs do. The existing privacy-minimal system-inventory collector records the same booleans without exposing untracked filenames and is stored with the run.

`FINALIZED` is a completion sentinel, not a scientific data file. It is written **last**, only after the final manifest, checksum manifest, and run-index update succeed. If finalization is interrupted before that point the marker is absent, so the bundle cannot be mistaken for a valid finalized publication candidate. Event/trace mutation is rejected after finalization.

## Automatic commit and push

Before any Git staging, publication requires the finalization sentinel and revalidates the marker contents against manifest schema/status, run ID/final status, payload metadata, file sizes, SHA-256 values, checksum scope, source provenance, and the matching `run-index` record. A missing, malformed, partial, corrupted, duplicated, or internally inconsistent finalized-looking bundle therefore fails closed rather than being committed.

Publication stages only `results/runs/<run-id>/...` and `results/run-index.jsonl`. It also refuses to publish if the source commit changed during the run, the run began with tracked modifications or untracked non-output files, non-output files became untracked before publication, unrelated tracked files would enter the commit, Git LFS is required but unavailable, or the remote is no longer fast-forward compatible. In every such case the experiment files remain on disk. This prevents an uncommitted `src/`, `configs/`, data, script, or other repository input from silently influencing a run whose manifest otherwise points to a clean commit SHA.

Automatic Git publication is a **single-writer boundary**. Later batch/concurrent execution may run scientific work in parallel only when useful, but shared `run-index` mutation and Git commit/push operations must be serialized (or an equivalently race-free design must be proven). Two experiments must never concurrently rewrite the index or advance the same Git branch. A simple publication lock/queue is preferred over distributed coordination; if safe serialization is unavailable, publication fails closed and preserves each local finalized bundle for later retry.

Commit format:

```text
experiment: <status> <run-id>

Run-ID: <run-id>
Protocol: <protocol-version>
Stage: <development|tuning|pilot|final>
Source-Commit: <sha>
Status: <status>
```

No manual staging, commit-message composition, or push belongs to the normal experiment workflow.

## Large artifacts

Large thesis-produced artifacts are allowed. Full traces, Parquet/NumPy data, videos, and model/checkpoint formats use selective Git LFS rules. Small JSON/CSV/Markdown provenance remains ordinary Git. Bibliography PDFs and bibliography LFS objects stay upstream in `ThesisBibliography`.
