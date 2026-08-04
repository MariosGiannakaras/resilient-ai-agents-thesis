# DEC-024 — Active-Document Reconciliation Is Part of Every Material Change

**Status:** Accepted; Codex prompt usage clarified  
**Date:** 2026-08-04

## Context

A repository-wide audit after DEC-023 found active files that still described already completed work as pending, including the complete bibliography import/authentication, the pre-DEC-023 technical architecture, and an obsolete Codex bootstrap mission. One post-import research workspace also incorrectly grouped two full-corpus robust-MDP sources under a citation-ready heading.

A single current-status overlay is insufficient if other active files can still mislead future Codex/ChatGPT work.

## Decision

- A material change is incomplete until all affected active context, requirements, research, architecture, workflow, prompt, decision, test, and status files are reconciled in the same PR.
- `docs/context/CURRENT_STATUS.md` is the shortest current-state authority, but contradictory active files are not allowed to remain simply because the overlay is newer.
- `docs/context/DOCUMENTATION_GOVERNANCE.md` defines the minimum change-impact matrix.
- Obsolete files are deleted when they no longer serve a purpose.
- Useful historical records are retained only with prominent historical/superseded labelling and current-authority pointers.
- Generated bibliography content is never hand-edited for consistency.
- `docs/context/CODEX_EXECUTION_PROMPT.md` is the only tracked current Codex prompt and is itself the directly executable Codex entrypoint. A second copied task prompt is not required.
- The canonical prompt is updated in the same PR whenever workflow, architecture, responsibilities, project state, or the active next task materially changes.
- CI runs `scripts/validate_documentation_consistency.py` for mechanically detectable stale-state conditions.
- Coherent changes should normally reach `main` through one squash merge even if connector tooling created multiple mechanical branch commits.

## Consequences

Every future implementation/research/status change carries a documentation-impact review. The user should not need to remember which active-looking file is outdated or manually keep a separate Codex prompt synchronized. Historical provenance is preserved without letting history become current instructions.

## Alternatives rejected

- rely only on `CURRENT_STATUS.md` while leaving stale active files untouched;
- fix documentation only when a contradiction is noticed later;
- keep multiple tracked Codex prompts for different old phases;
- require a manually copied/disposable Codex task prompt when the canonical tracked prompt can be executed directly;
- silently rewrite generated bibliography evidence;
- delete all historical records regardless of value.
