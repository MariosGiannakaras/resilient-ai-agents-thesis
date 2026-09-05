# Documentation Governance

## Purpose

Repository documentation is part of the thesis source of truth. Material code/research/architecture/workflow/task/lifecycle/delivery changes are incomplete while active documentation or operational resume state describes an older reality.

## Authority classes

### Active source of truth

The following current-state surfaces must be reconciled when materially affected:

- `AGENTS.md` — automatic cross-cutting agent instructions and recovery rules;
- `docs/context/WORK_STATE.json` — active operational checkpoint/resume pointer;
- `docs/context/TASKS.md` — canonical detailed task/dependency ledger;
- `docs/context/CURRENT_STATUS.md` — compact accepted project state/external gates;
- `README.md`, `app/README.md`;
- `PROJECT_CONTEXT`, requirements/decisions/constraints/questions/contradictions;
- `EXECUTION_WORKFLOW`, `IMPLEMENTATION_ROADMAP`, `DEFINITION_OF_DONE`;
- decision log/context changelog;
- active research/protocol/architecture/thesis/university documents relevant to the changed subject.

No tracked execution prompt is required. `AGENTS.md` is the prompt-free entrypoint.

### Accepted history

Historical decisions/evidence may preserve what was true when written. They must be clearly historical/superseded when retained and must not masquerade as current guidance. Git history is sufficient for obsolete bootstrap/status snapshots with no remaining reasoning value.

### Generated or externally owned content

Do not hand-edit generated bibliography content. `research/bibliography/` changes only through controlled immutable synchronization from `MariosGiannakaras/ThesisBibliography`.

## Task-registry governance

`TASKS.md` is the only canonical detailed task checklist. Update it when work starts/completes/blocks/unblocks, dependencies/acceptance change, required work is discovered, or the exact next task changes.

`READY` means dependencies and non-task readiness conditions are satisfied. Started unfinished work remains unchecked and `IN_PROGRESS`; completed work remains checked. Required work cannot live only in chat, TODO comments or PR prose.

## Operational work-state governance

`WORK_STATE.json` is deliberately separate from `TASKS.md` because it solves a different failure mode: loss of in-flight work across chat/session/quota interruptions. It may repeat only the minimum identifiers needed to resume the active package.

It must be updated:

- before every material implementation/document/research action;
- after every material validated checkpoint;
- when branch/PR/CI/blocker/next-action state changes;
- before a long/risky operation or session/context boundary;
- immediately after merge to normalize `main` to the next task/external gate.

A material PR must update `WORK_STATE.json` unless it is a narrowly automated generated-only transaction explicitly exempted by the continuity validator. Non-trivial work should be pushed and surfaced in an early draft PR so remote recovery does not depend on one local checkout.

## Prompt-free agent bootstrap

The user may say only "continue implementation". The agent must recover from `AGENTS.md`, `WORK_STATE.json`, `TASKS.md`, `CURRENT_STATUS.md`, actual Git state and open GitHub PR/CI state. Repository/Git/GitHub evidence overrides model/session memory.

Further reading is task-specific and search-driven. Do not create or require a separate execution prompt, copied task file, or repeated domain-policy bundle.

## Change-impact minimums

| Material change | Minimum current-state review |
|---|---|
| Any implementation/task work | `WORK_STATE`, `TASKS`, `CURRENT_STATUS` if accepted state/next gate changes, affected docs/tests/workflows |
| Agent/recovery/Git/CI policy | `AGENTS`, `WORK_STATE` schema/tooling, `EXECUTION_WORKFLOW`, this file, continuity/docs validators, CI, changelog |
| Project phase/blocker resolution | `WORK_STATE`, `TASKS`, `CURRENT_STATUS`, project context/questions/roadmap/DoD/changelog |
| User requirement/decision | requirements, user decisions, constraints/contradictions, task/status/work state when execution changes, decision/changelog |
| Science/protocol/evidence | controlling research/protocol/decision records, tasks/status/work state, tests/validators; preserve immutable evidence boundaries |
| Bibliography baseline/contract | bibliography integration/context/status/tasks when gates change, import validation/workflow; never hand-edit generated corpus |
| Application/UX | app/UI architecture, requirements/decisions, tasks/status/work state, tests and lifecycle docs |
| Thesis/review/defense/delivery | thesis/university/presentation workflow, tasks/status/work state, official-input questions and downstream consistency docs |

Review transitive stale wording when a statement is repeated elsewhere.

## Reconciliation procedure before merge

1. identify semantic changes and active task;
2. verify `WORK_STATE.json` describes the branch/PR/checkpoint and exact next action;
3. reconcile `TASKS.md` task state/dependencies/acceptance;
4. reconcile `CURRENT_STATUS.md` when accepted state or external gate changes;
5. search active docs for stale phase/path/status/count/blocker wording;
6. update affected decisions/changelog when material;
7. remove obsolete bootstrap/status files that can mislead future agents;
8. run targeted validators/tests, including project continuity and documentation consistency;
9. pass required PR CI and objective diff review;
10. merge when permitted, then normalize `WORK_STATE.json` on `main` immediately.

## No silent stale-state policy

Known obsolete current-state statements are defects. Current files must be corrected rather than left beside a newer overlay. Historical wording belongs only in clearly historical records or Git history.
