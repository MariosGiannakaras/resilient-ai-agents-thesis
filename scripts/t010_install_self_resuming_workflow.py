#!/usr/bin/env python3
"""Install the prompt-free, repository-authoritative self-resuming workflow."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def path(relative: str) -> Path:
    return ROOT / relative


def write(relative: str, content: str) -> None:
    target = path(relative)
    canonical = content.rstrip() + "\n"
    if target.read_text(encoding="utf-8") != canonical:
        target.write_text(canonical, encoding="utf-8")


def replace_once(relative: str, old: str, new: str) -> None:
    target = path(relative)
    text = target.read_text(encoding="utf-8")
    if new in text:
        return
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{relative}: expected one old occurrence, found {count}: {old[:120]!r}")
    target.write_text(text.replace(old, new, 1), encoding="utf-8")


def regex_once(relative: str, pattern: str, replacement: str) -> None:
    target = path(relative)
    text = target.read_text(encoding="utf-8")
    if replacement in text:
        return
    updated, count = re.subn(pattern, replacement, text, count=1, flags=re.MULTILINE)
    if count != 1:
        raise RuntimeError(f"{relative}: expected one regex match for {pattern!r}, found {count}")
    target.write_text(updated, encoding="utf-8")


# TASKS: four-source recovery core + active continuity package.
replace_once(
    "docs/context/TASKS.md",
    "Every Codex session MUST read:\n\n1. `AGENTS.md`\n2. `docs/context/TASKS.md`\n3. `docs/context/CURRENT_STATUS.md`\n\nUse available **session memory** together with repository/Git/GitHub/evidence, with repository evidence winning when stale. Inspect `git status`, the active branch, recent commits, current open PR/CI state and any `IN_PROGRESS` work before modification.",
    "Every implementation/repository session MUST recover from:\n\n1. `AGENTS.md`\n2. `docs/context/WORK_STATE.json`\n3. `docs/context/TASKS.md`\n4. `docs/context/CURRENT_STATUS.md`\n\nSession memory and conversation/model memory are advisory only. Repository/Git/GitHub/evidence wins when memory is stale or contradictory. Inspect `git status`, the active branch, recent commits, open PR/CI state and any `IN_PROGRESS` work before selecting new work.",
)
regex_once(
    "docs/context/TASKS.md",
    r"^- \*\*Current task:\*\* `T-712`.*$",
    "- **Current task:** `T-010` is **IN_PROGRESS** on PR #146: install the prompt-free self-resuming repository workflow and durable operational checkpoint contract. T-716 remains COMPLETE. T-712 remains DEFERRED until actual supervisor/reviewer feedback; T-713 remains downstream of T-712 plus authoritative official metadata/declaration and final Word/submission gates.",
)
regex_once(
    "docs/context/TASKS.md",
    r"^- .*Exact next action.*$",
    "- **Exact next action:** finish `T-010`: make `AGENTS.md` the no-prompt entrypoint, require `WORK_STATE.json` checkpoints, add continuity validation/CI, retire `CODEX_EXECUTION_PROMPT.md`, reconcile active workflow/governance docs, then merge PR #146 only after required checks pass.",
)
tasks = path("docs/context/TASKS.md")
text = tasks.read_text(encoding="utf-8")
if "- [ ] IN_PROGRESS `T-010`" not in text:
    anchor = "- [x] `T-009` — Project-scoped developer-documentation configuration.\n"
    addition = anchor + (
        "- [ ] IN_PROGRESS `T-010` — **Prompt-free self-resuming repository workflow and durable work-state checkpoints.**\n"
        "  - Depends on: `T-008`, `T-009` — satisfied.\n"
        "  - Scope: `AGENTS.md` becomes the automatic execution/recovery contract; `WORK_STATE.json` records the active operational checkpoint; every material action/checkpoint updates it; non-trivial work is pushed and surfaced in an early PR; Git/GitHub state is inspected before task selection.\n"
        "  - Acceptance: memory-independent recovery order is explicit; half-finished work resumes before new work; `scripts/project_checkpoint.py` and `scripts/validate_project_continuity.py` exist; material PRs update `WORK_STATE.json`; prompt dependency is removed; active docs/validators/CI are reconciled; PR #146 is green and merged; main is normalized to the next real task/external gate.\n"
    )
    if anchor not in text:
        raise RuntimeError("TASKS.md T-009 insertion anchor missing")
    tasks.write_text(text.replace(anchor, addition, 1), encoding="utf-8")
else:
    # T-010 may already be present from a previous idempotent run.
    pass

# CURRENT_STATUS: surface active repository-work package before the external academic gate.
status = path("docs/context/CURRENT_STATUS.md")
text = status.read_text(encoding="utf-8")
marker = "## Current execution state\n"
continuity = """## Active repository continuity work

