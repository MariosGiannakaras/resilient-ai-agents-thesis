# Result Provenance

## Principle

A reported number is valid only when its lineage can be reconstructed from primary run outputs through deterministic or explicitly versioned processing steps.

## Provenance chain

```text
Protocol version
  → experiment ID
  → run IDs and resolved configs
  → immutable raw files + checksums
  → processing script + parameters + Git commit
  → processed dataset/version
  → figure/table ID + generation manifest
  → thesis section/caption/claim
```

## Raw-result policy

- Raw results are immutable after run finalization.
- Each raw file receives a cryptographic checksum.
- Partial raw outputs from failed/cancelled runs are retained and labeled.
- Corrections produce a new file/version; original remains.
- Manual spreadsheet edits cannot be the source of final thesis values.
- Large-data retention and LFS/external-storage policy must be decided before final batches.

## Processed-result policy

Each processed dataset records:
- source run IDs and source checksums,
- included/excluded set and reasons,
- processing script/module and version,
- command/configuration,
- metric schema version,
- Git commit and dirty-state,
- generation timestamp,
- output checksum.

## Artifact identifiers

Recommended stable forms:
- `FIG-RQ1-001`
- `TAB-RQ1-001`
- `EXP-RQ1-BASELINE-001`
- `DATA-PROC-RQ1-001`

IDs must not be reused for materially different content.

## Figure/table manifest

Every thesis artifact must contain or be accompanied by:
- artifact ID and title,
- research question,
- experiment IDs,
- run IDs or a query resolving them,
- source raw/processed paths and checksums,
- script/notebook entrypoint,
- all rendering/aggregation parameters,
- Git commit,
- software environment,
- generation date,
- output path/checksum,
- intended thesis chapter/section,
- caveats.

## Thesis linkage

- Captions and nearby text may cite artifact IDs.
- A thesis claim register should map major quantitative claims to table/figure and run/analysis IDs.
- Numbers manually transcribed into prose must be checked against generated outputs.
- Final Word embeds rendered artifacts, but repository source files and manifests remain authoritative.

## Reproduction levels

1. **Trace reproduction:** regenerate the exact artifact from frozen processed data.
2. **Analysis reproduction:** regenerate processed data and artifacts from frozen raw runs.
3. **Experiment reproduction:** rerun experiments from configs/code under documented environment.
4. **Statistical reproduction:** obtain compatible distributions/conclusions where exact hardware nondeterminism prevents bitwise identity.

The project must state which level is achieved for each deliverable.
