#!/usr/bin/env python3
"""Validate mechanically detectable project-documentation consistency rules."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_ACTIVE = (
    "AGENTS.md",
    "README.md",
    "docs/context/CURRENT_STATUS.md",
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
    "docs/decisions/DECISION_LOG.md",
    "docs/context/CHANGELOG_CONTEXT.md",
)

OBSOLETE_ACTIVE_PATHS = (
    "docs/context/CODEX_BOOTSTRAP_PROMPT.md",
)

CURRENT_STATE_FILES = (
    "AGENTS.md",
    "README.md",
    "docs/context/CURRENT_STATUS.md",
    "docs/context/PROJECT_CONTEXT.md",
    "docs/context/OPEN_QUESTIONS.md",
    "docs/context/EXECUTION_WORKFLOW.md",
    "docs/context/IMPLEMENTATION_ROADMAP.md",
    "docs/context/CODEX_EXECUTION_PROMPT.md",
)

RESOLVED_STALE_FRAGMENTS = (
    "current citation-only consumer implementation still requires migration",
    "the current citation-only consumer implementation still requires migration",
    "effective read access must be tested by the migrated synchronization workflow",
    "complete research-corpus consumer integration details",
    "no preferred stack.",
    "`core/` must work without the ui",
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
            "docs/context/DOCUMENTATION_GOVERNANCE.md",
            "CODEX_TASK.md",
        ):
            if required not in prompt:
                errors.append(f"current Codex prompt missing required state-driven reference: {required}")

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