- `T-010` is **IN_PROGRESS** on PR #146. Its purpose is to make repository continuation independent of chat/model memory: `AGENTS.md` is the no-prompt entrypoint, `docs/context/WORK_STATE.json` is the operational resume pointer, and every material change/checkpoint must update that pointer before work proceeds.
- Recovery order is: working-tree work -> open PR -> unmerged pushed branch -> `WORK_STATE` -> `TASKS` `IN_PROGRESS` -> first dependency-valid `READY` task -> exact external gate.
- T-716 remains COMPLETE and immutable as the accepted review-ready thesis milestone. T-010 changes workflow/governance only; it does not change the thesis DOCX, protocol, frozen evidence, analysis or scientific assets.

"""
if continuity not in text:
    if marker not in text:
        raise RuntimeError("CURRENT_STATUS.md insertion marker missing")
    text = text.replace(marker, continuity + marker, 1)
text = re.sub(
    r"## Exact next action\n\n.*\Z",
    "## Exact next action\n\nFinish T-010 on PR #146, validate the prompt-free recovery/checkpoint workflow, and merge only when continuity/documentation/required PR CI is green. After merge, normalize `WORK_STATE.json` on `main` to T-712 DEFERRED unless real supervisor/reviewer feedback has arrived.\n",
    text,
    count=1,
    flags=re.DOTALL,
)
status.write_text(text, encoding="utf-8")

# Execution workflow becomes the detailed self-resuming contract.
write(
    "docs/context/EXECUTION_WORKFLOW.md",
    """# Execution and Review Workflow

## Operating model

The repository is the durable execution authority. The user may simply say **continue implementation**. The agent recovers state, resumes unfinished work, executes the next dependency-valid scope, performs routine Git/PR/CI work, and stops only at a genuine external or explicit authorization gate.

Conversation/model memory is advisory only. Repository/Git/GitHub evidence overrides it.

## Prompt-free session bootstrap

1. Load `AGENTS.md`.
2. Read `docs/context/WORK_STATE.json`.
3. Read `docs/context/TASKS.md`.
4. Read `docs/context/CURRENT_STATUS.md`.
5. Inspect working-tree status, current branch, recent commits and unpushed/unmerged work.
6. Inspect open PRs, CI/check status and relevant issues when GitHub access exists.
7. Reconcile discrepancies before new implementation.

No separate task prompt is required or authoritative.

## Recovery order

Resume in this order:

1. uncommitted working-tree changes;
2. open implementation PRs with unfinished or ready-to-merge work;
3. pushed unmerged branches with unique required work;
4. valid `WORK_STATE.json` active package;
5. `TASKS.md` `IN_PROGRESS` task;
6. first dependency-valid `READY` task;
7. exact `BLOCKED`/`DEFERRED` external gate.

Do not start new work while recoverable unfinished work exists unless it is objectively blocked and the ledger explicitly permits an independent package.

## Durable checkpoint protocol

`WORK_STATE.json` is the operational resume pointer and must never become a competing task ledger.

Before every material change, update:

- active task/work package;
- phase;
- branch/PR identity when known;
- last durable checkpoint;
- exact next action;
- blockers and pending substeps.

After every material validated checkpoint, update:

- completed substep/checkpoint;
- relevant validation result;
- exact next action;
- any changed blocker/PR/CI state.

Before long/risky operations, quota/context boundaries or session end, create a coherent Git checkpoint and push it when access permits. Substantial work must not exist only in a local working tree or conversation.

Use `scripts/project_checkpoint.py` for structured updates when convenient.

## Branch/PR lifecycle

For non-trivial work:

1. create/recover one coherent branch;
2. record the work package in `WORK_STATE.json` and `TASKS.md` before substantial implementation;
3. commit/push an early coherent checkpoint;
4. open a draft PR as soon as useful remote recovery state exists; convert to normal review when reviewable;
5. continue implementation with checkpoint updates rather than waiting until the end to expose the branch;
6. run targeted checks, then canonical PR CI;
7. review the actual diff/review threads; never self-`APPROVE`;
8. squash-merge when checks/review/repository policy permit;
9. immediately reconcile `WORK_STATE.json` on `main` to the next dependency-valid task or exact external gate.

## Task/document governance

`TASKS.md` is the canonical task/dependency ledger. Started work is `IN_PROGRESS`; completed work is checked; discovered required work receives a stable task ID. `CURRENT_STATUS.md` is compact accepted state. `WORK_STATE.json` is only the active checkpoint/resume pointer.

Every material PR reviews and reconciles affected active docs, status, tasks, tests, workflows and decisions according to `DOCUMENTATION_GOVERNANCE.md`.

## Validation discipline

Use the smallest relevant checks during implementation. GitHub PR CI is the canonical full-suite pre-merge guard. `scripts/validate_project_continuity.py` and `scripts/validate_documentation_consistency.py` are mandatory continuity/documentation guards for material work.

Scientific matrices are not CI test matrices. Required scientific/provenance/configuration state fails closed.

## Scientific/bibliography boundaries

Protocol-v2.1, frozen evidence, T-612 analysis, T-613 assets and accepted T-716 thesis lineage remain immutable except through their declared amendment/revision workflows. Bibliography lifecycle work remains upstream in `MariosGiannakaras/ThesisBibliography`; generated consumer files are never hand-edited.

## Current academic gate after T-010

