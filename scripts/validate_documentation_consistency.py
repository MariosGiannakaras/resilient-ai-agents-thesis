#!/usr/bin/env python3
"""Validate mechanically detectable project-documentation consistency rules."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_ACTIVE = (
    "AGENTS.md",
    "README.md",
    "CONTRIBUTING.md",
    ".github/pull_request_template.md",
    "docs/context/CURRENT_STATUS.md",
    "docs/context/WORK_STATE.json",
    "docs/context/TASKS.md",
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
    "docs/architecture/UI_INFORMATION_ARCHITECTURE.md",
    "docs/thesis/PRESENTATION_WORKFLOW.md",
    "docs/decisions/DECISION_LOG.md",
    "docs/context/CHANGELOG_CONTEXT.md",
    "docs/university/SOURCE_REGISTER.md",
)

OBSOLETE_ACTIVE_PATHS = (
    "docs/context/CODEX_BOOTSTRAP_PROMPT.md",
    "docs/context/BOOTSTRAP_VALIDATION.json",
    "docs/context/END_TO_END_JOURNEY.md",
    "docs/context/FINAL_BOOTSTRAP_AUDIT.md",
    "docs/context/SOURCE_AUDIT.md",
    "core",
    "bibliography",
)

CURRENT_STATE_FILES = (
    "AGENTS.md",
    "README.md",
    "CONTRIBUTING.md",
    ".github/pull_request_template.md",
    "docs/context/CURRENT_STATUS.md",
    "docs/context/TASKS.md",
    "docs/context/PROJECT_CONTEXT.md",
    "docs/context/CONFIRMED_REQUIREMENTS.md",
    "docs/context/USER_DECISIONS.md",
    "docs/context/CONSTRAINTS.md",
    "docs/context/OPEN_QUESTIONS.md",
    "docs/context/CONTRADICTIONS.md",
    "docs/context/EXECUTION_WORKFLOW.md",
    "docs/context/IMPLEMENTATION_ROADMAP.md",
    "docs/context/DEFINITION_OF_DONE.md",
    "docs/architecture/UI_INFORMATION_ARCHITECTURE.md",
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
    "END_TO_END_JOURNEY.md",
    "this repository remains private",
    "the repository remains private while it contains",
)

SESSION_START_CORE = (
    "AGENTS.md",
    "docs/context/TASKS.md",
    "docs/context/CURRENT_STATUS.md",
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

    current_status_path = ROOT / "docs/context/CURRENT_STATUS.md"
    if current_status_path.is_file():
        current_status = current_status_path.read_text(encoding="utf-8")
        for required in (
            "T-100",
            "T-200",
            "Exact next action",
            "bibliography-integration-v3",
            "progressive",
            "Still intentionally unfrozen",
        ):
            if required.casefold() not in current_status.casefold():
                errors.append(f"CURRENT_STATUS.md missing compact current-state invariant: {required}")
        if len(current_status.split()) > 1200:
            errors.append("CURRENT_STATUS.md exceeds the 1200-word session-start budget")

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
            "PRESENTATION_WORKFLOW.md",
            "T-008",
            "WORK_STATE.json",
            "T-512",
            "self-explanatory UX",
        ):
            if required.casefold() not in tasks.casefold():
                errors.append(f"TASKS.md missing required resumability/lifecycle/UX/bootstrap element: {required}")

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
                    f"TASKS.md marks {match.group('id')} READY while dependencies are incomplete: "
                    + ", ".join(incomplete)
                )

        resume_match = re.search(r"- \*\*Current task:\*\* `(?P<task>T-\d+)`", tasks)
        if not resume_match:
            errors.append("TASKS.md Resume state must name one current task ID")
        elif resume_match.group("task") not in ids:
            errors.append("TASKS.md Resume state current task must exist in the task checklist")

        t511_match = re.search(
            r"^- \[[x| ]\].*?`T-511`.*?^\s+- Depends on:\s*(.+)$",
            tasks,
            re.MULTILINE | re.DOTALL,
        )
        if not t511_match or "`T-512`" not in t511_match.group(1):
            errors.append("T-511 application validation must depend on T-512 UX/onboarding completion")

    requirements_path = ROOT / "docs/context/CONFIRMED_REQUIREMENTS.md"
    if requirements_path.is_file():
        requirements = requirements_path.read_text(encoding="utf-8")
        for required in (
            "REQ-UI-008",
            "REQ-UI-009",
            "REQ-UI-010",
            "REQ-UI-011",
            "REQ-UI-012",
            "REQ-UI-013",
            "REQ-UI-014",
            "REQ-UI-015",
            "REQ-REPO-011",
            "REQ-TEST-009",
        ):
            if required not in requirements:
                errors.append(f"CONFIRMED_REQUIREMENTS.md missing confirmed dashboard/execution requirement: {required}")

    ui_arch_path = ROOT / "docs/architecture/UI_INFORMATION_ARCHITECTURE.md"
    if ui_arch_path.is_file():
        ui_arch = ui_arch_path.read_text(encoding="utf-8").casefold()
        for required in (
            "self-explanatory ux contract",
            "lightweight onboarding",
            "previous",
            "next",
            "skip",
            "finish",
            "color alone",
            "pre-run review",
        ):
            if required.casefold() not in ui_arch:
                errors.append(f"UI_INFORMATION_ARCHITECTURE.md missing confirmed UX element: {required}")

    synthesis_path = ROOT / "docs/research/POSTIMPORT_EVIDENCE_SYNTHESIS.md"
    if synthesis_path.is_file():
        synthesis = synthesis_path.read_text(encoding="utf-8")
        start = synthesis.find("## Decision-driving citation-ready anchors")
        end = synthesis.find("\n## ", start + 3) if start >= 0 else -1
        section = synthesis[start:end if end >= 0 else None] if start >= 0 else ""
        manifest_path = ROOT / "research/bibliography/citation-ready/manifest.csv"
        if not manifest_path.is_file():
            errors.append("citation-ready manifest is missing")
        else:
            manifest_ids = set(
                re.findall(
                    r"^SRC-[A-F0-9]{10}",
                    manifest_path.read_text(encoding="utf-8"),
                    flags=re.MULTILINE,
                )
            )
            for source_id in sorted(set(re.findall(r"\bSRC-[A-F0-9]{10}\b", section))):
                if source_id not in manifest_ids:
                    errors.append(
                        f"{source_id} is labelled citation-ready in "
                        "POSTIMPORT_EVIDENCE_SYNTHESIS.md but is absent from the citation-ready manifest"
                    )

    inventory_path = ROOT / "docs/context/system-capability.accepted.json"
    capability_report_path = ROOT / "docs/context/SYSTEM_CAPABILITY_REPORT.md"
    if inventory_path.is_file() and capability_report_path.is_file():
        try:
            inventory_bytes = inventory_path.read_bytes()
            inventory = json.loads(inventory_bytes)
        except (OSError, json.JSONDecodeError) as error:
            errors.append(f"accepted system capability JSON is unreadable: {error}")
        else:
            if not isinstance(inventory, dict):
                errors.append("accepted system capability JSON must be an object")
                inventory = {}
            repository = inventory.get("repository", {})
            if not isinstance(repository, dict):
                errors.append("accepted system capability repository field must be an object")
                repository = {}
            report = capability_report_path.read_text(encoding="utf-8")
            expected_commit = repository.get("git_head")
            expected_sha256 = hashlib.sha256(inventory_bytes).hexdigest()
            if expected_commit and expected_commit not in report:
                errors.append("SYSTEM_CAPABILITY_REPORT.md does not cite accepted repository commit")
            if expected_sha256 not in report:
                errors.append("SYSTEM_CAPABILITY_REPORT.md does not cite accepted inventory SHA-256")

    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT), "status", "--porcelain"],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        result = None
    if result is not None and result.returncode != 0:
        errors.append("documentation validator could not inspect git status")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Documentation consistency validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
