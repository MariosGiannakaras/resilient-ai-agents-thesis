#!/usr/bin/env python3
"""Validate the already-reconciled canonical T-716 completion state.

The original version of this file was a one-shot text migration.  Final CI must be
repeatable, so the durable post-migration contract is now validated rather than trying
to replace text that is already current.
"""
from pathlib import Path

SEMANTIC = "b01f853af794e596f0dfb491a3f5401365ca3f01fd7d410194e539f0b8a10cc1"

REQUIRED = {
    "README.md": [
        "T-716 is now COMPLETE as the review-ready full-content thesis task",
        "11/11 final acceptance gates PASS",
        SEMANTIC,
    ],
    "docs/context/CURRENT_STATUS.md": [
        "**T-716 is COMPLETE.**",
        "T716_FINAL_ACCEPTANCE_AUDIT.md",
        SEMANTIC,
        "T-712` waits for **actual** supervisor/reviewer feedback",
    ],
    "docs/context/TASKS.md": [
        "`T-716` is **COMPLETE**",
        "- [x] `T-716`",
        "Stage-4/final T-716 checkpoint",
        "11 `T716_REWRITE_PLAN.md` gates",
    ],
    "thesis/archive/README.md": [
        "accepted T-716 full-content review authority",
        "T-716 is therefore COMPLETE",
        SEMANTIC,
    ],
    "docs/context/POST_THESIS_LIFECYCLE.md": [
        "T-716 — Full-content evidence-aware thesis — COMPLETE",
        "T-712 still requires actual supervisor/reviewer feedback",
    ],
    "docs/thesis/T716_REWRITE_PLAN.md": [
        "**Status:** COMPLETE",
        SEMANTIC,
    ],
}


def main() -> None:
    failures: list[str] = []
    for path, tokens in REQUIRED.items():
        text = Path(path).read_text(encoding="utf-8")
        for token in tokens:
            if token not in text:
                failures.append(f"{path}: missing {token!r}")
    if failures:
        raise SystemExit("T-716 final status validation FAIL:\n- " + "\n- ".join(failures))
    print("T-716 final status reconciliation validation PASS")


if __name__ == "__main__":
    main()