T-716 is COMPLETE. Unless actual supervisor/reviewer feedback has arrived, T-712 remains DEFERRED. T-713 remains downstream of actual feedback where applicable plus authoritative official metadata/declaration and final Word/submission checks. Do not manufacture work to bypass an external gate.
""",
)

# Documentation governance: WORK_STATE is an explicit exception to the no-parallel-status rule.
write(
    "docs/context/DOCUMENTATION_GOVERNANCE.md",
    """# Documentation Governance

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
""",
)

# README gets a user-visible continuation contract.
readme = path("README.md")
text = readme.read_text(encoding="utf-8")
anchor = "> `docs/context/TASKS.md` is the canonical task/dependency ledger. `docs/context/CURRENT_STATUS.md` is the compact current state. This README is the human-readable entry point.\n"
addition = anchor + (
    "\n## Agent continuation\n\n"
    "No task prompt is required. A coding/repository agent must recover from `AGENTS.md`, `docs/context/WORK_STATE.json`, `TASKS.md`, `CURRENT_STATUS.md`, actual Git state and open PR/CI state. Saying **continue implementation** is sufficient: unfinished work is resumed before new work, and every material checkpoint updates `WORK_STATE.json`.\n"
)
if "## Agent continuation" not in text:
    if anchor not in text:
        raise RuntimeError("README continuation anchor missing")
    readme.write_text(text.replace(anchor, addition, 1), encoding="utf-8")

# Context changelog records the durable workflow decision.
changelog = path("docs/context/CHANGELOG_CONTEXT.md")
text = changelog.read_text(encoding="utf-8")
entry = """## 2026-09-05 — T-010 prompt-free self-resuming workflow

- Made `AGENTS.md` the automatic execution/recovery contract: the user can say only "continue implementation" and the agent must recover objective repository/Git/GitHub state before selecting work.
- Added `docs/context/WORK_STATE.json` as a machine-readable operational resume pointer, plus checkpoint/continuity tooling and CI. Every material action/checkpoint must update it; `TASKS.md` remains the sole detailed task ledger.
- Established deterministic recovery priority: working tree -> open PR -> unmerged pushed branch -> WORK_STATE -> TASKS IN_PROGRESS -> first READY task -> exact external gate.
- Required early pushed checkpoints/draft PRs for non-trivial work and immediate post-merge main-state normalization so half-finished work cannot exist only in chat or one local checkout.
- Retired the tracked `CODEX_EXECUTION_PROMPT.md` dependency; project continuation is now prompt-free and repository-authoritative.

"""
if entry not in text:
    marker = "Record only material changes to the project source of truth. Detailed commit-by-commit history remains in Git; accepted decisions remain indexed in `docs/decisions/DECISION_LOG.md`.\n\n"
    if marker not in text:
        raise RuntimeError("CHANGELOG marker missing")
    changelog.write_text(text.replace(marker, marker + entry, 1), encoding="utf-8")

# Existing documentation validator must understand the prompt-free bootstrap.
validator = path("scripts/validate_documentation_consistency.py")
text = validator.read_text(encoding="utf-8")
text = text.replace('    "docs/context/CODEX_EXECUTION_PROMPT.md",\n', '')
if '    "docs/context/WORK_STATE.json",\n' not in text:
    text = text.replace('    "docs/context/CURRENT_STATUS.md",\n', '    "docs/context/CURRENT_STATUS.md",\n    "docs/context/WORK_STATE.json",\n', 1)
text = text.replace('            "three-file session-start core",\n', '            "WORK_STATE.json",\n')
pattern = r"    agents = read\(\"AGENTS\.md\"\).*?(?=    current_status_path = ROOT / \"docs/context/CURRENT_STATUS\.md\")"
replacement = '''    agents = read("AGENTS.md") if (ROOT / "AGENTS.md").is_file() else ""
    for required in (
        "docs/context/WORK_STATE.json",
        "continue implementation",
        "Repository/Git/GitHub evidence overrides",
        "before every material change",
        "after every material validated checkpoint",
        "open a draft PR",
        "scripts/validate_project_continuity.py",
    ):
        if required.casefold() not in agents.casefold():
            errors.append(f"AGENTS.md missing required prompt-free continuity invariant: {required}")
    if len(agents.splitlines()) > 180:
        errors.append("AGENTS.md exceeds the 180-line always-on context budget")
    if len(agents.split()) > 1700:
        errors.append("AGENTS.md exceeds the 1700-word always-on context budget")

'''
updated, count = re.subn(pattern, replacement, text, count=1, flags=re.DOTALL)
if count != 1:
    raise RuntimeError(f"documentation validator AGENTS/prompt block replacement count={count}")
validator.write_text(updated, encoding="utf-8")

# Legacy prompt/one-shot continuity scripts are obsolete and dangerous because they can recreate stale state.
for relative in (
    "docs/context/CODEX_EXECUTION_PROMPT.md",
    "scripts/t716_continuity_reconcile.py",
    "scripts/t716_continuity_contract_fix.py",
):
    target = path(relative)
    if target.exists():
        target.unlink()

print("T-010 prompt-free self-resuming workflow migration complete")
