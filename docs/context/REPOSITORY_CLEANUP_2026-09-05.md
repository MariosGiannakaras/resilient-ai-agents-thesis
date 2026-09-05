# Repository cleanup audit — 2026-09-05

## Rule

Cleanup is conservative. A path is removed only when all of the following are true:

1. it contains no scientific result/evidence/provenance/history;
2. it contains no useful documentation beyond a generic placeholder;
3. repository search finds no consumer/reference to the path;
4. no active build/runtime/test contract requires it.

Docs, results, decisions, research evidence, archived thesis deliverables, old draft lineages and implementation-history material are not deleted merely because they are currently inactive.

## Removed

The following directories contained only a tiny generic `README.md` placeholder and had no repository consumer. Removing the only tracked file removes the otherwise empty Git directory:

- `data/raw/`
- `data/processed/`
- `data/external/`
- `artifacts/figures/`
- `artifacts/tables/`
- `artifacts/exports/`

The active project does not use these generic folders for accepted evidence. Scientific outputs are organized under the versioned `results/` hierarchy; thesis deliverables are retained under `thesis/archive/`/`thesis/final/`; generated runtime output may still use the broader `artifacts/` convention where a tool explicitly creates it.

## Explicitly retained

- `results/**` — scientific runs, Study bundles, frozen evidence, analyses and T-613 assets.
- `research/bibliography/**` — immutable synchronized bibliography corpus and provenance.
- `docs/**` — requirements, decisions, architecture, methodology, audits, historical rationale and thesis workflow.
- `thesis/archive/**` — permanent historical/review DOCX milestones and QA identities.
- `thesis/drafts/**` — restored older drafts useful for reconstruction/history.
- `thesis/chapters/` and `thesis/appendices/` — retained because bibliography-validation code/tests still recognize the formal thesis path contract; removal would be a contract change rather than simple cleanup.
- historical Streamlit/React/NiceGUI decision/documentation material — retained as architecture history and supersession evidence.
- `.bibliography-sync-trigger` and bibliography sync workflows — active integration mechanism, not clutter.
- `.codex/`, `.github/`, project configuration and test infrastructure — active repository tooling/configuration.

## Transient junk check

No tracked `__pycache__`, `.pyc`, `.DS_Store` or equivalent obvious OS/Python cache residue was found in the current main tree. `.gitignore` already excludes Python/Node/Rust build caches, IDE/OS metadata, Office temp files, local databases/logs and incomplete run-bundle files.

## Cleanup boundary

No file was removed on the basis of age alone. If an apparently sparse directory is referenced by source code, tests, workflow contracts, evidence lineage or historical documentation, it remains until a separate explicit migration proves that contract obsolete.
