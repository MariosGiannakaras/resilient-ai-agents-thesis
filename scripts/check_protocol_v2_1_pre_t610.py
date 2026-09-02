#!/usr/bin/env python3
"""Run the phase-appropriate protocol-v2.1 conformance checks."""
from __future__ import annotations

import json
from pathlib import Path

from resilient_agents.study.pre_t610 import (
    run_pre_t610_readiness_package,
    run_synthetic_protocol_v21_pipeline_smoke,
    validate_protocol_v21_t610_completion,
)


_REPLACEMENT_STUDY = "protocol-v2.1-final--t610-recovery-01"


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    replacement_dir = repo_root / "results" / "studies" / _REPLACEMENT_STUDY
    if replacement_dir.exists():
        report = {
            "completion": validate_protocol_v21_t610_completion(repo_root),
            "synthetic_pipeline_smoke": run_synthetic_protocol_v21_pipeline_smoke(
                repo_root
            ),
        }
    else:
        report = run_pre_t610_readiness_package(repo_root)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
