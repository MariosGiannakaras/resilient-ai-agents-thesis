# Run Bundle and Automatic Git Publication

A `run_id` represents one whole experiment execution and may contain many seeds and episodes. Intermediate seed completion never creates a Git commit.

When the whole experiment reaches a final state (`complete`, `failed`, `cancelled`, `invalid`, or `excluded`), its bundle is finalized once. If automatic publication is enabled, exactly one result commit is created and pushed.

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
```

`results/run-index.jsonl` is updated once per finalized run. The manifest records protocol version/stage, timestamps, source Git commit, Python/platform provenance, final status, retention policy, file sizes, and SHA-256 digests. The existing privacy-minimal system-inventory collector is executed automatically at run start and stored with the run.

## Automatic commit and push

Publication stages only `results/runs/<run-id>/...` and `results/run-index.jsonl`. It refuses to publish if the source code changed during the run, the run began with tracked uncommitted changes, unrelated tracked files would enter the commit, Git LFS is required but unavailable, or the remote is no longer fast-forward compatible. In every such case the experiment files remain on disk.

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
