#!/usr/bin/env python3
"""Validate mechanically detectable project-documentation consistency rules."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_ACTIVE = (
    "AGENTS.md",
    "README.md",
    "CONTRIBUTING.md",
    ".github/pull_request_template.md",
    "app/README.md",
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
    "docs/context/DOCUMENTATION_GOVERNANCE.md",
    "docs/context/CODEX_EXECUTION_PROMPT.md",
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
    "app/README.md",
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
    "docs/context/CODEX_EXECUTION_PROMPT.md",
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
    if "src/resilient_agents/" not in agents:
        errors.append("AGENTS.md must name the accepted src/resilient_agents/ core")
    for required in (
        "docs/context/TASKS.md",
        "docs/context/CURRENT_STATUS.md",
        "UI_INFORMATION_ARCHITECTURE.md",
        "DOCUMENTATION_GOVERNANCE.md",
        "citation-ready/",
        "PR CI is the canonical full-suite pre-merge check",
        "Prefer targeted search",
    ):
        if required.casefold() not in agents.casefold():
            errors.append(f"AGENTS.md missing required compact routing/invariant: {required}")

    agents_core_match = re.search(
        r"Start every Codex session with exactly:\s*(?P<section>.*?)(?=\nThen read only)",
        agents,
        re.DOTALL,
    )
    if not agents_core_match:
        errors.append("AGENTS.md missing explicit compact three-file session-start core")
    else:
        listed = tuple(
            re.findall(r"^\d+\.\s+`([^`]+)`", agents_core_match.group("section"), re.MULTILINE)
        )
        if listed != SESSION_START_CORE:
            errors.append(
                "AGENTS.md session-start list must contain exactly: " + ", ".join(SESSION_START_CORE)
            )

    if len(agents.splitlines()) > 160:
        errors.append("AGENTS.md exceeds the 160-line always-on context budget")
    if len(agents.split()) > 1500:
        errors.append("AGENTS.md exceeds the 1500-word always-on context budget")

    prompt_path = ROOT / "docs/context/CODEX_EXECUTION_PROMPT.md"
    if prompt_path.is_file():
        prompt = prompt_path.read_text(encoding="utf-8")
        for required in (
            "AGENTS.md",
            "docs/context/CURRENT_STATUS.md",
            "docs/context/TASKS.md",
            "Read `docs/context/CODEX_EXECUTION_PROMPT.md` and execute it completely.",
            "Startup / resume",
            "IN_PROGRESS",
            "one bounded scope",
            "Do not self-approve",
            "Project: X/Y",
            "In-progress/failed work never counts as complete",
            "Stop conditions",
        ):
            if required not in prompt:
                errors.append(f"current Codex prompt missing required lean execution invariant: {required}")

        if "copy its contents to" in prompt.casefold() or "CODEX_TASK.md" in prompt:
            errors.append("current Codex prompt must be directly executable and must not require a copied task prompt")

        prompt_core_match = re.search(
            r"2\. Read only the session-start core:\n(?P<section>.*?)(?=\n3\.)",
            prompt,
            re.DOTALL,
        )
        if not prompt_core_match:
            errors.append("current Codex prompt missing explicit three-file session-start core")
        else:
            listed = tuple(
                re.findall(r"^[ \t]*- `([^`]+)`", prompt_core_match.group("section"), re.MULTILINE)
            )
            if listed != SESSION_START_CORE:
                errors.append(
                    "current Codex prompt session-start core must contain exactly: "
                    + ", ".join(SESSION_START_CORE)
                )

        duplicate_policy_headings = (
            "## Bibliography rules",
            "## Scientific rules",
            "## Architecture/UI rules",
            "## Lifecycle handoff rules",
            "## Proportional testing discipline",
        )
        for heading in duplicate_policy_headings:
            if heading in prompt:
                errors.append(f"current Codex prompt duplicates AGENTS.md domain policy section: {heading}")

        if len(prompt.split()) > 1200:
            errors.append("current Codex prompt exceeds the 1200-word lean execution budget")

    current_status_path = ROOT / "docs/context/CURRENT_STATUS.md"
    if current_status_path.is_file():
        current_status = current_status_path.read_text(encoding="utf-8")
        for required in (
            "T-100",
            "Exact next action",
            "bibliography-integration-v3",
            "progressive-disclosure",
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
            "three-file session-start core",
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
            r"^- \[ \] BLOCKED `T-511`.*?^\s+- Depends on:\s*(.+)$",
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
