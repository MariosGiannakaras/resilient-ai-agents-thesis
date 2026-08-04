# Contributing

This repository is private and serves one thesis project, but changes must follow a controlled process.

## Before making a change

- Read `AGENTS.md` and the relevant canonical context files.
- Identify the requirement or decision that justifies the change.
- If none exists, record the need or open issue before implementation.
- Identify every active document, prompt, test, workflow, schema, or status statement that depends on the thing being changed.

## Documentation consistency rule

A change is not complete when only the code or primary document is updated.

In the same Pull Request:

1. update every active source-of-truth document affected by the change;
2. update the current Codex execution prompt if the active phase, workflow, architecture, or responsibilities changed;
3. delete obsolete compatibility files when they no longer serve a purpose;
4. preserve genuinely historical records only when useful, and mark them prominently as historical so they cannot be mistaken for current instructions;
5. update `CURRENT_STATUS.md`, `OPEN_QUESTIONS.md`, `DECISION_LOG.md`, and `CHANGELOG_CONTEXT.md` when their claims are affected;
6. add or update automated consistency checks when a stale state can be detected mechanically.

`docs/context/DOCUMENTATION_GOVERNANCE.md` defines the dependency/update matrix. `docs/context/CURRENT_STATUS.md` is the authoritative current-state summary.

## Branches and commits

- `main`: stable thesis source of truth.
- Feature/research branches: use short descriptive names such as `research/gridworld-spec`, `feat/run-registry`, `experiments/run-schema-v1`.
- Keep commits small but meaningful; squash related connector-generated commits before merging when practical.
- Typical prefixes: `docs:`, `research:`, `feat:`, `experiments:`, `test:`, `fix:`, `chore:`.
- Commit and Pull Request text is written in English.

## Pull Request checklist

- [ ] The change maps to a requirement, issue, or decision.
- [ ] Relevant tests were added or updated.
- [ ] No secrets or generated artifacts without provenance were added.
- [ ] Every affected active source-of-truth/status/prompt file was reviewed and reconciled.
- [ ] Obsolete files were deleted or explicitly marked historical rather than left as misleading current guidance.
- [ ] Results are not presented as final without a frozen protocol.
- [ ] Figures/tables can be reproduced.
- [ ] Documentation matches actual behavior and current repository state.
- [ ] Automated review findings were addressed or explicitly rejected with a reason.

## Data and results

- Do not modify finalized raw results.
- Whole-experiment outputs are retained and versioned automatically; large configured artifact formats use Git LFS.
- Do not manually prune large run data merely to reduce repository size. Change retention only through an explicit storage/protocol decision if real storage limits appear.
- Every processed artifact must identify source run IDs and the processing script.
- Failed runs retain metadata and a failure reason.

## Bibliography

- Do not acquire, copy, convert, or curate new primary bibliography sources in this repository.
- The canonical bibliography lifecycle belongs to `MariosGiannakaras/ThesisBibliography`.
- This repository consumes only the verified generated package under `research/bibliography/` through the controlled synchronization workflow.
- Do not hand-edit generated bibliography imports.

## Thesis content

- Every factual claim requires a real source or real project result.
- Every result claim must map to run IDs/figure/table IDs.
- Source-derived scientific evidence remains in the original source language.
- Current official Department guidance overrides repository placeholders.
