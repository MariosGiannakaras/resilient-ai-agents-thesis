#!/usr/bin/env python3
"""Validate mechanically detectable project-documentation consistency rules."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_ACTIVE = (
    "AGENTS.md",
    "README.md",
    "docs/context/CURRENT_STATUS.md",
    "docs/context/TASKS.md",
    "docs/context/END_TO_END_JOURNEY.md",
    "docs/context/PROJECT_CONTEXT.md",
    "docs/context/CONFIRMED_REQUIREMENTS.md",
    "docs/context/USER_DECISIONS.md",
    "docs/context/CONSTRAINTS.md",
    "docs/context/OPEN_QUESTIONS.md",
    "docs/context/CONTRADICTIONS.md",
    "docs/context/EXECUTION_WORKFLOW.md",
    "docs/context/IMPLEMENTATION_ROADMAP.md",
    "docs/context/DEFINITION_OF_DONE.md",
    "docs/context/DOCUMENTATION_GOVERNANCE.md",
    "docs/context/CODEX_EXECUTION_PROMPT.md",
    "docs/thesis/PRESENTATION_WORKFLOW.md",
    "docs/decisions/DECISION_LOG.md",
    "docs/context/CHANGELOG_CONTEXT.md",
    "docs/university/SOURCE_REGISTER.md",
)

OBSOLETE_ACTIVE_PATHS = (
    "docs/context/CODEX_BOOTSTRAP_PROMPT.md",
    "docs/context/BOOTSTRAP_VALIDATION.json",
)

CURRENT_STATE_FILES = (
    "AGENTS.md",
    "README.md",
    "docs/context/CURRENT_STATUS.md",
    "docs/context/TASKS.md",
    "docs/context/END_TO_END_JOURNEY.md",
    "docs/context/PROJECT_CONTEXT.md",
    "docs/context/CONFIRMED_REQUIREMENTS.md",
    "docs/context/USER_DECISIONS.md",
    "docs/context/CONSTRAINTS.md",
    "docs/context/OPEN_QUESTIONS.md",
    "docs/context/CONTRADICTIONS.md",
    "docs/context/EXECUTION_WORKFLOW.md",
    "docs/context/IMPLEMENTATION_ROADMAP.md",
    "docs/context/DEFINITION_OF_DONE.md",
    "docs/context/CODEX_EXECUTION_PROMPT.md",
    "docs/thesis/PRESENTATION_WORKFLOW.md",
    "docs/university/SOURCE_REGISTER.md",
)

RESOLVED_STALE_FRAGMENTS = (
    "current citation-only consumer implementation still requires migration",
    "the current citation-only consumer implementation still requires migration",
    "effective read access must be tested by the migrated synchronization workflow",
    "complete research-corpus consumer integration details",
    "no preferred stack.",
    "`core/` must work without the ui",
    "repository sha-256 pending local calculation by codex",
    "repository sha-256 pending codex local verification",
)

TASK_RE = re.compile(
    r"^- \[(?P<checked>x| )\](?:\s+(?P<status>READY|BLOCKED|DEFERRED|IN_PROGRESS))?\s+`(?P<id>T-\d+)`",
    re.MULTILINE,
)


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def main() -> int:
    errors: list[str] = []

    for relative in REQUIRED_ACTIVE:
        if not (ROOT / relative).is_file():
            errors.append(f"missing active source-of-truth file: {relative}")

    for relative in OBSOLETE_ACTIVE_PATHS:
        if (ROOT / relative).exists():
            errors.append(f"obsolete active file must be removed: {relative}")

    for relative in CURRENT_STATE_FILES:
        path = ROOT / relative
        if not path.is_file():
            continue
        lowered = path.read_text(encoding="utf-8").casefold()
        for fragment in RESOLVED_STALE_FRAGMENTS:
            if fragment.casefold() in lowered:
                errors.append(f"stale resolved statement in {relative}: {fragment}")

    agents = read("AGENTS.md") if (ROOT / "AGENTS.md").is_file() else ""
    if "src/resilient_agents/" not in agents:
        errors.append("AGENTS.md must name the accepted src/resilient_agents/ core")

    prompt_path = ROOT / "docs/context/CODEX_EXECUTION_PROMPT.md"
    if prompt_path.is_file():
        prompt = prompt_path.read_text(encoding="utf-8")
        for required in (
            "docs/context/CURRENT_STATUS.md",
            "docs/context/TASKS.md",
            "docs/context/END_TO_END_JOURNEY.md",
            "docs/context/DOCUMENTATION_GOVERNANCE.md",
            "Read `docs/context/CODEX_EXECUTION_PROMPT.md` and execute it completely.",
            "Mandatory startup and resume procedure",
            "IN_PROGRESS",
        ):
            if required not in prompt:
                errors.append(f"current Codex prompt missing required state/task-driven reference: {required}")
        if "copy its contents to" in prompt.casefold() or "CODEX_TASK.md" in prompt:
            errors.append("current Codex prompt must be directly executable and must not require a copied task prompt")

    tasks_path = ROOT / "docs/context/TASKS.md"
    if tasks_path.is_file():
        tasks = tasks_path.read_text(encoding="utf-8")
        for required in (
            "## Mandatory session rule",
            "## Resume state",
            "## Quota/interruption resilience",
            "IN_PROGRESS",
            "session memory",
            "git status",
            "Exact next action",
            "END_TO_END_JOURNEY.md",
            "PRESENTATION_WORKFLOW.md",
        ):
            if required.casefold() not in tasks.casefold():
                errors.append(f"TASKS.md missing required resumability/lifecycle element: {required}")

        matches = list(TASK_RE.finditer(tasks))
        ids = [match.group("id") for match in matches]
        if not ids:
            errors.append("TASKS.md must contain task IDs using the canonical checklist syntax")
        duplicates = sorted({task_id for task_id in ids if ids.count(task_id) > 1})
        if duplicates:
            errors.append(f"TASKS.md contains duplicate task IDs: {', '.join(duplicates)}")

        completed = {match.group("id") for match in matches if match.group("checked") == "x"}
        for index, match in enumerate(matches):
            if match.group("status") != "READY":
                continue
            block_end = matches[index + 1].start() if index + 1 < len(matches) else len(tasks)
            block = tasks[match.end():block_end]
            depends_match = re.search(r"^\s+- Depends on:\s*(.+)$", block, re.MULTILINE)
            if not depends_match:
                continue
            dependencies = set(re.findall(r"`(T-\d+)`", depends_match.group(1)))
            incomplete = sorted(dependencies - completed)
            if incomplete:
                errors.append(
                    f"TASKS.md marks {match.group('id')} READY while dependencies are incomplete: {', '.join(incomplete)}"
                )

        resume_match = re.search(r"- \*\*Current task:\*\* `(?P<task>T-\d+)`", tasks)
        if not resume_match:
            errors.append("TASKS.md Resume state must name one current task ID")
        elif resume_match.group("task") not in ids:
            errors.append("TASKS.md Resume state current task must exist in the task checklist")

    synthesis_path = ROOT / "docs/research/POSTIMPORT_EVIDENCE_SYNTHESIS.md"
    if synthesis_path.is_file():
        synthesis = synthesis_path.read_text(encoding="utf-8")
        start = synthesis.find("## Decision-driving citation-ready anchors")
        end = synthesis.find("\n## ", start + 3) if start >= 0 else -1
        section = synthesis[start:end if end >= 0 else None] if start >= 0 else ""
        for non_citation_ready in ("SRC-FC42D9798A", "SRC-3C0F7CC819"):
            if non_citation_ready in section:
                errors.append(
                    f"{non_citation_ready} must not be labelled citation-ready in POSTIMPORT_EVIDENCE_SYNTHESIS.md"
                )

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("Documentation consistency validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
